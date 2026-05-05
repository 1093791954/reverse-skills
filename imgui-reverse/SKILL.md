---
name: imgui-reverse
description: Summarize and apply Dear ImGui workflows for Windows game reverse engineering overlays. Use when the task involves ImGui environment setup, external windows, internal DX11 hook rendering, Win32 message-loop hooking, fonts or Chinese text, common widgets, or resolution/crash issues in reverse-engineering tools and game overlays.
---

# ImGui Reverse

Use this skill to turn the ImGui article series into a practical reverse-overlay workflow. Treat the series as a staged path from environment setup, to common controls, to external overlay windows, to internal DX11 hook integration.

## Workflow

1. Identify the target mode first: external overlay, internal overlay, or control/widget usage.
2. Read only the relevant part of [references/series.md](references/series.md) instead of loading the whole file.
3. Prefer lifting stable patterns from the series, then adapt them to the current project instead of rewriting from memory.
4. Keep Win32, DX11, and ImGui initialization order explicit. Most failures in this series come from incorrect init order, missing device/context state, or missing message forwarding.

## Article Map

- Read articles `1-2` for environment setup and the minimal external ImGui window.
- Read articles `3-10` for window composition and common controls: static text, buttons, colors, checkbox/radio, input, slider, progress bar.
- Read article `11` for fonts, glyph ranges, and Chinese text support.
- Read article `12` for a standalone external overlay form.
- Read articles `13-18` for internal rendering: framework setup, DX11 vtable hook, internal windows, Win32 message hook, and resolution-change stability.

## External Overlay Path

Use this path when the user wants a separate overlay process or tool window.

1. Start from the environment and sample-project setup in articles `1-2`.
2. Reuse the article sequence for controls instead of composing widgets ad hoc.
3. Use article `11` before debugging text corruption, missing Chinese glyphs, or font atlas issues.
4. Use article `12` as the baseline for an independent overlay shell.

Focus on:

- ImGui sample reuse instead of greenfield setup.
- Stable Win32 window creation and event pumping.
- Explicit font loading and glyph-range selection.
- Keeping the overlay loop independent from the target game process.

## Internal DX11 Hook Path

Use this path when the user wants an injected internal menu or ESP-like drawing layer.

1. Start from article `13` for the minimal internal ImGui frame.
2. Read articles `14-15` together for DX11 vtable understanding and Present-style hook implementation.
3. Read article `16` for drawing ImGui windows after the hook is stable.
4. Read article `17` for message-loop forwarding or WndProc-style input integration.
5. Read article `18` when fullscreen or resolution changes trigger crashes or device-state invalidation.

Check these points every time:

- Device, context, swap chain, render target, and ImGui context are initialized once.
- Hook installation and uninstallation are symmetric.
- Input is forwarded only when the menu is active or when explicit capture is intended.
- Resolution changes recreate render targets and any size-dependent state.

## Troubleshooting

- If the overlay opens but widgets do not react, inspect the Win32 message path first, then article `17`.
- If Chinese text renders as squares or mojibake, read article `11` and verify font file, glyph range, and font atlas rebuild.
- If the internal overlay crashes only after changing resolution or toggling fullscreen, use article `18` and re-check device-object rebuild order.
- If DX11 hook code works in a sample but not in the target, verify the swap-chain acquisition path and vtable index assumptions before touching ImGui code.

## Reference Use

- Use [references/series.md](references/series.md) as the source notebook for the full 18-article series.
- Search within that file by article number or keyword such as `DX11`, `Hook消息循环`, `字体`, `中文`, `外部绘制`, or `分辨率`.
- When answering or implementing, compress the article material into actionable steps rather than repeating tutorial narration.
