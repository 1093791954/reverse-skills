# Software Development Core Checklists

## Code Review

- Check correctness, maintainability, readability, security, testability, compatibility, and operational impact.
- Mark comments as blocker, suggestion, or nit.
- Prefer smaller follow-up issues over expanding an already large change unless correctness requires it.

## Test Strategy

- Unit: pure logic and fast branch coverage.
- Integration: persistence, framework wiring, adapters, and external boundaries.
- Contract: API producer/consumer compatibility and schema changes.
- E2E: critical user or business paths only.
- Manual: exploratory, visual, hardware, platform, or third-party flows that automation cannot reliably cover.

## ADR Template

```text
Title:
Status: proposed | accepted | superseded
Context:
Decision:
Consequences:
Alternatives considered:
```

## Design Patterns

- Creational: Factory Method, Abstract Factory, Builder, Prototype, Singleton.
- Structural: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy.
- Behavioral: Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor.
- Common engineering extensions: Repository, Dependency Injection, Unit of Work.

Use a pattern when it names and contains real complexity. Avoid introducing a pattern if a direct local helper is clearer.

## Large-System Architecture Review

- Business boundary: bounded context, ownership, ubiquitous language, and user-visible capability.
- Data boundary: source of truth, consistency model, migration path, backup/restore, and retention.
- Communication: sync/async, idempotency, retries, timeouts, ordering, and backpressure.
- Operations: telemetry, SLO, runbook, capacity, rollout, rollback, and incident path.
- Security: least privilege, safe defaults, secrets, input validation, dependency risk, and auditability.
