---
name: desktop-application-development
description: Desktop application engineering guidance for app architecture, local storage, settings, file system integration, installation, updates, signing, OS integration, logs, crash reporting, and cross-platform release decisions. Use when Codex builds or modifies native or cross-platform desktop apps.
---

# Desktop Application Development

## Workflow

1. Identify the target platforms, framework, packaging path, update model, signing requirements, local data model, and OS integrations.
2. Separate user documents, settings, cache, logs, secrets, and generated data.
3. Design install/update/uninstall, migration, rollback, crash reporting, and diagnostics before release changes.
4. Check platform differences for paths, permissions, menus, shortcuts, notifications, file associations, and background behavior.
5. Validate with clean install, upgrade, downgrade/rollback where supported, offline/permission failure, and multi-platform smoke tests.

## Core Rules

- Store secrets in the OS keyring or platform credential store, not plain config files.
- Treat auto-update as a security-sensitive feature: signature verification, failure recovery, and version compatibility are required.
- Prefer explicit platform adapters for OS integration rather than scattering platform checks through business logic.
- Keep local logs useful for support without leaking secrets or personal data.

## References

Read `references/checklists.md` for packaging, local data, updates, diagnostics, and platform compatibility checks.
