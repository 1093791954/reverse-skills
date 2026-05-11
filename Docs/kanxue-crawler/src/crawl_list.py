"""抓取版块帖子列表，把 (tid, title, url) 写入 state/threads.sqlite。"""
from __future__ import annotations

import argparse
import logging
import re
import sys
import time
from typing import Iterable

from selectolax.parser import HTMLParser

from .core import Config, KxClient, Throttled, DailyCapReached, init_thread_table, open_db

log = logging.getLogger("kanxue.list")

# /forum-{fid}-{page}.htm  (按发帖时间) — 实测带 ?orderby=lastpid&digest=0 也是这个结构
LIST_URL = "https://bbs.kanxue.com/forum-{fid}-{page}.htm"

THREAD_HREF_RE = re.compile(r"thread-(\d+)\.htm$")


def parse_list_page(html: str) -> list[tuple[int, str]]:
    """返回 [(tid, title), ...]。只取主题链接，去掉分页内的"最后一页"指向的 thread-{tid}-{p}.htm。"""
    tree = HTMLParser(html)
    out: dict[int, str] = {}
    for a in tree.css("table.threadlist a[href*='thread-']"):
        href = a.attributes.get("href") or ""
        m = THREAD_HREF_RE.search(href)
        if not m:
            continue
        title = (a.text() or "").strip()
        if not title:
            continue
        tid = int(m.group(1))
        # 取最长那条文本（标题），跳过仅图标的链接
        if tid not in out or len(title) > len(out[tid]):
            out[tid] = title
    return list(out.items())


def crawl_forum(cli: KxClient, fid: int, max_pages: int, db) -> Iterable[tuple[int, str]]:
    """从第 1 页开始抓 max_pages 页（用于刷最新）。"""
    yield from _crawl_forum_pages(cli, fid, range(1, max_pages + 1), db)


def crawl_forum_pages(cli: KxClient, fid: int, page_range, db) -> Iterable[tuple[int, str]]:
    """抓任意页码范围（用于回填老帖）。page_range 是可迭代的整数序列。"""
    yield from _crawl_forum_pages(cli, fid, page_range, db)


def _crawl_forum_pages(cli: KxClient, fid: int, pages, db):
    referer = f"https://bbs.kanxue.com/forum-{fid}.htm"
    now = int(time.time())
    for page in pages:
        url = LIST_URL.format(fid=fid, page=page)
        try:
            html = cli.get(url, referer=referer)
        except DailyCapReached as e:
            log.error("daily cap reached: %s", e)
            return
        except Throttled as e:
            log.error("throttled, stopping forum %s page %s: %s", fid, page, e)
            return
        rows = parse_list_page(html)
        log.info("forum=%s page=%s got %d threads", fid, page, len(rows))
        if not rows:
            log.info("no rows; stop forum %s at page %s", fid, page)
            return
        with db:
            for tid, title in rows:
                db.execute(
                    """
                    INSERT INTO threads (tid, fid, title, url, list_seen_at)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(tid) DO UPDATE SET
                        title=excluded.title,
                        list_seen_at=excluded.list_seen_at
                    """,
                    (tid, fid, title, f"https://bbs.kanxue.com/thread-{tid}.htm", now),
                )
        yield from rows
        referer = url


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    p = argparse.ArgumentParser()
    p.add_argument("--forum", type=int, action="append", required=True,
                   help="目标版块 fid，可重复指定")
    p.add_argument("--max-pages", type=int, default=3)
    args = p.parse_args(argv)

    cfg = Config.load()
    cli = KxClient(cfg)
    db = open_db(cfg.state_dir, "threads.sqlite")
    init_thread_table(db)
    try:
        total = 0
        for fid in args.forum:
            for _ in crawl_forum(cli, fid, args.max_pages, db):
                total += 1
        print(f"done. total threads ingested (incl. duplicates updated): {total}")
    finally:
        cli.close()
        db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
