# 第一批软件开发技能验证样例

## `software-development-core`

- 规划一个跨模块重构，要求拆分迁移、行为变更、测试和回滚步骤。
- Review 一个 PR，判断测试覆盖、架构边界、安全风险和发布风险。
- 为一个重要架构决策写 ADR，并说明备选方案和后果。

## `backend-development`

- 为现有服务新增分页查询 API，要求兼容旧客户端并补 OpenAPI schema。
- 设计一个异步任务处理流程，要求幂等、重试、死信和可观测性。
- Review 一个数据库 migration，判断锁、回滚、前后兼容和部署顺序。

## `frontend-development`

- 修复一个 React/Vue 表单流程，要求区分 server state、form state 和 UI state。
- 优化一个列表页面的 LCP/INP/CLS，并设计性能验证方法。
- 为自定义 combobox 或 dialog 增加键盘和 ARIA 行为测试。

## `frontend-ui-design`

- 改造一个后台 dashboard，使其更适合扫描、筛选、比较和重复操作。
- 设计一个复杂表单，覆盖 label、helper、placeholder、error、loading 和 submit 状态。
- 审查一个页面是否存在过度 hero、装饰性卡片、信息层级不清和响应式问题。

## `desktop-application-development`

- 设计桌面应用的安装、自动更新、签名校验和失败回滚策略。
- 规划本地数据目录，区分配置、缓存、日志、用户文件和密钥。
- 为跨平台桌面应用列出 Windows/macOS/Linux 的路径、菜单、通知和权限差异。

## `desktop-gui-development`

- 为 Electron/Tauri 应用设计 IPC API，要求最小权限、sender 校验和 payload validation。
- 实现桌面应用菜单、工具栏、快捷键和 command palette 的统一命令模型。
- 修复多窗口状态同步和关闭窗口时未保存更改的处理逻辑。

## `desktop-gui-design`

- 设计专业工具类软件的多面板工作区、属性面板、状态栏和工具栏。
- 优化设置页，把长表单改为按任务分组的设置结构。
- 审查桌面软件的键盘流、焦点状态、选择状态和长任务反馈。

## `devops-sre-production`

- 为一个服务准备 production readiness checklist 和发布前检查。
- 设计 SLI/SLO、error budget、burn-rate alert 和 dashboard。
- 编写事故 runbook 和 postmortem 模板，覆盖诊断、缓解、回滚、升级和 action items。
