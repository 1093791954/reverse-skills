# 数美 Shumei（fverify / 滑块）

## 1. 产品形态
- 滑块（拼图/缺口）、文字点选、图标点选、空间推理、智能无感。
- 接入：`https://captcha.fengkongcloud.com`、`captcha.fengkongcloud.com/ca/v3/...`。
- 上下游：先 `register` 获取设备指纹 ID，再 `fverify` 提交答案；前端 SDK 名 `shumei.js` / `dfp_*`。

## 2. 检测维度
- **DES 加密**：经典版 fverify 请求体使用 DES（多篇逆向文章证实），key 由 `organization` + `appId` 派生。
- **设备指纹（dfp）**：Canvas/WebGL/Audio/Font/UA-CH/电池/语言/平台/插件 列表 hash 化。
- **轨迹**：`movePath` 二阶差分；零抖动直线必失败。
- **频率**：同一 `organization` + IP 限制每分钟次数。
- **图片缩放校验**：滑块图片有真实像素与显示尺寸两套，缺口位置必须相对真实像素计算。

## 3. 关键端点与字段
| 端点 | 字段 |
|------|------|
| `/ca/v3/register` | `organization`, `appId`, `protocol`, `model`, `os`, `network` |
| `/ca/v3/fverify` | `data`(DES/AES 加密)，包含 `move`, `time`, `slidePath`, `dpr`, `ua`, `riskInfo` |
| `/img/<path>.jpg` | 背景图与滑块图，需配对解决 |

**data 明文**：`{"reg":"<token>","time":<ms>,"path":"<base64 trace>","loc":<x>,"size":{"w":...,"h":...},"ua":"...","sm":{...}}`。

## 4. 已公开研究
- CSDN「数美滑块逆向分析」(137826783)：抓包定位加密位置 + Python 调用。
- CSDN「【逆向】数美滑块逆向解析」(132393267)：DES 识别与 ddddocr 配合。
- CSDN「数美滑块 js 逆向」(124301699)：DES 加密细节。
- CSDN「数美滑块逆向流程」(145869569 ✅ R4 已验证)：图片接口、参数传递、轨迹指纹猜测、环境补全 + JS 内 DES 加解密示例。**R5 替换原 124388541（已撤稿/404）**。
- 多个 GitHub 协议研究项目 `shumei-captcha-research`。

## 5. 防御性分析思路
1. 抓 `/register` 看返回 `organization` 与 token，明确 DES key 派生公式。
2. `data` 解密后先看 schema：哪些字段固定、哪些字段必随机。
3. 缺口 CV：背景图无干扰，模板匹配或 ddddocr `slide_match` 即可，准确率 90%+。
4. 轨迹仿真：录制人类样本 100+ 条 → KDE 采样生成。
5. 看 `riskInfo` 段是否包含 `webdriver`/`dpr`/`outerW` 等检测点。

## 6. 已知缓解 / 更新历史
- 2021 引入 AES-CBC 替换部分 DES 字段。
- 2023 强化 dfp 字段，加入 `WebGL_VENDOR_UNMASKED`/`audioFingerprint`。
- 推出推理题（语义匹配 + 空间）。
- 对 `headless` 环境直接降到无感失败、强制弹滑块。

## 6.5 与同盾 / 黑盒
- 数美与同盾（TongDun）BlackBox 在同一类「行为风控大盒」赛道。同盾 BlackBox 见 CSDN 159074707（WASM AES-GCM/RSA + 时序还原），同样产品形态值得研究对照。

## 7. 待研究问题
- 新版 fverify 是否完全切换到 AES-GCM？
- dfp 在多设备共用账号场景下的稳定性。
- 推理题候选标注是否会暗藏陷阱样本（adversarial）。
