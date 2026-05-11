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

## 轮次统计

| 轮次 | 目的 | 有效来源 | 新增术语 | 新增分类 | 结论 |
|---:|---|---:|---:|---:|---|
| 0 | 从 TODO 中建立种子词表 | 0 | 38 | 8 | 建立初始分类：core/backend/frontend/frontend-ui/desktop-app/desktop-gui/desktop-gui-design/devops-sre |
| 1 | 宽泛搜索官方 handbook、GitHub、Google/Bing 结果 | 18 | 45 | 0 | 原分类成立，新增 security、accessibility、observability 作为横切关注点 |
| 2 | 深挖 frontend/UI、desktop、SRE、production readiness | 17 | 32 | 0 | 发现 Electron/Tauri 权限与安全边界、Core Web Vitals、SLO/error budget 等关键知识簇 |
| 3 | 技能工程与 broader taxonomy 收敛查询 | 8 | 9 | 0 | 新结果主要是已有主题的命名参考，没有新增一级技能 |
| 4 | 最后一轮 2026/skills/taxonomy 查询 | 6 | 6 | 0 | 连续两轮新增术语少于 10、无新增分类；达到收敛标准 |

## 收敛判断

连续第 3、4 轮均满足：

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
