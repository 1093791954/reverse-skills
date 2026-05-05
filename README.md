# Reverse Skills

This repository collects Codex skill packs for reverse-engineering research workflows.

## Skills

| Skill | Purpose |
| --- | --- |
| `imgui-reverse` | Dear ImGui workflows for Windows game reverse engineering overlays, including external windows, DX11 hook rendering, input forwarding, fonts, and common widgets. |
| `ue-reverse` | Unreal Engine reverse workflows covering source setup, `GName` / `FName`, `UObject`, `FUObjectArray`, `UWorld`, actor traversal, world-to-screen, bones, IoStore, and reflection metadata. |
| `packed-sample-analysis` | Lawful packed-sample and protected-binary analysis workflow, focused on triage, runtime observation, dump validation, and safe reporting boundaries. |

## Layout

```text
.
├── imgui-reverse/
│   ├── SKILL.md
│   ├── agents/
│   └── references/
├── packed-sample-analysis/
│   ├── SKILL.md
│   └── references/
└── ue-reverse/
    ├── SKILL.md
    ├── agents/
    └── references/
```

## Usage

Copy a skill directory into your Codex skills directory, or install this repository as a local skill source if your Codex setup supports repository-based skills.

Each `SKILL.md` is the entry point. The `references/` folders hold longer notes that should be loaded only when a task needs that specific context.

## Notes

Local Codex config backups, collection helpers, generated manifests, and generated caches are intentionally ignored.
