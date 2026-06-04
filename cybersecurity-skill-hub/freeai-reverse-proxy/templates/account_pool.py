"""Account pool for the reverse-proxy.

An "account" is a tuple (proxy, optional device_uuid, optional cookies)
representing one identity to use against an upstream free chat site.
Single accounts have small daily quotas; we maintain a pool, rotate
across them, mark dead/exhausted, and auto-replenish.

State is persisted to a JSON file so the pool survives server restarts.
File writes are atomic (`.tmp` + `os.replace`) and serialized via an
`asyncio.Lock`.

This module has zero dependency on httpx / FastAPI / specific drivers.
"""
from __future__ import annotations

import asyncio
import json
import os
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

DEFAULT_STORE_PATH = Path(__file__).parent / "account_pool.json"
DEFAULT_SEED_PATH = (
    Path(__file__).parent.parent / "_methodology" / "proxies"
    / "us_chatgptorg_working.txt"
)


# Tunables (env-configurable)
EXHAUSTED_TTL_SECONDS = int(os.environ.get(
    "REVERSE_PROXY_EXHAUSTED_TTL", str(24 * 3600)))
DEAD_ERROR_THRESHOLD = int(os.environ.get(
    "REVERSE_PROXY_DEAD_THRESHOLD", "3"))
DEAD_ERROR_WINDOW_SECONDS = int(os.environ.get(
    "REVERSE_PROXY_DEAD_WINDOW", "60"))
DAILY_RESET_INTERVAL = 86400


@dataclass
class Account:
    id: str
    proxy: str = ""              # "socks5://h:p" / "http://h:p" / "" = direct
    device_uuid: str | None = None
    cookies: dict[str, str] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    last_used_at: float = 0.0
    requests_today: int = 0
    requests_total: int = 0
    exhausted_until: float = 0.0   # unix ts; 0 = not exhausted
    consec_errors: int = 0
    last_error_at: float = 0.0
    dead: bool = False
    in_flight: int = 0
    last_reset_at: float = field(default_factory=time.time)

    def to_json(self) -> dict:
        return asdict(self)

    @classmethod
    def from_json(cls, d: dict) -> "Account":
        return cls(**d)

    @classmethod
    def from_proxy(cls, proxy: str) -> "Account":
        # Stable id = first 12 chars of sha-like hash of the proxy string
        import hashlib
        h = hashlib.sha256(proxy.encode("utf-8")).hexdigest()[:12]
        return cls(id=f"acc_{h}", proxy=proxy)


class NoAccountsAvailable(Exception):
    pass


class AccountPool:
    """In-memory pool with JSON-file persistence.

    Lifecycle:
        pool = AccountPool.load_or_init()
        acc = await pool.claim()
        try:
            ... use acc.proxy ...
            await pool.release(acc, outcome="ok")
        except UpstreamRateLimited:
            await pool.release(acc, outcome="exhausted")
        except (TimeoutError, OSError):
            await pool.release(acc, outcome="unreachable")
    """

    def __init__(self,
                 path: Path = DEFAULT_STORE_PATH,
                 min_live: int = 3):
        self.path = Path(path)
        self.accounts: dict[str, Account] = {}
        self._lock = asyncio.Lock()
        self.min_live: int = min_live
        self.refresh_requested: bool = False
        self.last_refresh_at: float = 0.0

    # -------- Persistence --------

    @classmethod
    def load_or_init(cls,
                     path: Path = DEFAULT_STORE_PATH,
                     seed_path: Path = DEFAULT_SEED_PATH,
                     min_live: int = 3) -> "AccountPool":
        pool = cls(path=path, min_live=min_live)
        if pool.path.exists():
            try:
                data = json.loads(pool.path.read_text("utf-8"))
                for a in data.get("accounts", []):
                    acc = Account.from_json(a)
                    # `in_flight` is purely in-process state; if a previous
                    # server crashed mid-request, the persisted file may
                    # still show in_flight>0. Reset so the account becomes
                    # claimable again at startup.
                    acc.in_flight = 0
                    pool.accounts[acc.id] = acc
                pool.last_refresh_at = data.get("last_refresh_at", 0.0)
            except Exception as e:
                print(f"[pool] load failed: {e}; starting empty", flush=True)
                pool.accounts = {}
        if not pool.accounts and seed_path and Path(seed_path).exists():
            seed = _read_proxies(seed_path)
            for p in seed:
                acc = Account.from_proxy(p)
                pool.accounts[acc.id] = acc
            print(f"[pool] seeded {len(pool.accounts)} accounts from "
                  f"{seed_path}", flush=True)
        return pool

    def _persist_sync(self) -> None:
        """Atomic write of the pool to disk."""
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        payload = {
            "accounts": [a.to_json() for a in self.accounts.values()],
            "last_refresh_at": self.last_refresh_at,
        }
        tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                       encoding="utf-8")
        os.replace(tmp, self.path)

    async def _persist_async(self) -> None:
        # SQLite-style fast write — for now we just call sync from inside
        # the lock; throughput is OK because writes are infrequent.
        self._persist_sync()

    # -------- Stats / health --------

    def live_count(self) -> int:
        now = time.time()
        return sum(1 for a in self.accounts.values()
                   if not a.dead and a.exhausted_until <= now
                   and a.in_flight == 0)

    def stats(self) -> dict:
        now = time.time()
        live = exhausted = dead = in_flight = 0
        for a in self.accounts.values():
            if a.dead:
                dead += 1
            elif a.exhausted_until > now:
                exhausted += 1
            else:
                live += 1
            in_flight += a.in_flight
        return {
            "live": live,
            "exhausted": exhausted,
            "dead": dead,
            "in_flight": in_flight,
            "total": len(self.accounts),
            "last_refresh_at": self.last_refresh_at,
        }

    # -------- Claim / release --------

    async def claim(self) -> Account:
        async with self._lock:
            now = time.time()
            self._maybe_daily_reset(now)
            candidates = [
                a for a in self.accounts.values()
                if not a.dead
                and a.exhausted_until <= now
                and a.in_flight == 0
            ]
            if not candidates:
                if self.live_count() == 0:
                    self.refresh_requested = True
                raise NoAccountsAvailable(
                    f"no live accounts (total={len(self.accounts)})")
            candidates.sort(key=lambda a: (a.last_used_at, a.requests_today))
            chosen = candidates[0]
            chosen.in_flight = 1
            chosen.last_used_at = now
            await self._persist_async()
            if self.live_count() < self.min_live:
                self.refresh_requested = True
            return chosen

    async def release(self, acc: Account, outcome: str) -> None:
        """outcome ∈ {ok, exhausted, unreachable, dead}."""
        async with self._lock:
            now = time.time()
            account = self.accounts.get(acc.id, acc)
            account.in_flight = max(0, account.in_flight - 1)
            if outcome == "ok":
                account.requests_today += 1
                account.requests_total += 1
                account.consec_errors = 0
            elif outcome == "exhausted":
                account.exhausted_until = now + EXHAUSTED_TTL_SECONDS
            elif outcome == "unreachable":
                # 3 errors within DEAD_ERROR_WINDOW_SECONDS → dead
                if (now - account.last_error_at) < DEAD_ERROR_WINDOW_SECONDS:
                    account.consec_errors += 1
                else:
                    account.consec_errors = 1
                account.last_error_at = now
                if account.consec_errors >= DEAD_ERROR_THRESHOLD:
                    account.dead = True
            elif outcome == "dead":
                account.dead = True
            await self._persist_async()

    # -------- Replenishment hook --------

    async def add(self, acc: Account) -> bool:
        """Add an account; returns True if newly added (not duplicate)."""
        async with self._lock:
            if acc.id in self.accounts:
                return False
            self.accounts[acc.id] = acc
            await self._persist_async()
            return True

    async def add_proxies(self, proxies: Iterable[str]) -> int:
        """Convenience helper: turn each proxy URL into a fresh Account."""
        added = 0
        async with self._lock:
            for p in proxies:
                acc = Account.from_proxy(p)
                if acc.id not in self.accounts:
                    self.accounts[acc.id] = acc
                    added += 1
            self.last_refresh_at = time.time()
            await self._persist_async()
        return added

    # -------- Internal --------

    def _maybe_daily_reset(self, now: float) -> None:
        for a in self.accounts.values():
            if (now - a.last_reset_at) >= DAILY_RESET_INTERVAL:
                a.requests_today = 0
                a.last_reset_at = now
                # Auto-recover from "exhausted" once the window elapses.
                if a.exhausted_until and a.exhausted_until <= now:
                    a.exhausted_until = 0.0
                # Death is sticky; manual revive only.


# -------- Helpers --------

def _read_proxies(path: Path) -> list[str]:
    out = []
    for line in Path(path).read_text("utf-8").splitlines():
        line = line.split("#")[0].strip()
        if line:
            out.append(line)
    return out
