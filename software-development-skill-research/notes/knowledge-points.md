# 软件开发技能知识点整理

## `software-development-core`

- 代码审查要覆盖 correctness、maintainability、security、testability、readability，而不是只看样式。
- 变更应尽量小而完整；大改动先拆设计、迁移、行为变更和清理步骤。
- Review comment 要区分 blocker、suggestion、nit，减少无谓阻塞。
- 设计前先确认目标、非目标、约束、回滚路径和验收标准。
- 测试策略先按风险选层级：unit、integration、contract、E2E、manual exploratory。
- 交付前检查：diff 范围、测试结果、文档影响、迁移/兼容、配置、监控/回滚。

## `backend-development`

- API 设计优先保证一致性、可演进性、错误格式稳定、分页/过滤/排序明确。
- 鉴权和授权分开处理；记录谁能做什么，而不是只检查是否登录。
- 数据库 migration 要考虑前后兼容、回滚、长事务、锁、批量变更。
- 缓存必须记录失效策略、数据一致性预期和 fallback。
- 队列/异步任务必须处理幂等、重试、死信、顺序和可观测性。
- 服务上线前必须有 health/readiness、结构化日志、关键指标、错误追踪和容量假设。

## `frontend-development`

- 性能要围绕用户体验指标：LCP、INP、CLS，并以真实用户或 75 分位为主。
- 前端状态要分清 server state、client UI state、URL state、form state。
- 可访问性是工程约束：语义 HTML、键盘可达、focus、aria、对比度。
- 性能优化优先检查 bundle、渲染阻塞资源、图片/字体、hydration、长任务。
- 测试组合：组件测试覆盖状态，E2E 覆盖关键流程，视觉回归覆盖布局。

## `frontend-ui-design`

- 设计系统至少要有颜色、语义色、字号、间距、组件状态、使用/禁用规则。
- 表单设计要分离 label、placeholder、helper、error，避免把说明塞进输入框。
- 所有交互组件必须有 hover/focus/active/disabled/loading/error/empty 状态。
- dashboard 和后台工具优先信息密度、扫描效率和重复操作效率，而不是营销式 hero。
- 破坏性操作要确认；高置信成功操作可以 optimistic update，但必须能回滚或 reconcile。

## `desktop-application-development`

- 桌面应用需要处理安装、更新、签名、配置、日志、崩溃报告、文件关联和权限。
- 平台差异要显式记录：Windows/macOS/Linux 的菜单、快捷键、路径、通知、权限不同。
- 本地数据要区分配置、缓存、用户文件、密钥；密钥优先使用 OS keyring。
- 自动更新必须考虑签名校验、失败回滚、用户中断和版本兼容。
- 选择 Electron/Tauri/Qt/WPF/WinUI 时，要记录运行时体积、安全边界、原生能力和团队技能。

## `desktop-gui-development`

- Electron 必须默认禁用远程内容 Node integration，开启 context isolation 和 sandbox，限制导航/新窗口/外部链接。
- Tauri v2 权限要用 capabilities 精确授予窗口和 webview；避免把所有权限放进默认窗口。
- Qt/QML 应分离 UI 状态、业务逻辑和平台集成，避免把复杂逻辑写死在视图层。
- 桌面 GUI 需要稳定处理窗口生命周期、焦点、快捷键、菜单、系统托盘、多窗口状态同步。
- IPC 必须校验 sender/origin，暴露最小 API surface，避免把系统能力直接给 webview。

## `desktop-gui-design`

- 桌面专业软件优先清晰工作区：导航、内容区、属性面板、状态栏、工具栏职责分明。
- 高级工具应支持快捷键、菜单、右键菜单、批量选择、撤销/重做、可恢复操作。
- 设置页应按任务分组，避免把全部选项堆成长表单。
- 视觉密度要适合长时间工作：字号、间距、对比度、选中态和焦点态要稳定。
- 多窗口/面板软件要明确当前上下文，避免用户不知道操作作用于哪个对象。

## `devops-sre-production`

- SLO 必须来自用户可感知的行为，不能只看服务器内部成功率。
- Error budget 用于平衡发布速度和可靠性，不是单纯的 uptime 报表。
- Burn-rate alert 比单点阈值更适合 SLO 消耗速度告警。
- Runbook 要写清触发条件、诊断入口、缓解步骤、回滚步骤、升级路径和验证方式。
- Postmortem 要 blameless，记录 timeline、影响、根因、检测缺口、修复项和 owner。
- Production readiness 要覆盖监控、日志、容量、备份恢复、依赖、降级、回滚、安全和 on-call。
