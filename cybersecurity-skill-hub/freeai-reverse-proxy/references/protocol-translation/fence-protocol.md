# Tool-Call Fence 协议规约

> 这是反代的核心创新：免费聊天站点上游的 LLM 不能直接吐 OpenAI `tool_calls`，所以我们用"在文本流里夹 markdown 代码块"的方式合成。

## 协议格式

注入到 system prompt 尾的指令（节选自 `_common/tool_proxy.py` 的 `build_tool_system_addendum()`）：

```
You have access to the following tools:

- bash(command, description): run a shell command
- read(filePath): read a file
- ...（每个工具的 JSON Schema 转成自然语言）

When you need to use a tool, output ONLY a markdown code block, exactly like this:

```tool_call
{"name": "<tool_name>", "arguments": { ... }}
```

After the closing ``` fence you may continue with your normal response.
You may emit multiple tool_call blocks in a single message; each block is one call.
```

模型回复（理想形态）：

```
Sure, I'll list the files first.

```tool_call
{"name": "bash", "arguments": {"command": "ls -la"}}
```

Once that returns I'll analyze the output.
```

## FenceStreamParser 状态机

`_common/tool_proxy.py` 的 `FenceStreamParser` 是一个把上游文本流 → OpenAI 事件流的状态机。状态：

- **TEXT**：常规文本，发 `TextDelta`。
- **MAYBE_FENCE_START**：看到 ` ``` `，可能是 fence 开始也可能是普通代码块；缓冲直到看到换行后的 `tool_call` 标签。
- **IN_FENCE**：在 ` ```tool_call ` 内，累积 JSON 直到 ` ``` ` 关闭。
- **FENCE_END**：解析 JSON，发 `ToolCallStart` / `ToolCallArgsDelta` / `ToolCallEnd`。

每个状态都要处理"分片到达"的情况：上游可能把 ` ```too ` 一个 chunk、`l_call\n{"na` 一个 chunk、`me":"bash"...` 一个 chunk 这样切碎。所以缓冲到完整 token 再做判断。

### 容错点

1. **JSON 容错**：`{name, arguments}` 标准格式，但模型有时直接 `{name, command, description}`（少了 arguments 包一层）。parser 兼容两种。
2. **空 arguments**：`{name}` 没 arguments key → 当作 `{}`。
3. **fence 内多余文字**：fence 内除了 JSON 还有解释文字 → 提取 `{...}` 最外层匹配的 JSON。
4. **mixed 文本**：fence 前的 prose + fence + fence 后的 prose 都要分别发 `TextDelta` + `ToolCall*`。
5. **跨流 chunks**：上游 chunk 是 `["```too", "l_call\n{\"na", ...]` 这样的不完整 token，必须缓冲。

## fence 不合规的几种"事故"

模型有时会：

1. **完全不出 fence**：直接 prose 回复，无视 tool 协议。→ 触发 retry-on-no-tool-use（见 `stability-fixes/retry-on-no-tool-use.md`）。
2. **fence 名字写错**：` ```toolcall ` / ` ```tool ` / ` ```call ` → 当作普通 markdown block 走 TEXT。
3. **JSON 不合法**：缺引号、单引号、注释 → 尝试容错解析，失败则当 TEXT 处理 + 记日志。
4. **过早闭 fence**：` ```tool_call\n{"name":\n``` ` → parser 报错，flush 已缓冲的文本，回 TEXT 状态。

## 性能注意

- parser 是**纯 Python 字符串扫描**，单 chunk < 1 µs，不要怕慢。
- 不要写正则！状态机更稳，能处理任意分片。
- 状态字段用 `self.buf` + `self.state` + `self.call_id`，每次 feed 都返回 list 事件。

## 完整实现

见 `templates/tool_proxy_skeleton.py` 或工程内 `_common/tool_proxy.py`。
