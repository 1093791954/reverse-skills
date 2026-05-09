# 第三方打码平台（合规边界与安全研究边界）

## ⚠️ 合法性声明
本文件仅用于「企业内部安全审计、合规性评估、学术研究」。**严禁将打码平台用于商业风控绕过、批量注册、刷单、爬取受保护商业数据等违法违规行为**。本笔记不提供可运行的接入代码，仅梳理协议形态供分析对比。

## 1. 主流平台
| 平台 | 类型 | 覆盖 |
|------|------|------|
| 2Captcha | 商业 | reCAPTCHA, hCaptcha, FunCaptcha, 极验, Turnstile, AWS WAF, DataDome, Kasada |
| Anti-Captcha | 商业 | 类似 2Captcha |
| CapSolver | 商业 | 类似，主打 AI 自动化（ImageToText, ReCaptchaV2/V3, HCaptcha, FunCaptcha, Turnstile, Geetest, AntiAwsWafTask, KasadaCaptchaSolver） |
| YesCaptcha | 商业 | 中国市场为主 |
| Cap-Monster | 商业 | 老牌 |
| NopeCHA | 商业 + 浏览器扩展 | reCAPTCHA, hCaptcha, FunCaptcha |
| EzCaptcha | 商业 | 类似 |
| Death by CAPTCHA | 商业 | 老牌 |
| 超人打码 | 中国 | 简单图片为主 |
| 联众打码 | 中国 | 简单图片为主 |

## 2. 工作模式
- **人工**：把题目传给后台真人识别，几秒~几十秒返回。多用于复杂题（如顶象推理）。
- **AI 自动化**：CapSolver/NopeCHA 用自己训的 ML 模型，平台规模化收题。
- **混合**：AI 优先，识别失败转人工。
- **Token 池**：部分平台维护「热 token」池（提前用真浏览器养好），按需发放（reCAPTCHA v3 专用）。

## 3. 接口形态（参考，非接入指南）
- 同步：单次请求带 sitekey/url/userAgent/cookies/proxy → 等待结果（5-30s）。
- 异步：先 createTask → 再 getTaskResult，轮询。
- 任务类型常见：`RecaptchaV2Task`, `RecaptchaV3TaskProxyless`, `HCaptchaTask`, `FunCaptchaTask`, `GeeTestTask`, `TurnstileTaskProxyless`, `AntiAwsWafTask`, `DataDomeTask`, `KasadaCaptchaSolver`, `ImageToTextTask`。

## 4. 已公开研究
- CSDN「如何自动解决 FunCaptcha | 使用 CapSolver Captcha 扩展」(139301017)。
- CSDN「如何识别 AWS WAF Captcha 亚马逊验证码」与「如何绕过/自动识别 Amazon WAF Captcha」：CapSolver 流程。
- CSDN「FunCaptcha 与其他验证码的技术对比分析」(155192657)：EzCaptcha 对比。
- CSDN「Yandex SmartCaptcha 解锁器」：AI 解 Yandex。
- CSDN「Web3 自动化中的验证挑战：solver 对比」。
- 各平台官方文档（合规时使用）。

## 5. 防御性分析（评估自家站点）
1. 用主流平台测试自家 captcha 通过率：90%+ 表示难度不够；< 30% 才算实用。
2. 关注「打码平台返回 token 后的服务端校验」：token 是否绑定 IP/UA？是否限频？
3. 引入设备指纹 + 行为评分作为多因素，让 captcha token 单独不够用。
4. 对接 IP 信誉 API 屏蔽数据中心 IP。

## 6. 趋势
- AI 自动化平台越来越强，人工成本占比下降。
- 厂商反过来对打码平台流量做指纹聚类（短时大量 sitekey + 不同 cookie 模式）。
- 法规层面：欧盟 GDPR / 中国《网络安全法》对未授权使用日趋严格。

## 7. 待研究
- 如何在自家站点检测打码平台 token（共享 IP 段/cookie 异常/timing 分布）。
- 不同平台对最新版 Turnstile/Kasada 的实测通过率。
