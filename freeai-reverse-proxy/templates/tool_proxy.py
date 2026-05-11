"""Tool-call inject + stream-parse helpers.

The free chat sites we reverse-proxy don't natively support tool use.
We inject a `system` instruction that teaches the model to emit tool
calls as fenced markdown blocks:

    ```tool_call
    {"name": "<tool_name>", "arguments": {...}}
    ```

This module:
  - builds the system-prompt addendum from a list of ToolSpec
  - parses the model's streaming text output and converts detected
    fences into ToolCall* StreamChunks for the driver-base layer.
"""
from __future__ import annotations

import json
import re
import uuid
from typing import AsyncIterator

from driver_base import (
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

FENCE_OPEN = "```tool_call"
FENCE_CLOSE = "```"


def build_tool_system_addendum(tools: list[ToolSpec]) -> str:
    """Generate the system-prompt addendum that teaches the model how to
    emit tool calls. Output is plain markdown to be appended to (or set
    as) the system message."""
    if not tools:
        return ""
    spec_lines = []
    for t in tools:
        spec_lines.append(
            f"- name: {t.name}\n"
            f"  description: {t.description}\n"
            f"  parameters: {json.dumps(t.parameters, ensure_ascii=False)}"
        )
    spec = "\n".join(spec_lines)
    return f"""

# TOOL USE PROTOCOL

You have access to the following tools:

{spec}

When you decide to use a tool, output a SINGLE fenced markdown block
exactly like this and nothing else after it (no commentary, no follow-up
text in the same turn):

```tool_call
{{"name": "<tool_name>", "arguments": {{...JSON object holding ALL parameters...}}}}
```

CRITICAL FORMAT RULES (read carefully):
1. The OUTER object has exactly two keys: "name" and "arguments".
2. ALL tool parameters MUST go INSIDE the "arguments" object — do NOT put
   them at the top level next to "name".

GOOD example for a `bash` tool with parameter `command`:
```tool_call
{{"name": "bash", "arguments": {{"command": "ls -la"}}}}
```

BAD example (this will FAIL — parameters at top level):
```tool_call
{{"name": "bash", "command": "ls -la"}}
```

After emitting the fence, STOP. The user will reply with a message of
the form:

```tool_result
{{"name": "<tool_name>", "result": ...}}
```

Use the result and continue. If you do NOT need a tool, just answer
in plain natural language (no fences). Only emit `tool_call` fences
when you genuinely need a tool's output.
"""


def _build_tool_choice_directive(tool_choice) -> str:
    """Translate an OpenAI `tool_choice` value into a system-prompt
    directive paragraph. Returns "" for `auto` / None (default behavior).

    Accepts:
      - None or "auto"   → no directive
      - "none"           → forbid any tool call
      - "required"       → mandate exactly one tool call
      - {"type":"function","function":{"name":"X"}}  → mandate that tool
    """
    if tool_choice is None or tool_choice == "auto":
        return ""
    if tool_choice == "none":
        return (
            "\n\nIMPORTANT: For this turn, do NOT use any tool. Do not emit "
            "any `tool_call` fence. Answer entirely in plain natural "
            "language.\n"
        )
    if tool_choice == "required":
        return (
            "\n\nIMPORTANT: For this turn, you MUST emit exactly one "
            "`tool_call` fence. Do not answer in plain text. Pick whichever "
            "tool best fits the user's request.\n"
        )
    if tool_choice == "required-strong":
        # Used by the server's retry-on-no-tool-use path. The previous
        # attempt produced plain text and zero tool calls. Be extremely
        # explicit about the required output format.
        return (
            "\n\nCRITICAL OUTPUT FORMAT — READ CAREFULLY:\n"
            "Your previous reply was rejected because it was plain text. "
            "For this turn you MUST output a `tool_call` fence as your "
            "FIRST action. The very first three characters of your reply "
            "MUST be the three backticks of the opening fence:\n"
            "```tool_call\n"
            "{\"name\": \"<one of the available tool names>\", "
            "\"arguments\": { ... }}\n"
            "```\n"
            "Do NOT preface the fence with any explanation. Do NOT say "
            "'I will use ...'. Do NOT describe what you are about to do. "
            "Output the fence first, then optionally a brief sentence after "
            "the closing fence. Failing to start with the fence will cause "
            "the user's task to fail.\n"
        )
    if isinstance(tool_choice, dict):
        fn = (tool_choice.get("function") or {})
        forced_name = fn.get("name", "")
        if forced_name:
            return (
                f"\n\nIMPORTANT: For this turn, you MUST call the tool "
                f"named `{forced_name}` exactly once via a `tool_call` "
                f"fence. Do not call any other tool. Do not answer in "
                f"plain text.\n"
            )
    return ""


def inject_tools_into_request(req: ChatRequest, tool_choice=None) -> ChatRequest:
    """Return a NEW ChatRequest with the tool-protocol prompt injected
    into / appended to the system message. Original `req` is not mutated.

    `tool_choice` follows the OpenAI shape: None | "auto" | "none" |
    "required" | {"type":"function","function":{"name":"X"}}.
    """
    if not req.tools:
        return req

    addendum = build_tool_system_addendum(req.tools) + \
               _build_tool_choice_directive(tool_choice)
    new_messages: list[Message] = []
    sys_seen = False
    for m in req.messages:
        if m.role == "system" and not sys_seen:
            new_messages.append(Message(role="system",
                                        content=m.content + addendum))
            sys_seen = True
        else:
            new_messages.append(m)
    if not sys_seen:
        new_messages.insert(0, Message(role="system",
                                       content=addendum.lstrip()))
    return ChatRequest(
        model=req.model,
        messages=new_messages,
        tools=req.tools,
        max_tokens=req.max_tokens,
        temperature=req.temperature,
        top_p=req.top_p,
        stream=req.stream,
    )


# --- Streaming parser ------------------------------------------------------

class FenceStreamParser:
    """State machine that consumes raw text chunks (str) from the upstream
    chat stream and yields canonical StreamChunks with tool calls extracted.

    States:
      - "text"          → forward text to user
      - "fence_open"    → saw ```tool_call header, accumulating JSON
      - "fence_close"   → saw closing ```, parse + emit ToolCallEnd

    Boundary tolerance:
      - chunks may split the fence header arbitrarily. We buffer up to
        len(FENCE_OPEN) chars before deciding whether to forward.
    """

    def __init__(self) -> None:
        self.state: str = "text"
        self.buf: str = ""               # holds bytes that may be the start of a fence
        self.fence_buf: str = ""         # holds bytes still inside the fence (not yet emitted as args-delta)
        self.fence_accum: str = ""       # FULL accumulated JSON content of the in-progress fence (for final parse)
        self.current_call_id: str | None = None
        self.last_emitted_tool: bool = False

    def _new_call_id(self) -> str:
        return f"call_{uuid.uuid4().hex[:12]}"

    def feed(self, text: str) -> list[StreamChunk]:
        """Feed a text chunk. Returns a list of StreamChunks to emit
        (TextDelta / ToolCallStart / ToolCallArgsDelta / ToolCallEnd)."""
        out: list[StreamChunk] = []
        if not text:
            return out

        # Append to whichever buffer we're filling
        if self.state == "text":
            self.buf += text
            out.extend(self._consume_text_buf())
        elif self.state == "fence_open":
            self.fence_buf += text
            out.extend(self._consume_fence_buf())
        return out

    def _consume_text_buf(self) -> list[StreamChunk]:
        out: list[StreamChunk] = []
        # Look for the fence open marker
        idx = self.buf.find(FENCE_OPEN)
        if idx >= 0:
            # emit text before the fence
            if idx > 0:
                out.append(TextDelta(text=self.buf[:idx]))
            # advance past `FENCE_OPEN` + newline
            after_fence = self.buf[idx + len(FENCE_OPEN):]
            # strip leading newline if present
            if after_fence.startswith("\n"):
                after_fence = after_fence[1:]
            self.state = "fence_open"
            self.fence_buf = after_fence
            self.fence_accum = ""
            self.current_call_id = self._new_call_id()
            self.buf = ""
            out.append(ToolCallStart(call_id=self.current_call_id))
            out.extend(self._consume_fence_buf())
            return out

        # No full fence found; check if buffer might be PARTIAL prefix of fence
        # (so we don't emit `\`\``)
        # only hold at most len(FENCE_OPEN) - 1 chars for that
        safe_len = max(0, len(self.buf) - (len(FENCE_OPEN) - 1))
        if safe_len > 0:
            out.append(TextDelta(text=self.buf[:safe_len]))
            self.buf = self.buf[safe_len:]
        return out

    def _consume_fence_buf(self) -> list[StreamChunk]:
        out: list[StreamChunk] = []
        idx = self.fence_buf.find(FENCE_CLOSE)
        if idx >= 0:
            # we have the closing fence. Emit any final pre-close bytes
            # as the last args-delta, then parse the FULL accumulated json.
            tail = self.fence_buf[:idx]
            if tail:
                out.append(ToolCallArgsDelta(
                    call_id=self.current_call_id, arguments_delta=tail))
                self.fence_accum += tail
            json_text = self.fence_accum.rstrip()
            try:
                parsed = json.loads(json_text)
                tool_name = parsed.get("name", "")
                if "arguments" in parsed and isinstance(parsed["arguments"], dict):
                    # Canonical form: {"name":..., "arguments": {...}}
                    args = parsed["arguments"]
                else:
                    # Tolerant form: model put params at top level alongside
                    # "name" (e.g. {"name":"bash","command":"ls"}). Strip the
                    # name and treat the rest as args.
                    args = {k: v for k, v in parsed.items() if k != "name"}
            except json.JSONDecodeError:
                tool_name = "unknown"
                args = {"_raw": json_text}
            out.append(ToolCallEnd(
                call_id=self.current_call_id,
                tool_name=tool_name,
                arguments=args,
            ))
            # reset for any text after the fence
            self.state = "text"
            after = self.fence_buf[idx + len(FENCE_CLOSE):]
            if after.startswith("\n"):
                after = after[1:]
            self.fence_buf = ""
            self.fence_accum = ""
            self.current_call_id = None
            self.last_emitted_tool = True
            self.buf = after
            out.extend(self._consume_text_buf())
            return out

        # No close yet — emit incremental args-delta of what we have so far
        # (best effort streaming UX). We only emit chars that won't interfere
        # with detecting `\`\``.
        safe_len = max(0, len(self.fence_buf) - (len(FENCE_CLOSE) - 1))
        if safe_len > 0:
            chunk = self.fence_buf[:safe_len]
            self.fence_buf = self.fence_buf[safe_len:]
            self.fence_accum += chunk
            out.append(ToolCallArgsDelta(
                call_id=self.current_call_id,
                arguments_delta=chunk,
            ))
        return out

    def flush(self) -> list[StreamChunk]:
        """Call when upstream stream ends. Emits any leftover text."""
        out: list[StreamChunk] = []
        if self.state == "text" and self.buf:
            out.append(TextDelta(text=self.buf))
            self.buf = ""
        elif self.state == "fence_open":
            # incomplete fence — recover the full original text as plain text
            # so the user still sees what the model was trying to say.
            recovered = FENCE_OPEN + "\n" + self.fence_accum + self.fence_buf
            out.append(TextDelta(text=recovered))
            self.fence_buf = ""
            self.fence_accum = ""
            self.current_call_id = None
            self.state = "text"
        return out


# --- Helpers for tool result roundtrip ------------------------------------

def encode_tool_result(tool_name: str, result) -> str:
    """Wrap a tool result into the protocol's tool_result fence so the
    model knows what came back."""
    return (f"```tool_result\n"
            f"{json.dumps({'name': tool_name, 'result': result}, ensure_ascii=False)}\n"
            f"```\n")
