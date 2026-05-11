# 第 5 轮补强搜索记录

## 目的

在已有分类收敛后，按用户要求再扩充搜索一次。重点补强前一轮较薄弱的横切主题：安全编码、测试策略、架构文档、可观测性、API 规范、可访问性和 AI coding agent 指令。

## MCP 浏览器验证

- GitHub：`OWASP ASVS API Security secure coding practices`
- Google：`OWASP secure coding practices API Security Top 10 ASVS`
- Bing：`architecture decision records C4 model arc42 software architecture documentation`

## 新增高价值来源

| 来源 | 主题 | 价值 |
|---|---|---|
| OWASP Secure Coding Practices | secure coding | 技术无关安全编码 checklist，可转成变更审查安全项 |
| OWASP API Security Top 10 2023 | API security | API 授权、业务流、SSRF、rate limit 等风险词表 |
| OWASP ASVS | application security | 安全控制验证要求，适合做安全测试 checklist |
| CISA Secure by Design | secure by design | 把安全默认值和厂商责任前移到设计阶段 |
| Martin Fowler Practical Test Pyramid | testing strategy | 测试粒度组合、contract test、E2E 成本权衡 |
| Google Testing Blog E2E guidance | testing strategy | E2E 测试脆弱性和维护成本风险 |
| ADR organization / adr-tools | architecture decisions | 决策记录和 decision log 结构 |
| C4 model | architecture diagrams | 系统上下文、容器、组件图层级 |
| arc42 | architecture documentation | 轻量架构文档模板 |
| OpenTelemetry docs | observability | signals、instrumentation、collector、vendor-neutral telemetry |
| Azure Well-Architected Operational Excellence | operations | safe deployment、observability、incident response |
| OpenAPI docs | API design | OAD、securitySchemes、components、examples |
| Google AIP | API design | resource-oriented API design 和规则治理 |
| Zalando RESTful API Guidelines | API design | 一致性 API 规范、CC-BY 4.0 |
| JSON:API | API format | JSON API 请求/响应规范 |
| WCAG 2.2 | accessibility | W3C 可访问性合规基线 |
| ARIA APG | accessible widgets | 常见 widget pattern 和 keyboard support |
| GOV.UK frontend accessibility | accessibility | WCAG 2.2 AA、组件和辅助技术测试 |
| GitHub Copilot custom instructions | AI coding agent | repository/path-specific/agent instructions |

## 分类影响

- 不新增第一批一级技能。
- `api-design`、`testing-strategy`、`secure-coding` 可作为第二批候选技能。
- `design-patterns`、`large-scale-software-architecture` 可作为第二批候选技能；第一批先合并进 `software-development-core` 和 `backend-development`。
- `software-development-core` 需要纳入 ADR/C4/arc42、测试策略、安全默认值和 AI-friendly codebase。
- `backend-development` 需要纳入 OpenAPI、Google AIP、JSON:API、OWASP API Security。
- `frontend-development` 和 `frontend-ui-design` 需要纳入 WCAG 2.2、ARIA APG、GOV.UK accessibility。
- `devops-sre-production` 需要纳入 OpenTelemetry 和 Azure Well-Architected operational excellence。

## 设计模式与大型工程架构追加

事实口径：

- GoF 经典设计模式是 23 个，不是 26 个。
- “26 种设计模式”后续如需使用，建议明确为“GoF 23 个经典模式 + 3 个工程常用扩展模式”。
- 建议的 3 个扩展模式：Repository、Dependency Injection、Unit of Work。

GoF 23 个模式：

- Creational：Factory Method、Abstract Factory、Builder、Prototype、Singleton。
- Structural：Adapter、Bridge、Composite、Decorator、Facade、Flyweight、Proxy。
- Behavioral：Chain of Responsibility、Command、Iterator、Mediator、Memento、Observer、State、Strategy、Template Method、Visitor。

大型工程架构新增关注点：

- Architecture styles：N-tier、microservices、event-driven。
- Domain modeling：DDD、bounded context、ubiquitous language、aggregate、domain event。
- Boundary patterns：hexagonal architecture / ports and adapters。
- Distributed system review：API gateway、service ownership、data autonomy、eventual consistency、observability、deployment independence。
- Well-architected review：operational excellence、security、reliability、performance efficiency、cost optimization、sustainability。

## 审查备注

- Alistair Cockburn 原始 Hexagonal Architecture 页面在 web 搜索中可访问，但 PowerShell `Invoke-WebRequest` 检查失败；保留为原始出处，同时增加 AWS Prescriptive Guidance 作为稳定补充来源。
- GoF 23 个模式以 Refactoring Guru 和 SourceMaking 作为目录入口；正式写技能时不复制其示例代码或长篇解释。
