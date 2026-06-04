# OpenAI tool_calls 流式 Wire Format

> 撞过 3 个 cron iter 才搞对。错一点就是 OpenCode 的 "Invalid Tool" 沉默挂死。

## 正确格式（chunk 序列）

```
# 1) 角色/内容初始 chunk（可选但建议）
data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","model":"...",
       "choices":[{"index":0,"delta":{"role":"assistant","content":""},
                   "finish_reason":null}]}

# 2) HEADER chunk：必须包含 id + type + name，arguments 为空串 ""
data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","model":"...",
       "choices":[{"index":0,
                   "delta":{"tool_calls":[
                     {"index":0,
                      "id":"call_abc123",
                      "type":"function",
                      "function":{"name":"bash","arguments":""}}
                   ]},
                   "finish_reason":null}]}

# 3) ARG-DELTA chunks：只带 index + arguments 片段（~64 字节切片）
data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","model":"...",
       "choices":[{"index":0,
                   "delta":{"tool_calls":[
                     {"index":0,
                      "function":{"arguments":"{\"command\": \"ls"}}
                   ]},
                   "finish_reason":null}]}

data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","model":"...",
       "choices":[{"index":0,
                   "delta":{"tool_calls":[
                     {"index":0,
                      "function":{"arguments":" -la\"}"}}
                   ]},
                   "finish_reason":null}]}

# 4) finish chunk
data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","model":"...",
       "choices":[{"index":0,"delta":{},"finish_reason":"tool_calls"}]}

# 5) usage chunk（必须，否则 OpenCode 240s 挂死等 usage）
data: {"id":"chatcmpl-xxx","object":"chat.completion.chunk","model":"...",
       "choices":[],"usage":{"prompt_tokens":0,"completion_tokens":0,"total_tokens":0}}

data: [DONE]

```

## 致命错误（撞过的坑）

### 错误 1：HEADER 里就塞 arguments JSON

```
# 错的
data: ... "tool_calls":[{"index":0,"id":"call_x","type":"function",
       "function":{"name":"bash","arguments":"{\"command\":\"ls -la\"}"}}]
```

效果：@ai-sdk/openai-compatible 的 assembler 把第一个 chunk merge 进 slot 0，第二个相同 index 的 chunk 又来一次 name+args，**它会把空 name 覆盖到 slot 里**，最终调用时 `tool_name === ""` → "Invalid Tool"。

修复：HEADER 只放 name + 空 args，后续只发 args delta，不再带 name。

### 错误 2：name 在 ARG-DELTA 里重复

```
# 错的
data: ... "tool_calls":[{"index":0,
        "function":{"name":"bash","arguments":"{\"command\""}}]
```

效果：同上，name 字段重复在 delta 中出现，SDK 的 merge 逻辑认为是新的覆盖。

修复：ARG-DELTA 只带 `index` + `function.arguments`，**绝不**带 `name`、`id`、`type`。

### 错误 3：不发 usage chunk

OpenCode @ai-sdk/openai-compatible 在 `stream_options.include_usage=true` 时会**一直等 usage chunk**，等不到 → 240s 客户端超时。

修复：解析请求里的 `stream_options.include_usage`，是 `true` 就在 finish_reason chunk 之后**发**一个占位 usage chunk：

```python
so = body.get("stream_options") or {}
include_usage = bool(so.get("include_usage"))
# ...
if include_usage:
    usage_payload = {
        "id": f"chatcmpl-{uuid.uuid4().hex[:24]}",
        ...
        "choices": [],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }
    yield f"data: {json.dumps(usage_payload)}\n\n".encode()
```

### 错误 4：缓存写入在 `yield StreamDone` 之后

```python
# 错的（FastAPI 关 generator 时这行可能不跑）
async for ch in driver.chat_stream(req):
    yield ch
    if isinstance(ch, StreamDone):
        await cache.insert(...)  # ← 这里可能丢
```

修复：把 cache.insert 放到 yield 之前：

```python
async for ch in driver.chat_stream(req):
    if isinstance(ch, StreamDone) and not had_error:
        await cache.insert(...)  # ← 先写
    yield ch  # ← 再 yield
```

## 校验

`test_app_e2e.py` 里的 `wire-format` 用例就是测这个 — 模拟一次 tool 调用，断言：
- 有且只有 1 个 HEADER chunk 含 name+id+type，arguments=""。
- ≥ 1 个 ARG-DELTA chunk 只含 index + arguments 片段。
- 把所有 args 片段拼起来能 JSON parse 出原始对象。
- finish chunk 的 finish_reason="tool_calls"。

跑：

```cmd
cd chatgpt.org
python test_app_e2e.py
# expect: PASS wire-format
```
