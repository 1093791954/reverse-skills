# User-Layer Fence 注入（system wrap 时的备选方案）

> 2026-05-11 新增。原始策略是把 fence 协议指令注入到 **system message** 末尾（见 `fence-protocol.md`）。当目标站点把 client 传的 system message 抹掉或硬覆盖时（duck.ai / 部分 agent wrap），把同样的指令挪到 **user message** 也能工作。

## 适用场景

- 第 4a 类拒绝信号：system 被 wrap，但模型仍输出**自由文本**（不是图片/SVG/模板）。
- 也适用于：站点完全不接受 `messages[0].role="system"`（只允许 user/assistant 角色）。
- 不适用于：4b 模板化输出、4c 完全无 chat 接口。

## 重写规则

```
client 真实请求（OpenAI 格式）:
  messages = [
    {role: "system", content: "<freeai-system> + <tool-protocol-directive>"},
    {role: "user", content: "List the files"}
  ]

→ 反代重写为（合并所有 system 到首条 user 前缀）:
  messages = [
    {role: "user", content:
        "[INSTRUCTIONS]\n"
        + "<freeai-system>\n\n"
        + "<tool-protocol-directive>\n\n"
        + "[/INSTRUCTIONS]\n\n"
        + "[TASK]\n"
        + "List the files\n"
        + "[/TASK]"
    }
  ]
```

要点：
1. **保留 client 真实 system 内容**（不丢失业务指令）。
2. 用显式分隔符 `[INSTRUCTIONS]...[/INSTRUCTIONS]` + `[TASK]...[/TASK]` 帮助模型区分元指令和任务本身。
3. **多轮历史**：把整轮 system+user 组合并到 **第一条** user message；后续轮次保持 user/assistant 原样。

## 多轮处理

```
client:
  messages = [
    {role: "system",    content: "<sys>"},
    {role: "user",      content: "U1"},
    {role: "assistant", content: "A1 (含 tool_call)"},
    {role: "tool",      content: "tool result"},
    {role: "user",      content: "U2"}
  ]

→ 重写：
  messages = [
    {role: "user",      content: "[INSTRUCTIONS] <sys> [/INSTRUCTIONS]\n\n[TASK] U1 [/TASK]"},
    {role: "assistant", content: "A1（fence 协议合成的 markdown 表示）"},
    {role: "user",      content: "[TOOL_RESULT]\n<tool result>\n[/TOOL_RESULT]\n\nU2"},
  ]
```

注意：
- 第二条往后的 user 也要用 `[TASK]` 标签，让模型识别"指令 / 工具结果 / 新任务"的边界。
- 不要重复注入 INSTRUCTIONS（避免上下文爆炸）；只在**首条 user** 注入完整规约。

## 在 `app.py` 里实现

伪代码（建议加到 `_common/tool_proxy.py` 旁边一个 `user_layer_proxy.py`）：

```python
def inject_tools_into_request_user_layer(
        req: ChatRequest, tool_choice=None) -> ChatRequest:
    """Same purpose as inject_tools_into_request(), but the directive
    lives in the first user message instead of the system message.
    Use when the upstream site overwrites or drops system role."""
    if not req.tools:
        return req
    directive = (
        build_tool_system_addendum(req.tools)
        + _build_tool_choice_directive(tool_choice)
    )
    new_messages: list[Message] = []
    sys_buffer = []
    first_user_seen = False
    for m in req.messages:
        if m.role == "system":
            sys_buffer.append(m.content)
            continue
        if m.role == "user" and not first_user_seen:
            first_user_seen = True
            sys_text = "\n\n".join(sys_buffer)
            combined = (
                f"[INSTRUCTIONS]\n{sys_text}\n\n{directive}\n[/INSTRUCTIONS]\n\n"
                f"[TASK]\n{m.content}\n[/TASK]"
            )
            new_messages.append(Message(role="user", content=combined))
            continue
        if m.role == "tool":
            # OpenAI 风格 tool result → 包成 [TOOL_RESULT]
            new_messages.append(Message(
                role="user",
                content=f"[TOOL_RESULT]\n{m.content}\n[/TOOL_RESULT]"))
            continue
        new_messages.append(m)
    return ChatRequest(
        model=req.model,
        messages=new_messages,
        tools=req.tools,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
        top_p=req.top_p,
        stream=req.stream,
    )
```

driver 用哪种 inject 由 driver 自己决定（在 `chat_stream` 调 `_build_body` 前决定）：

```python
class DuckAIDriver(ChatDriver):
    def __init__(...):
        ...
        self.use_user_layer_inject = True  # site-specific config

    async def chat_stream(self, req):
        if self.use_user_layer_inject:
            req = inject_tools_into_request_user_layer(req)
        else:
            req = inject_tools_into_request(req)
        ...
```

## 实战陷阱

1. **第一次工具循环失败率比 system-layer 注入高**：因为模型对 user-layer "扮演 system" 的指令服从率低，retry-on-no-tool-use 的命中率会上升 — 不是坏事，retry 机制已经准备好了。
2. **`required-strong` 指令在 user 层效果更好**：放 user 层时，"你的回复前 3 个字符必须是 fence"这种强约束更容易触发模型遵守（user 比 system 更新鲜）。
3. **历史很长时上下文爆炸**：`[INSTRUCTIONS]` 段最多 2KB，超过就只保留 tool-protocol 关键段，丢弃 client 的非 tool-related system 内容。
4. **某些站点会过滤 markdown 反引号**：先用 base64 包 fence 内 JSON 也可考虑：
   ```
   ```tool_call_b64
   eyJuYW1lIjogImJhc2giLCAuLi59
   ```
   ```
   增加 driver 端的 base64 解码步骤。

## 校验

新站点起来后，写一个 `test_user_layer_fence.py`：

```python
def test_first_turn_emits_fence():
    req = make_chat_request(tools=[...], system="...", user="List files")
    rewritten = inject_tools_into_request_user_layer(req)
    assert rewritten.messages[0].role == "user"
    assert "[INSTRUCTIONS]" in rewritten.messages[0].content
    assert "tool_call" in rewritten.messages[0].content
    assert "[TASK]" in rewritten.messages[0].content
```

加 E2E 跑一次真实工具循环，看 retry 后 fence 是否出现。
