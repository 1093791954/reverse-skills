"""Background pool refresher.

Periodically (every `interval_s`) and on-demand (when
`pool.refresh_requested == True` or `pool.live_count() < pool.min_live`)
re-runs the proxy validator against `_methodology/proxies/us_all.txt`,
adds any newly fresh proxies to the AccountPool, and persists the
updated pool to disk.

This is started as an asyncio Task by `app.py`'s lifespan.
"""
from __future__ import annotations

import asyncio
import time
from pathlib import Path

from account_pool import AccountPool

DEFAULT_REFRESH_INTERVAL_S = 1800  # 30 min
PROXIES_DIR = Path(__file__).parent.parent / "_methodology" / "proxies"
SEED_TXT = PROXIES_DIR / "us_all.txt"
WORKING_TXT = PROXIES_DIR / "us_chatgptorg_working.txt"


async def refresh_once(pool: AccountPool, max_candidates: int = 50,
                       concurrency: int = 30) -> int:
    """Returns the number of newly-added accounts."""
    if not SEED_TXT.exists():
        return 0
    try:
        # Lazy import; validator is in another tree so we plug into its
        # probe_proxy function rather than re-implementing.
        import sys
        sys.path.insert(0, str(PROXIES_DIR))
        import validate_proxies as vp  # type: ignore
    except Exception as e:
        print(f"[refresher] cannot import validator: {e}", flush=True)
        return 0

    src_lines = []
    for line in SEED_TXT.read_text("utf-8").splitlines():
        line = line.split("#")[0].strip()
        if not line:
            continue
        if line.startswith("socks4://"):
            continue  # httpx + socksio doesn't speak socks4
        src_lines.append(line)

    seen = {a.proxy for a in pool.accounts.values()}
    candidates = [p for p in src_lines if p not in seen]
    if not candidates:
        print("[refresher] no new candidates in source list", flush=True)
        return 0
    candidates = candidates[:max_candidates]
    print(f"[refresher] probing {len(candidates)} candidates", flush=True)

    sem = asyncio.Semaphore(concurrency)

    async def bound(p):
        async with sem:
            return await vp.probe_proxy(p)

    results = await asyncio.gather(*[bound(p) for p in candidates])
    fresh = [r["proxy"] for r in results if r.get("verdict") == "OK_FRESH"]
    print(f"[refresher] {len(fresh)} OK_FRESH out of {len(candidates)}",
          flush=True)
    if fresh:
        added = await pool.add_proxies(fresh)
        # Persist to working txt so cold-start has a known-good seed
        try:
            existing = set()
            if WORKING_TXT.exists():
                for line in WORKING_TXT.read_text("utf-8").splitlines():
                    line = line.split("#")[0].strip()
                    if line:
                        existing.add(line)
            new_lines = [p for p in fresh if p not in existing]
            if new_lines:
                with WORKING_TXT.open("a", encoding="utf-8") as f:
                    f.write(f"\n# refresher add {time.ctime()}\n")
                    for p in new_lines:
                        f.write(f"{p}\n")
        except Exception as e:
            print(f"[refresher] persist working_txt err: {e}", flush=True)
        return added
    return 0


async def refresher_loop(pool: AccountPool,
                         interval_s: int = DEFAULT_REFRESH_INTERVAL_S
                         ) -> None:
    while True:
        try:
            need = (pool.live_count() < pool.min_live or
                    pool.refresh_requested)
            if need:
                added = await refresh_once(pool)
                pool.refresh_requested = False
                pool.last_refresh_at = time.time()
                print(f"[refresher] added {added}; "
                      f"pool stats={pool.stats()}", flush=True)
        except Exception as e:
            print(f"[refresher] error: {type(e).__name__}: {e}", flush=True)
        await asyncio.sleep(interval_s)
