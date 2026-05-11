# 软件开发技能分类与边界

## 结论

第一批保持 8 个技能，不新增一级分类。搜索过程发现的 security、accessibility、observability、testing、AI-friendly codebase 都是横切能力，应该写入相关技能的检查项，而不是单独拆成第一批技能。

## 第一批技能

| 技能 | 边界 | 不包含 |
|---|---|---|
| `software-development-core` | 需求澄清、设计评审、代码质量、重构、调试、测试策略、PR/MR review、交付检查 | 具体前端/后端/桌面框架细节 |
| `backend-development` | API、数据库、缓存、队列、鉴权、并发、可靠性、可观测性、服务端测试 | UI 实现、桌面安装打包 |
| `frontend-development` | React/Vue/TypeScript、状态管理、路由、构建、性能、可访问性、前端测试 | 视觉设计审美规则、后端数据建模 |
| `frontend-ui-design` | Web UI/UX、布局、组件、视觉层级、响应式、表单、仪表盘、设计系统使用 | 框架工程细节、后端 API |
| `desktop-application-development` | 桌面应用架构、配置、文件系统、更新、安装包、系统集成、跨平台发布 | 单个 GUI 控件细节 |
| `desktop-gui-development` | Qt/WPF/WinUI/Electron/Tauri/native GUI 控件、窗口、菜单、快捷键、IPC、事件 | 视觉设计语言 |
| `desktop-gui-design` | 专业桌面软件信息密度、工具栏、属性面板、设置页、工作流设计 | 框架 API、打包发布 |
| `devops-sre-production` | CI/CD、发布、监控、日志、告警、回滚、容量、SLO、事故处理 | 业务功能开发 |

## 横切关注点

- Security：进入 backend、frontend、desktop、devops 的检查项；不独立成第一批技能。
- Accessibility：进入 frontend-development、frontend-ui-design、desktop-gui-design。
- Observability：进入 backend-development、devops-sre-production。
- Testing：software-development-core 负责策略；各技术技能负责落地测试类型。
- AI-friendly codebase：进入 software-development-core，作为代码可读性和上下文密度规则。

## 合并/拆分原则

- 如果技能触发词高度重叠，就合并；如果执行步骤和检查项差异明显，就拆分。
- `frontend-development` 与 `frontend-ui-design` 必须分开：一个偏工程实现，一个偏界面判断。
- `desktop-application-development` 与 `desktop-gui-development` 必须分开：一个偏生命周期/系统集成，一个偏窗口/控件/事件。
- `desktop-gui-development` 与 `desktop-gui-design` 必须分开：一个偏代码实现，一个偏专业软件体验。
