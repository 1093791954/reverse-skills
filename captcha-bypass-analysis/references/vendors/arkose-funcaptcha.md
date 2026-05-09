# Arkose Labs FunCaptcha

## 1. 产品形态
- "MatchKey" 系列交互题：3D 物体旋转（roller/rotation）、相同物体匹配（select）、立方体方向、动物方向、卡车方向、骰子点数、迷宫等数十种。
- 触发场景：Twitter/X、OpenAI、LinkedIn、Roblox、Microsoft 注册、Outlook 风控。
- 域名：`arkoselabs.com`、`client-api.arkoselabs.com`、`<sitekey>-api.arkoselabs.com`。
- 核心 JS：`api.js`、`enforcement.fcc...js`（强混淆）。

## 2. 检测维度
- **bda（Browser Data）**：环境指纹大字符串，AES-CBC + base64，关键字段含 Canvas/WebGL/Audio/UA/语言/时区/字体/插件/`navigator` 全集。
- **行为埋点**：`fc-game` 容器内的鼠标移动/点击/拖拽时间序列，`game_token` 一一对应。
- **TLS / HTTP2**：检测 JA3 与 UA 一致性。
- **answer encoding**：`r=<game_token>&...&guess=<base64 encoded answer>`，guess 是按题型变化的小 JSON。
- **suppressed**：风控通过时直接给 `solved_at_load_time:true`。

## 3. 关键端点与字段
| 端点 | 字段 |
|------|------|
| `<sitekey>-api.arkoselabs.com/v2/<surl>/api.js` | 引导 |
| `client-api.arkoselabs.com/fc/gt2/public_key/<key>` | POST `bda`, `public_key`, `site`, `userbrowser`, `capi_version` → 返回 `token`, `r`, `meta`, `region` |
| `/fc/gfct/` | 拿题面、图序号 |
| `/fc/ca/` | 提交答案 `guess`, `analytics_tier`, `r` |
| `/fc/a/` | 二次校验 |
| `/fc/gc/` | 流量统计 |

**bda 解码后**结构是数组，每项 `{key, value}`，value 多为 hash。常见 key：`f`（fingerprint），`n`(nonce ts)，`wh`(window hash)，`enhanced_fp`(子数组), `fe`(feature list), `ife_hash`。

## 4. 已公开研究
- CSDN 多篇 FunCaptcha sitekey 定位与 capsolver 调用（130971860、139301017、155098149、131481879）。
- GitHub `noahcoolboy/funcaptcha-challenger`：题型分类 + ONNX 模型。
- arxiv「3D Rotation CAPTCHA Solving」论文，旋转题目用 ResNet-18 回归角度。
- Twitter API 注册逆向圈的多篇博文（Mozilla/Cloudflare 相关 CDN 的 FCC 解密）。
- Bypass tooling：`@fcsolver`, `funcaptcha-solver` Node 包（参考结构，不直接接入）。

## 5. 防御性分析思路
1. `enforcement.fcc...js` 混淆：是 jscrambler + 字符串加密 + 控制流平坦化。先用 `babel-plugin-deobfuscate-jscrambler`，再 hand-trace `bda` 的拼装。
2. AES key 派生：基于 `userbrowser`（UA 字符串本身）做 PBKDF2-like，看 `enforcement` 内 `key=...` 的赋值点。
3. 旋转题答案是从 0 到 game_data.length-1 的整数 index，对模型来说是分类问题。
4. 立方体方向：6 类分类（front/back/left/right/top/bottom）。
5. `analytics_tier` 决定提交粒度，企业版会要求多次行为采样。

## 6. 已知缓解 / 更新历史
- 2020 收购后并入 OKTA，加大企业部署。
- 2022 起强化 `enhanced_fp`，加入 GPU 渲染时序、字体宽度数组。
- 2023 题型扩到 50+；引入相似度匹配（select 题）。
- 对 headless Chromium 的 `navigator.webdriver` / `Permissions API` 一致性强校验。

## 7. 待研究问题
- `region` 字段对题目难度的影响？
- 多次失败后题型升级序列。
- 3D 题图是否有 watermarking 反训练？
