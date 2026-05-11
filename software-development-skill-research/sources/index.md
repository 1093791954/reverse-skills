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
| https://github.com/microsoft/api-guidelines | 官方 GitHub repo | A | API design | REST API 命名、一致性、版本、错误、分页、兼容性 | GitHub API 显示 license=Other；只总结，不复制内容 |
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
| https://github.com/mercari/production-readiness-checklist | GitHub repo | B | production readiness | 微服务上线前检查、服务 live readiness | GitHub API 显示 MIT；可总结，引用需保留来源 |
| https://github.com/kgoralski/microservice-production-readiness-checklist | GitHub repo | B | microservice readiness | observability、database、API、SDK 支持边界 | GitHub API 显示 Apache-2.0；可总结，引用需保留来源 |
| https://github.com/futurice/backend-best-practices | GitHub repo | B | backend | go-live checklist、日志、持久化、部署、责任划分 | GitHub API 显示 license=Other；只总结，不复制内容 |
| https://github.com/joho/awesome-code-review | GitHub repo | B | code review | code review 资料索引、论文、工具、公司实践 | GitHub API 未返回 license；只作为入口 |
| https://github.com/yasir2000/awesome-software-architecture | GitHub repo | B | architecture | 架构模式、原则、测试、工程博客入口 | GitHub API 显示 CC0-1.0；curated list，只作为入口 |
| https://devlevel.app/ | 技能矩阵 | B | skill taxonomy | backend/frontend/devops/SRE/infra/release role taxonomy | 用于技能分类校准 |
| https://github.com/vadimcomanescu/codex-skills | GitHub repo | C | Codex skills | 现有技能 catalog、frontend/backend/devops 技能命名参考 | GitHub API 显示 MIT；只做命名和触发描述参考 |
| https://github.com/akillness/oh-my-skills | GitHub repo | C | Codex skills | 技能集合、TDD、debugging、architecture、design-system 命名 | GitHub API 未返回 license；只做技能工程参考 |
| https://www.reddit.com/r/sre/ | 论坛 | C | SRE practice | runbook、postmortem、SLO 实操痛点 | 只作为词表扩展 |
| https://www.reddit.com/r/Frontend/ | 论坛 | C | frontend/UI | 后端开发者补 UI 能力、design system、user flow | 只作为词表扩展 |
| https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/ | 官方安全项目 | A | secure coding | 技术无关的安全编码 checklist、软件安全原则、术语 | 适合 backend/frontend/desktop 的安全检查项 |
| https://owasp.org/API-Security/ | 官方安全项目 | A | API security | OWASP API Security Top 10 2023、授权、业务流保护、SSRF 等 API 风险 | 适合 backend-development |
| https://owasp.org/www-project-application-security-verification-standard/ | 官方安全标准 | A | application security | Web 应用安全控制验证要求、安全开发需求 | 适合 software-development-core/backend-development |
| https://www.cisa.gov/securebydesign | 政府安全指导 | A | secure by design | secure by design/default、厂商责任、安全默认值 | 适合 software-development-core/devops-sre-production |
| https://martinfowler.com/articles/practical-test-pyramid.html | 工程实践文章 | B | testing strategy | 不同粒度自动化测试、测试金字塔、contract test、E2E 权衡 | 适合 software-development-core |
| https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html | 官方工程博客 | A | testing strategy | Google 测试金字塔、E2E 测试成本与脆弱性 | 适合 software-development-core |
| https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices | 官方文档 | A | unit testing | 单元测试可读性、脆弱测试、测试设计准则 | 适合 software-development-core |
| https://adr.github.io/ | ADR 组织站点 | B | architecture decisions | ADR 定义、decision log、architecturally significant requirement | 适合 software-development-core |
| https://github.com/npryce/adr-tools | GitHub repo | B | ADR tooling | ADR 命令行工具、`doc/architecture/decisions` 目录惯例 | 需检查 license；只作为工具入口 |
| https://c4model.info/ | 官方模型站点 | B | architecture diagrams | C4 的 Person/System/Container/Component 抽象和四类图 | 适合 software-development-core |
| https://arc42.org/documentation | 官方模板站点 | B | architecture documentation | 轻量架构文档模板、stakeholder-oriented documentation | 适合 software-development-core |
| https://opentelemetry.io/docs/ | 官方文档 | A | observability | vendor-neutral telemetry、traces/metrics/logs、instrumentation | 适合 backend-development/devops-sre-production |
| https://opentelemetry.io/docs/concepts/signals/ | 官方文档 | A | observability signals | OpenTelemetry signals、metrics/logs/traces/events | 适合 backend-development/devops-sre-production |
| https://prometheus-docs.netlify.app/docs/practices/alerting/ | 官方文档镜像 | B | alerting | alert 规则、用户影响导向告警、监控系统自监控 | 优先查 prometheus.io 原站；镜像只作备份入口 |
| https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/ | 官方文档 | A | operational excellence | DevOps culture、observability、automation、safe deployment、incident response | 适合 devops-sre-production |
| https://learn.openapis.org/specification/ | 官方学习文档 | A | OpenAPI | OpenAPI Description、paths/responses/securitySchemes/components/examples | 适合 backend-development |
| https://google.aip.dev/ | 官方 API 指南 | A | API design | Google AIP、resource-oriented API design、API rule governance | 适合 backend-development |
| https://opensource.zalando.com/restful-api-guidelines/ | 工程团队指南 | B | API design | RESTful API/event guidelines、一致性、Problem JSON、rate limits | CC-BY 4.0；引用需署名 |
| https://jsonapi.org/format/index.html | 规范站点 | B | API format | JSON:API 1.1、资源请求/响应、扩展和 profile | 适合 backend-development |
| https://www.w3.org/TR/WCAG22/ | W3C 标准 | A | accessibility | WCAG 2.2 成功标准、可访问性合规基线 | 适合 frontend-development/frontend-ui-design |
| https://www.w3.org/WAI/ARIA/apg/ | W3C 指南 | A | accessible widgets | ARIA design patterns、keyboard support、roles/states/properties | 适合 frontend-development/frontend-ui-design |
| https://www.gov.uk/service-manual/technology/accessibility-for-developers-an-introduction | 政府服务手册 | A | frontend accessibility | GOV.UK Design System、WCAG 2.2 AA、辅助技术测试 | 适合 frontend-development/frontend-ui-design |
| https://docs.github.com/en/copilot/concepts/about-customizing-github-copilot-chat-responses | 官方文档 | A | AI coding instructions | repository/path-specific/agent instructions、短自包含规则、优先级 | 适合 software-development-core/技能工程 |
| https://refactoring.guru/design-patterns/catalog | 设计模式目录 | B | GoF design patterns | GoF 23 个经典模式，按 creational/structural/behavioral 分类 | 可总结模式意图，不复制长篇内容 |
| https://sourcemaking.com/design_patterns | 设计模式目录 | B | design patterns | 设计模式、refactoring、UML 入口 | 可作为辅助入口 |
| https://learn.microsoft.com/en-us/azure/architecture/patterns/ | 官方架构中心 | A | cloud design patterns | 云设计模式、问题/权衡/示例结构 | 适合 backend/devops/architecture |
| https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/ | 官方架构中心 | A | architecture styles | N-tier、microservices、event-driven 等架构风格选择 | 适合 software-development-core/backend |
| https://learn.microsoft.com/en-us/azure/architecture/microservices/ | 官方架构中心 | A | microservices | bounded context、数据自治、API gateway、observability、DevOps | 适合 backend-development |
| https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/event-driven | 官方架构中心 | A | event-driven architecture | producer/consumer/channel、pub-sub、eventual consistency、调试/监控挑战 | 适合 backend/devops |
| https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis | 官方架构中心 | A | DDD domain analysis | bounded context、ubiquitous language、domain concern、microservice 切分 | 适合 backend-development |
| https://learn.microsoft.com/en-us/azure/architecture/microservices/model/microservice-boundaries | 官方架构中心 | A | microservice boundaries | bounded context、aggregate/entity/domain service、迭代式边界识别 | 适合 backend-development |
| https://alistair.cockburn.us/hexagonal-architecture | 原始架构文章 | B | hexagonal architecture | ports and adapters、核心应用与外部设备隔离、可测试性 | Web 搜索可访问，PowerShell 检查失败；保留为原始出处 |
| https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html | 官方架构指导 | A | hexagonal architecture | AWS 对 ports/adapters、domain、ports、adapters、依赖反转的解释 | 稳定补充来源 |
| https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html | 官方架构框架 | A | well-architected | AWS 六大支柱：operational excellence/security/reliability/performance/cost/sustainability | 适合 devops-sre-production |
| https://cloud.google.com/architecture/framework | 官方架构框架 | A | well-architected | Google Cloud Well-Architected Framework、可靠性、可扩展性、解耦 | 适合 devops-sre-production |

## 排除规则

- 不明授权 PDF、盗版书籍镜像、复制粘贴书籍内容的仓库不进入技能资料库。
- 论坛内容只进入“术语/痛点/场景”，不单独形成规则。
- GitHub 仓库必须在正式引用前检查 license；license 不清时只记录 URL 和概念，不复制内容。
