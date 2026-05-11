# Desktop Application Development Checklists

## Local Data

- Settings, cache, logs, user documents, secrets, and database files use distinct locations.
- Data migrations are versioned and recoverable.
- Logs redact credentials, tokens, and sensitive user data.

## Packaging And Updates

- Installer supports clean install, upgrade, uninstall, and repair where relevant.
- Updates are signed and verified.
- Failed updates leave the app in a runnable state.
- Version compatibility is tested across at least one previous release when possible.

## OS Integration

- File associations, URL protocols, notifications, tray, startup items, and permissions are documented.
- Platform-specific paths and shortcuts match OS conventions.
- Long-running work has progress, cancellation, and recovery behavior.

## Diagnostics

- Crash reports include app version, platform, feature area, and redacted context.
- Support logs can be collected without exposing secrets.
