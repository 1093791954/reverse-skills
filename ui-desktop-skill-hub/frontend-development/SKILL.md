---
name: frontend-development
description: Frontend engineering workflow for React, Vue, TypeScript, routing, state management, browser performance, Core Web Vitals, accessibility, forms, frontend testing, and build behavior. Use when Codex implements web UI behavior, fixes frontend bugs, improves performance, adds accessibility, or writes component/E2E/visual tests.
---

# Frontend Development

## Workflow

1. Inspect the app framework, routing, state libraries, design system, test setup, and existing component patterns.
2. Classify state before implementing: server state, URL state, client UI state, form state, or derived state.
3. Preserve accessibility from the first pass: semantic HTML, labels, keyboard flow, focus, names, roles, and status messages.
4. Check performance impact for new routes, large components, images, fonts, hydration, long tasks, and bundle size.
5. Validate with component tests for state, E2E tests for critical flows, accessibility checks for interactive UI, and visual checks for layout risk.

## Core Rules

- Prefer semantic HTML before ARIA. Use ARIA APG patterns only when native semantics do not cover the widget.
- Keep data fetching, mutation state, optimistic updates, and error recovery explicit.
- Avoid hiding essential state in local component variables when URL or server state is the source of truth.
- Use Core Web Vitals as user-facing performance signals: LCP, INP, CLS, preferably at the 75th percentile.

## References

Read `references/checklists.md` for accessibility, performance, state, and frontend testing checks.
