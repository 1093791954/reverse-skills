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
└── ue-reverse/
    ├── SKILL.md
    ├── agents/
    └── references/
```

## 使用方式

把需要的技能目录复制到你的 Codex skills 目录中，或者在 Codex 支持的情况下把本仓库作为本地技能源使用。

每个技能目录里的 `SKILL.md` 是入口文件。`references/` 目录保存更长的参考笔记，实际使用时只需要按任务加载相关文件。

## 说明

本仓库会忽略本地 Codex 配置备份、采集脚本、生成的 manifest 和缓存文件，避免把个人环境残留上传到远端。
