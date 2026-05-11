# DevOps SRE Production Checklists

## Production Readiness

- Ownership, on-call path, runbook, dashboards, alerts, rollback, and support contacts are defined.
- Service has health/readiness checks and dependency visibility.
- Backup/restore and disaster recovery assumptions are tested or documented.
- Security controls and secret handling are reviewed.

## SLOs And Alerting

- SLI reflects user-visible success, latency, freshness, durability, or availability.
- SLO target has a rationale and an error budget.
- Alerts distinguish page-worthy symptoms from ticket-worthy cleanup.
- Burn-rate alerts are preferred for SLO consumption.

## Telemetry

- Metrics have bounded cardinality.
- Logs are structured and redacted.
- Traces propagate context across services.
- OpenTelemetry instrumentation is configured with sampling and cost in mind.

## Release And Incident Response

- Release has canary/gradual rollout or an explicit reason not to.
- Rollback is tested or mechanically clear.
- Incident response includes severity, commander, communications, mitigation, and postmortem.
- Postmortems are blameless and track action items to completion.
