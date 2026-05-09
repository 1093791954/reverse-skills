# Yandex SmartCaptcha

## 1. 产品形态
- Yandex Cloud 旗下人机验证，2021 上线，主推俄罗斯/独联体市场，部分国际客户。
- 题型：经典滑块、点选图标、PoW 无感、旋转拖动。集成域：`smartcaptcha.yandexcloud.net`。
- 与 Yandex 主域账号体系联动；passport.yandex 注册时强制使用。
- 客户端 JS：`https://smartcaptcha.yandexcloud.net/captcha.js`，token 字段名 `smart-token`。

## 2. 检测维度
- **指纹**：Canvas/WebGL/Audio/Font，UA-CH 检查；俄区会强校验时区与语言（ru-RU / en-US 影响题目）。
- **行为**：滑块/点选轨迹完整记录，差分 + 修改版 base64 进 token。
- **PoW**：SHA-256 难度位前导 0；不同 sitekey 难度不同。
- **多重路径**：`get` 拉题 → `check` 提交 → `validate` 通行。
- **图像题**：俄文 OCR 居多，PaddleOCR + ddddocr-Cyrillic 套；旋转题用回归网络。

## 3. 关键端点与字段
| 端点 | 用途 | 关键字段 |
|------|------|---------|
| `smartcaptcha.yandexcloud.net/captcha.js` | SDK | sitekey 注入 |
| `/get-captcha` | 拉题 | `sitekey`, `cdata`, `gid`, `device_info` |
| `/check-captcha` | 提交 | `solution`, `track`(轨迹), `pow`, `token` |
| `/validate` | 服务端二次校验 | `secret`, `token`, `ip` |
| Header `Sec-CH-UA-*` | 客户端品牌 | 必须真实 |

## 4. 已公开研究
- CSDN「验证码逆向之 yandexcloud-smartcaptcha」(144747267)：完整流程示例。
- CSDN「Yandex SmartCaptcha 解锁器」(150271159)：商业 solver 接入说明。
- CSDN「Yandex 复杂还原验证码识别」(155946668)。
- CSDN「某 yandex 图标点选验证码逆向（RPC 通信加密）」(142468295)：RPC + 加密方案。
- CSDN「yandex 不定长旋转验证码 PPOCR 识别案例」(140931877)：旋转题的 PaddleOCR 方案。
- 2Captcha / CapSolver 任务类型：`YandexSmartCaptchaTaskProxyless`，按答案计费。

## 5. 防御性分析思路（授权审计）
1. 用 mitmproxy 抓 `get-captcha` → `check-captcha` 全链。
2. 找 captcha.js 的 webpack root，定位 SHA-256 PoW 入口；难度位通常在 `cdata` 字段返回。
3. 滑块缺口：背景多带噪和切片，灰度+Canny+模板匹配仍可，但需 sigma 调到 1.5-2。
4. 点选图标：CLIP / Gemini Vision 直接出坐标；俄文文字题需 PaddleOCR-Cyrillic 模型。
5. 旋转题：回归网络（EfficientNet-B0 / ResNet-18）训练角度回归即可，0-360 → 双 sin/cos 输出。
6. token 复用：5-15 min；俄区 IP 通过率显著高，海外 IP 题目变难。

## 6. 已知缓解 / 更新历史
- 2022 加旋转题型。
- 2023 PoW 难度位提升至 22-26。
- 2024 风控引入 device_info（包含 GPU 型号），UA 与 GPU 不匹配（如 mac UA + intel GPU）会评分低。
- 2025 检测 Permissions API 状态序列。

## 7. 待研究问题
- `track` 字段轨迹差分编码细节。
- `device_info` 完整字段表与权重。
- 是否存在与 Yandex Passport 联动的 trust score 复用机制。
