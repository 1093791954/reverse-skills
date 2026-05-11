# 软件开发技能资料搜集总结

## 结果

已完成第一阶段公开资料搜集和收敛判断。最终保留 8 个一级技能方向：

1. `software-development-core`
2. `backend-development`
3. `frontend-development`
4. `frontend-ui-design`
5. `desktop-application-development`
6. `desktop-gui-development`
7. `desktop-gui-design`
8. `devops-sre-production`

横切主题 security、accessibility、observability、testing、AI-friendly codebase 不单独作为第一批技能，而是进入相关技能的检查项。

## 关键发现

- 软件开发通用技能应以“流程和风险控制”为主：需求、设计、review、测试、交付。
- 后端技能应围绕 API contract、数据演进、异步可靠性、鉴权授权和可观测性。
- 前端工程技能应把 Core Web Vitals、可访问性、状态边界和测试组合写成硬性检查。
- UI 设计技能应聚焦设计系统、组件状态、表单、信息层级和响应式，而不是泛泛审美建议。
- 桌面应用需要拆成工程、GUI 实现和 GUI 设计三类，否则安装更新、IPC 安全、窗口控件、专业软件体验会混在一起。
- SRE 技能必须围绕 SLO/error budget、burn-rate alert、runbook、incident response、postmortem 和 production readiness。

## 收敛状态

搜索循环共 5 轮：

- 第 0 轮建立种子分类。
- 第 1 轮找到官方 handbook、GitHub curated list、API/design/review 资料。
- 第 2 轮深挖前端、UI、桌面、SRE。
- 第 3 轮扩展到技能工程和架构资料，未新增一级分类。
- 第 4 轮搜索 2026 skill taxonomy 和 Codex skills 资料，仍未新增一级分类。

按人工归纳口径，连续两轮新增术语少于 10 且无新增分类，达到停止标准。这个判断用于停止泛搜；创建具体技能前仍应按技能方向做定向补搜和来源复核。

## 审查备注

- 2026-05-11 复查 `sources/index.md` 中全部 URL，均返回 HTTP 200。
- GitHub 仓库 license 已用 GitHub API 抽查：MIT、Apache-2.0、CC0、Other、未返回 license 都已在来源索引中标注。
- `search-log.md` 中的新增来源/术语数量是人工归纳计数，不是脚本去重的精确审计数字。

## 下一步

- 使用 `skill-creator` 初始化 8 个技能目录。
- 每个技能先写短 `SKILL.md`，必要时增加 `references/`。
- 先创建 `software-development-core`，因为它会为其他技能提供通用执行框架。
- 第二批再考虑拆出专项技能：`api-design`、`testing-strategy`、`electron-security`、`sre-incident-response`、`design-system-governance`。
