# 搜索循环日志

## 搜索入口

- MCP 浏览器验证：
  - Google：`software development engineering handbook best practices GitHub`
  - Bing：`software development engineering handbook best practices GitHub`
  - GitHub：`production readiness checklist SRE`
- Web 搜索查询：
  - `software engineering handbook GitHub best practices open source`
  - `site:github.com engineering handbook software development best practices`
  - `Google Engineering Practices documentation code review testing official`
  - `Microsoft REST API Guidelines GitHub official`
  - `backend development best practices API database caching queue reliability GitHub`
  - `frontend checklist GitHub performance accessibility testing best practices`
  - `UI design system guidelines GitHub design system best practices`
  - `desktop application architecture best practices GitHub Electron Tauri Qt WPF`
  - `SRE handbook production readiness checklist Google SRE book official GitHub`

## 轮次统计口径

下表是研究过程中的人工归纳计数，不是由脚本精确去重生成的审计数字。它只用于判断是否继续扩展搜索；正式创建技能时，应以 `sources/index.md` 中逐条验证过的来源为准。

## 轮次统计

| 轮次 | 目的 | 有效来源 | 新增术语 | 新增分类 | 结论 |
|---:|---|---:|---:|---:|---|
| 0 | 从 TODO 中建立种子词表 | 约 0 | 约 38 | 8 | 建立初始分类：core/backend/frontend/frontend-ui/desktop-app/desktop-gui/desktop-gui-design/devops-sre |
| 1 | 宽泛搜索官方 handbook、GitHub、Google/Bing 结果 | 约 18 | 约 45 | 0 | 原分类成立，新增 security、accessibility、observability 作为横切关注点 |
| 2 | 深挖 frontend/UI、desktop、SRE、production readiness | 约 17 | 约 32 | 0 | 发现 Electron/Tauri 权限与安全边界、Core Web Vitals、SLO/error budget 等关键知识簇 |
| 3 | 技能工程与 broader taxonomy 收敛查询 | 约 8 | 约 9 | 0 | 新结果主要是已有主题的命名参考，没有新增一级技能 |
| 4 | 最后一轮 2026/skills/taxonomy 查询 | 约 6 | 约 6 | 0 | 连续两轮新增术语少于 10、无新增分类；达到收敛标准 |

## 收敛判断

按人工归纳口径，连续第 3、4 轮均满足：

- 新增有效来源低于第 2 轮的 20%-50% 区间，且大多是已有主题的同义入口。
- 新增术语少于 10 个。
- 没有新增一级技能分类。

因此停止继续泛搜，进入资料合并和技能草案阶段。

## 后续可定向补搜

- 当创建具体技能时，再按技能补搜框架级资料：
  - `backend-development`：OpenAPI、OAuth/OIDC、PostgreSQL、Redis、Kafka、gRPC。
  - `frontend-development`：React、Vue、TypeScript、Vite、Playwright、Testing Library。
  - `desktop-gui-development`：Qt/QML、WPF/WinUI、Electron/Tauri IPC、installer/update/signing。
  - `devops-sre-production`：Prometheus、OpenTelemetry、Kubernetes、GitHub Actions、Argo CD。

## 第 5 轮：定向补强

用户要求再次扩充搜索，因此在已收敛分类基础上补强横切领域。该轮不是重新打开无限泛搜，而是覆盖前一轮资料相对薄弱的主题。

MCP 浏览器验证：

- GitHub：`OWASP ASVS API Security secure coding practices`
- Google：`OWASP secure coding practices API Security Top 10 ASVS`
- Bing：`architecture decision records C4 model arc42 software architecture documentation`

Web 搜索查询：

- `OWASP secure coding practices checklist official developer guide`
- `OWASP API Security Top 10 official 2023 API development checklist`
- `Architecture Decision Records official GitHub adr-tools Michael Nygard`
- `OpenTelemetry official documentation observability logs metrics traces`
- `OpenAPI specification official documentation API design`
- `WCAG 2.2 official W3C accessibility guidelines`
- `GitHub Copilot coding agent best practices repository instructions official`

新增知识簇：

- 安全编码：OWASP SCP、OWASP API Security Top 10、ASVS、CISA Secure by Design。
- 测试策略：Practical Test Pyramid、Google Testing Blog、Microsoft unit testing guidance。
- 架构文档：ADR、C4、arc42。
- 可观测性：OpenTelemetry signals、Azure Well-Architected operational excellence、Prometheus alerting。
- API 设计：OpenAPI、Google AIP、Zalando RESTful API Guidelines、JSON:API。
- 可访问性：WCAG 2.2、ARIA APG、GOV.UK accessibility guidance。
- AI 友好代码库：GitHub Copilot repository/path-specific/agent instructions。

## 第 5 轮追加：设计模式与大型工程架构

用户补充“26 种设计模式、大型工程软件设计架构”。审查后采用保守口径：GoF 经典设计模式是 23 个；若后续需要“26 种”，应写成“23 个 GoF 模式 + 3 个工程常用扩展模式”，并明确扩展模式不是 GoF 原始目录。

追加查询：

- `Gang of Four design patterns 23 official list creational structural behavioral`
- `Refactoring Guru design patterns catalog creational structural behavioral`
- `Microsoft cloud design patterns official architecture center`
- `Microsoft Azure Architecture Center architecture styles official microservices event-driven layered CQRS`
- `Google Cloud architecture framework official system design reliability scalability`
- `AWS Well-Architected Framework official software architecture reliability operational excellence`
- `domain driven design bounded context official Microsoft microservices architecture guide`
- `hexagonal architecture ports and adapters official Alistair Cockburn`

新增知识簇：

- GoF 设计模式：creational/structural/behavioral 三类，共 23 个经典模式。
- 工程扩展模式候选：Repository、Dependency Injection、Unit of Work。它们可作为“常用架构/实现模式”，不应混称为 GoF。
- 大型工程架构：N-tier、microservices、event-driven、domain-driven design、bounded context、hexagonal/ports-adapters、well-architected pillars。
