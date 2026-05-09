# Cloudflare Turnstile（含 5s 盾 / Managed Challenge / cf_clearance）

## 1. 产品形态
- **Turnstile widget**：嵌入式无感/可见验证，多用于注册、登录；返回 `cf-turnstile-response` token，服务端 `siteverify` 验证。
- **Managed Challenge**（边缘）：Cloudflare 域名 `/cdn-cgi/challenge-platform/...`，弹出 5s 倒计时（旧称 5s 盾）或直接放行；通过后下发 `cf_clearance` cookie。
- **Bot Fight Mode / Super Bot Fight Mode**：纯被动检测，不弹 UI。
- **WAF + JS Challenge**：和 Turnstile 共用 challenge platform JS。

## 2. 检测维度
- **环境一致性**：UA / UA-CH / TLS JA3-JA4 / HTTP2 SETTINGS / ALPN。
- **指纹**：Canvas、WebGL、AudioContext、Font、Battery、HardwareConcurrency、DeviceMemory、`window.chrome` 完整性、`navigator.permissions.query({name:'notifications'})` 返回值。
- **行为**：Turnstile widget 下方有「不可见」的鼠标 entry、focus、scroll 监听。
- **PoW**：Turnstile 引入 SHA-256 PoW，约 100k iterations，弱 GPU/CPU 设备压力大；从 `chl_opt.cType=managed` 携带难度。
- **session token chain**：`cf_chl_*` cookie 多个，必须按顺序拿。
- **ASN/IP 黑名单**：常见 VPN 段直接降到 captcha。

## 3. 关键端点与字段
| 端点 | 字段 |
|------|------|
| `/cdn-cgi/challenge-platform/h/<g/b>/orchestrate/<chlPagesMgmt|jsch>/v1` | 拉主 JS |
| `/cdn-cgi/challenge-platform/h/.../<random>` | 上报 / 验证 |
| Turnstile `https://challenges.cloudflare.com/turnstile/v0/api.js` | widget 引导 |
| `/turnstile/v0/<sitekey>/...` | challenge 与 token |
| `siteverify`（开发者后端调）| `secret`, `response`, `remoteip` |

**chl_opt**：内嵌 `<script>window._cf_chl_opt={cType:'managed',...,cFPWv:'<wasm hash>',cZone:'<host>'}`。
**cf_clearance**：cookie 形如 `<base64>.<ts>.<hash>`，ttl 默认 30min（业务可调到 30 天）。

## 4. 已公开研究
- CSDN「2025 年如何绕过 Cloudflare 反爬虫挑战」(146931443)。
- CSDN「自动绕过 Cloudflare 验证码 - 两条相反的方法」(137376844)：`undetected-chromedriver` vs `cloudscraper` 比较。
- CSDN「深入理解 Cloudflare Turnstile：工作原理分析与 Python 自动化解决方案」(159429874)。
- CSDN「Cloudflare 5 秒盾逆向实战：13 次请求背后的 Python 补环境框架搭建指南」(97848186)：完整 13 个请求链。
- CSDN「Nstbrowser 指纹浏览器全方位实战指南」(153009820)：指纹浏览器商业方案。
- GitHub `FlareSolverr`：通用反爬代理，公开维护 cf 请求链。
- CapSolver / 2Captcha 文档「Turnstile-Token-Standard」：商业方案接口（合法授权场景）。

## 5. 防御性分析思路
1. challenge JS 名字随时间 rotate，hash 化，每次开启新 session 必须先 GET `/cdn-cgi/challenge-platform/...orchestrate` 取最新 JS。
2. Turnstile widget 内部用 `MessageChannel` 跨 iframe 通信，token 是 `<base64>.<base64>.<base64>` 三段；中间段含 PoW 解。
3. 纯算困难：JS 用 webpack-style 大量 chunk + 字符串数组旋转 + WASM 关键运算，实际研究多走「真浏览器 + stealth」。
4. `cf_clearance` 一旦绑定 IP+UA+JA3，禁止跨节点复用。
5. Turnstile sitekey 公开，`siteverify` 的 idempotency-key 不允许复用同一 token。

## 6. 已知缓解 / 更新历史
- 2022 Turnstile 上线替代 hCaptcha。
- 2023 PoW 加入 + Workers 边缘风控。
- 2024 强化 UA-CH、`Sec-CH-UA-Full-Version-List` 校验。
- 对 `nodriver`、`patchright`、`camoufox` 持续打 patch；camoufox 维护团队也在持续更新。

## 7. 待研究问题
- Turnstile token 中间段 PoW 难度的下发逻辑。
- challenge JS 不同 zone 之间是否复用相同字符串数组。
- Bot Fight Mode 的纯被动评分阈值。
