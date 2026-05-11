# Backend Development Checklists

## API Contract

- Define resource names, methods, status codes, error format, pagination, filtering, sorting, idempotency, and versioning.
- Use OpenAPI for request/response schemas, security schemes, examples, and compatibility review.
- Use Problem Details or another consistent error envelope.
- Add contract tests when external clients rely on the API.

## Security

- Check OWASP API risks: broken object-level authorization, broken function-level authorization, unrestricted resource consumption, SSRF, excessive data exposure, and unsafe business flows.
- Validate input at trust boundaries.
- Avoid logging secrets, tokens, credentials, or sensitive PII.

## Data And Migrations

- Plan expand/migrate/contract steps for risky schema changes.
- Avoid long blocking locks on production tables.
- Include rollback or forward-fix instructions.
- Ensure old and new app versions can coexist during deployment.

## Reliability

- Set timeouts for outbound calls.
- Make retries bounded and safe.
- Use idempotency keys or dedupe where requests/jobs may repeat.
- Emit structured logs, metrics, traces, and correlation IDs for important paths.

## Production Readiness

- Health/readiness checks exist and reflect dependencies realistically.
- Dashboards and alerts cover user-visible failures.
- Runbooks explain diagnosis, mitigation, rollback, and escalation.
