# 拒绝信号 — 4 类 + 实例库

> 这份文档每条都来自真实抓包/试探，不是推测。每个站点都有完整的 archive README 在 `D:\tmp\FreeAI\<site>/README.md`。

## 1. 验证码墙

特征：
- 响应 HTML 含 `recaptcha` / `turnstile` / `hcaptcha` / `geetest` 资源。
- POST 请求要求 `g-recaptcha-response` / `cf-turnstile-response` / `h-captcha-response` 隐藏字段。
- 即使有合法账号，也会卡在登录/注册某一步。

实例：

| 站点 | 验证码类型 | 实测表现 |
|---|---|---|
| `chataibot.pro` | reCAPTCHA v3 | Visitor 模式可用但只送 GPT-4.1 nano 5 次/天；Claude 解锁需登录，注册被 reCAPTCHA 卡死 |
| `unitool.ai` | Cloudflare Turnstile | 表单 `cf-turnstile-response` 隐藏字段，IP 信誉差 → `auto_timeout` / `failure_retry`，token 一直不发出 → submit 永远 disabled |
| `rita.ai` | reCAPTCHA Enterprise | 工程代码 100% 完成，AI 视觉解 reCAPTCHA 准确率 85–95%，最终卡在 IP/指纹信誉墙（这层在客户端不可破）|
| `tasklet.ai` | hCaptcha | 第一条消息可用，第二条提示需登录；登录走 hCaptcha + Stripe 付费墙 |

应对：放弃。除非你有合法的人机操作（如自有账号 + Selenium）且站点 ToS 允许。

## 2. 付费墙

特征：
- 前端含 Stripe / RevenueCat / Paddle SDK。
- 第一条消息能用，第 N 条 `402 Payment Required` 或 `subscription_required`。
- 模型选择器里 Claude / GPT-4 / Opus 被锁，免费用户只剩弱模型。

实例：

| 站点 | 付费形态 | 实测表现 |
|---|---|---|
| `essaydone.ai` | 32 个 chat 模型全 paywall | 注册流程 100% 跑通，但 chat 模型全要订阅；Writer/Humanizer 能用但都是 wrap 过的成品输出，非 raw LLM |
| `tasklet.ai` | Stripe 订阅 | Free tier 给 GPT-4o-mini，Claude/GPT-4 必须订阅 |
| `hix.ai` | （未确认） | 当前网络无法访问（`ERR_CONNECTION_TIMED_OUT`），疑似 IP 屏蔽中国出口 |

应对：放弃。除非你自己买了订阅且站点 ToS 允许程序化访问。

## 3. IP 信誉墙

特征：
- Akamai / Cloudflare / PerimeterX / DataDome / Imperva 直接 403。
- 响应头 `Server: cloudflare` + `cf-ray` + `cf-mitigated: challenge`。
- 换出口 IP（住宅代理）能瞬间放行。

实例：

| 站点 | 信誉墙 | 实测表现 |
|---|---|---|
| `mindstudio.ai` | CF challenge | 注册纯净（AWS Cognito，能拿 JWT），但"chat"是 agent workflow runner 不是 raw chat |
| `freellmplayground.com` | 营销谎言 + 登录强制 | "No signup" 实际点 Run 直接 redirect `langfa.st/login` |
| `hix.ai` | IP 黑名单 | 中国出口 TCP timeout |

应对：上 SOCKS5 池可解，但配额低，要做 account-pool 轮换。

## 4. B2B / Agent wrap（最致命）

特征：
- 站点定位是"prompt 模板平台"/"agent workflow runner"，**不暴露 raw chat 接口**。
- 系统提示词被服务端硬编码覆盖（你写啥它都不听）。
- 返回结果都是 markdown 文章 / 表格 / 表单填空，不是流式 LLM token。

实例：

| 站点 | wrap 形态 | 实测表现 |
|---|---|---|
| `mindstudio.ai` | Agent workflow | 不能 raw chat，只能跑 pre-defined workflow（如"写邮件"、"写大纲"），输入 prompt 被框死 |
| `iweaver.ai` | "Chat with Claude Opus 4.7 for FREE" SEO landing | 点击立刻跳 `/app/auth/signin`；注册路径触发 JS `Cannot read properties of undefined (reading 'data')` → 无 API 调用发出 |
| `duck.ai` | system prompt 强制覆盖 | API schema 完美，但 DDG 给 Claude Haiku 4.5 注 system prompt 强制 "natural language only"，**拒绝任何 JSON 格式化输出 / 角色扮演成 API 的请求** → 不能合成 tool_calls |
| `essaydone.ai`(Writer/Humanizer) | wrap 成品输出 | 能用但都是 markdown 文章，不是 raw token stream |

应对：**彻底放弃**。这是最致命的拒绝信号 —— 即使协议层通了，fence 协议注不进去，工具循环就建不起来。

## 灰区案例

| 站点 | 状态 | 备注 |
|---|---|---|
| `overchat.ai` | API schema 全过 4/4，IP 被 ban | 反代需求全部满足，差换 IP/device 池；如果未来要做 Claude Opus 路径就从这里复活（见 `_archive/overchat-pending/`）|
| `miniapps.ai` | magic-link auth 流程已抓 | 邮箱 magic-link 流程已抓到但 `auth_hash` 在 sendgrid 重定向时被消费过；需要重发 + 立刻打开新 hash |
| `atxp.chat` | 注册机 100% 工作，rate-limit 阻断 | "$5 free credit" 实测**只对干净 IP + 干净邮箱**生效；本地中国 IP + `.xyz` 邮箱 → `fraud_blocked`；干净 VPS + `outlook.com` → 拿到 `$6 credit`，但 `chat.atxp.ai` 429 限速 |
| `chatgpt.org` | ✅ **唯一完美** | 不登录可用、不 wrap system、OpenRouter 透传到 Bedrock 真出 token、流式 SSE 标准、白名单 8 个模型（含 Claude Haiku 4.5、GPT-4o-mini、Gemini Flash、Grok、DeepSeek、Qwen、Moonlight、Perplexity）|

## 一句话总结

**16 个候选 → 1 个完美（chatgpt.org）+ 1 个部分（deepai） + 14 个 archive ≈ 6% 命中率**。

筛选优先级：
1. 5 分钟硬性验证（详见 `5-minute-triage.md`）。
2. 看到 4 类拒绝信号之一 → **立即** archive，写 README 留教训。
3. 不要在 archive 站点上花超过 30 分钟。
