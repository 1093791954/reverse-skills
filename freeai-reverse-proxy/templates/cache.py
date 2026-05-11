"""Local prompt-prefix cache for the reverse-proxy.

Mimics OpenAI's prompt-cache savings: a chat completion's response is
keyed by a hash of the conversation **prefix** (everything before the
last user message). Identical prefixes (which is what OpenCode produces
when its long system+history prefix is unchanged across turns) hit the
cache and skip both the upstream call AND the account-pool consumption.

Modes (env REVERSE_PROXY_CACHE):
  disabled  - skip cache entirely
  exact     - key includes ALL messages; only identical inputs hit
  prefix    - key = messages[:-1], plus a `last_user_hash` verifier
              against messages[-1]. Default.

Storage: SQLite at _reverse_proxy/prompt_cache.db. WAL mode for
concurrent readers. TTL 7 days, total size capped at 256 MB.
"""
from __future__ import annotations

import asyncio
import gzip
import hashlib
import json
import os
import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

DEFAULT_DB_PATH = Path(__file__).parent / "prompt_cache.db"
DEFAULT_TTL_SECONDS = int(os.environ.get(
    "REVERSE_PROXY_CACHE_TTL_DAYS", "7")) * 86400
DEFAULT_MAX_BYTES = int(os.environ.get(
    "REVERSE_PROXY_CACHE_MAX_BYTES", str(256 * 1024 * 1024)))
DEFAULT_MODE = os.environ.get("REVERSE_PROXY_CACHE", "prefix").lower()


@dataclass
class CachedResponse:
    """Materialized assistant response for one cached input."""
    text: str = ""
    tool_calls: list = field(default_factory=list)
    sse: bytes | None = None  # optional pre-rendered SSE bytes for replay

    def to_blob(self) -> bytes:
        payload = {"text": self.text, "tool_calls": self.tool_calls}
        return gzip.compress(json.dumps(payload, ensure_ascii=False).encode())

    @classmethod
    def from_blob(cls, blob: bytes,
                  sse_blob: bytes | None = None) -> "CachedResponse":
        d = json.loads(gzip.decompress(blob).decode())
        return cls(text=d.get("text", ""),
                   tool_calls=d.get("tool_calls") or [],
                   sse=gzip.decompress(sse_blob) if sse_blob else None)


class PromptCache:
    """SQLite-backed cache. Methods are thread-safe via a single lock
    (SQLite WAL plus a Python lock keeps it simple)."""

    def __init__(self,
                 db_path: Path = DEFAULT_DB_PATH,
                 ttl_seconds: int = DEFAULT_TTL_SECONDS,
                 max_bytes: int = DEFAULT_MAX_BYTES,
                 mode: str = DEFAULT_MODE):
        self.db_path = Path(db_path)
        self.ttl_seconds = ttl_seconds
        self.max_bytes = max_bytes
        self.mode = mode if mode in ("disabled", "exact", "prefix") else "prefix"
        self._lock = asyncio.Lock()
        self._init_db()

    # ---------- DB ----------

    def _conn(self) -> sqlite3.Connection:
        c = sqlite3.connect(self.db_path)
        c.execute("PRAGMA journal_mode=WAL")
        c.execute("PRAGMA synchronous=NORMAL")
        return c

    def _init_db(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as c:
            c.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    model TEXT NOT NULL,
                    last_user_hash TEXT NOT NULL,
                    response_blob BLOB NOT NULL,
                    sse_blob BLOB,
                    bytes INTEGER NOT NULL,
                    created_at REAL NOT NULL,
                    last_hit_at REAL NOT NULL,
                    hit_count INTEGER NOT NULL DEFAULT 0
                )
            """)
            c.execute("CREATE INDEX IF NOT EXISTS cache_lru "
                      "ON cache(last_hit_at)")
        self._gc()

    # ---------- Keys ----------

    @classmethod
    def _canon_messages(cls, messages: list) -> str:
        canon = []
        for m in messages:
            if hasattr(m, "role"):
                # dataclass-like (driver_base.Message)
                canon.append({
                    "role": getattr(m, "role", None),
                    "content": getattr(m, "content", None),
                    "name": getattr(m, "name", None),
                    "tool_call_id": getattr(m, "tool_call_id", None),
                })
            else:
                # dict-like
                canon.append({
                    "role": m.get("role"),
                    "content": m.get("content"),
                    "name": m.get("name"),
                    "tool_call_id": m.get("tool_call_id"),
                })
        return json.dumps(canon, ensure_ascii=False, sort_keys=True)

    def _last_user_hash(self, messages: list) -> str:
        last_user = None
        for m in reversed(messages):
            if hasattr(m, "role"):
                r = m.role
            else:
                r = m.get("role")
            if r == "user":
                last_user = m
                break
        if last_user is None:
            return ""
        if hasattr(last_user, "content"):
            c = last_user.content or ""
        else:
            c = last_user.get("content") or ""
        return hashlib.sha256(c.encode("utf-8")).hexdigest()

    def make_key(self, model: str, messages: list) -> tuple[str, str]:
        """Returns (key, last_user_hash). Key depends on mode."""
        if self.mode == "exact":
            canon = self._canon_messages(messages)
            return (
                hashlib.sha256(f"{model}\n{canon}".encode()).hexdigest(),
                self._last_user_hash(messages),
            )
        # prefix mode
        last_user_idx = None
        for i in range(len(messages) - 1, -1, -1):
            if hasattr(messages[i], "role"):
                r = messages[i].role
            else:
                r = messages[i].get("role")
            if r == "user":
                last_user_idx = i
                break
        if last_user_idx is None:
            prefix = messages
        else:
            prefix = messages[:last_user_idx]
        canon = self._canon_messages(prefix)
        return (
            hashlib.sha256(f"{model}\n{canon}".encode()).hexdigest(),
            self._last_user_hash(messages),
        )

    # ---------- Lookup / insert ----------

    async def lookup(self, model: str,
                     messages: list) -> Optional[CachedResponse]:
        if self.mode == "disabled":
            return None
        key, last_user_hash = self.make_key(model, messages)
        async with self._lock:
            now = time.time()
            with self._conn() as c:
                row = c.execute(
                    "SELECT last_user_hash, response_blob, sse_blob, "
                    "created_at FROM cache WHERE key=?",
                    (key,),
                ).fetchone()
                if row is None:
                    return None
                stored_lu, blob, sse_blob, created_at = row
                if (now - created_at) > self.ttl_seconds:
                    c.execute("DELETE FROM cache WHERE key=?", (key,))
                    return None
                if self.mode == "prefix" and stored_lu != last_user_hash:
                    return None
                # Update LRU + hit_count
                c.execute(
                    "UPDATE cache SET last_hit_at=?, hit_count=hit_count+1 "
                    "WHERE key=?",
                    (now, key),
                )
            return CachedResponse.from_blob(blob, sse_blob)

    async def insert(self, model: str, messages: list,
                     response: CachedResponse) -> None:
        if self.mode == "disabled":
            return
        key, last_user_hash = self.make_key(model, messages)
        blob = response.to_blob()
        sse_blob = (gzip.compress(response.sse)
                    if response.sse is not None else None)
        size = len(blob) + (len(sse_blob) if sse_blob else 0)
        now = time.time()
        async with self._lock:
            with self._conn() as c:
                c.execute(
                    "INSERT OR REPLACE INTO cache (key, model, last_user_hash, "
                    "response_blob, sse_blob, bytes, created_at, "
                    "last_hit_at, hit_count) VALUES "
                    "(?,?,?,?,?,?,?,?,?)",
                    (key, model, last_user_hash, blob, sse_blob, size,
                     now, now, 0),
                )
            self._evict_if_over_cap()

    # ---------- Maintenance ----------

    def _gc(self) -> None:
        """Drop expired rows + evict to fit under max_bytes."""
        now = time.time()
        with self._conn() as c:
            c.execute("DELETE FROM cache WHERE created_at < ?",
                      (now - self.ttl_seconds,))
        self._evict_if_over_cap()

    def _evict_if_over_cap(self) -> None:
        with self._conn() as c:
            row = c.execute("SELECT COALESCE(SUM(bytes),0) FROM cache").fetchone()
            total = row[0] if row else 0
            if total <= self.max_bytes:
                return
            cur = c.execute(
                "SELECT key, bytes FROM cache ORDER BY last_hit_at ASC")
            to_delete = []
            for key, bs in cur:
                to_delete.append(key)
                total -= bs
                if total <= self.max_bytes:
                    break
            if to_delete:
                placeholders = ",".join("?" for _ in to_delete)
                c.execute(f"DELETE FROM cache WHERE key IN ({placeholders})",
                          to_delete)

    def stats(self) -> dict:
        with self._conn() as c:
            row = c.execute(
                "SELECT COUNT(*), COALESCE(SUM(bytes),0), "
                "COALESCE(SUM(hit_count),0) FROM cache").fetchone()
        return {
            "rows": row[0],
            "bytes": row[1],
            "hit_count_total": row[2],
            "mode": self.mode,
        }
