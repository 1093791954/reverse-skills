# Google reCAPTCHA（v2 / v3 / Enterprise）

## 1. 产品形态
- **v2 "I'm not a robot" checkbox**：出现 3x3 或 4x4 九格图片选择，主题为「traffic lights/crosswalks/buses/...」；有 audio challenge 兜底。
- **v2 Invisible**：无复选框，直接触发打分，低分 fallback 九格图。
- **v3**：纯打分（0.0 ~ 1.0），不弹窗；开发者自行决定阈值。
- **Enterprise**：v3 升级版，支持 reason codes、WAF 集成、mobile SDK。
- 域名：`www.google.com/recaptcha/api2/...`、`www.recaptcha.net`、`www.gstatic.com/recaptcha/releases/<hash>/recaptcha__en.js`。

## 2. 检测维度
- **行为**：鼠标入场/点击抖动、滚轮、触摸压力（mobile）、keystroke 间隔。
- **环境指纹**：Canvas、WebGL、Audio、字体、Timezone、Plugin 列表（Chrome 已废弃但仍检测）、UA-CH。
- **Google session cookie**：`NID`, `HSID`, `SID`, `__Secure-3PSID`（已登录 Google 分数显著更高）。
- **TLS/HTTP2**：Akamai-like JA3/JA4 侧写；HTTP/2 SETTINGS frame 顺序。
- **IP 信誉**：住宅 > 数据中心。
- **历史 token 链**：`c` token 绑定上次 interaction。
- **模型**：CNN 判图 + 行为 LSTM。

## 3. 关键端点与字段
| 端点 | 字段 |
|------|------|
| `api2/anchor` | 初始化，返回 `c`/`k` |
| `api2/reload` | `reason=fi/q/t`, `c`, `k`, `chr`, `vch`, `ct`, `bg`（混淆环境数据） |
| `api2/userverify` | `c`, `response`（答案数组） |
| `api2/payload` | 下图片 |
| Enterprise `enterprise.js` | 增加 `grecaptcha.enterprise.execute()` |

**token**：`03AGdBq...`，外层 base64，内层带 `k`(siteKey)+指纹+分数+ts 的加密结构。

## 4. 已公开研究
- `unicaps-py` (GitHub) 工作流文档。
- 2captcha / anti-captcha / capsolver 公开 API 文档定义了 `userAgent/cookies/c` 接入参数（厂商产品，合法用于授权场景）。
- Arxiv 多篇「Audio CAPTCHA attack using Whisper/Vosk」论文（2022-2024）。
- GitHub `recaptcha-v3-bypass`、`solve-recaptcha`（注意：商业绕过工具不写进脚本）。
- CSDN 多篇 reCAPTCHA v3 评分机制阐述，强调 cookie warming + residential IP 才能 stable 0.7+。

## 5. 防御性分析思路
1. 想评估自家站点 reCAPTCHA v3 策略：对同一 siteKey 用多账号 + 不同指纹浏览器产生 token，服务端解 token `assessment` 看 reason codes。
2. 九格图数据集公开（`captcha-dataset/recaptcha`）可训练 YOLO/CLIP 识别。
3. 音频挑战：Whisper-large → 英文数字，公开数据集准确率 >95%。
4. `bg` 字段：RC4-like + base64，看 anchor.html 下发的 key。

## 6. 已知缓解 / 更新历史
- 2018 v3 上线，彻底放弃交互。
- 2020 Enterprise 上线。
- 2023 对 Whisper 检测：加入背景噪音、变速、双人对话干扰。
- Chromium 内置 `chrome://badges`（UMA） 与 reCAPTCHA 交叉。
- 2024 对 `HeadlessChrome` UA、`navigator.plugins.length==0` 等一律 0.1 分以下。

## 7. 待研究问题
- Enterprise reason codes 完整 enum？
- 音频挑战 2024 版对 Whisper-v3 的鲁棒性？
- `c` token 在 30min 内重复使用的次数上限？
