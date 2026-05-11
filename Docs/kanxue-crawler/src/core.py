"""HTTP / 风控 / 存储底层。所有爬虫脚本都通过 KxClient 发请求。"""
from __future__ import annotations

import json
import logging
import random
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
try:
    import tomllib  # py3.11+
except ImportError:  # pragma: no cover
    import tomli as tomllib  # type: ignore
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/148.0.0.0 Safari/537.36"
)

log = logging.getLogger("kanxue")


@dataclass
class Config:
    min_delay: float
    max_delay: float
    post_thread_min_delay: float
    post_thread_max_delay: float
    daily_request_cap: int
    session_thread_cap: int
    timeout: float
    max_retries: int
    output_dir: Path
    state_dir: Path
    cookies_path: Path
    forums: dict[int, str]

    @classmethod
    def load(cls, path: Path | None = None) -> "Config":
        path = path or (ROOT / "config.toml")
        with open(path, "rb") as f:
            cfg = tomllib.load(f)
        net = cfg["network"]
        paths = cfg["paths"]
        forums = {int(k): v for k, v in cfg["forums"].items()}
        return cls(
            min_delay=float(net["min_delay"]),
            max_delay=float(net["max_delay"]),
            post_thread_min_delay=float(net.get("post_thread_min_delay", 0)),
            post_thread_max_delay=float(net.get("post_thread_max_delay", 0)),
            daily_request_cap=int(net.get("daily_request_cap", 600)),
            session_thread_cap=int(net.get("session_thread_cap", 20)),
            timeout=float(net["timeout"]),
            max_retries=int(net["max_retries"]),
            output_dir=ROOT / paths["output_dir"],
            state_dir=ROOT / paths["state_dir"],
            cookies_path=ROOT / paths["cookies"],
            forums=forums,
        )


def load_cookies(path: Path) -> dict[str, str]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("cookies", {})


class Throttled(Exception):
    """触发风控限流。需要长时间退避或停止人工介入。"""


class DailyCapReached(Exception):
    """已达每日请求上限。立刻停止，明天再继续。"""


def _today_key() -> str:
    return time.strftime("%Y-%m-%d")


class RequestLedger:
    """跨进程持久化的"今日请求计数器"。落在 state/ledger.sqlite，永远不会因为进程重启而重置。"""

    def __init__(self, state_dir: Path):
        state_dir.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(state_dir / "ledger.sqlite")
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS req_count (day TEXT PRIMARY KEY, n INTEGER NOT NULL)"
        )
        self._conn.commit()

    def today_count(self) -> int:
        row = self._conn.execute("SELECT n FROM req_count WHERE day=?", (_today_key(),)).fetchone()
        return row[0] if row else 0

    def bump(self) -> int:
        with self._conn:
            self._conn.execute(
                "INSERT INTO req_count(day,n) VALUES(?,1) ON CONFLICT(day) DO UPDATE SET n=n+1",
                (_today_key(),),
            )
        return self.today_count()

    def close(self) -> None:
        self._conn.close()


class KxClient:
    """带风控防御的 httpx 同步客户端。

    - 顺序抓取，无并发
    - 每请求间随机 sleep（默认 8~22s，模拟正常阅读）
    - 每日全局请求计数：超过 daily_request_cap 立刻停止
    - 429/403/连续 5xx 走指数退避；连续 ≥3 次直接抛 Throttled，让上层停下来
    - 返回 200 但内容像验证码/未登录页 -> 抛 Throttled
    """

    BASE = "https://bbs.kanxue.com"

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.cookies = load_cookies(cfg.cookies_path)
        self._client = httpx.Client(
            http2=True,
            timeout=cfg.timeout,
            headers={
                "User-Agent": DEFAULT_UA,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Ch-Ua": '"Chromium";v="148", "Google Chrome";v="148", "Not.A/Brand";v="99"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
            },
            cookies=self.cookies,
            follow_redirects=True,
        )
        self._consecutive_block = 0
        self.ledger = RequestLedger(cfg.state_dir)

    def close(self) -> None:
        self._client.close()
        self.ledger.close()

    def _sleep(self) -> None:
        time.sleep(random.uniform(self.cfg.min_delay, self.cfg.max_delay))

    def post_thread_pause(self) -> None:
        """每抓完一个帖子之后调用，模拟"看完一篇再翻下一篇"的真实间隔。"""
        if self.cfg.post_thread_max_delay > 0:
            t = random.uniform(self.cfg.post_thread_min_delay, self.cfg.post_thread_max_delay)
            log.info("inter-thread pause %.1fs", t)
            time.sleep(t)

    @retry(
        retry=retry_if_exception_type((httpx.TransportError, httpx.RemoteProtocolError)),
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=2, min=2, max=30),
        reraise=True,
    )
    def _raw_get(self, url: str, *, referer: str | None = None) -> httpx.Response:
        headers: dict[str, str] = {}
        if referer:
            headers["Referer"] = referer
        return self._client.get(url, headers=headers)

    def get(self, url: str, *, referer: str | None = None) -> str:
        """抓取并返回 HTML 文本。所有抓取入口都走这里。"""
        if not url.startswith("http"):
            url = f"{self.BASE}/{url.lstrip('/')}"
        # 每日请求上限保护
        n_today = self.ledger.today_count()
        if n_today >= self.cfg.daily_request_cap:
            raise DailyCapReached(f"daily cap {self.cfg.daily_request_cap} reached ({n_today}). stop.")
        self._sleep()
        resp = self._raw_get(url, referer=referer)
        cnt = self.ledger.bump()
        log.info("GET %s -> %s (%d bytes, today=%d/%d)",
                 url, resp.status_code, len(resp.content), cnt, self.cfg.daily_request_cap)
        if resp.status_code in (403, 429) or resp.status_code >= 500:
            self._consecutive_block += 1
            backoff = min(120, 10 * (2 ** self._consecutive_block))
            log.warning("status=%d block_count=%d backoff=%ds",
                        resp.status_code, self._consecutive_block, backoff)
            time.sleep(backoff)
            if self._consecutive_block >= 3:
                raise Throttled(f"too many blocks at {url}, giving up to protect account")
            return self.get(url, referer=referer)
        body = resp.text
        if "验证码" in body and "submit" in body and len(body) < 6000:
            raise Throttled(f"captcha page at {url}")
        if "请登录" in body and "user-login" in body and len(body) < 12000:
            raise Throttled("session expired, re-login required")
        self._consecutive_block = 0
        return body


# ---------------- state (sqlite) ----------------

def open_db(state_dir: Path, name: str) -> sqlite3.Connection:
    state_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(state_dir / name)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn


def init_thread_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS threads (
            tid INTEGER PRIMARY KEY,
            fid INTEGER NOT NULL,
            title TEXT,
            url TEXT,
            list_seen_at INTEGER,
            crawled_at INTEGER
        )
        """
    )
    # 每个版块的"老帖回填游标"：记录已经从尾页方向往回扫到第几页（数字越大表示已经扫到越深）
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS forum_backfill (
            fid INTEGER PRIMARY KEY,
            last_backfill_page INTEGER NOT NULL DEFAULT 1,
            updated_at INTEGER
        )
        """
    )
    conn.commit()
