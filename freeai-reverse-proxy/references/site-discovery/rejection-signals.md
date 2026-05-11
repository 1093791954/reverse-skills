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

> **2026-05-11 重要修订**：第 4 类不再是单一致命信号，拆成三种子类，处理策略不同。

### 4a — system 被 wrap 但**模型仍输出自由文本**（**可救**，user-layer fence 注入）

特征：
- 服务端把 client 传的 system prompt 抹掉或 normalization
- 但用户消息能直接喂给底层 LLM
- 返回是流式（或可一次拿到）的自由文本

**应对：可救！把 tool 协议从 system 层挪到 user 层**：

```
client 真实 system: "<protocol-directive: emit tool_call fence ...>"
+ client user: "List the files"

→ 反代重写为单个 user message:
   "[INSTRUCTIONS: When you need a tool, output ```tool_call\n{...}\n```]
    [TASK]: List the files"
→ 发给目标站点（system 字段不填 / 填默认值）
→ 拿到自由文本响应
→ FenceStreamParser 照常解析
```

实例：

| 站点 | 子类 | 可救方法 |
|---|---|---|
| `duck.ai` | 4a | DDG 强注 "natural language only" 是 system 层；改在 user 层附 `[INSTRUCTIONS: respond in JSON]` 之类，仍可能被前缀检测拒，但**值得重试** |

### 4b — 模型输出**模板化结果**而非自由文本（**致命**）

特征：
- 返回直接是图片 URL / SVG 文件 / 幻灯片 JSON / PDF 链接
- 没有 token stream / chat-style 文本
- 无法塞 fence 协议（连"输出格式"都不是模型决定的）

实例：

| 站点 | 子类 | 表现 |
|---|---|---|
| `designarena.ai` | 4b | 用户输入"创意提示" → 多模型并排出图 → 用户投票。返回是图片对比页面，没有文本流 |
| `essaydone.ai` (Writer/Humanizer) | 4b | 返回 markdown 文章，是 wrap 过的成品 |

应对：**彻底放弃**。

### 4c — 完全不暴露 chat 接口，只能跑**预设 workflow**（**致命**）

特征：
- 站点是 prompt 模板店 / agent workflow runner
- 唯一接口是"选模板 + 填表单 + 跑工作流"
- 没有 free-form chat

实例：

| 站点 | 子类 | 表现 |
|---|---|---|
| `mindstudio.ai` | 4c | 只能跑 pre-defined workflow（写邮件 / 大纲），输入被框死 |
| `iweaver.ai` | 4c | SEO landing 点击直跳 signin，注册流程触发 JS bug，没有 chat 接口 |
| `chatlyai.app` | 4c (待重判，可能是 4a) | OmniAgent 包装；`/agent/chat` 路径暗示有 chat-style 入口，可重试 |

应对：**彻底放弃**。

---

如何快速分辨 4a vs 4b vs 4c？

| 探测点 | 4a | 4b | 4c |
|---|---|---|---|
| 有 free-form textarea 让用户输入任意文本 | ✅ | ❌ | ❌ (有但被模板限制) |
| 响应是 token stream 或自由文本 | ✅ | ❌ (图片/文件/结构化) | ❌ (模板填空) |
| 重写后能否拿到模型真实输出 | ✅ 可能 | ❌ 后端不调 LLM 直接出图 | ❌ 输入被预处理框死 |

**5 分钟硬性验证**：发"`Tell me a joke about cats in exactly 12 words.`"，看是不是真的拿到一段自由的句子且**长度大致符合**。如果是 → 是 4a 可救；如果回的是模板化结果 → 4b/4c archive。

## 5. 站点已 sunset / shutdown（2026-05-11 新增）

特征：
- 首页 title 含 `Legacy` / `Archive` / `Goodbye` / `Sunset` / `Story`
- 文案含**过去时 + 明确日期区间**："June 2024 — April 2026"、"provided/served free access"
- 主区域是 "By the Numbers" 回顾页（registered users / countries / models retired），不是 chat 入口
- 没有 textarea / chat input

实例：

| 站点 | sunset 信号 | 实测表现 |
|---|---|---|
| `yupp.ai` | title="Legacy \| Yupp"、"June 2024 — April 2026 Yupp **provided** free access" | 1M+ users / 90K Discord / 200 countries / 900+ AI models 全是回顾数据，没有 chat 接口 |
| `yupp.dev` | 整域名 ERR_TIMED_OUT | yupp 的开发者域名一同下线 |

应对：**永久 archive，不重试**。"曾经存在但 sunset"是不可逆信号。

> 检测可以做到非常早：访问首页前 **先看 HTML title + body 第一屏文字**，含 "Legacy/Sunset/Story/2024 — 2026" 关键词 + 没有 textarea = 直接 archive，30 秒就能判断。

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

## 规则修订记录

### 2026-05-11 — 放宽"登录"限制

旧规则：站点必须**完全不登录**才进入下一步，否则 archive。
新规则：**允许域名邮箱注册路径**（用户接受跑批量域名邮箱）。也即：

| 站点形态 | 旧规则 | 新规则 |
|---|---|---|
| 完全不登录就能聊（chatgpt.org 类）| ✅ 通过 | ✅ 通过 |
| 邮箱注册 + magic-link / 验证码完成登录 | ❌ archive | ⚠️ **可以试** — 看注册路径是否被 captcha 卡死、是否接受 `.xyz` / 一次性邮箱 |
| 强电话号 / 强信用卡 / KYC | ❌ archive | ❌ 仍 archive |
| reCAPTCHA Enterprise / 高级 captcha | ❌ archive | ❌ 仍 archive（破不掉）|
| 一般 Turnstile / hCaptcha 基础 | ❌ archive | ⚠️ 降级到不优先（理论可叠 captcha solver，但成本高）|
| B2B / Agent wrap | ❌ archive | ❌ 仍 archive（结构性，登录也救不了）|
| system prompt 被 wrap | ❌ archive | ❌ 仍 archive（同上）|

实际操作：判定登录形态后，**继续走 5 分钟验证的第 2 步起**（不 wrap system + 流式 SSE + system 可注入 + 稳定 ≥ 10 次）。如果这几项都过且只是登录拦路，那这是个**值得做注册机**的候选（参考 atxp.chat 注册机经验，但避开它的 rate-limit）。

### 2026-05-11 — 新增第 5 类（sunset）拒绝信号

见上文 "5. 站点已 sunset / shutdown"。来源：Yupp 实测发现。
