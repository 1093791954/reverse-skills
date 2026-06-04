# Token 复用与 IP 信誉

## 1. 思路概述
- 多数验证码服务下发的 token 都有「短时窗口可复用」特性：拿到 1 个高分 token，可以在 30s ~ 30min 内重复用于多个业务接口。
- 配合「热账号 + 热 IP + 热指纹」预热策略可以显著提高通过率（reCAPTCHA v3 经典技巧）。
- 各厂商 ttl/单次性策略不同，要逐个量化。

## 2. 各厂商窗口（社区观察，需以授权实测为准）
| 厂商 | token / cookie | 默认 ttl | 是否绑定 IP/UA |
|------|---------------|---------|---------------|
| reCAPTCHA v3 | g-recaptcha-response | ~120s 单次 | 强绑定 |
| reCAPTCHA v2 | g-recaptcha-response | ~120s 单次 | 强绑定 |
| Turnstile | cf-turnstile-response | ~5min | 强 |
| cf_clearance | 30min（业务可调最长 30 天） | 强 | |
| Akamai _abck | 长 ttl，但最关键的第三段会失效 | 中 | |
| DataDome cookie | 1-3 分钟 | 强 | |
| PerimeterX _px3 | 30-60 分钟 | 强 | |
| Kasada x-kpsdk-ct | 单次/极短 | 强 | |
| 极验 v3 challenge | 单次 | 强 | |
| 极验 v4 process_token | 单次 | 强 | |
| hCaptcha h-captcha-response | 120s 单次 | 强 | |

## 3. 热账号预热（reCAPTCHA v3 专属）
- 用一个真浏览器账号 + 住宅 IP + 真实指纹，做日常正常浏览行为（每天浏览 N 个页面、点击、停留），让 Google 累积「可信 cookie」（NID / __Secure-3PSID）。
- 之后用同 cookie + 同 UA + 同 JA3 在受保护页面调用 `grecaptcha.execute()`，分数显著高于 cold 启动。
- 商业打码平台 `RecaptchaV3` 任务背后多是这种热 token 池。

## 4. IP 信誉 API
| 服务 | 用途 |
|------|------|
| IPQualityScore (IPQS) | fraud score，多家厂商参考 |
| IP2Proxy | 数据中心/VPN/Tor/住宅区分 |
| Spur | 住宅代理识别 |
| MaxMind GeoIP2 | 地区/ASN |
| AbuseIPDB | 滥用历史 |
| Cloudflare 自家威胁评分 | 边缘内嵌 |

## 5. 防御性分析步骤
1. 拿一个测试账号，对每个厂商抓 100 次成功 token，记录 (issued_at, used_at, status)。
2. 计算实际 ttl 与可复用次数。
3. 验证 IP 绑定：换 IP 重用同 token，看是否拒绝。
4. 与指纹绑定：换 UA 重用同 token，看是否拒绝。
5. 长期：构建 token 池监控（多账号 × 多 IP），观察各 cell 的可用性曲线。

## 6. 已公开资料
- 各厂商笔记里都有 ttl 段（vendors/*）。
- CapSolver / 2Captcha 文档里多任务类型注释了 "token valid for ..."。
- arxiv「Stale CAPTCHA token reuse attack」类论文。

## 7. 缓解 / 趋势
- 厂商缩短 ttl + 增加单次性。
- 边缘 idempotency-key 校验。
- 多因素打分让单 token 不够。
- IP 信誉 + 指纹 + token 三因素同时考核。

## 8. 待研究
- 各厂商 token 在跨 origin 下的复用规则（CORS）。
- 热账号预热的最优"真人浏览路径"模板。
