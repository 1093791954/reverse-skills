"""Echo driver — self-check / unit-test only.

This driver doesn't call any real LLM.  It echoes the user's last
message back, and (for the `echo-tool` model) synthesises a fake
tool_call fence to exercise the FenceStreamParser → OpenAI
tool_calls wire-format chain end-to-end without touching the
network.

Put this in `_common/echo.py` so every per-site server can register
it for `test_app_e2e.py` to use.
"""
from __future__ import annotations

import asyncio
import json
from typing import AsyncIterator

from driver_base import (
    ChatDriver,
    ChatRequest,
    StreamChunk,
    StreamDone,
    TextDelta,
    ToolCallEnd,
)
from tool_proxy import FenceStreamParser


class EchoDriver(ChatDriver):
    name = "echo"
    supported_models = ["echo-1", "echo-tool"]

    async def chat_stream(
        self, req: ChatRequest
    ) -> AsyncIterator[StreamChunk]:
        last_user = ""
        for m in req.messages:
            if m.role == "user":
                last_user = m.content
        # echo-1: just echo
        if req.model == "echo-1":
            text = f"(echo) {last_user}"
            for piece in _slice(text, 8):
                yield TextDelta(text=piece)
                await asyncio.sleep(0)
            yield StreamDone(finish_reason="stop")
            return
        # echo-tool: pretend the model called the first tool with q=<user input>
        tool_name = "search"
        if req.tools:
            tool_name = req.tools[0].name
        args = {"q": last_user}
        # Emit a tool_call fence block as if the LLM produced it, then route
        # through the parser so the wire-format is identical to a real run.
        fence = "```tool_call\n" + json.dumps(
            {"name": tool_name, "arguments": args}) + "\n```\n"
        parser = FenceStreamParser()
        for piece in _slice(fence, 8):
            for out in parser.feed(piece):
                yield out
        for out in parser.flush():
            yield out
        yield StreamDone(finish_reason="tool_calls")

    async def health_check(self) -> bool:
        return True


def _slice(s: str, n: int):
    for i in range(0, len(s), n):
        yield s[i:i + n]
