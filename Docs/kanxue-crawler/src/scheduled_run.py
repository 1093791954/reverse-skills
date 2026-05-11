"""systemd timer 调用的入口。每天定时跑一次。

工作流（混合优先级：新帖 + 逐渐补老帖）：
  阶段 A — 刷新最新：所有白名单版块第 1 页（少量也可指定 --list-pages 加几页）
  阶段 B — 抓最新未抓的帖子：按 list_seen_at DESC 取 ≤ --threads 个 tid 下载
  阶段 C — 老帖回填：剩余请求额度 > 阈值时，挑几个版块的"下一页"（forum_backfill.last_backfill_page+1）刷一遍 list，
           顺便也把那些老帖加入待抓队列；下次再有额度时它们也会被消化掉

设计原则：
- 每次 systemd 触发都是独立、幂等、可中断的
- 任何 Throttled / DailyCapReached / 异常 → 写邮件 + exit
- 跑完一定发简报邮件
"""
from __future__ import annotations

import argparse
import logging
import sys
import time
import traceback
from pathlib import Path

from .core import Config, KxClient, Throttled, DailyCapReached, init_thread_table, open_db
from .crawl_list import crawl_forum, crawl_forum_pages
from .crawl_thread import crawl_one
from .notify import send_email

ROOT = Path(__file__).resolve().parent.parent

log = logging.getLogger("kanxue.scheduled")


def is_logged_in(html: str) -> bool:
    indicators = ["user-tasks-", "退出", "我的会员", "user-center"]
    hit = sum(1 for k in indicators if k in html)
    return hit >= 2


def socket_host() -> str:
    import socket
    try:
        return socket.gethostname()
    except Exception:
        return "?"


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    p = argparse.ArgumentParser()
    p.add_argument("--list-pages", type=int, default=1,
                   help="阶段 A：每个白名单版块抓多少页 list（拿最新）")
    p.add_argument("--threads", type=int, default=100,
                   help="阶段 B：本次最多下载多少帖正文")
    p.add_argument("--backfill-pages-per-forum", type=int, default=1,
                   help="阶段 C：每次回填给老版块新增多少页索引深度")
    p.add_argument("--backfill-forums-per-run", type=int, default=5,
                   help="阶段 C：每次最多挑多少个版块做回填")
    p.add_argument("--backfill-min-budget", type=int, default=300,
                   help="阶段 C：今日剩余 GET 额度大于多少才进行回填")
    p.add_argument("--forums", type=str, default="",
                   help="逗号分隔的 fid 列表；为空则用 config.toml [forums] 全部白名单")
    args = p.parse_args(argv)

    cfg = Config.load()
    cli = KxClient(cfg)
    db = open_db(cfg.state_dir, "threads.sqlite")
    init_thread_table(db)

    if args.forums:
        target_fids = [int(x) for x in args.forums.split(",") if x.strip()]
    else:
        target_fids = list(cfg.forums.keys())

    summary: list[str] = []
    failed = False
    stage_a_added = 0
    stage_b_done = 0
    stage_c_added = 0

    try:
        # === Step 0: 登录态检查 ===
        try:
            html = cli.get("https://bbs.kanxue.com/")
        except Exception as e:
            send_email(
                subject="[kanxue-crawler] 启动失败：首页都拉不到",
                body=f"host={socket_host()} time={time.strftime('%F %T')}\n{e!r}\n{traceback.format_exc()}",
                project_root=ROOT,
            )
            return 2
        if not is_logged_in(html):
            send_email(
                subject="[kanxue-crawler] cookies 失效，需要本机重新登录后同步",
                body=(
                    f"主机: {socket_host()}\n时间: {time.strftime('%F %T')}\n\n"
                    "check_login 没检测到登录态。\n"
                    "请在本机 playwright 重新登录看雪后，把新的 state/cookies.json 推到服务器：\n"
                    "  python deploy/bootstrap_remote.py    # 它会顺便重传 cookies\n"
                    "或单独走：\n"
                    "  bash deploy/push_cookies.sh root@YOUR_VPS_HOST\n"
                ),
                project_root=ROOT,
            )
            log.error("cookies expired, stop.")
            return 3
        log.info("login OK")

        # === 阶段 A：刷新最新 ===
        log.info("=== 阶段 A: 刷新最新 ===")
        for fid in target_fids:
            try:
                for _ in crawl_forum(cli, fid, args.list_pages, db):
                    stage_a_added += 1
            except (Throttled, DailyCapReached) as e:
                log.warning("[stage A] stop: %s", e)
                summary.append(f"[A] STOP: {e}")
                failed = True
                break
        summary.append(f"[A] 刷新最新：{len(target_fids)} 个版块各 {args.list_pages} 页 → 见到 {stage_a_added} 条")

        # === 阶段 B：下载未抓正文 ===
        if not failed:
            log.info("=== 阶段 B: 下载未抓正文（最新优先）===")
            placeholders = ",".join("?" * len(target_fids))
            rows = db.execute(
                f"SELECT tid, fid, title FROM threads "
                f"WHERE crawled_at IS NULL AND fid IN ({placeholders}) "
                f"ORDER BY list_seen_at DESC LIMIT ?",
                (*target_fids, args.threads),
            ).fetchall()
            for idx, (tid, fid, _title) in enumerate(rows):
                forum_name = cfg.forums.get(fid, f"forum-{fid}")
                try:
                    meta = crawl_one(cli, tid, fid, forum_name, cfg.output_dir)
                except DailyCapReached as e:
                    log.warning("[stage B] daily cap: %s", e)
                    summary.append(f"[B] STOP at #{idx+1}: daily cap reached")
                    failed = True
                    break
                except Throttled as e:
                    log.error("[stage B] throttled: %s", e)
                    summary.append(f"[B] THROTTLED at #{idx+1}: {e}")
                    failed = True
                    send_email(
                        subject="[kanxue-crawler] 触发风控，已停止",
                        body=f"主机: {socket_host()}\n时间: {time.strftime('%F %T')}\n\n{e!r}\n\n"
                             "建议：检查 cookies 是否失效；过几小时再重新跑；或手动浏览器访问看雪查看是否有验证码",
                        project_root=ROOT,
                    )
                    break
                except Exception as e:
                    log.exception("[stage B] failed tid=%s: %s", tid, e)
                    summary.append(f"[B] FAIL tid={tid}: {e!r}")
                    continue
                db.execute("UPDATE threads SET crawled_at=?, title=? WHERE tid=?",
                           (meta.crawled_at, meta.title, tid))
                db.commit()
                stage_b_done += 1
                if idx < len(rows) - 1:
                    cli.post_thread_pause()
            summary.append(f"[B] 下载帖子：{stage_b_done}/{len(rows)} 完成")

        # === 阶段 C：老帖回填（剩余额度足够时才做）===
        if not failed:
            today_used = cli.ledger.today_count()
            remain = cfg.daily_request_cap - today_used
            log.info("=== 阶段 C: 老帖回填 (今日剩余额度 %d) ===", remain)
            if remain >= args.backfill_min_budget:
                # 挑 last_backfill_page 最小（最久没回填的）几个版块
                rows = db.execute(
                    """
                    SELECT t.fid,
                           COALESCE(b.last_backfill_page, 1) AS lbp
                    FROM (SELECT DISTINCT fid FROM threads WHERE fid IN ({ph})) t
                    LEFT JOIN forum_backfill b ON b.fid = t.fid
                    ORDER BY lbp ASC, t.fid ASC
                    LIMIT ?
                    """.format(ph=",".join("?" * len(target_fids))),
                    (*target_fids, args.backfill_forums_per_run),
                ).fetchall()
                for fid, lbp in rows:
                    next_pages = list(range(lbp + 1, lbp + 1 + args.backfill_pages_per_forum))
                    log.info("[C] backfill fid=%s pages=%s", fid, next_pages)
                    forum_added = 0
                    last_ok_page = lbp
                    try:
                        for tid, _title in crawl_forum_pages(cli, fid, next_pages, db):
                            forum_added += 1
                        last_ok_page = max(next_pages)
                    except (Throttled, DailyCapReached) as e:
                        log.warning("[C] stop fid=%s: %s", fid, e)
                        failed = True
                    # 把游标推进到本轮成功抓到的最后一页
                    db.execute(
                        """
                        INSERT INTO forum_backfill(fid, last_backfill_page, updated_at)
                        VALUES (?, ?, ?)
                        ON CONFLICT(fid) DO UPDATE SET
                            last_backfill_page=excluded.last_backfill_page,
                            updated_at=excluded.updated_at
                        """,
                        (fid, last_ok_page, int(time.time())),
                    )
                    db.commit()
                    stage_c_added += forum_added
                    if failed:
                        break
                summary.append(f"[C] 老帖回填：新增索引 {stage_c_added} 条，覆盖 {len(rows)} 个版块")
            else:
                summary.append(f"[C] 跳过老帖回填（剩余额度 {remain} < 阈值 {args.backfill_min_budget}）")

    finally:
        cli.close()
        db.close()

    log.info("=== summary ===")
    for line in summary:
        log.info(line)

    # 简报邮件
    try:
        import sqlite3 as _sql
        conn = _sql.connect(ROOT / "state" / "threads.sqlite")
        try:
            total, done = conn.execute(
                "SELECT COUNT(*), SUM(crawled_at IS NOT NULL) FROM threads"
            ).fetchone()
            done = done or 0
            recent_titles = conn.execute(
                "SELECT tid, title FROM threads "
                "WHERE crawled_at IS NOT NULL ORDER BY crawled_at DESC LIMIT 10"
            ).fetchall()
            per_forum = conn.execute(
                "SELECT fid, COUNT(*), SUM(crawled_at IS NOT NULL) "
                "FROM threads GROUP BY fid ORDER BY fid"
            ).fetchall()
        finally:
            conn.close()
        ledger = _sql.connect(ROOT / "state" / "ledger.sqlite")
        try:
            row = ledger.execute(
                "SELECT n FROM req_count WHERE day=?", (time.strftime("%Y-%m-%d"),)
            ).fetchone()
            today_n = row[0] if row else 0
        finally:
            ledger.close()

        status_emoji = "✅" if not failed else "⚠️"
        subject = (
            f"[kanxue-crawler] {status_emoji} 日报 {time.strftime('%Y-%m-%d %H:%M')} "
            f"本次新抓 {stage_b_done} 帖，累计 {done}/{total}"
        )
        body_lines = [
            f"主机: {socket_host()}",
            f"完成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"本次结果: {'失败/中断' if failed else '正常完成'}",
            "",
            f"今日 GET 用量: {today_n}/{cfg.daily_request_cap}",
            f"全部已收录索引: {total}    已下载正文: {done}",
            f"本次新增索引(A): {stage_a_added}    本次新下载(B): {stage_b_done}    本次回填索引(C): {stage_c_added}",
            "",
            "本次执行简报：",
        ]
        body_lines.extend(f"  - {line}" for line in summary)
        if recent_titles:
            body_lines.append("")
            body_lines.append("最近抓完的 10 篇：")
            for tid, title in recent_titles:
                body_lines.append(f"  - {tid}  {title}")
        if per_forum:
            body_lines.append("")
            body_lines.append("各版块进度（fid, 索引数, 已下载）：")
            forum_names = cfg.forums
            for fid, ftotal, fdone in per_forum:
                fdone = fdone or 0
                name = forum_names.get(fid, f"forum-{fid}")
                body_lines.append(f"  - {fid:>4}  {name:<14}  {fdone}/{ftotal}")
        body_lines.append("")
        body_lines.append("说明：本邮件由 systemd timer 调用 scheduled_run 自动发出。")
        send_email(subject=subject, body="\n".join(body_lines), project_root=ROOT)
    except Exception as e:
        log.exception("failed to send summary email: %s", e)

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
