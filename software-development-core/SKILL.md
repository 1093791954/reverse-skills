---
name: software-development-core
description: General software engineering workflow for planning, reviewing, refactoring, testing, debugging, and safely delivering code changes. Use when Codex needs to make or review code changes across any stack, define implementation plans, assess quality risks, choose tests, document architecture decisions, apply design patterns, or prepare a change for commit or release.
---

# Software Development Core

## Workflow

1. Start by reading the existing code, tests, docs, and local conventions before choosing an implementation shape.
2. State the goal, non-goals, constraints, rollback concerns, and acceptance criteria when the work is broad or risky.
3. Keep changes small and behavior-focused. Separate migrations, behavior changes, cleanup, and formatting unless the repo already couples them.
4. Choose tests by risk: unit for local logic, integration/contract for boundaries, E2E for critical user flows, and manual checks only where automation is impractical.
5. Review the final diff for correctness, maintainability, security, testability, compatibility, and operational impact.

## Architecture And Design

- Use ADRs for important decisions. Capture context, decision, status, consequences, and rejected alternatives.
- Use C4 or similarly layered diagrams to clarify system boundaries, containers, components, and external actors.
- Apply design patterns only when they match a real variation point. GoF has 23 classic patterns; Repository, Dependency Injection, and Unit of Work are common engineering patterns, not GoF originals.
- For large systems, review architecture style, business boundaries, data ownership, communication mode, deployment model, observability, and evolution path.

## Review Checklist

- Correctness: the code handles the main path, edge cases, error paths, and concurrency/state interactions.
- Maintainability: names, module boundaries, dependencies, and abstractions match the existing codebase.
- Security: untrusted input, authz/authn, secrets, file/network access, SSRF/injection, and unsafe defaults are checked.
- Testing: tests cover the riskiest behavior and do not only assert implementation details.
- Delivery: docs, config, migrations, monitoring, rollback, and compatibility impacts are explicit.

## References

Read `references/checklists.md` for detailed prompts on code review, testing strategy, ADRs, design patterns, and large-system architecture review.
