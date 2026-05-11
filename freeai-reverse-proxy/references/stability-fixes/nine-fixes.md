# 稳定性修复 9 件套（按 cron iter 顺序）

每一项都对应一次**真实**的失败案例 + 一次 commit 修复。完整溯源请看 `D:\tmp\FreeAI\_methodology\PLAN.md` 的 "Cron iter X" 段落和工程仓库的 git log。

## 1. include_usage 240s 挂死（commit `8f157b9`）

**症状**：OpenCode 调用反代 → 反代正确响应 finish_reason=stop → 客户端再等 240s 才超时退出。

**根因**：OpenCode 用 `@ai-sdk/openai-compatible`，请求里带了 `stream_options: {include_usage: true}`。它会**一直等**一个最后的 `usage` chunk，等不到 → 240s 客户端超时。

**修复**：解析 `stream_options.include_usage`，在 finish_reason chunk 之后、`[DONE]` 之前，发一个占位 usage chunk：

```python
so = body.get("stream_options") or {}
include_usage = bool(so.get("include_usage"))
# ... finish chunk 之后 ...
if include_usage:
    yield _emit_usage_chunk({"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0})
```

效果：240s → 38s（实际 read 任务）。

## 2. tool_calls wire format "Invalid Tool"（commit `34f3f66`）

**症状**：模型确实吐了 `tool_call` fence，FenceStreamParser 正确解析，但 OpenCode 报 "Invalid Tool" 拒绝执行。

**根因**：HEADER chunk 里同时含 `name + 整段 arguments JSON`，第二个 chunk 又来一次 name+args，@ai-sdk merge 时把空 name 覆盖进 slot 0 的 `tool_name` 字段。

**修复**：分两段：
- HEADER：`{index, id, type, function: {name, arguments: ""}}`（args 空串）
- ARG-DELTA：多个 `{index, function: {arguments: <slice>}}`（**不带** name/id/type）
- finish：`finish_reason="tool_calls"`

详见 `protocol-translation/openai-wire-format.md`。

## 3. 流式 cache.insert 被 GC（commit `8bffcd2`）

**症状**：流式调用同一个 prompt 两次，第二次仍然 cache miss（应该是 HIT）。

**根因**：

```python
async for ch in driver.chat_stream(req):
    yield ch                # ← FastAPI 在客户端 close 时会立即关 generator
    if isinstance(ch, StreamDone):
        await cache.insert(...)  # ← 永远不执行
```

**修复**：把 cache.insert 放到 yield **之前**：

```python
async for ch in driver.chat_stream(req):
    if isinstance(ch, StreamDone) and not had_error:
        await cache.insert(...)
    yield ch
```

加 fallback：如果上游异常没发 StreamDone，generator 结束后还要再尝试一次 insert（用 has_seen_done 标志位）。

## 4. retry-on-no-tool-use（commit `86d45d9`）

**症状**：模型有时（grep / 复杂任务上 ~30% 概率）忽略 fence 协议指令，直接出 prose；客户端拿到 plain text + finish_reason=stop，但任务需要 tool_call，结果就是任务 fail。

**根因**：Claude Haiku 4.5 不是 100% 服从 system prompt 注入；这是模型行为，不是协议 bug。

**修复**：

```python
# 缓冲第一次 attempt 全部 chunk
chunks_1 = []
had_tool_call_1 = False
async for ch in driver.chat_stream(req):
    chunks_1.append(ch)
    if isinstance(ch, ToolCallEnd):
        had_tool_call_1 = True

if had_tool_call_1 or not needs_retry_guard:
    for ch in chunks_1: yield ch
    return

# 没出 tool_call，retry 一次用 required-strong
req2 = inject_tools_into_request(req_no_inject, tool_choice="required-strong")
async for ch in driver.chat_stream(req2):
    yield ch
```

`needs_retry_guard` 触发条件：客户端带了 tools + 历史里没 assistant tool_calls + 第一次 attempt 不是 upstream error / 空流。

## 5. SOCKS5 ProtocolError 让流崩（commit `86d45d9`）

**症状**：某些 free SOCKS5 代理返回 `Malformed reply`，`socksio.exceptions.ProtocolError` 一路 bubble 到 ASGI 层，整个请求 500。

**根因**：driver 的 `_try_one_proxy` 原本只 catch `httpx.TimeoutException / httpx.RequestError / OSError`，没 catch socksio 的异常。

**修复**：加 catch-all：

```python
try:
    async with httpx.AsyncClient(...) as client:
        async with client.stream(...) as r:
            ...
except (httpx.TimeoutException, httpx.RequestError, OSError) as e:
    yield ("unreachable", f"network error: {e}")
except Exception as e:
    # SOCKS lib 异常、未知错误等
    yield ("unreachable", f"unexpected: {type(e).__name__}: {e}")
```

外层 driver 拿到 `unreachable` 就换下一个 proxy。

## 6. 90s 墙钟 deadline（commit `c73773d`）

**症状**：read 任务的"工具结果 → 最终答案"那个 turn 上游 SSE 慢滴流 579 秒（10 分钟）才结束。OpenCode 360s timeout 打死客户端。

**根因**：httpx 的 read timeout 只看**相邻字节间隔**（默认 120s）。如果上游每 30 秒滴一个字节，永远不超时。

**修复**：在 `aiter_lines()` 循环里加墙钟 deadline：

```python
import time as _time
deadline_s = float(os.environ.get("REVERSE_PROXY_STREAM_DEADLINE", "90"))
deadline = _time.monotonic() + deadline_s
async for line in r.aiter_lines():
    if _time.monotonic() > deadline:
        yield ("unreachable", f"stream wall-clock exceeded {deadline_s}s")
        return
    ...
```

超过就 yield `unreachable`，外层 driver 换 proxy。

## 7. retry 只在"text 但无 fence"时触发（commit `72d46f9`）

**症状**：bash 任务在某次运行中 5 个 driver retry 全是 SOCKS error → 我的代码触发 retry → retry 也是 5 个 SOCKS error → 整个测试超时。

**根因**：我的 retry guard 太宽，"任何没 tool_call 的 attempt"都 retry，包括上游 error / 空流。但 error / 空流是网络层问题，retry 也无效，徒增延迟。

**修复**：

```python
had_error_1 = any(isinstance(c, StreamDone) and c.finish_reason == "error" for c in chunks_1)
had_text_1 = any(isinstance(c, TextDelta) for c in chunks_1)

if had_tool_call_1 or not needs_retry_guard or had_error_1 or not had_text_1:
    for ch in chunks_1: yield ch
    return
# 只有"出了文本但没 fence"才走 retry
```

## 8. max_retries 5 → 10（commit `b851600`）

**症状**：第一个 agent 请求偶尔 5 retry 全 fail（pool 64，~8% 错误率 → 5 连失败概率 ~1/15 = ~7%）。

**修复**：

```python
max_retries = int(os.environ.get("REVERSE_PROXY_MAX_RETRIES", "10"))
```

10 连失败概率 ~1/400，可接受。

## 9. test_multi_turn TimeoutExpired bug（commit `0abcbf7`）

**症状**：单个慢任务超时 → 整个多轮测试 abort，后续任务 + R2 cache hit 验证全跑不到。

**根因**：

```python
except subprocess.TimeoutExpired as e:
    raw = e.stdout.decode(...)  # ← e.stdout 已经是 str（subprocess.run(text=True)）
                                #    AttributeError: 'str' object has no attribute 'decode'
```

**修复**：

```python
raw_stdout = e.stdout if isinstance(e.stdout, str) else (
    e.stdout.decode("utf-8", "replace") if e.stdout else "")
```

## 合在一起的效果

- `test_opencode_agent.py`：从 **0/3 → 3/3 PASS**
- `test_multi_turn.py`：从 **abort → ALL OK**（R1 3/4 + R2 OK，pool 46→46 live）
- 18 个 cron iter，每个 ≤ 15 分钟

## 环境变量速查

| 变量 | 默认 | 含义 |
|---|---|---|
| `REVERSE_PROXY_DEBUG` | unset | 详细 SSE chunk + 上游 raw text 打到 stderr |
| `REVERSE_PROXY_DEBUG_FULL` | unset | dump 每个请求 body 到 `req_dump_v2/` |
| `REVERSE_PROXY_DISABLE_REFRESHER` | unset | 跳过后台 proxy 探活 |
| `REVERSE_PROXY_REFRESH_INTERVAL` | 1800 | 探活间隔（秒）|
| `REVERSE_PROXY_MAX_RETRIES` | 10 | 单请求 driver retry budget |
| `REVERSE_PROXY_STREAM_DEADLINE` | 90 | 单个上游流墙钟 deadline（秒）|
| `REVERSE_PROXY_EXHAUSTED_TTL` | 86400 | exhausted account 屏蔽时长（秒）|
| `REVERSE_PROXY_CACHE_MODE` | `prefix` | `disabled` / `exact` / `prefix` |
| `FREEAI_BEARER_TOKEN` | unset | 设置则启用 Bearer auth 中间件 |
