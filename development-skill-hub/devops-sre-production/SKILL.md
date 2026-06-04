---
name: devops-sre-production
description: Production readiness, DevOps, and SRE guidance covering CI/CD, deployment, monitoring, logs, metrics, traces, SLOs, error budgets, alerting, runbooks, incident response, postmortems, rollback, capacity, and operational reliability. Use when Codex prepares services for production or improves operations.
---

# DevOps SRE Production

## Workflow

1. Identify the service, users, dependencies, deployment path, rollback path, SLOs, and on-call ownership.
2. Check production readiness before release: telemetry, dashboards, alerts, runbooks, capacity, backup/restore, security, and rollback.
3. Design SLOs around user-visible behavior, not only internal server metrics.
4. Alert on symptoms and SLO burn rate where possible; avoid noisy cause-only alerts.
5. After incidents, capture timeline, impact, detection gaps, mitigations, root causes, action items, owners, and due dates.

## Core Rules

- Metrics show trends and alert conditions; logs explain discrete events; traces explain cross-service request paths.
- Error budgets balance reliability and release velocity.
- Runbooks must be executable under stress: clear trigger, diagnosis, mitigation, rollback, escalation, and verification.
- Deployments need safe rollout, health checks, rollback, and observability before broad exposure.

## References

Read `references/checklists.md` for production readiness, SLOs, alerting, incidents, and release checks.
