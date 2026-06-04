# Frontend Development Checklists

## State

- Server state: cache, stale time, loading, error, retry, mutation, invalidation.
- URL state: filters, search, selected resource, pagination, shareable view.
- Form state: validation, dirty state, submit state, error mapping, reset behavior.
- UI state: menus, tabs, disclosure, hover/focus, transient feedback.

## Accessibility

- Every form control has a label and error association.
- Interactive elements are keyboard reachable and have visible focus.
- Dynamic updates use appropriate status messages.
- Custom widgets follow ARIA APG keyboard patterns.
- Color is not the only information channel.

## Performance

- Check bundle growth, route splitting, render-blocking resources, image sizing, font loading, hydration, and long tasks.
- Optimize for LCP, INP, and CLS rather than synthetic scores alone.
- Prefer measuring real user impact when data is available.

## Testing

- Component tests cover state transitions and edge cases.
- E2E tests cover critical user paths, not every branch.
- Visual regression covers layout-dense or design-system-sensitive surfaces.
- Accessibility checks cover keyboard and screen-reader relevant paths.
