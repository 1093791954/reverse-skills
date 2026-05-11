# ADR 001: Keep order listing in commerce-platform

Status: proposed

## Context

Order listing is used by the admin dashboard, support tooling, and billing reconciliation. The data source is currently owned by commerce-platform.

## Decision

Keep the order listing API in commerce-platform and expose a paginated `/orders` endpoint.

## Consequences

- Commerce-platform remains the source of truth for order listing.
- Dashboard and support tooling use the same contract.
- Future extraction to a separate order-query service requires a new ADR.
