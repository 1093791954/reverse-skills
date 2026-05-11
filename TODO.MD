# TODO: 软件开发技能搜集与整理计划

## 目标

从 GitHub、官方文档、开放教材、公开工程实践资料中搜集软件开发相关知识，整理、合并并沉淀为 Codex 可自动发现和复用的技能。

正式技能目录放在：

```text
C:\Users\GOD\.codex\skills\
```

研究和中间材料目录放在：

```text
D:\tmp\SKILLS\software-development-skill-research\
```

## 第一阶段：技能分类定稿

- [x] 确认第一批技能名称和边界。
- [x] 确认哪些技能需要独立创建，哪些技能只作为参考资料合并进已有技能。
- [x] 避免技能描述过宽，确保每个技能能被 Codex 准确触发。

建议第一批技能：

- [x] `software-development-core`：通用开发流程、代码质量、重构、测试、调试、交付检查。
- [x] `backend-development`：API、数据库、缓存、队列、鉴权、并发、可靠性、部署。
- [x] `frontend-development`：React/Vue/TypeScript、状态管理、路由、构建、性能、测试。
- [x] `frontend-ui-design`：Web UI/UX、布局、组件、视觉层级、响应式、表单、仪表盘。
- [x] `desktop-application-development`：桌面应用架构、配置、更新、安装包、系统集成、跨平台发布。
- [x] `desktop-gui-development`：Qt/WPF/WinUI/Electron/Tauri/native GUI 控件、事件、窗口、菜单、快捷键。
- [x] `desktop-gui-design`：桌面软件信息架构、工具栏、属性面板、设置页、专业软件工作流。
- [x] `devops-sre-production`：CI/CD、发布、监控、日志、告警、回滚、容量、故障处理。

## 第二阶段：GitHub 搜集

- [x] 为每个技能方向列 GitHub 搜索关键词。
- [x] 搜集高质量 repositories、awesome lists、engineering handbooks、style guides、checklists。
- [x] 优先选择有明确 license、长期维护、star/fork/issue 活跃度合理的项目。
- [x] 记录每个来源的 URL、license、适合提炼的内容、是否可直接引用或只能总结。
- [x] 排除不明授权、复制粘贴书籍内容、侵权资料镜像。

候选搜索方向：

- [ ] `software engineering handbook`
- [ ] `backend best practices`
- [ ] `api design guidelines`
- [ ] `frontend checklist`
- [ ] `frontend performance checklist`
- [ ] `ui design system guidelines`
- [ ] `desktop application architecture`
- [ ] `qt application best practices`
- [ ] `electron security checklist`
- [ ] `sre handbook`
- [ ] `production readiness checklist`

## 第三阶段：资料整理

- [x] 在 `software-development-skill-research\sources\` 保存来源索引。
- [x] 在 `software-development-skill-research\notes\` 为每个技能方向整理摘要。
- [x] 将重复内容合并为统一规则，保留冲突点和适用条件。
- [x] 把实践规则写成 Codex 可执行的流程、检查清单和决策准则。
- [x] 避免长篇教程化内容，技能正文保持精简。

建议研究目录：

```text
D:\tmp\SKILLS\software-development-skill-research\
├── sources\
├── notes\
├── drafts\
└── merged\
```

## 第四阶段：创建技能

- [ ] 使用 `skill-creator` 工作流初始化每个技能目录。
- [ ] 每个技能至少包含 `SKILL.md`。
- [ ] 需要细分资料时使用 `references\`，不要把所有内容塞进 `SKILL.md`。
- [ ] 需要稳定复用的脚本时使用 `scripts\`。
- [ ] 使用 `quick_validate.py` 验证技能格式。
- [ ] 确认技能 frontmatter 的 `description` 能准确覆盖触发场景。

## 第五阶段：验证与迭代

- [ ] 为每个技能准备 3-5 个真实任务样例。
- [ ] 使用真实代码仓库或小型样例项目测试技能是否能指导 Codex 完成任务。
- [ ] 记录技能触发不准、内容过长、规则冲突、缺少检查项等问题。
- [ ] 根据测试结果更新 `SKILL.md` 和 `references\`。
- [ ] 完成后提交到当前 Git 仓库。

## 提交与推送

- [ ] 每次只提交一组相关技能或一批清晰的资料整理结果。
- [ ] 提交信息使用 conventional commit，中文摘要。
- [ ] 推送远端时使用代理端口 `7897`：

```powershell
git -c http.proxy=http://127.0.0.1:7897 -c https.proxy=http://127.0.0.1:7897 push origin main
```
