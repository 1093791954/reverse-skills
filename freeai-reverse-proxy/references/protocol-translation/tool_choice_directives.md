# tool_choice 指令注入

OpenAI 的 `tool_choice` 默认是 `"auto"`，但通过 fence 协议合成 tool_calls 时，**单纯依靠 system prompt 注入是不够的** — Claude Haiku 4.5 大约 30% 概率会忽略指令直接出纯文本。

## 4 档指令强度

`_common/tool_proxy.py` 的 `_build_tool_choice_directive()` 输出 4 档：

### `"auto"` / `None` — 默认（不追加指令）

```
（什么都不加 — 模型自己决定要不要用工具）
```

### `"none"` — 禁止工具

```
IMPORTANT: For this turn, do NOT use any tool. Do not emit any `tool_call`
fence. Answer entirely in plain natural language.
```

### `"required"` — 必须用工具

```
IMPORTANT: For this turn, you MUST emit exactly one `tool_call` fence.
Do not answer in plain text. Pick whichever tool best fits the user's request.
```

### `"required-strong"` — 极强工具指令（关键）

```
CRITICAL OUTPUT FORMAT — READ CAREFULLY:
Your previous reply was rejected because it was plain text. For this turn
you MUST output a `tool_call` fence as your FIRST action. The very first
three characters of your reply MUST be the three backticks of the opening
fence:
```tool_call
{"name": "<one of the available tool names>", "arguments": { ... }}
```
Do NOT preface the fence with any explanation. Do NOT say 'I will use ...'.
Do NOT describe what you are about to do. Output the fence first, then
optionally a brief sentence after the closing fence. Failing to start with
the fence will cause the user's task to fail.
```

`required-strong` 把"开头 3 字符必须是 ` ``` `"显式说穿，模型合规率显著上升。

## 自动升级（首轮 nudge）

在 `app.py` 里：

```python
effective_tool_choice = body.get("tool_choice")
if (tools and effective_tool_choice in (None, "auto")
        and not any(
            (m.get("tool_calls") if isinstance(m, dict) else None)
            for m in body.get("messages", []))):
    effective_tool_choice = "required-strong"
```

**触发条件**：
- 客户端带了 `tools: [...]`
- 没有显式 `tool_choice` 或 `tool_choice="auto"`
- 历史里没有 assistant tool_calls（即这是**第一个** tool-eligible turn）

这样保证第一次（最容易"忘记"用工具）的轮次模型一定看到强指令；后续轮次保留 auto，让模型能选择停止工具循环。

## 为什么不放在客户端

客户端（OpenCode 等）不知道我们用 fence 协议，它把 `tool_choice` 当成 OpenAI 的标准字段。所以**升级必须在反代里偷偷做**，对客户端透明。

## 何时还不够

即使升级到 `required-strong`，Haiku 4.5 仍有少数情况不出 fence。那时进入下一层兜底：`retry-on-no-tool-use`（见 `stability-fixes/retry-on-no-tool-use.md`）。
