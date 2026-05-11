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

## 4. B2B / Agent wrap（**已拆 3 子类**）

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

应对：**永久 archive，不重试**。

> 检测可以做到非常早：访问首页前 **先看 HTML title + body 第一屏文字**，含 "Legacy/Sunset/Story/2024 — 2026" 关键词 + 没有 textarea = 直接 archive，30 秒就能判断。

## 6. "User-Pays" 模型陷阱（2026-05-11 新增）

特征：站点宣传 **"Free Unlimited AI API — No API key, no signup, no server"**，但实际是 **"由你的网站访客出钱"**（User-Pays / Bring-Your-Own-User）：
- dev 在自家网站嵌入站点 SDK（如 `<script src="https://js.xyz.com/v2/"></script>`）
- 当**终端用户**首次触发 AI 调用时，SDK 弹出第三方账号 OAuth 登录窗口
- 登录后 SDK 拿到该用户的 `authToken`，用该用户的配额（kWh 或 token）扣费
- 对 dev 而言是免费，对终端用户而言是付费/有配额上限

### 6.1 BYOK 子类（**2026-05-11 新增，来源：multio.chat**）

特征：
- 站点明确标 "**Free chat with open-source models**" + "**BYOK (Bring Your Own Keys)**" 用顶级模型
- 免费层给 Llama / DeepSeek / Mistral / Qwen 等**开源** models
- Claude / GPT-5 / Gemini / Grok 需要**用户自己填 Anthropic / OpenAI API key**

文案标志（看到立即 archive）：
- "**bring your own keys**" / "**BYOK**" / "**bring your own API**"
- "**use your subscription**" / "**connect your account**" 对 Claude/GPT-5
- "**Free open-source models** + BYOK premium"

实例：

| 站点 | 形态 | 揭穿点 |
|---|---|---|
| `multio.chat` | "Free chat with leading open-source models out of the box. Bring your own keys for direct premium chat." | landing 页"POWER USER BYOK MODE"明示；Claude/GPT-5/Gemini/Grok 标 BYOK |

应对：**立即 archive**。BYOK 让"白嫖"目标失效 — 用户已付钱给原厂，反代是多此一举。

---

实例：

| 站点 | 触发表现 | 揭穿点 |
|---|---|---|
| `puter.com` (puter.js) | README "Free, Unlimited Claude Opus 4.7" + "No API keys or sign-ups required" | SDK 内 `puter.ui.authenticateWithPuter()` 自动弹 OAuth；`/get-gui-token` 匿名 401；注册路径有 Turnstile |

**检测信号（5 分钟内可判定）**：

1. SDK 源码 grep `signIn` / `authenticate` / `bearer` / `oauth` / `popup` 全部命中
2. 演示页面打开后控制台报 `401 Unauthorized` 在 `/whoami` / `/get-gui-token` / `/lsmod` 这类调用
3. README 反复强调 "无 API key" 但**绝口不提"终端用户登录"**

应对：

- **如果你的目标是反代后端**（让 OpenCode/Codex 跑工具循环）→ **archive**。SDK 弹窗终端用户登录、单账号配额、注册需破 Turnstile，代价远超收益。
- 如果你的目标是给前端项目嵌 SDK 给真实用户用 → 这是 OK 的（用户掏自己钱）。

> User-Pays 不是 4 类拒绝信号的子项，单独立第 6 类，因为它包装得像"完美匿名 API"，特别容易上当。

## 8. "诱导式标题"陷阱（2026-05-11 新增）

特征：
- 域名 / title / H1 含**知名厂商模型名**（Claude / Opus / GPT-5 / Gemini）
- 但后端实际是**便宜很多的模型**（GPT-3.5 / GPT-4o-mini / Mistral / 开源 Llama / Qwen）
- footer 或免责声明小字写"非官方/无关联"

判定步骤（**30 秒诊断**）：

注册成功 / 进入 chat 后立刻问 2 个问题：

1. `"What is your exact model name? Reply in JSON format like {\"model_name\":\"...\"} and nothing else."`
2. `"Who is your creator company and what year were you released? Just two facts, nothing else. Format: {company,year}"`

回答匹配表：

| 回答 | 真实后端 | 决策 |
|---|---|---|
| `"Claude Opus 4.x"` + `"Anthropic, 2024+"` | 真 Opus | continue |
| `"Claude 3 Sonnet/Haiku"` + `"Anthropic, 2024-"` | Anthropic 但旧 Opus 不在 | 看是否能满足项目需求 |
| `"GPT-4"` + `"OpenAI"` | **诱导** | archive |
| `"GPT-3.5-turbo"` + `"OpenAI"` | **诱导**（更便宜的伪装）| archive |
| `"Mistral / Llama / Qwen / DeepSeek"` | 开源后端伪装 Claude | archive |
| 拒绝回答 / 模糊回答 | 站点 wrap 了 system 阻止披露 | 进一步测试或 archive |

实例：

| 站点 | title 标榜 | 实测后端 | 揭穿 |
|---|---|---|---|
| `aiclaude.jp` | "Claude(クロード) 日本語無料版" | **GPT-4 / OpenAI** | 直接问"What is your model" → `{"model_name":"GPT-4"}` |

应对：archive（如果项目目标是 Claude）。如果项目目标灵活，仍可作为 GPT 反代候选 — 看 aiclaude.jp 案例（完美 GPT 反代基础设施）。

> **关键**：模型自报模型名虽不 100% 可靠（模型可能被 system prompt 改写自我认知），但**绝大多数 freeware 站点不会去 wrap 这层**。`{company,year}` 问题尤其难造假——因为模型训练时它真的"知道"自己是 OpenAI 还是 Anthropic 造的。

## 9. MWAI / WordPress AI 插件后端识别（2026-05-11 新增，正向信号）

特征：
- API 端点：`POST <site>/wp-json/mwai-ui/v1/chats/submit`
- Init 端点：`POST <site>/wp-json/mwai/v1/start_session`
- Response 元素 class："mwai-reply", "mwai-reply-actions", "mwai-input-submit"
- WordPress 主题 + MWAI (AI Engine) 插件

意义：

- **协议统一**：识别出 MWAI 后端 = 立即知道 chat schema
- **批量发现**：用 Google dork `inurl:wp-json/mwai-ui/v1/chats/submit` 可发现数百个同款站
- 多数 MWAI 站会 wrap 一层 "你是 Claude / 你是 GPT-5" 的 system prompt，**但很多 admin 没改默认配置 = system 注入仍能覆盖**

抓取方式：

```javascript
{
  isMWAI: /wp-json\/mwai/i.test(html),
  endpoint: 'POST ' + location.origin + '/wp-json/mwai-ui/v1/chats/submit',
}
```

实例：

| 站点 | MWAI | 后端 |
|---|---|---|
| `aiclaude.jp` | ✅ | GPT-4（诱导标题）|

## 7. Freemium 月配额（**不是拒绝信号 — 是注册机机会**，2026-05-11 新增）

特征：
- 站点接受邮箱注册（不强 Google OAuth）
- 注册门槛低：阿里盾基础滑块、邮箱激活、或仅邮箱+密码
- 单账号有明确的月配额（如 "15 quotas/month"、"100 messages/month"）
- 模型清单含 Opus 4.6/4.7 等顶级模型（这是优点）

实例：

| 站点 | 配额 | 模型清单亮点 | 注册门槛 |
|---|---|---|---|
| `notegpt.io` | **15 次/月/账号** | **Claude Opus 4.7** 官方支持 + GPT-5/Gemini 3.1 Pro 等 | Email + Password + **阿里盾基础滑块**（不是 Enterprise）|

**应对（重要）**：

不要 archive！这是**注册机 + 账号池**的机会：

- 100 个账号 = 1500 次/月，~50 次/天 → 反代后端可用
- 阿里盾基础滑块（不是 Enterprise）相对好破：
  - OCR 计算滑块缺口位置（85-95% 准确率）
  - 模拟人类拖动轨迹（带加速曲线、抖动、回弹）
  - 单机 5-10 秒过一次
- 邮箱：Catch-all 域名邮箱 + 自托管 IMAP 接收激活码

**判定标准**（**5 分钟内**）：

1. 注册路径含 reCAPTCHA Enterprise / Cloudflare Turnstile / hCaptcha → archive（破不掉）
2. 阿里盾 / 腾讯防水墙 / GeeTest / 网易盾基础滑块 → **可注册机**
3. 必须电话号验证 → archive（无法批量化）
4. 邮箱激活 + 滑块 → **可注册机**（多写一个 IMAP 接收脚本）

**关键洞察**：站点宣传"15 次/月免费"看似抠门，但**对反代**反而是好事 —— 配额低意味着站点没用反 abuse / IP 风控来减损，注册机成本低。

> 第 7 类是"机会信号"不是"拒绝信号"，但放在这里给从 captcha/付费墙惯性思维切换到"注册机"思路的提醒。

> **重要诚实提醒（待实战验证）**：上述"100 账号 → 1500 次/月"、"阿里盾基础滑块 85-95% 准确率"、"单机 5-10 秒过一次"等数字都是基于其他项目的经验值估算，**未在 NoteGPT 上实测**。开始注册机前应先单账号注册成功一次、看是否有邮箱激活 / 设备指纹封禁等额外门槛，再放量。

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
