---
name: backend-development
description: Backend service and API development guidance covering REST/API design, OpenAPI, database changes, migrations, caching, queues, auth, concurrency, observability, reliability, security, and production readiness. Use when Codex works on server-side code, APIs, persistence, background jobs, service integrations, microservice boundaries, or backend tests.
---

# Backend Development

## Workflow

1. Identify the contract first: endpoint/event/job name, caller, auth requirements, schema, compatibility, and failure behavior.
2. Inspect the existing service boundaries, persistence patterns, migration style, validation, logging, and tests before editing.
3. Keep API and data changes backward-compatible unless a breaking change is explicitly requested and documented.
4. Add idempotency, timeouts, retries, and observability where work crosses process, network, queue, or database boundaries.
5. Validate with unit tests for logic, integration tests for storage/framework behavior, and contract tests for public interfaces.

## Core Rules

- Separate authentication from authorization. Check object-level and function-level permissions, not just login state.
- Migrations must account for rollback, locking, long-running writes, old code reading new data, and new code reading old data.
- Cache changes need an invalidation strategy, consistency expectation, fallback, and observability.
- Queue and background job code must handle duplicate delivery, retries, dead letters, ordering assumptions, and partial failure.
- Public APIs should define pagination, filtering, sorting, error shape, rate limit behavior, versioning, and examples.

## Architecture

- Use bounded contexts and business capabilities to split services; do not split only by database tables or code volume.
- Event-driven designs reduce producer/consumer coupling but introduce eventual consistency, replay, ordering, and debugging costs.
- Hexagonal or ports/adapters structure is useful when isolating domain logic from databases, UI, queues, or external APIs.

## References

Read `references/checklists.md` for API, data, security, reliability, and production readiness checks.
