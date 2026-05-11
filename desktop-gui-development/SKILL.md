---
name: desktop-gui-development
description: Desktop GUI implementation guidance for Qt, QML, WPF, WinUI, Electron, Tauri, native controls, window lifecycle, menus, shortcuts, IPC, webview security, and event/state handling. Use when Codex implements desktop windows, controls, menus, keyboard shortcuts, IPC, or GUI behavior.
---

# Desktop GUI Development

## Workflow

1. Identify the GUI stack, state model, command model, threading model, window lifecycle, and platform constraints.
2. Keep view code focused on presentation and interaction. Put business logic behind services, view models, commands, or ports.
3. Make menus, shortcuts, toolbar actions, context menus, and command availability consistent.
4. For Electron/Tauri/webview apps, define the IPC and permission boundary before exposing native capabilities.
5. Validate focus behavior, keyboard paths, multi-window state, long-running tasks, cancellation, and platform-specific behavior.

## Core Rules

- Electron: keep context isolation and sandbox on; avoid Node integration for remote content; validate IPC sender and payloads.
- Tauri: grant capabilities per window/webview and keep permissions minimal.
- Qt/QML: avoid embedding complex domain logic in views; expose explicit state and commands.
- WPF/WinUI: keep binding, command, and async UI-thread behavior explicit.

## References

Read `references/checklists.md` for window lifecycle, command surfaces, IPC security, and GUI validation checks.
