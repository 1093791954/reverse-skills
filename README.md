# Reverse Skills

## 交流

QQ群：`1005370499`

群名：`AP1中转站交流`

加群链接：[点击链接加入群聊【AP1中转站交流】](https://qm.qq.com/q/w1ZV6oBr44)

这是一个 Codex 技能仓库，用来沉淀逆向工程研究相关的工作流、参考资料和任务入口。

## 技能列表

| 技能 | 用途 |
| --- | --- |
| `imgui-reverse` | 面向 Windows 游戏逆向覆盖层的 Dear ImGui 工作流，包含外部窗口、DX11 Hook 渲染、消息转发、字体中文支持和常用控件。 |
| `ue-reverse` | Unreal Engine 逆向工作流，覆盖源码环境准备、`GName` / `FName`、`UObject`、`FUObjectArray`、`UWorld`、Actor 遍历、世界坐标转屏幕坐标、骨骼绘制、IoStore 和反射元数据。 |
| `packed-sample-analysis` | 合法授权场景下的加壳样本与保护二进制分析流程，重点是静态初筛、运行观察、Dump 校验和安全报告边界。 |
| `vmp-unpack-analysis` | 合法授权场景下的 VMP/VMProtect 保护样本分析流程，覆盖保护分类、OEP/Dump 校验、VM 边界识别、handler/状态建模和报告交付。 |
| `riskcontrol-analysis` | 合法授权场景下的移动 App / iOS / Web / H5 / 小程序 / PC 浏览器风控、反爬、设备指纹、加密参数还原与人机验证对抗的通用工作流（覆盖字节/阿里/美团/京东/拼多多/B站/快手/知乎/网易云/小红书/微信 mmtls/QQ wtlogin 等大站参数 + Akamai/CF/PX/DataDome/Kasada/Imperva/瑞数/极验/网易盾/数美/顶象/同盾 等反爬厂商 + JA3/JA4/Canvas/WebGL 指纹 + Frida/Magisk/unidbg/OLLVM/SSL Pinning 工具链 + Play Integrity/TEE Key Attestation/AVB/PAC/SEP）。 |
| `jshook-skill` | JavaScript 逆向自动化工具技能，以 submodule 方式引用独立仓库。 |
| `reverse-skill` | Web JS 逆向分析技能集合，以 submodule 方式引用独立仓库。 |

## 目录结构

```text
.
├── imgui-reverse/
│   ├── SKILL.md
│   ├── agents/
│   └── references/
├── packed-sample-analysis/
│   ├── SKILL.md
│   └── references/
├── ue-reverse/
    ├── SKILL.md
    ├── agents/
    └── references/
├── vmp-unpack-analysis/
│   ├── SKILL.md
│   ├── agents/
│   └── references/
├── jshook-skill/          # submodule
└── reverse-skill/         # submodule
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
