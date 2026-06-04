# Reverse Skills

## 交流

QQ群：`1005370499`

群名：`AP1中转站交流`

加群链接：[点击链接加入群聊【AP1中转站交流】](https://qm.qq.com/q/w1ZV6oBr44)

这是一个 Codex 技能仓库，用来沉淀逆向工程研究相关的工作流、参考资料和任务入口。

当前目录已经按主题做了第一轮归类，避免技能目录散落在仓库根目录。

## 分类目录

| 分类目录 | 说明 |
| --- | --- |
| `cybersecurity-skill-hub/` | 网络安全、逆向、风控、样本分析、Web 参数还原等技能。 |
| `development-skill-hub/` | 后端、DevOps、通用软件开发等工程技能。 |
| `ui-desktop-skill-hub/` | 前端、桌面应用、GUI 设计与开发相关技能。 |
| `research-skill-hub/` | 资料检索、政策文档等研究辅助技能。 |

根目录当前主要保留两类内容：

- 安全研究工具或外部仓库，例如 `x64dbg`、`ImHex`、`capa`、`webcrack`
- 仓库配置与辅助目录，例如 `.claude`、`.playwright-mcp`

## 网络安全技能

| 技能 | 用途 |
| --- | --- |
| `cybersecurity-skill-hub/imgui-reverse` | 面向 Windows 游戏逆向覆盖层的 Dear ImGui 工作流，包含外部窗口、DX11 Hook 渲染、消息转发、字体中文支持和常用控件。 |
| `cybersecurity-skill-hub/ue-reverse` | Unreal Engine 逆向工作流，覆盖源码环境准备、`GName` / `FName`、`UObject`、`FUObjectArray`、`UWorld`、Actor 遍历、世界坐标转屏幕坐标、骨骼绘制、IoStore 和反射元数据。 |
| `cybersecurity-skill-hub/packed-sample-analysis` | 合法授权场景下的加壳样本与保护二进制分析流程，重点是静态初筛、运行观察、Dump 校验和安全报告边界。 |
| `cybersecurity-skill-hub/vmp-unpack-analysis` | 合法授权场景下的 VMP/VMProtect 保护样本分析流程，覆盖保护分类、OEP/Dump 校验、VM 边界识别、handler/状态建模和报告交付。 |
| `cybersecurity-skill-hub/riskcontrol-analysis` | 合法授权场景下的移动 App / iOS / Web / H5 / 小程序 / PC 浏览器风控、反爬、设备指纹、加密参数还原与人机验证对抗的通用工作流。 |
| `cybersecurity-skill-hub/captcha-bypass-analysis` | 验证码类型、厂商、自动化、轨迹、指纹绕过等分析工作流。 |
| `cybersecurity-skill-hub/freeai-reverse-proxy` | 合法授权场景下把免费 LLM 聊天网站包装成 OpenAI 兼容反向代理的工作流。 |
| `cybersecurity-skill-hub/jshook-skill` | JavaScript 逆向自动化工具技能，以 submodule 方式引用独立仓库。 |
| `cybersecurity-skill-hub/reverse-skill` | Web JS 逆向分析技能集合，以 submodule 方式引用独立仓库。 |

## 目录结构

```text
.
├── cybersecurity-skill-hub/
│   ├── captcha-bypass-analysis/
│   ├── imgui-reverse/
│   ├── jshook-skill/      # submodule
│   ├── reverse-skill/     # submodule
│   ├── riskcontrol-analysis/
│   ├── ue-reverse/
│   └── vmp-unpack-analysis/
├── development-skill-hub/
│   ├── backend-development/
│   ├── devops-sre-production/
│   └── software-development-core/
├── ui-desktop-skill-hub/
│   ├── frontend-development/
│   ├── frontend-ui-design/
│   └── desktop-gui-development/
├── research-skill-hub/
│   └── china-official-documents/
└── x64dbg/                # tool repository
```

## 使用方式

把需要的技能目录复制到你的 Codex skills 目录中，或者在 Codex 支持的情况下把本仓库作为本地技能源使用。

每个技能目录里的 `SKILL.md` 是入口文件。`references/` 目录保存更长的参考笔记，实际使用时只需要按任务加载相关文件。

包含 submodule 的完整克隆方式：

```bash
git clone --recurse-submodules <repo-url>
```

## 说明

本仓库会忽略本地 Codex 配置备份、采集脚本、生成的 manifest 和缓存文件，避免把个人环境残留上传到远端。
