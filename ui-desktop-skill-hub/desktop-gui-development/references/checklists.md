# Desktop GUI Development Checklists

## Window And State

- Window creation, restore, close, minimize, focus, and multi-monitor behavior are handled.
- Unsaved changes and long-running operations are protected during close/navigation.
- Multi-window state has a clear source of truth.

## Commands

- Menu, toolbar, shortcut, context menu, and command palette actions map to the same command model.
- Disabled actions explain why when the reason is not obvious.
- Undo/redo support is considered for destructive or editing operations.

## IPC And Webview Security

- Expose a narrow API surface.
- Validate sender, origin, payload shape, and permissions.
- Avoid passing raw file system or shell capability to untrusted UI code.
- Use CSP and navigation/window-open restrictions for webview content.

## GUI Validation

- Keyboard-only operation works for primary flows.
- Focus order is stable.
- Loading and error states do not block the event loop.
- Platform-specific shortcuts and menus follow conventions.
