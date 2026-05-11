"""消费 state/threads.sqlite 里的待抓帖子，落盘到 output/<fid>_<name>/<tid>/。

每帖输出：
- raw/page-N.html    : 原始 HTML（用于以后重新解析）
- meta.json          : 标题/版块/作者/楼层数/附件/分页数
- post.md            : Markdown 化的主楼正文 + 楼层回复
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from selectolax.parser import HTMLParser, Node

from .core import Config, KxClient, Throttled, DailyCapReached, init_thread_table, open_db

log = logging.getLogger("kanxue.thread")

THREAD_URL = "https://bbs.kanxue.com/thread-{tid}.htm"
THREAD_PAGE_URL = "https://bbs.kanxue.com/thread-{tid}-{page}.htm"

PAGE_NUM_RE = re.compile(r"thread-\d+-(\d+)\.htm")
SAFE_FS_RE = re.compile(r"[\\/:*?\"<>|\r\n\t]+")


def safe_name(s: str, limit: int = 60) -> str:
    s = SAFE_FS_RE.sub("_", s).strip(" ._")
    return s[:limit] or "untitled"


@dataclass
class PostFloor:
    pid: str
    floor: str
    author: str
    author_url: str
    time: str
    html: str
    markdown: str


@dataclass
class ThreadMeta:
    tid: int
    fid: int
    title: str
    url: str
    forum_name: str
    pages: int
    author: str
    author_url: str
    created_at: str
    floors_count: int
    attachments: list[str] = field(default_factory=list)
    crawled_at: int = 0


# ---------------- HTML -> Markdown ----------------

INLINE_TAGS = {"strong", "b", "em", "i", "u", "code", "span", "font", "small"}


def node_to_md(node: Node, indent: int = 0) -> str:
    """轻量 HTML→Markdown，专为看雪 .message 内的标签集设计：
    p / h1-h6 / pre>code / code / a / img / ul/ol/li / blockquote / br / hr / table。
    其他标签直接吐 children 文本。"""
    if node is None:
        return ""
    tag = node.tag
    if tag == "-text":
        return node.text(deep=False) or ""
    children_md = "".join(node_to_md(c, indent) for c in node.iter(include_text=True)) if node.tag != "pre" else ""

    if tag == "br":
        return "\n"
    if tag == "hr":
        return "\n\n---\n\n"
    if tag == "p":
        return f"{children_md.strip()}\n\n"
    if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
        level = int(tag[1])
        return f"\n{'#' * level} {children_md.strip()}\n\n"
    if tag == "a":
        href = node.attributes.get("href") or ""
        return f"[{children_md.strip() or href}]({href})"
    if tag == "img":
        src = node.attributes.get("src") or ""
        alt = node.attributes.get("alt") or ""
        # 看雪图片是相对路径 upload/attach/...，补全到绝对地址
        if src and not src.startswith(("http://", "https://", "//")):
            src = f"https://bbs.kanxue.com/{src.lstrip('/')}"
        return f"![{alt}]({src})"
    if tag == "code" and (node.parent and node.parent.tag != "pre"):
        return f"`{node.text() or ''}`"
    if tag == "pre":
        # 内部一般是 <code class="language-xxx hljs ...">
        code_node = node.css_first("code")
        lang = ""
        if code_node:
            cls = code_node.attributes.get("class") or ""
            m = re.search(r"language-([a-zA-Z0-9_+\-]+)", cls)
            if m:
                lang = m.group(1)
            text = code_node.text() or ""
        else:
            text = node.text() or ""
        return f"\n```{lang}\n{text.rstrip()}\n```\n\n"
    if tag in {"ul", "ol"}:
        items = []
        for i, li in enumerate(node.css("li")):
            inner = "".join(node_to_md(c, indent + 1) for c in li.iter(include_text=True)).strip()
            bullet = "-" if tag == "ul" else f"{i + 1}."
            items.append(f"{'  ' * indent}{bullet} {inner}")
        return "\n" + "\n".join(items) + "\n\n"
    if tag == "blockquote":
        inner = children_md.strip().splitlines()
        return "\n" + "\n".join(f"> {ln}" for ln in inner) + "\n\n"
    if tag in INLINE_TAGS:
        if tag in {"strong", "b"}:
            return f"**{children_md}**"
        if tag in {"em", "i"}:
            return f"*{children_md}*"
        return children_md
    if tag == "table":
        # 表格简化为 HTML 内联（后期再扩展）
        return f"\n\n{node.html}\n\n"
    return children_md


def collapse_md(s: str) -> str:
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip() + "\n"


# ---------------- 帖子页解析 ----------------

def parse_thread_page(html: str) -> tuple[str, list[PostFloor], int, str, str, str, list[str]]:
    """返回 (page_title, floors, total_pages, breadcrumb, op_author, op_time, attach_links)。"""
    tree = HTMLParser(html)

    # 1) 标题 (document.title 形如 "[原创]xxx-Android安全-看雪安全社区...")
    title_full = (tree.css_first("title").text() if tree.css_first("title") else "") or ""
    # 标题形如 "[原创]xxx-Android安全-看雪安全社区..."；先去掉 "-看雪..."，再剥掉版块尾缀。
    # 比起逐个版块名硬编码，更稳：用面包屑 (社区 / 版块名 / 发新帖) 拿到精确版块名，再从标题尾巴去掉。
    title = title_full
    if "-看雪" in title:
        title = title.rsplit("-看雪", 1)[0]
    if breadcrumb:
        # breadcrumb 文本类似 "社区Android安全发新帖"  或 "社区 Android安全 发新帖"
        bc_clean = re.sub(r"\s+", "", breadcrumb)
        m = re.search(r"社区(.+?)(?:发新帖|$)", bc_clean)
        forum_name_in_bc = m.group(1) if m else ""
        if forum_name_in_bc and title.endswith("-" + forum_name_in_bc):
            title = title[: -(len(forum_name_in_bc) + 1)]
    title = title.strip()

    # 2) 面包屑 (社区/Android安全/...)
    bc_el = tree.css_first(".breadcrumb")
    breadcrumb = (bc_el.text(strip=True) if bc_el else "")

    # 3) 楼层
    floors: list[PostFloor] = []
    op_author = op_author_url = op_time = ""

    # 主楼：在 .card.message_card 内，含 .message[isfirst="1"]
    op_card = tree.css_first(".card.message_card")
    op_message = op_card.css_first('.message[isfirst="1"]') if op_card else tree.css_first('.message[isfirst="1"]')
    if op_message is not None:
        # 主楼作者：card 内有多个 user-home 链接（头像 + 用户名），取首个**有文本**的
        if op_card is not None:
            for a in op_card.css("a[href*='user-home']"):
                txt = a.text(strip=True)
                if txt:
                    op_author = txt
                    op_author_url = a.attributes.get("href") or ""
                    break
            if op_author_url and not op_author_url.startswith("http"):
                op_author_url = f"https://bbs.kanxue.com/{op_author_url.lstrip('/')}"
            # 时间：card 内首个 yyyy-m-d 文本
            for sp in op_card.css("span"):
                t = (sp.text() or "").strip()
                if re.match(r"^\d{4}-\d{1,2}-\d{1,2}", t):
                    op_time = t
                    break

        floors.append(
            PostFloor(
                pid="OP",
                floor="1",
                author=op_author,
                author_url=op_author_url,
                time=op_time,
                html=op_message.html or "",
                markdown=collapse_md(node_to_md(op_message)),
            )
        )

    # 回复楼层：每个 tr.post（看雪用 table 渲染）
    for post in tree.css("tr.post"):
        pid = post.attributes.get("data-pid") or post.attributes.get("id") or ""
        msg = post.css_first(".message")
        if msg is None:
            continue
        floor_el = post.css_first(".floor, [class*='lou']")
        floor = (floor_el.text(strip=True) if floor_el else "").strip() or str(len(floors) + 1)
        author = ""
        author_url = ""
        for a in post.css("a[href*='user-home']"):
            txt = a.text(strip=True)
            if txt:
                author = txt
                author_url = a.attributes.get("href") or ""
                break
        if not author_url:
            first_a = post.css_first("a[href*='user-home']")
            if first_a:
                author_url = first_a.attributes.get("href") or ""
        if author_url and not author_url.startswith("http"):
            author_url = f"https://bbs.kanxue.com/{author_url.lstrip('/')}"
        time_text = ""
        for span in post.css("span"):
            t = (span.text() or "").strip()
            if re.match(r"^\d{4}-\d{1,2}-\d{1,2}", t):
                time_text = t
                break
        floors.append(
            PostFloor(
                pid=pid,
                floor=floor,
                author=author,
                author_url=author_url,
                time=time_text,
                html=msg.html or "",
                markdown=collapse_md(node_to_md(msg)),
            )
        )

    # 4) 总页数
    total_pages = 1
    for a in tree.css("a[href*='thread-']"):
        href = a.attributes.get("href") or ""
        m = PAGE_NUM_RE.search(href)
        if m:
            total_pages = max(total_pages, int(m.group(1)))

    # 5) 附件链接（站内附件下载入口）
    attach_links: list[str] = []
    for a in tree.css("a"):
        href = a.attributes.get("href") or ""
        if "attach" in href and "download" in href:
            full = href if href.startswith("http") else f"https://bbs.kanxue.com/{href.lstrip('/')}"
            if full not in attach_links:
                attach_links.append(full)

    return title, floors, total_pages, breadcrumb, op_author, op_time, attach_links


# ---------------- 落盘 ----------------

def render_post_md(meta: ThreadMeta, floors: list[PostFloor]) -> str:
    lines: list[str] = []
    lines.append(f"# {meta.title}\n")
    lines.append(f"- **链接**: {meta.url}")
    lines.append(f"- **版块**: {meta.forum_name} (fid={meta.fid})")
    lines.append(f"- **作者**: {meta.author}  ({meta.author_url})")
    lines.append(f"- **发表**: {meta.created_at}")
    lines.append(f"- **楼层数**: {meta.floors_count}    **页数**: {meta.pages}")
    if meta.attachments:
        lines.append(f"- **附件**: {len(meta.attachments)} 个")
    lines.append("\n---\n")
    for fl in floors:
        head = f"## #{fl.floor}  {fl.author}    {fl.time}"
        lines.append(head)
        lines.append(fl.markdown.rstrip())
        lines.append("\n---\n")
    return "\n".join(lines)


def crawl_one(cli: KxClient, tid: int, fid: int, forum_name: str, out_root: Path) -> ThreadMeta:
    forum_dir = out_root / f"{fid}_{safe_name(forum_name, 30)}"
    forum_dir.mkdir(parents=True, exist_ok=True)

    # 先抓首页拿到真实标题，再决定最终目录名
    url1 = THREAD_URL.format(tid=tid)
    html1 = cli.get(url1)
    title, floors, total_pages, breadcrumb, op_author, op_time, attaches = parse_thread_page(html1)

    final_dir = forum_dir / f"{tid}_{safe_name(title or f'thread-{tid}')}"
    raw_dir = final_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    (raw_dir / "page-1.html").write_text(html1, encoding="utf-8", errors="ignore")

    # 后续分页
    all_floors = list(floors)
    all_attach = list(attaches)
    for p in range(2, total_pages + 1):
        url_p = THREAD_PAGE_URL.format(tid=tid, page=p)
        html_p = cli.get(url_p, referer=url1)
        (raw_dir / f"page-{p}.html").write_text(html_p, encoding="utf-8", errors="ignore")
        _, fl_p, _, _, _, _, atts_p = parse_thread_page(html_p)
        for fl in fl_p:
            if fl.pid == "OP":
                continue
            all_floors.append(fl)
        for a in atts_p:
            if a not in all_attach:
                all_attach.append(a)

    meta = ThreadMeta(
        tid=tid,
        fid=fid,
        title=title or f"thread-{tid}",
        url=url1,
        forum_name=forum_name,
        pages=total_pages,
        author=op_author,
        author_url=floors[0].author_url if floors else "",
        created_at=op_time,
        floors_count=len(all_floors),
        attachments=all_attach,
        crawled_at=int(time.time()),
    )

    (final_dir / "meta.json").write_text(
        json.dumps(asdict(meta), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (final_dir / "post.md").write_text(render_post_md(meta, all_floors), encoding="utf-8")
    return meta


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=10, help="本次最多抓多少帖")
    p.add_argument("--fid", type=int, action="append", help="只抓某些版块的帖")
    p.add_argument("--tid", type=int, help="只抓单个 tid 调试")
    args = p.parse_args(argv)

    cfg = Config.load()
    cli = KxClient(cfg)
    db = open_db(cfg.state_dir, "threads.sqlite")
    init_thread_table(db)

    try:
        if args.tid:
            fid = 0
            row = db.execute("SELECT fid FROM threads WHERE tid=?", (args.tid,)).fetchone()
            if row:
                fid = row[0]
            forum_name = cfg.forums.get(fid, f"forum-{fid}")
            meta = crawl_one(cli, args.tid, fid, forum_name, cfg.output_dir)
            db.execute("UPDATE threads SET crawled_at=? WHERE tid=?", (meta.crawled_at, args.tid))
            db.commit()
            print(f"OK {args.tid}  floors={meta.floors_count}  pages={meta.pages}  -> {meta.title}")
            return 0

        sql = "SELECT tid, fid, title FROM threads WHERE crawled_at IS NULL"
        params: list = []
        if args.fid:
            sql += f" AND fid IN ({','.join('?'*len(args.fid))})"
            params.extend(args.fid)
        sql += " ORDER BY list_seen_at DESC LIMIT ?"
        params.append(args.limit)
        rows = db.execute(sql, params).fetchall()

        if not rows:
            print("nothing pending. run crawl_list first.")
            return 0

        print(f"will crawl {len(rows)} threads")
        for idx, (tid, fid, title) in enumerate(rows):
            forum_name = cfg.forums.get(fid, f"forum-{fid}")
            try:
                meta = crawl_one(cli, tid, fid, forum_name, cfg.output_dir)
            except DailyCapReached as e:
                log.error("daily cap reached, stop: %s", e)
                break
            except Throttled as e:
                log.error("throttled, stop: %s", e)
                break
            except Exception as e:
                log.exception("failed tid=%s: %s", tid, e)
                continue
            db.execute("UPDATE threads SET crawled_at=?, title=? WHERE tid=?",
                       (meta.crawled_at, meta.title, tid))
            db.commit()
            print(f"OK {tid:>7}  floors={meta.floors_count:<3}  pages={meta.pages:<2}  {meta.title[:60]}")
            # 每帖之间的额外停顿（除了最后一帖）
            if idx < len(rows) - 1:
                cli.post_thread_pause()
    finally:
        cli.close()
        db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
