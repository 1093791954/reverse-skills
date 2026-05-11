---
name: desktop-gui-design
description: Desktop GUI design guidance for professional tools and native-feeling desktop software, including workspace layout, toolbars, property panels, settings pages, density, focus, keyboard workflows, accessibility, and long-running task feedback. Use when Codex improves desktop app usability or visual design.
---

# Desktop GUI Design

## Workflow

1. Identify the user's repeated workflow, primary objects, secondary objects, and command frequency.
2. Choose the workspace model: document, project, inspector, dashboard, queue, editor, or multi-pane tool.
3. Place commands by frequency and context: toolbar, menu bar, context menu, shortcut, command palette, or inspector.
4. Design focus, selection, disabled, empty, loading, progress, conflict, and error states.
5. Validate density, scan path, keyboard efficiency, accessibility, and recovery from mistakes.

## Core Rules

- Professional desktop tools should prioritize stable layout, information density, and repeated action efficiency.
- Toolbars are for frequent commands; menus are for discoverability and full command coverage; property panels are for selected-object editing.
- Settings pages should be grouped by task and risk, not presented as one long form.
- Long-running operations need progress, cancellation, background behavior, and completion/error feedback.

## References

Read `references/checklists.md` for workspace, command placement, density, settings, and accessibility checks.
