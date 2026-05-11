"""快速验证 cookies 是否还登录有效：访问 user-center / 我的帖子 之类页面看是否未跳登录。"""
from __future__ import annotations

import logging
import sys

from .core import Config, KxClient

log = logging.getLogger("kanxue.check")


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    cfg = Config.load()
    cli = KxClient(cfg)
    try:
        html = cli.get("https://bbs.kanxue.com/")
    finally:
        cli.close()
    # 登录后首页会包含 "退出" / user-tasks / user-center 等关键字
    indicators = ["user-tasks-", "退出", "我的会员", "user-center"]
    hit = [k for k in indicators if k in html]
    print(f"login indicators found: {hit}")
    if len(hit) >= 2:
        print("OK: cookies are still valid.")
        return 0
    print("FAIL: cookies expired or unauthenticated. Re-login in playwright and re-export cookies.json.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
