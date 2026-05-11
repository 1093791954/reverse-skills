"""chatgpt.org reverse-proxy: OpenAI-compatible API in front of
chatgpt.org/api/chat (Amazon Bedrock Claude Haiku 4.5 et al via
OpenRouter passthrough).

This server speaks the OpenAI protocol on `127.0.0.1:8888` and
translates each request into chatgpt.org's native SSE format via
the `ChatGPTOrgDriver` next door (see ./driver.py).  Tool use is
synthesised via the ```tool_call``` fence protocol implemented in
`_common/tool_proxy.py` (see also the cron-iter stability fixes:
retry-on-no-tool-use, wall-clock deadline, required-strong nudge,
SOCKS protocol-error catch-all, max_retries=10).

Run:
    pip install fastapi uvicorn httpx
    python run.py
    # or
    uvicorn app:app --host 127.0.0.1 --port 8888

Endpoints:
    POST /v1/chat/completions       OpenAI protocol
    GET  /v1/models                 list mapped models
    GET  /healthz                   readiness probe
"""
from __future__ import annotations

# Make `_common/` importable as a flat package of top-level modules
# (driver_base, tool_proxy, account_pool, cache, pool_refresher).
import sys as _sys
from pathlib import Path as _Path
_COMMON_DIR = _Path(__file__).parent.parent / "_common"
if str(_COMMON_DIR) not in _sys.path:
    _sys.path.insert(0, str(_COMMON_DIR))

import asyncio
import json
import os
import time
import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse

from driver_base import (
    ChatDriver,
    ChatRequest,
    Message,
    StreamChunk,
    StreamDone,
    TextDelta,
    ToolCallArgsDelta,
    ToolCallEnd,
    ToolCallStart,
    ToolSpec,
)
from tool_proxy import inject_tools_into_request


# --- Driver registry -------------------------------------------------------

DRIVERS: dict[str, ChatDriver] = {}
MODEL_TO_DRIVER: dict[str, str] = {}  # external model name → driver name


def register_driver(driver: ChatDriver) -> None:
    DRIVERS[driver.name] = driver
    for m in driver.supported_models:
        MODEL_TO_DRIVER[m] = driver.name


def select_driver(model: str) -> ChatDriver:
    drv_name = MODEL_TO_DRIVER.get(model)
    if drv_name is None:
        # Default fallback: try first driver with any registered model
        for drv in DRIVERS.values():
            if drv.supported_models:
                return drv
        raise HTTPException(404, f"No driver registered for model {model!r}")
    drv = DRIVERS.get(drv_name)
    if drv is None:
        raise HTTPException(500, f"Driver {drv_name} not loaded")
    return drv


# --- Lifespan: register drivers --------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the AccountPool (singleton on app.state).
    try:
        from account_pool import AccountPool
        pool = AccountPool.load_or_init()
        app.state.pool = pool
        print(f"[reverse_proxy] pool stats: {pool.stats()}")
    except Exception as e:
        print(f"[reverse_proxy] pool init failed: {e}")
        app.state.pool = None

    # Initialize the PromptCache (singleton on app.state).
    try:
        from cache import PromptCache
        app.state.cache = PromptCache()
        print(f"[reverse_proxy] cache stats: {app.state.cache.stats()}")
    except Exception as e:
        print(f"[reverse_proxy] cache init failed: {e}")
        app.state.cache = None

    # Register drivers.  This server is dedicated to chatgpt.org, but
    # we also load the shared echo driver so the unit-test suite
    # (test_app_e2e.py etc.) can exercise the protocol layer without
    # touching the live upstream.
    try:
        from echo import EchoDriver
        register_driver(EchoDriver())
    except ImportError:
        pass
    try:
        from driver import ChatGPTOrgDriver
        # Wire pool into the driver
        register_driver(ChatGPTOrgDriver(pool=app.state.pool))
    except (ImportError, FileNotFoundError) as e:
        print(f"[reverse_proxy] driver load failed: {e}")
    print(f"[reverse_proxy] {len(DRIVERS)} driver(s) loaded: "
          f"{list(DRIVERS.keys())}")
    print(f"[reverse_proxy] {len(MODEL_TO_DRIVER)} model(s) routable")

    # Background pool refresher (skipped during pytest / TestClient runs
    # because there's no event loop ready for tasks long-living past
    # context teardown — controlled by env)
    refresher_task = None
    import os as _os
    if app.state.pool is not None and not _os.environ.get(
            "REVERSE_PROXY_DISABLE_REFRESHER"):
        try:
            from pool_refresher import refresher_loop
            interval = int(_os.environ.get(
                "REVERSE_PROXY_REFRESH_INTERVAL", "1800"))
            refresher_task = asyncio.create_task(
                refresher_loop(app.state.pool, interval_s=interval))
            print(f"[reverse_proxy] refresher task started "
                  f"(every {interval}s)")
        except Exception as e:
            print(f"[reverse_proxy] refresher start failed: {e}")

    yield

    if refresher_task is not None:
        refresher_task.cancel()
        try:
            await refresher_task
        except (asyncio.CancelledError, Exception):
            pass


app = FastAPI(title="FreeAI Reverse Proxy", lifespan=lifespan)


# --- Bearer-token auth middleware ------------------------------------------
#
# Off by default (local-only usage).  Set FREEAI_BEARER_TOKEN to enable.
# When enabled, every request to /v1/* must carry
#   Authorization: Bearer <token>
# /healthz stays public so a load-balancer or you-with-curl can probe
# liveness without sharing the key.
_AUTH_TOKEN = os.environ.get("FREEAI_BEARER_TOKEN", "").strip()


@app.middleware("http")
async def _bearer_auth(request: Request, call_next):
    if not _AUTH_TOKEN:
        return await call_next(request)
    path = request.url.path
    if path == "/healthz" or path == "/" or path.startswith("/docs") \
            or path.startswith("/openapi"):
        return await call_next(request)
    auth = request.headers.get("authorization") or ""
    expected = f"Bearer {_AUTH_TOKEN}"
    if auth != expected:
        from fastapi.responses import JSONResponse as _JR
        return _JR(
            {"error": {"message": "missing or invalid Bearer token",
                       "type": "auth_error", "code": "unauthorized"}},
            status_code=401,
        )
    return await call_next(request)


# --- Request/response shapes (OpenAI) --------------------------------------

def _msg_from_openai(d: dict) -> Message:
    """Translate one OpenAI message into our canonical Message.

    Special cases:
    - role=assistant with tool_calls: serialize each tool call as a
      ```tool_call fenced markdown block appended to the content,
      because our upstream backend doesn't speak native tool_calls.
    - role=tool: convert to a user message wrapped in a ```tool_result
      fence, so the model sees the tool's output in fence protocol.
    """
    role = d.get("role", "user")
    content = d.get("content")
    if isinstance(content, list):
        # OpenAI vision-style content array; flatten to text
        parts = []
        for c in content:
            if isinstance(c, dict) and c.get("type") == "text":
                parts.append(c.get("text", ""))
        content = "".join(parts)
    elif content is None:
        content = ""

    if role == "assistant" and d.get("tool_calls"):
        # Re-encode native tool_calls into our fence protocol so the
        # upstream model sees a consistent multi-turn history.
        fence_blocks = []
        for tc in d["tool_calls"]:
            fn = tc.get("function") or {}
            try:
                args_obj = json.loads(fn.get("arguments") or "{}")
            except Exception:
                args_obj = {"_raw": fn.get("arguments")}
            fence_blocks.append(
                "```tool_call\n" +
                json.dumps({"name": fn.get("name", ""),
                            "arguments": args_obj},
                           ensure_ascii=False) +
                "\n```"
            )
        content = (content or "") + ("\n" if content else "") + \
                  "\n".join(fence_blocks)

    if role == "tool":
        # Translate tool result back into a user message that uses our
        # fence protocol (the upstream backend doesn't support tool role).
        tool_name = d.get("name") or ""
        tool_call_id = d.get("tool_call_id")
        result_payload = {"name": tool_name, "result": content}
        if tool_call_id:
            result_payload["tool_call_id"] = tool_call_id
        wrapped = ("```tool_result\n" +
                   json.dumps(result_payload, ensure_ascii=False) +
                   "\n```")
        return Message(role="user", content=wrapped,
                       name=None, tool_call_id=tool_call_id)

    return Message(
        role=role,
        content=content,
        name=d.get("name"),
        tool_call_id=d.get("tool_call_id"),
    )


def _tool_from_openai(d: dict) -> ToolSpec:
    fn = d.get("function", {})
    return ToolSpec(
        name=fn.get("name", ""),
        description=fn.get("description", ""),
        parameters=fn.get("parameters", {}),
    )


# --- SSE encoder for OpenAI client -----------------------------------------

def _openai_chunk(model: str, choice_delta: dict, finish_reason=None) -> bytes:
    payload = {
        "id": f"chatcmpl-{uuid.uuid4().hex[:24]}",
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model,
        "choices": [{"index": 0, "delta": choice_delta,
                     "finish_reason": finish_reason}],
    }
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n".encode()


def _stream_to_openai_sse(
    chunks: AsyncIterator[StreamChunk], model: str,
    include_usage: bool = False,
) -> AsyncIterator[bytes]:
    """Convert canonical StreamChunks to OpenAI SSE bytes.

    If `include_usage` is True (set when the client passes
    stream_options.include_usage=true), an additional final chunk with
    `usage: {prompt_tokens, completion_tokens, total_tokens}` is emitted
    BEFORE `data: [DONE]\\n\\n`. Some clients (e.g. OpenCode's
    @ai-sdk/openai-compatible assembler) block waiting for that chunk
    when they requested it, otherwise they hit their request timeout.
    """
    import os as _os
    debug = bool(_os.environ.get("REVERSE_PROXY_DEBUG"))

    def _emit(payload_dict, finish_reason=None):
        """Wrap an OpenAI delta into a `data: ...\n\n` byte string and
        also tee it to debug log if enabled."""
        chunk_bytes = _openai_chunk(model, payload_dict, finish_reason)
        if debug:
            try:
                # decode + strip the framing prefix for readability
                line = chunk_bytes.decode("utf-8")
                line = line[len("data: "):].rstrip()
                print(f"[sse->] {line}", flush=True)
            except Exception:
                pass
        return chunk_bytes

    async def gen():
        # role hint
        yield _emit({"role": "assistant", "content": ""})
        finish: str | None = None
        # Per-stream tool index counter. We only allocate an index at
        # ToolCallEnd, NOT at ToolCallStart, because we don't know the
        # tool name until the fence body parses, and OpenAI's wire format
        # requires `function.name` to appear in the FIRST tool_calls
        # chunk. See PLAN.md Section 1.3.
        next_tool_index = 0
        async for ch in chunks:
            if isinstance(ch, TextDelta):
                yield _emit({"content": ch.text})
            elif isinstance(ch, ToolCallStart):
                # Defer emission until ToolCallEnd. We don't have the tool
                # name yet (the fence body hasn't been parsed), and emitting
                # an empty-name header at this point breaks OpenAI SDK
                # consumers (they cache name="" in the slot and treat it
                # as an "invalid" tool).
                pass
            elif isinstance(ch, ToolCallArgsDelta):
                # Drop: the raw fence text is the outer
                # {"name":..., "arguments":{...}} wrapper, not the inner
                # arguments string OpenAI clients want. We emit the canonical
                # form when the fence parser yields ToolCallEnd.
                pass
            elif isinstance(ch, ToolCallEnd):
                idx = next_tool_index
                next_tool_index += 1
                args_str = json.dumps(ch.arguments, ensure_ascii=False)
                if debug:
                    print(f"[sse-out tool_calls] index={idx} "
                          f"name={ch.tool_name!r} args={args_str[:300]}",
                          flush=True)
                # 1) HEADER chunk: id + type + function.name with EMPTY args.
                yield _emit({
                    "tool_calls": [{
                        "index": idx,
                        "id": ch.call_id,
                        "type": "function",
                        "function": {
                            "name": ch.tool_name,
                            "arguments": "",
                        },
                    }]
                })
                # 2) ARG-DELTA chunks: slice the JSON-encoded args into
                # ~64-byte fragments (or one chunk if shorter). Each chunk
                # carries ONLY the index and function.arguments delta.
                CHUNK = 64
                if not args_str:
                    args_str = "{}"
                pos = 0
                while pos < len(args_str):
                    frag = args_str[pos:pos + CHUNK]
                    pos += CHUNK
                    yield _emit({
                        "tool_calls": [{
                            "index": idx,
                            "function": {"arguments": frag},
                        }]
                    })
                finish = "tool_calls"
            elif isinstance(ch, StreamDone):
                # Driver-emitted "stop" must NOT clobber the "tool_calls"
                # finish reason set when we saw a fence end.
                if not (finish == "tool_calls" and ch.finish_reason == "stop"):
                    finish = ch.finish_reason
        yield _emit({}, finish_reason=finish or "stop")
        if include_usage:
            # We don't actually count tokens (the upstream is anonymous and
            # the chatgpt.org passthrough doesn't return usage). Emit a
            # placeholder usage chunk so clients that requested it can
            # finalize their stream assembly without timing out.
            usage_payload = {
                "id": f"chatcmpl-{uuid.uuid4().hex[:24]}",
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": model,
                "choices": [],
                "usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0,
                },
            }
            usage_bytes = (f"data: "
                           f"{json.dumps(usage_payload, ensure_ascii=False)}"
                           f"\n\n").encode()
            if debug:
                print(f"[sse->] {usage_bytes.decode().rstrip()}", flush=True)
            yield usage_bytes
        yield b"data: [DONE]\n\n"
    return gen()


# --- Endpoints -------------------------------------------------------------

@app.get("/healthz")
async def healthz():
    pool = getattr(app.state, "pool", None)
    cache = getattr(app.state, "cache", None)
    return {
        "ok": True,
        "drivers": list(DRIVERS.keys()),
        "pool": pool.stats() if pool else None,
        "cache": cache.stats() if cache else None,
    }


@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [{"id": m, "object": "model", "owned_by": d}
                 for m, d in MODEL_TO_DRIVER.items()]
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    # If REVERSE_PROXY_DUMP_DIR is set, write the raw incoming body as JSON
    # to that directory keyed by timestamp+nonce. Used to diff repeated
    # client requests when tracking down cache misses.
    try:
        import os as _os
        dump_dir = _os.environ.get("REVERSE_PROXY_DUMP_DIR")
        if dump_dir:
            from pathlib import Path as _P
            _P(dump_dir).mkdir(parents=True, exist_ok=True)
            fname = (f"{int(time.time()*1000)}-{uuid.uuid4().hex[:6]}.json")
            (_P(dump_dir) / fname).write_text(
                json.dumps(body, ensure_ascii=False, indent=2),
                encoding="utf-8")
    except Exception:
        pass
    # Debug: log every incoming request body to understand client behavior
    try:
        import os as _os
        if _os.environ.get("REVERSE_PROXY_DEBUG"):
            print(f"[req] body keys: {list(body.keys())}", flush=True)
            print(f"[req] model: {body.get('model')!r}", flush=True)
            print(f"[req] stream: {body.get('stream')!r}", flush=True)
            print(f"[req] tools count: {len(body.get('tools') or [])}", flush=True)
            if body.get("tools"):
                _names = [t.get("function", {}).get("name")
                          for t in body["tools"]]
                print(f"[req] tool names: {_names}", flush=True)
            msgs = body.get("messages", [])
            print(f"[req] messages count: {len(msgs)}", flush=True)
            for i, m in enumerate(msgs):
                role = m.get("role")
                content = m.get("content")
                if isinstance(content, str):
                    full_dump = bool(_os.environ.get(
                        "REVERSE_PROXY_DEBUG_FULL"))
                    cs = content if full_dump else content[:200]
                else:
                    cs = json.dumps(content)[:200]
                print(f"[req]   [{i}] {role}: {cs!r}", flush=True)
                if m.get("tool_calls"):
                    print(f"[req]   [{i}] tool_calls: "
                          f"{json.dumps(m['tool_calls'])[:200]}", flush=True)
            print(f"[req] ---", flush=True)
    except Exception as _e:
        print(f"[req] debug log err: {_e}", flush=True)
    model = body.get("model", "")
    drv = select_driver(model)
    msgs = [_msg_from_openai(m) for m in body.get("messages", [])]
    tools = [_tool_from_openai(t) for t in body.get("tools") or []]
    req = ChatRequest(
        model=model,
        messages=msgs,
        tools=tools,
        max_tokens=body.get("max_tokens") or 4000,
        temperature=body.get("temperature") or 0.7,
        top_p=body.get("top_p") or 1.0,
        stream=bool(body.get("stream", False)),
    )
    # Inject tool-protocol system prompt if tools were provided.
    # Honor `tool_choice` ("none" | "auto" | "required" | named function)
    # by appending an extra directive to the system message.
    effective_tool_choice = body.get("tool_choice")
    # First-turn nudge: when tools are present, the client is in "auto"
    # mode (or didn't specify), and the conversation has not yet seen any
    # assistant tool_calls, intermittent model behavior (Claude Haiku
    # 4.5 via chatgpt.org) sometimes ignores our fence-protocol directive
    # and replies in plain text with finish_reason=stop. Document this in
    # PLAN.md cron iter 8 findings.
    # Mitigation: when this is the first opportunity to call a tool,
    # upgrade tool_choice from "auto" (default) to "required" so the
    # injected directive becomes a hard MUST. We keep "auto" behavior for
    # subsequent turns (history has assistant tool_calls) so the model
    # can stop the loop when done.
    # First-turn nudge: when tools are present, the client is in "auto"
    # mode (or didn't specify), and the conversation has not yet seen any
    # assistant tool_calls, intermittent model behavior (Claude Haiku
    # 4.5 via chatgpt.org) sometimes ignores our fence-protocol directive
    # and replies in plain text with finish_reason=stop. Document this in
    # PLAN.md cron iter 8 findings.
    # Mitigation: when this is the first opportunity to call a tool,
    # upgrade tool_choice from "auto" (default) to "required-strong" — a
    # very explicit directive that compels the model to start the reply
    # with the opening fence. Empirically this avoids the slow
    # buffer-then-retry path which can multiply latency 5x via
    # downstream proxy churn.
    if (tools and effective_tool_choice in (None, "auto")
            and not any(
                (m.get("tool_calls") if isinstance(m, dict) else None)
                for m in body.get("messages", []))):
        effective_tool_choice = "required-strong"
    req_no_inject = req
    req = inject_tools_into_request(req, tool_choice=effective_tool_choice)

    # ---- Cache lookup (BEFORE pool.claim) ----
    # Cache hits MUST NOT consume an account.
    pc = getattr(app.state, "cache", None)
    cached = None
    cache_key_for_insert = None
    if pc is not None:
        try:
            cached = await pc.lookup(model, req.messages)
        except Exception as _e:
            print(f"[cache] lookup err: {_e}", flush=True)
            cached = None
        if cached is not None:
            print(f"[cache HIT] model={model} text_len={len(cached.text)} "
                  f"tool_calls={len(cached.tool_calls)}", flush=True)
        else:
            cache_key_for_insert = (model, list(req.messages))

    if not req.stream:
        # ---- Cache HIT path (non-stream) ----
        if cached is not None:
            msg = {"role": "assistant", "content": cached.text}
            finish = "stop"
            if cached.tool_calls:
                msg["tool_calls"] = cached.tool_calls
                finish = "tool_calls"
            return JSONResponse({
                "id": f"chatcmpl-{uuid.uuid4().hex[:24]}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": model,
                "choices": [{"index": 0, "message": msg,
                             "finish_reason": finish}],
                "x_freeai_cache": "HIT",
            })

        # Aggregate to a single non-stream response
        text_parts: list[str] = []
        tool_calls_assembled: list[dict] = []
        upstream_error: str | None = None
        async for ch in drv.chat_stream(req):
            if isinstance(ch, TextDelta):
                text_parts.append(ch.text)
            elif isinstance(ch, ToolCallEnd):
                tool_calls_assembled.append({
                    "id": ch.call_id,
                    "type": "function",
                    "function": {
                        "name": ch.tool_name,
                        "arguments": json.dumps(ch.arguments,
                                                ensure_ascii=False),
                    }
                })
            elif isinstance(ch, StreamDone) and ch.finish_reason == "error":
                upstream_error = ch.error_message or "unknown upstream error"
        if upstream_error and not text_parts and not tool_calls_assembled:
            # Translate to OpenAI-style error so the SDK raises correctly
            return JSONResponse(
                {"error": {"message": upstream_error,
                           "type": "upstream_error",
                           "code": "upstream_error"}},
                status_code=502,
            )
        msg = {"role": "assistant", "content": "".join(text_parts)}
        if tool_calls_assembled:
            msg["tool_calls"] = tool_calls_assembled
            finish = "tool_calls"
        else:
            finish = "stop"
        # ---- Cache INSERT (non-stream) ----
        if pc is not None and cache_key_for_insert and not upstream_error:
            try:
                from cache import CachedResponse
                _m, _msgs = cache_key_for_insert
                await pc.insert(_m, _msgs, CachedResponse(
                    text=msg["content"],
                    tool_calls=msg.get("tool_calls") or [],
                ))
            except Exception as _e:
                print(f"[cache] insert err: {_e}", flush=True)
        return JSONResponse({
            "id": f"chatcmpl-{uuid.uuid4().hex[:24]}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [{"index": 0, "message": msg, "finish_reason": finish}],
        })

    # Streaming
    # Honor stream_options.include_usage so OpenAI-SDK clients that
    # requested usage don't block waiting for it (causes 240s+ hangs in
    # OpenCode's @ai-sdk/openai-compatible).
    so = body.get("stream_options") or {}
    include_usage = bool(so.get("include_usage"))

    # Retry-on-no-tool-use: when tools are requested and this is the first
    # tool-eligible turn, the upstream model (Claude Haiku 4.5 via
    # chatgpt.org) sometimes ignores the fence-protocol directive and
    # emits plain text. Detect that case after the first attempt and try
    # once more with a stronger directive. To do this we buffer the first
    # attempt fully before deciding whether to stream it or retry.
    needs_retry_guard = (
        bool(tools)
        and effective_tool_choice in ("auto", "required", "required-strong")
        and not any(
            (m.get("tool_calls") if isinstance(m, dict) else None)
            for m in body.get("messages", []))
    )
    if os.environ.get("REVERSE_PROXY_DEBUG"):
        print(f"[retry-guard] tools={len(tools)} "
              f"effective_tool_choice={effective_tool_choice!r} "
              f"needs_retry_guard={needs_retry_guard}", flush=True)

    async def _drive_with_retry():
        """Run drv.chat_stream; if the first attempt produced no tool_calls
        when tools were requested, retry once with `required-strong`.

        Yields the chunks of whichever attempt succeeded (or the second
        attempt if both failed — so the client still sees something).
        """
        from driver_base import StreamDone, TextDelta, ToolCallEnd
        # Attempt 1: buffer fully
        chunks_1: list = []
        had_tool_call_1 = False
        had_error_1 = False
        had_text_1 = False
        async for ch in drv.chat_stream(req):
            chunks_1.append(ch)
            if isinstance(ch, ToolCallEnd):
                had_tool_call_1 = True
            elif isinstance(ch, TextDelta):
                had_text_1 = True
            elif isinstance(ch, StreamDone) and ch.finish_reason == "error":
                had_error_1 = True
        # Skip retry when:
        #   - attempt 1 produced a tool_call (success — emit it)
        #   - retry guard is off (subsequent turn / no tools / etc.)
        #   - attempt 1 errored (no tool-protocol fault to recover from;
        #     just surface the error, don't burn another upstream cycle)
        #   - attempt 1 produced no text AND no tool_call (degenerate
        #     empty stream — avoid hammering pool)
        if (had_tool_call_1 or not needs_retry_guard or had_error_1
                or not had_text_1):
            for ch in chunks_1:
                yield ch
            return
        # Attempt 2 with stronger directive. Don't pass original tool_choice
        # — force `required-strong`.
        print("[retry] first attempt produced no tool_calls; retrying with "
              "required-strong", flush=True)
        req2 = inject_tools_into_request(req_no_inject,
                                         tool_choice="required-strong")
        chunks_2: list = []
        had_tool_call_2 = False
        async for ch in drv.chat_stream(req2):
            chunks_2.append(ch)
            if isinstance(ch, ToolCallEnd):
                had_tool_call_2 = True
        if had_tool_call_2:
            for ch in chunks_2:
                yield ch
            return
        # Both attempts failed — return attempt 2's chunks (newer text).
        print("[retry] second attempt also produced no tool_calls; "
              "returning plain text", flush=True)
        for ch in chunks_2:
            yield ch

    if cached is not None:
        # Replay synthesized SSE from cached response.
        async def _replay():
            from driver_base import StreamDone, TextDelta, ToolCallEnd
            if cached.text:
                yield TextDelta(text=cached.text)
            for tc in cached.tool_calls or []:
                fn = tc.get("function") or {}
                try:
                    args_obj = json.loads(fn.get("arguments") or "{}")
                except Exception:
                    args_obj = {}
                yield ToolCallEnd(
                    call_id=tc.get("id", f"call_{uuid.uuid4().hex[:12]}"),
                    tool_name=fn.get("name", ""),
                    arguments=args_obj,
                )
            yield StreamDone(
                finish_reason="tool_calls" if cached.tool_calls else "stop")
        sse = _stream_to_openai_sse(_replay(), model,
                                    include_usage=include_usage)
        return StreamingResponse(sse, media_type="text/event-stream",
                                 headers={"x-freeai-cache": "HIT"})

    # Real upstream call + tee for cache insert
    if pc is not None and cache_key_for_insert:
        # Wrap the chunk stream with a tee that captures content/tool_calls
        # so we can cache the full assembled response after streaming ends.
        captured_text: list[str] = []
        captured_tool_calls: list[dict] = []
        had_error = [False]

        async def _tee():
            from driver_base import (StreamDone, TextDelta, ToolCallEnd)
            saw_done = False
            async for ch in _drive_with_retry():
                if isinstance(ch, TextDelta):
                    captured_text.append(ch.text)
                elif isinstance(ch, ToolCallEnd):
                    captured_tool_calls.append({
                        "id": ch.call_id,
                        "type": "function",
                        "function": {
                            "name": ch.tool_name,
                            "arguments": json.dumps(
                                ch.arguments, ensure_ascii=False),
                        }
                    })
                elif isinstance(ch, StreamDone):
                    saw_done = True
                    if ch.finish_reason == "error":
                        had_error[0] = True
                    # Insert into cache BEFORE yielding the StreamDone, so
                    # the caching write happens even if the consumer
                    # discards the generator immediately after the final
                    # chunk (FastAPI's StreamingResponse may close the
                    # async iterator on connection drop, never executing
                    # post-yield code).
                    if not had_error[0]:
                        try:
                            from cache import CachedResponse
                            _m, _msgs = cache_key_for_insert
                            await pc.insert(_m, _msgs, CachedResponse(
                                text="".join(captured_text),
                                tool_calls=captured_tool_calls,
                            ))
                        except Exception as _e:
                            print(f"[cache] insert err: {_e}", flush=True)
                yield ch
            # Fallback: if the upstream forgot to emit a StreamDone, also
            # insert here. Idempotent because make_key + INSERT OR REPLACE.
            if not saw_done and not had_error[0]:
                try:
                    from cache import CachedResponse
                    _m, _msgs = cache_key_for_insert
                    await pc.insert(_m, _msgs, CachedResponse(
                        text="".join(captured_text),
                        tool_calls=captured_tool_calls,
                    ))
                except Exception as _e:
                    print(f"[cache] insert err: {_e}", flush=True)

        sse = _stream_to_openai_sse(_tee(), model,
                                    include_usage=include_usage)
    else:
        sse = _stream_to_openai_sse(_drive_with_retry(), model,
                                    include_usage=include_usage)
    return StreamingResponse(sse, media_type="text/event-stream")


# --- Run as script ---------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8888)
