# 网易易盾 NECaptcha（dun.163.com）

## 1. 产品形态
- 普通版滑块、智能无感、文字点选、图标点选、推理、旋转、拼图。
- BlackBox：行为风控 SDK，非验证码本身，但共享同一套环境采集，常一起部署。
- 接入方式：`https://cstaker.dun.163.com`，前端核心 `nc.js`、`NECaptcha.instance`。

## 2. 检测维度
- **cb 参数**：Checkbox token，来自 `https://c.dun.163.com/api/v3/get`，受时间/IP/UA 绑定。
- **fp（fingerprint）**：本地生成长字符串，Canvas/WebGL/Audio/字体/navigator hash 拼接 + AES。
- **acToken**：账号关联 token，滑动前先拿。
- **data**：提交时的大串，含 traceData（鼠标轨迹）、checkTime、滑动距离、环境。DES / AES 交叉加密。
- **轨迹特征**：间隔抖动、dx 二阶差分、y 方向微抖（越直越像机器）。

## 3. 关键端点与字段
| 端点 | 字段 |
|------|------|
| `/api/v3/get` | `cb`, `fp`, `ac`, `cv`, `referer`, `token` |
| `/api/v3/check` | `data`, `cb`, `token` |
| `/api/v2/image`（旧） | `cb`, `id` |
| 背景图: `/vf/...jpg` | 由 server 下发 url |

**data 明文**（整理后）：`{"traceData": "base64轨迹", "checkTime": 毫秒, "slideData": {"movePath":[[x,y,t]...]}, "ac": "...", "env":{...}}`，外层 AES-CBC 用 `cb` 派生 key。

## 4. 已公开研究
- CSDN「网易易盾滑块逆向」(146161519)：4 次请求流程，`cb` webpack 逆向。
- CSDN「逆向百例——网易易盾滑块验证码」(156750700)：`data` 与 `traceData` 轨迹加密还原。
- CSDN「破解网易易盾滑块验证码」(141715981)：Selenium + OpenCV 去黑边 + 模板匹配。
- CSDN「易盾滑块分析」(153614210)：AST 解混淆 webpack chunk。
- CSDN「某网易易盾滑块验证码」(134739665)：`acToken`, `fp`, `cb` 全字段解析，号称 100% 通过率（注意样本小）。
- CSDN「逆向实战：新版同盾 BlackBox 环境补全与指纹对抗解析」(159074707)：BlackBox WASM Token、AES-GCM/RSA、请求载荷解密。

## 5. 防御性分析思路
1. 从 `/v3/get` response 反查 `data` schema；易盾多次请求把 `cb` 旋转一次。
2. webpack chunk 追 `n.exports = function(e){...}` 类入口，`cb` 常在某个 `r.prototype.hash` 里。
3. 缺口 CV：拿背景图灰度 + sobel + 模板匹配，或直接 ddddocr `slide_match`。
4. 把 `traceData` 反编码后按 (x,y,t) 还原，比对人类采集的分布，找差异。
5. 新版 BlackBox 用 WASM 做 AES-GCM，建议用 `wasm-dis` 辅助反汇编，再把 memory layout 打印出来。

## 6. 已知缓解 / 更新历史
- 2022 推智能无感（NECaptcha Inline）。
- 2023 引入 WASM 关键算子，JS 层几乎无可读逻辑。
- 2024 上线旋转版 + 推理题（相似度匹配）。
- 对 `screen.width!=availWidth`, `deviceMemory`, `hardwareConcurrency` 做一致性交叉校验。

## 7. 待研究问题
- 新版 BlackBox WASM 里 RSA 公钥是否随 session 变化？
- `cb` 旋转周期（是否每 300s）。
- 推理题的候选编号编码方式。

## 8. 别名与国际化（R4 补充）

- **NECaptcha**（NetEase Captcha）= 网易易盾验证码的官方英文产品名；JS SDK 入口 `window.NECaptcha`，全局校验字段也叫 `NECaptchaValidate`（有时驼峰写作 `neCaptchaValidate`）。
- 易盾官方 npm 包：`@neteaseyidun/intelligent-form-captcha`、`yidun-captcha-react`（社区维护）。
- 海外站点偶见独立子域 `c.dun.163yun.com`、`necaptcha.nie.netease.com`，与国内 `dun.163.com` 走相同协议。
- 同盾 BlackBox（见 `tongdun-blackbox.md`）与易盾 BlackBox 完全是不同公司不同方案，但在中文圈讨论中常混称为"某盾 blackBox"，定位时务必区分宿主域：
  - `fp.tongdun.net` / `fraudmetrix.cn` → 同盾。
  - `dun.163.com` / `163yun.com` → 易盾。
- 与同盾的混淆来源：双方都把核心采集 SDK 命名为 BlackBox，且都用 RC4/AES 双层 + WASM 路线，但 token 字段名（同盾 `blackBox` vs 易盾 `data`/`fp`）和接口完全不同。

## 9. 待研究问题（追加）
- NECaptcha 国际化（i18n）题面下发与中文是否走同一接口，是否在 `lang=en-US` 时切换不同题库。
- iOS Native SDK 的 BlackBox 字段是否与 Web 等价。
