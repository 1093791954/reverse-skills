"""Per-site ChatDriver skeleton.

Copy this file to <new-site>/driver.py, replace the SITE-SPECIFIC
markers, then point app.py at it via:

    from driver import MyNewDriver
    register_driver(MyNewDriver(pool=app.state.pool))

The shape comes from `chatgpt.org/driver.py`, which is the only
fully validated driver in the project (PASS 3/3 in
test_opencode_agent.py + multi_turn ALL OK).  Read that file for
all the stability fixes baked in:

- retry-on-no-tool-use (handled by app.py)
- 90-second wall-clock deadline per upstream stream
- SOCKS5 ProtocolError catch-all
- max_retries=10 with LRU account pool
- exhausted (429) vs unreachable (5xx/timeout) classification
- proper account release in try/finally

Required SDKs:
    pip install httpx 'httpx[socks]'
"""
from __future__ import annotations

# --- _common/ sibling import (let the driver be unit-testable on its own) ---
import sys as _sys
from pathlib import Path as _Path
_COMMON_DIR = _Path(__file__).parent.parent / "_common"
if str(_COMMON_DIR) not in _sys.path:
    _sys.path.insert(0, str(_COMMON_DIR))

import json
import os
import time
from typing import AsyncIterator

import httpx

from driver_base import (
    ChatDriver,
    ChatRequest,
    StreamChunk,
    StreamDone,
    TextDelta,
    ToolCallEnd,
)
from tool_proxy import FenceStreamParser


# ============================ SITE-SPECIFIC ============================
SITE_API_URL = "https://<your-site>/api/chat"   # ← change me

MODEL_MAPPING: dict[str, str] = {
    # OpenAI alias (what clients ask for) → upstream model id
    "claude-haiku-4-5": "anthropic/claude-haiku-4-5",
    # add more aliases here
}

DEFAULT_UPSTREAM_MODEL = "anthropic/claude-haiku-4-5"


def _build_body(req: ChatRequest) -> dict:
    """Translate our canonical ChatRequest into the site's native body."""
    upstream_model = MODEL_MAPPING.get(req.model, DEFAULT_UPSTREAM_MODEL)
    return {
        "model": upstream_model,
        "messages": [
            {"role": m.role, "content": m.content}
            for m in req.messages
            if m.role in ("system", "user", "assistant")
        ],
        # site-specific extras here
    }


def _headers() -> dict:
    """Mimic a real browser. Most free sites don't require auth at all,
    but they DO sniff User-Agent / Origin / Referer."""
    return {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "Origin": "https://<your-site>",
        "Referer": "https://<your-site>/chat",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/130.0.0.0 Safari/537.36",
    }
# ======================================================================


class MyNewDriver(ChatDriver):
    name = "<your-site>"
    supported_models = list(MODEL_MAPPING.keys()) + [
        v for v in MODEL_MAPPING.values()
    ]

    def __init__(self, pool=None):
        self._pool = pool
        self._env_proxy = (
            os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY") or "")

    def _get_pool(self):
        if self._pool is not None:
            return self._pool
        from account_pool import AccountPool
        self._pool = AccountPool.load_or_init()
        return self._pool

    async def _try_one_proxy(self, proxy: str | None, body: dict, parser):
        """Yields:
            ('chunk', StreamChunk)   — real content
            ('done', finish_reason)  — clean stream end
            ('exhausted', err_msg)   — upstream said 429 / "limit reached"
            ('unreachable', err_msg) — connection / format / SOCKS error
        """
        client_kwargs = {"timeout": httpx.Timeout(120.0, connect=15.0)}
        if proxy:
            client_kwargs["proxy"] = proxy
            client_kwargs["verify"] = False  # free proxies often have weird certs
        try:
            async with httpx.AsyncClient(**client_kwargs) as client:
                async with client.stream(
                    "POST", SITE_API_URL,
                    headers=_headers(),
                    json=body,
                ) as r:
                    if r.status_code != 200:
                        text = await r.aread()
                        text_s = (text.decode(errors="replace")
                                  if isinstance(text, bytes) else str(text))
                        if r.status_code == 429 or "limit reached" in text_s.lower():
                            yield ("exhausted", f"upstream {r.status_code}: "
                                                f"{text_s[:200]}")
                        else:
                            yield ("unreachable", f"upstream {r.status_code}: "
                                                  f"{text_s[:200]}")
                        return

                    upstream_ct = r.headers.get("content-type", "")
                    if "text/event-stream" not in upstream_ct.lower():
                        text = await r.aread()
                        text_s = (text.decode(errors="replace")
                                  if isinstance(text, bytes) else str(text))
                        if "limit reached" in text_s.lower() or '"error"' in text_s:
                            yield ("exhausted", f"non-stream: {text_s[:200]}")
                        else:
                            yield ("unreachable", f"non-stream {upstream_ct}: "
                                                  f"{text_s[:200]}")
                        return

                    # === Wall-clock deadline (fixes slow-trickle streams) ===
                    deadline_s = float(os.environ.get(
                        "REVERSE_PROXY_STREAM_DEADLINE", "90"))
                    deadline = time.monotonic() + deadline_s

                    finish_reason: str | None = None
                    async for line in r.aiter_lines():
                        if time.monotonic() > deadline:
                            yield ("unreachable",
                                   f"wall-clock {deadline_s}s exceeded via "
                                   f"{proxy or 'no-proxy'}")
                            return
                        if not line or line.startswith(":"):
                            continue
                        if not line.startswith("data: "):
                            continue
                        data = line[6:].strip()
                        if data == "[DONE]":
                            continue
                        try:
                            ev = json.loads(data)
                        except json.JSONDecodeError:
                            continue
                        choice = (ev.get("choices") or [{}])[0]
                        delta = choice.get("delta") or {}
                        txt = delta.get("content") or ""
                        if txt:
                            for out in parser.feed(txt):
                                yield ("chunk", out)
                        fr = choice.get("finish_reason")
                        if fr:
                            finish_reason = fr
                    for out in parser.flush():
                        yield ("chunk", out)
                    yield ("done", finish_reason or "stop")
                    return
        except (httpx.TimeoutException, httpx.RequestError, OSError) as e:
            yield ("unreachable",
                   f"network error via {proxy or 'no-proxy'}: "
                   f"{type(e).__name__}: {e}")
        except Exception as e:
            # SOCKS5 ProtocolError, etc.
            yield ("unreachable",
                   f"unexpected via {proxy or 'no-proxy'}: "
                   f"{type(e).__name__}: {e}")

    async def chat_stream(
        self, req: ChatRequest
    ) -> AsyncIterator[StreamChunk]:
        body = _build_body(req)
        max_retries = int(os.environ.get("REVERSE_PROXY_MAX_RETRIES", "10"))
        from account_pool import NoAccountsAvailable

        pool = self._get_pool()
        last_err = "no attempts"

        for attempt in range(max_retries):
            try:
                acc = await pool.claim()
                proxy = acc.proxy or None
                claimed = True
            except NoAccountsAvailable as e:
                acc = None
                claimed = False
                proxy = self._env_proxy
                last_err = f"pool empty: {e}"

            parser = FenceStreamParser()
            outcome: str = "unreachable"
            err: str = ""
            buffered: list[StreamChunk] = []
            had_real_chunk = False
            finish_reason = None

            async for kind, payload in self._try_one_proxy(proxy, body, parser):
                if kind == "chunk":
                    buffered.append(payload)
                    had_real_chunk = True
                elif kind == "done":
                    outcome = "done"
                    finish_reason = payload
                elif kind == "exhausted":
                    outcome = "exhausted"
                    err = payload
                    break
                elif kind == "unreachable":
                    outcome = "unreachable"
                    err = payload
                    break

            if outcome == "done":
                if claimed and acc is not None:
                    await pool.release(acc, "ok")
                for c in buffered:
                    yield c
                yield StreamDone(finish_reason=finish_reason or "stop")
                return

            if had_real_chunk:
                # Mid-stream failure — surface partial output rather than retry.
                if claimed and acc is not None:
                    await pool.release(acc, "unreachable")
                for c in buffered:
                    yield c
                yield StreamDone(
                    finish_reason="error",
                    error_message=f"stream interrupted ({outcome}): {err}",
                )
                return

            # Pre-content failure — release + retry on the next account.
            if claimed and acc is not None:
                await pool.release(acc, outcome=outcome)
            last_err = err or outcome
            if not claimed:
                break

        yield StreamDone(
            finish_reason="error",
            error_message=f"all {max_retries} attempts failed; last: {last_err}",
        )

    async def health_check(self) -> bool:
        return True
