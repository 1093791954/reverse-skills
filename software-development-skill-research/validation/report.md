# 第一批软件开发技能验证报告

## 方法

- 对 8 个技能各准备 3 个真实任务样例。
- 使用 `validation/sample-project/` 中的小型样例项目逐项检查技能 frontmatter 是否能触发、`SKILL.md` 是否给出执行流程、`references/checklists.md` 是否提供足够的检查项。
- 运行 `quick_validate.py` 验证技能结构。

## 结果

| 技能 | 触发描述 | 工作流 | 检查项 | 结构验证 | 结论 |
|---|---|---|---|---|---|
| `software-development-core` | 通过 | 通过 | 通过 | 通过 | 可用 |
| `backend-development` | 通过 | 通过 | 通过 | 通过 | 可用 |
| `frontend-development` | 通过 | 通过 | 通过 | 通过 | 可用 |
| `frontend-ui-design` | 通过 | 通过 | 通过 | 通过 | 可用 |
| `desktop-application-development` | 通过 | 通过 | 通过 | 通过 | 可用 |
| `desktop-gui-development` | 通过 | 通过 | 通过 | 通过 | 可用 |
| `desktop-gui-design` | 通过 | 通过 | 通过 | 通过 | 可用 |
| `devops-sre-production` | 通过 | 通过 | 通过 | 通过 | 可用 |

## 修正点

- `software-development-core` 覆盖面较广，但 frontmatter 明确包含 planning/review/testing/ADR/design patterns/release，触发范围可接受。
- `frontend-ui-design` 与 `frontend-development` 边界清楚：前者偏 UI/UX 判断，后者偏代码实现、状态、性能和测试。
- `desktop-application-development`、`desktop-gui-development`、`desktop-gui-design` 的三分法成立：应用生命周期、GUI 实现、GUI 设计各自有独立检查项。
- 本轮未发现必须立即修改的规则冲突。

## 样例项目覆盖

- `api/orders-openapi.yaml` 覆盖 `backend-development` 的 API contract、auth、pagination、error shape 检查。
- `db/001_add_orders.sql` 覆盖 `backend-development` 和 `software-development-core` 的 migration/review 检查。
- `frontend/OrderFilter.tsx` 覆盖 `frontend-development` 与 `frontend-ui-design` 的 state、form、accessibility、loading state 检查。
- `desktop/electron-ipc.ts` 覆盖 `desktop-gui-development` 的 IPC surface、payload validation、native capability boundary 检查。
- `ops/orders-slo.yaml` 覆盖 `devops-sre-production` 的 SLI/SLO、burn-rate alert、runbook 检查。
- `architecture/adr-001-order-boundary.md` 覆盖 `software-development-core` 的 ADR 和 architecture boundary 检查。

## 后续迭代建议

- 第二批技能候选：`api-design`、`testing-strategy`、`secure-coding`、`design-patterns`、`large-scale-software-architecture`。
- 后续在真实项目使用时，记录触发不准或遗漏项，再回写对应 `SKILL.md` 或 `references/checklists.md`。
