# Cloudflare Turnstile / cf_clearance / 5s 盾 - notes

## 摘要

Cloudflare Bot Management 是国际反爬覆盖率最高的厂商。

| 参数/Cookie | 含义 |
|---|---|
| `cf_clearance` | challenge 通过后颁发的长期 cookie（~30 分钟到几小时） |
| `__cf_bm` | 短期会话 cookie（5 分钟） |
| `cf_chl_*` | challenge 状态 cookie |
| `cdata` / `flow` | Turnstile widget 参数 |

**模式**：
- **JS Challenge**（5 秒盾）：跳到 `cdn-cgi/challenge-platform/...` 跑 orchestrate.js → 通过返回 cf_clearance。
- **Managed Challenge**：根据风险动态判断（无感 / Turnstile / 验证码）。
- **Interactive Challenge**：必须真人交互（Turnstile widget 点击）。
- **Turnstile**：替代 reCAPTCHA 的 widget，几乎全无感（基于 PAT）。

## 识别签名

- 拦截页含 `cdn-cgi/challenge-platform/h/.../orchestrate/managed/v1/...`。
- HTML 头 `Server: cloudflare` + `cf-ray: ...`。
- Cookie 含 `cf_clearance` / `__cf_bm`。
- Turnstile widget URL `challenges.cloudflare.com/turnstile/v0/...`。

## 还原方法

**绝大多数场景**走真浏览器：

1. **`undetected-chromedriver`** + Selenium：开 stealth 模式，让 navigator.webdriver = false 等。
2. **`DrissionPage`**：基于 CDP，国内常用。
3. **`puppeteer-real-browser-go`**：r0vx/turnstile 用过的方案。
4. **`curl-impersonate`+`tls-client`**：绕过 TLS 指纹（CF 强校验 JA3/JA4）。
5. **MITM 劫持 challenges.cloudflare.com**：linux.do 上有人做插件，用自己的逆向逻辑替代真 CF（高级用法）。
6. **付费 API**：CapSolver、2captcha、yescaptcha 等用真人池+池化解决。

**纯算还原**目前没有可靠的开源方案——CF 反破解非常勤奋，每周都换混淆。

## raw-hits 来源

- 见 [raw-hits/web-batch1.md Q2](../raw-hits/web-batch1.md)。

## 关键 URL

入门：
- [cloudflare 5s 盾解密 (dairoot 2024-08)](https://dairoot.cn/2024/08/05/cloudflare5s-bypass/)
- [cloudflare 五秒盾突破 (掘金 2023)](https://juejin.cn/post/7238920970563027003)
- [取巧绕过 Cloudflare v2 (林伟源 2023-03)](https://linweiyuan.github.io/2023/03/14/一种取巧的方式绕过-Cloudflare-v2-验证.html)

进阶：
- [Cloudflare Turnstile 验证码插件 (linux.do 2025-10)](https://linux.do/t/topic/1010988) — MITM 劫持
- [Cloudflare 防护与 Turnstile 实战 (CSDN 2025-09)](https://blog.csdn.net/qq_33253945/article/details/152059625)
- [r0vx/turnstile cf-clearance-scraper-go (GitHub)](https://github.com/r0vx/turnstile)

工具：
- [curl-impersonate (lwthiker)](https://github.com/lwthiker/curl-impersonate)
- [tls-client (bogdanfinn)](https://github.com/bogdanfinn/tls-client)
- [undetected-chromedriver (ultrafunkamsterdam)](https://github.com/ultrafunkamsterdam/undetected-chromedriver)

## 工作流建议

1. 先看是 JS Challenge 还是 Managed/Turnstile：访问被 302 到 challenge URL → JS；正常进入但偶尔出 widget → Managed。
2. JS Challenge 用 undetected-chromedriver 几行代码即可。
3. Turnstile 比较麻烦，要么 CDP 真浏览器+真人池，要么付费 API。
4. cf_clearance 与 IP/UA 强绑定，不能跨节点复用。
5. CF 持续更新，2026 年的方案不一定 2027 还能用——保持 CapSolver/yescaptcha 这类付费 API 作为兜底。

## 关键术语

- **orchestrate.js**：CF 的 JS Challenge 主文件，每天换。
- **PAT (Private Access Tokens)**：iOS 16+/Safari 17+ 替代 captcha 的隐私令牌；CF 已支持，配合 Apple/Google 设备无需出现 widget。
