# 自我审查记录

## 2026-05-11

目的：降低资料库中的幻觉风险，区分已验证事实、人工归纳和待复核内容。

## 检查项

- URL 可访问性：从 `sources/index.md` 抽取全部 URL，用 PowerShell `Invoke-WebRequest` 检查。结果：全部返回 HTTP 200。
- GitHub license：用 GitHub API 检查 8 个 GitHub 仓库的 license、stars、archived、pushed_at。结果已回写到 `sources/index.md` 的授权备注。
- 统计口径：`search-log.md` 中轮次的有效来源/新增术语数量不是脚本精确统计，已改为“约数”和人工归纳口径。
- 来源等级：A/B/C 等级保留，但只代表研究优先级，不代表可以复制内容。

## GitHub license 抽查

| Repo | License | Stars | Archived | Last pushed |
|---|---|---:|---|---|
| microsoft/api-guidelines | Other | 23268 | false | 2025-08-11 |
| mercari/production-readiness-checklist | MIT | 931 | false | 2021-11-22 |
| kgoralski/microservice-production-readiness-checklist | Apache-2.0 | 218 | false | 2024-10-23 |
| futurice/backend-best-practices | Other | 2353 | false | 2019-09-20 |
| joho/awesome-code-review | not reported | 5024 | false | 2024-09-09 |
| yasir2000/awesome-software-architecture | CC0-1.0 | 71 | false | 2022-05-08 |
| vadimcomanescu/codex-skills | MIT | 7 | false | 2026-01-22 |
| akillness/oh-my-skills | not reported | 13 | false | 2026-05-11 |

## Remaining Risk

- 部分“可提炼内容”是基于搜索结果和页面主题的摘要，需要在创建对应技能时再次打开来源页面核对细节。
- GitHub stars 和 pushed_at 会随时间变化；本记录只代表 2026-05-11 的抽查状态。
- 论坛来源只用于词表扩展，不作为最终技能规则依据。
