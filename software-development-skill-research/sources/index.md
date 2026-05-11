# 软件开发技能资料来源索引

> 验证日期：2026-05-11。用途：为后续 Codex 软件开发技能提炼流程、检查清单和决策准则。本文只记录公开来源和可总结的知识点，不复制第三方长篇原文。

## 来源分级

- A：官方文档、官方 handbook、标准组织或项目官方资料。
- B：知名开源组织、工程团队、长期维护的 GitHub 仓库或 curated list。
- C：论坛、博客、个人资料库。只用于词表扩展和实践线索，不作为单一依据。

## 高价值来源

| 来源 | 类型 | 等级 | 主题 | 可提炼内容 | 授权/使用备注 |
|---|---|---:|---|---|---|
| https://google.github.io/eng-practices/ | 官方工程实践 | A | code review, maintainability | Code review 的目标、reviewer/author 职责、可维护性优先级、变更规模控制 | 总结规则，不复刻原文 |
| https://docs.gitlab.com/development/code_review/ | 官方开发文档 | A | code review, MR workflow | MR 审查流程、domain expert、review etiquette、review SLO | 总结流程和检查点 |
| https://handbook.gitlab.com/handbook/engineering/workflow/code-review/ | 官方 handbook | A | engineering workflow | review response SLO、maintainer/domain expert 模型、PTO/阻塞处理 | 适合 software-development-core |
| https://github.com/microsoft/api-guidelines | 官方 GitHub repo | A | API design | REST API 命名、一致性、版本、错误、分页、兼容性 | 查看仓库 license 后再引用；技能中只总结 |
| https://docs.github.com/en/rest/using-the-rest-api | 官方文档 | A | API usage | 认证、分页、rate limit、错误处理、最佳实践 | 适合 backend-development |
| https://web.dev/performance | 官方文档 | A | frontend performance | Core Web Vitals、PageSpeed、DevTools、性能课程入口 | 适合 frontend-development |
| https://web.dev/articles/vitals | 官方文档 | A | Core Web Vitals | LCP/INP/CLS、75th percentile、RUM 与工具测量 | 适合 frontend-development |
| https://www.electronjs.org/docs/latest/tutorial/security | 官方文档 | A | desktop security | Electron 安全 checklist、Node integration、context isolation、CSP、IPC sender 验证 | 适合 desktop-gui-development |
| https://v2.tauri.app/security/ | 官方文档 | A | desktop security | trust boundary、权限模型、安全默认值 | 适合 desktop-application-development |
| https://tauri.app/learn/security/capabilities-for-windows-and-platforms/ | 官方教程 | A | desktop capabilities | 多窗口 capabilities、平台差异、最小权限 | 适合 desktop-gui-development |
| https://learn.microsoft.com/en-us/windows/apps/get-started/best-practices | 官方文档 | A | Windows desktop | Windows app UX、窗口尺寸、Share、WinUI 建议 | 适合 desktop-application-development |
| https://learn.microsoft.com/en-us/windows/apps/get-started/make-apps-great-for-windows | 官方文档 | A | Windows UX | Windows 应用体验重点、UI/UX pattern、WinUI Gallery | 适合 desktop-gui-design |
| https://doc.qt.io/qt-6/qt-intro.html | 官方文档 | A | Qt desktop | Qt Quick/QML、跨平台部署、UI 技术选择 | 适合 desktop-gui-development |
| https://sre.google/sre-book/service-level-objectives/ | 官方开放书籍 | A | SRE | SLI/SLO/SLA、指标选择、目标设置、error budget | 适合 devops-sre-production |
| https://sre.google/sre-book/embracing-risk/ | 官方开放书籍 | A | SRE | error budget、产品与可靠性权衡、风险量化 | 适合 devops-sre-production |
| https://cloud.google.com/stackdriver/docs/solutions/slo-monitoring/alerting-on-budget-burn-rate | 官方文档 | A | alerting | burn-rate alert、SLO-based alert policy | 适合 devops-sre-production |
| https://sre.google/workbook/postmortem-culture/ | 官方开放书籍 | A | incident response | blameless postmortem、timeline、action item 跟踪 | 适合 devops-sre-production |
| https://designsystem.digital.gov/documentation/code-guidelines/ | 官方设计系统 | A | design system | USWDS code guidelines、贡献流程、可访问性/一致性 | 适合 frontend-ui-design |
| https://government.github.io/best-practices/design-systems/ | 政府 GitHub Pages | B | design systems | 政府设计系统索引、style guide/playbook 命名差异 | 适合词表扩展 |
| https://www.interface.guide/ | 设计 guideline | B | web interface | keyboard、focus、hit target、loading、optimistic update、destructive action | 适合 frontend-ui-design |
| https://github.com/mercari/production-readiness-checklist | GitHub repo | B | production readiness | 微服务上线前检查、服务 live readiness | 查看 repo license 后再引用 |
| https://github.com/kgoralski/microservice-production-readiness-checklist | GitHub repo | B | microservice readiness | observability、database、API、SDK 支持边界 | 查看 repo license 后再引用 |
| https://github.com/futurice/backend-best-practices | GitHub repo | B | backend | go-live checklist、日志、持久化、部署、责任划分 | 查看 repo license 后再引用 |
| https://github.com/joho/awesome-code-review | GitHub repo | B | code review | code review 资料索引、论文、工具、公司实践 | curated list，只作为入口 |
| https://github.com/yasir2000/awesome-software-architecture | GitHub repo | B | architecture | 架构模式、原则、测试、工程博客入口 | curated list，只作为入口 |
| https://devlevel.app/ | 技能矩阵 | B | skill taxonomy | backend/frontend/devops/SRE/infra/release role taxonomy | 用于技能分类校准 |
| https://github.com/vadimcomanescu/codex-skills | GitHub repo | C | Codex skills | 现有技能 catalog、frontend/backend/devops 技能命名参考 | 只做命名和触发描述参考 |
| https://github.com/akillness/oh-my-skills | GitHub repo | C | Codex skills | 技能集合、TDD、debugging、architecture、design-system 命名 | 只做技能工程参考 |
| https://www.reddit.com/r/sre/ | 论坛 | C | SRE practice | runbook、postmortem、SLO 实操痛点 | 只作为词表扩展 |
| https://www.reddit.com/r/Frontend/ | 论坛 | C | frontend/UI | 后端开发者补 UI 能力、design system、user flow | 只作为词表扩展 |

## 排除规则

- 不明授权 PDF、盗版书籍镜像、复制粘贴书籍内容的仓库不进入技能资料库。
- 论坛内容只进入“术语/痛点/场景”，不单独形成规则。
- GitHub 仓库必须在正式引用前检查 license；license 不清时只记录 URL 和概念，不复制内容。
