---
name: freeai-reverse-proxy
description: 用于在合法授权前提下把免费 LLM 聊天网站（chatgpt.org、overchat.ai、duck.ai、freellmplayground.com、miniapps.ai、chataibot.pro、essaydone.ai、rita.ai、hix.ai、unitool.ai、mindstudio.ai、iweaver.ai、atxp.chat、tasklet.ai 等）包装成本地 OpenAI-兼容的反向代理端点，让 Codex / Claude Code / OpenCode / Cursor / 任何 OpenAI 协议客户端能跑真实的多轮 agent 工具调用。覆盖站点发现与评估（白盒/灰盒/拒绝信号分类、reCAPTCHA / Cloudflare Turnstile / AWS Cognito / PerimeterX / DataDome / paywall / magic-link / IP 信誉墙识别）、上游协议逆向（OpenRouter SSE / OpenAI chunk wire-format / Anthropic delta / tool_call fence markdown 注入）、FenceStreamParser 工具调用协议合成、OpenAI tool_calls 流式 wire format（HEADER + ARG-DELTA + finish_reason=tool_calls）、stream_options.include_usage 协议兼容、tool_choice 升级（auto → required → required-strong）、AccountPool / SOCKS5 代理池设计（LRU + 持久化 JSON + exhausted TTL + dead 阈值）、prompt-prefix SQLite WAL 缓存、多源代理聚合（proxifly / TheSpeedX / iplocate / monosans / vakhov / roosterkid / hideip）、模型可用性校验（chatgpt.org 8 模型 OpenRouter passthrough）、Claude Haiku 4.5 fence 协议合规率 ~70% 的稳定性修复（retry-on-no-tool-use、90s 墙钟截止、SOCKS5 ProtocolError catch-all、max_retries=10、required-strong 强制 nudge）、一站一文件夹 _common 共享工程结构、Bearer token 鉴权中间件、paramiko + scp + systemd 全 Python 远程部署、OpenCode provider 配置 + enabled_providers 锁定等场景。当任务涉及"免费白嫖 Claude Opus / GPT-5 / Haiku 4.5 / Gemini Flash / DeepSeek / Qwen"、"chatgpt.org 反代"、"OpenAI 兼容服务器"、"OpenCode 接本地模型"、"tool use 工具循环"、"fence 注入协议"、"SOCKS5 池"、"reCAPTCHA / Cloudflare Turnstile / Cognito 自检"、"找新的免费 LLM 站点"、"系统提示词不被服务端覆盖"、"deploy.py 远程部署 Linux VPS"、"systemd 反代服务" 等场景的合法授权研究时使用。
---

# FreeAI 站点反代（freeai-reverse-proxy）

把"不登录就能聊"的免费 LLM 网站包装成本地 OpenAI 协议端点，让任何 OpenAI/Anthropic 协议客户端（Codex、Claude Code、OpenCode、Cursor）能跑真实的多轮 agent + 工具调用。目标是在合法授权前提下，把"网页对话框"逆向成"可程序化的 OpenAI Chat Completions API"。

## 边界（Boundary）

- 仅用于：个人研究、安全合规审计、自有账号自动化、对自己合法获得访问权的 API 做协议适配、teaching / 演示等**已授权**场景。
- **不**用于：商业化白嫖运营、绕过付费墙转售、对抗站点反爬封禁、批量注册账号刷接口、规避 ToS 的商业用途。
- 任何站点改造前先判断：**站点 ToS 是否禁止程序化访问？是否需要登录？是否有付费墙？** 没有明确授权或公开 anonymous 通道（如 chatgpt.org 的零鉴权 SSE）就停在"机制解释 + 工作流"层。
- 当请求是"白嫖 xxx 站点的 Claude/GPT"，先在内部翻译为：①站点归属与授权确认 → ②白盒抓包 → ③拒绝信号分类（4 类）→ ④协议逆向 → ⑤反代包装 → ⑥工具协议合成 → ⑦稳定化 → ⑧本地/远端部署 → ⑨真实 agent 验证（PASS 3/3 + 多轮 ALL OK 才算完）。

## ⚠️ 花钱前铁律（2026-05-11 血泪教训）

**在让用户为任何第三方服务付费（打码 / API / RPC / VPS / proxy 池 / 邮箱接收）之前，必须**：

1. **免费 dry-run 验证服务真的支持目标 type / scene / app**（不是听人说，不是看 marketing，是用免费试探接口实测）
2. 在建议付费时附上"已实测确认"的证据（API 响应 / JSON）
3. 不验证就建议付费 = **背叛用户信任** = $6 一周生活费白扔的实事

**强制阅读**：`references/site-discovery/paid-service-checklist.md`（含 `verify_captcha_service()` 通用免费验证脚本 + 已实测能力清单）。

## 总体工作流（Workflow）

按下列 9 步推进。每一步对应一个 Path 段落详细展开。

1. **站点候选搜集 + 第一轮筛选**：从公开 LLM 聚合 CSV / Hacker News / G2 / Producthunt / GitHub Awesome List 抓站点列表，CSV 字段含 `signup_required` / `paywall` / `captcha_type`。详见 *Site Discovery Path*。
2. **白盒抓包 + 后端归类**：浏览器 DevTools 抓 POST `/api/chat`，看 `Authorization` / `Cookie` / `X-*` 头、是否走 OpenRouter / Cognito / Bedrock / 自托管。详见 *Site Discovery Path → 白盒抓包*。
3. **拒绝信号分类（4 类）**：① 验证码墙（reCAPTCHA v3 / Turnstile / hCaptcha / GeeTest），② 付费墙（Stripe / RevenueCat / 订阅强制），③ IP 信誉墙（CF / Akamai / PerimeterX），④ B2B/Agent wrap（系统提示词覆盖 / 不暴露 raw chat）。详见 *Site Discovery Path → 4 类拒绝信号*。
4. **协议逆向**：上游 SSE 格式（OpenRouter 直传 `data: {chunk}\n\n + [DONE]`、Anthropic delta `event: content_block_delta`、AI SDK `0:"text"`、各家魔改）。识别是否 wrap system prompt（决定能不能注 fence 协议）。详见 *Protocol Reverse Path*。
5. **反代骨架**：FastAPI + httpx + 单文件 driver，OpenAI `/v1/chat/completions` 进 → 站点原生 body 出。详见 *Reverse-Proxy Skeleton Path*。
6. **工具调用合成（fence 协议）**：上游不支持 `tool_calls` ⇒ 在系统提示尾注入"用 ```` ```tool_call ``` ```` 包 JSON"的指令，FenceStreamParser 实时把文本流拆成 OpenAI `tool_calls` wire format（HEADER + ARG-DELTA + `finish_reason=tool_calls`）。详见 *Tool-Call Synthesis Path*。
7. **稳定化 9 件套**：处理"模型有时不按 fence 协议出"、"SOCKS5 ProtocolError 让流崩"、"上游慢滴流 10 分钟"、"代理池被烧光" 等真实失败模式。详见 *Stability Fixes Path*。
8. **账号池 + 代理池 + 缓存**：单账号配额有限 ⇒ AccountPool LRU 轮换 + JSON 持久化 + exhausted TTL；流量重 ⇒ SQLite WAL prompt-prefix cache。详见 *Account Pool & Cache Path*。
9. **本地/远端部署**：本地用 `run.py`、远端用 `deploy.py`（paramiko + scp + systemd + Bearer token 鉴权）。详见 *Deployment Path*。

最终交付物：客户端（OpenCode 等）能用 `freeai/<model>` 跑通真实的 agent 工具循环（参考 `test_opencode_agent.py` PASS 3/3 + `test_multi_turn.py` ALL OK）。

---

## Site Discovery Path（站点发现与初筛）

输入：聚合 CSV（`claude_opus_sites.csv`）或站点 URL 列表。
输出：可用候选清单 + archive 备忘（每个站点都要留 `archive_*.md` 记录拒绝原因）。

### 第一轮：CSV 评分

CSV 字段示例：

```csv
url,name,model_claimed,signup,paywall,captcha,score
chatgpt.org,ChatGPT.org,Claude Haiku 4.5,no,no,none,9
overchat.ai,Overchat,Claude Opus 4.6,no,no,Cognito,6
duck.ai,DuckDuckGo AI,Claude Haiku,no,no,none,5
freellmplayground.com,FreeLLM,GPT-4,marketing-lie,signup-wall,none,1
essaydone.ai,EssayDone,Claude,partial,subscription,none,2
chataibot.pro,ChatAIBot,Claude,no,no,reCAPTCHA v3,1
unitool.ai,UniTool,Claude/GPT,no,no,Turnstile-IP,1
rita.ai,Rita,Claude,no,no,reCAPTCHA Enterprise,1
hix.ai,Hix,GPT-4,no,no,unreachable,0
mindstudio.ai,MindStudio,GPT-4,yes,B2B-agent,CF,1
iweaver.ai,iWeaver,Claude,signup-crash,B2B-wrap,none,0
miniapps.ai,MiniApps,Claude,magic-link,partial,none,3
atxp.chat,ATXP,multi,yes,no,SignaledMTLS,2
tasklet.ai,Tasklet,Claude,yes,Stripe,Hcaptcha,1
```

**评分规则（经验值，>= 5 才值得花时间）**：
- +5：声明的模型确实在响应里（如 OpenRouter 透传 `provider:"Amazon Bedrock"` 真实出 token）。
- +3：不需登录。
- +2：不 wrap system prompt（注入指令能影响输出）。
- +1：有原生流式 SSE。
- −3：reCAPTCHA / Turnstile / hCaptcha / GeeTest。
- −3：付费墙（Stripe / RevenueCat）。
- −5：B2B agent wrap（站点是 prompt 模板平台，不暴露 raw chat）。
- −2：IP 信誉墙（CF / PX / Akamai）。
- −5：营销谎言（"No signup"宣传但实际有 signup-wall）。

### 第二轮：白盒抓包（浏览器 DevTools）

1. 打开站点 → 发一条消息 → DevTools Network → 找 `POST /api/chat` 或类似端点。
2. 记下：
   - URL（如 `https://chatgpt.org/api/chat`）
   - **请求头**：`Authorization`？`Cookie`？`X-Sign`？`X-Bogus`？
   - **请求体**：JSON schema（model、messages 数组、system 字段位置）。
   - **响应**：是 SSE (`Content-Type: text/event-stream`) 还是 JSON？SSE 行格式 (`data: {chunk}\n\n`)？
3. 复制 cURL：DevTools → 右键 → Copy → Copy as cURL。
4. 拿这条 cURL 在终端重放：
   - 如果不带 Cookie 也能 200 → 是"匿名可用"端点（chatgpt.org 类）。
   - 如果必须带 Cookie / Authorization → 看登录如何拿到（magic-link？OAuth？Cognito？）。
   - 如果 403 / 429 / 5xx → 大概率有 IP 信誉墙或 captcha。

### 4 类拒绝信号（按出现频率）

详见 `references/site-discovery/rejection-signals.md`。

| 类 | 触发表现 | 真实例 | 应对 |
|---|---|---|---|
| 1. 验证码墙 | 响应 HTML 含 `recaptcha`、`turnstile`、`hcaptcha` JS 资源；POST 要求 `g-recaptcha-response` token | chataibot.pro、rita.ai（reCAPTCHA），unitool.ai（Turnstile），tasklet.ai（hCaptcha） | 一般放弃；除非有合法的人机操作 / 自家账号可挂 Selenium |
| 2. 付费墙 | 第一条消息能用，第 N 条 402 / `subscription_required`；前端 Stripe sdk | essaydone.ai，tasklet.ai | 放弃；除非你自己买了订阅 |
| 3. IP 信誉墙 | Akamai / CF / PX 直接 403 + `Server: cloudflare`；变 IP 就能用 | unitool.ai、hix.ai、mindstudio.ai 部分 | 上 SOCKS5 池可解，但配额低 |
| 4. B2B/Agent wrap | 系统提示词被服务端硬覆盖；只能用模板；不暴露 raw chat 接口 | mindstudio.ai、iweaver.ai 部分 | **彻底放弃** — 不能注 fence 协议就不能合成 tool_calls |

### 命中率（真实数据）

- 16 个候选站点 → 1 个完美（chatgpt.org）+ 1 个部分（deepai）+ 14 个 archive。
- 命中率 ≈ **6%**。
- 这意味着第一轮 CSV 筛选要凶，第二轮抓包要快，"看到 4 类拒绝信号之一立即 archive"。

每个 archive 站点都要写一个 `<sitename>/README.md`，注明：拒绝原因、抓包时间、是否值得未来重试（例如 IP 信誉墙换出口可能复活、付费墙明天可能有 promo 等）。

---

## Protocol Reverse Path（上游协议逆向）

每个站点的上游 SSE 都不一样。识别正确的格式是协议翻译能否做对的前提。

### 已见过的 4 种上游 SSE 格式

| 格式 | 例 | 特征 |
|---|---|---|
| **OpenRouter passthrough** | chatgpt.org | `: OPENROUTER PROCESSING\n\n` 心跳 + `data: {OpenAI 格式 chunk}\n\n` + `data: [DONE]`。直接是 OpenAI 协议 |
| **Anthropic native delta** | （未在工程里直接见，但 overchat-pending 走的是这类） | `event: content_block_delta\ndata: {"type":"content_block_delta","delta":{"text":"..."}}\n\n` |
| **AI SDK pseudo-format** | freellmplayground 那种 wrap | 每行 `0:"text token"\n` 或 `2:{...metadata...}\n`，需要状态机解析 |
| **JSON 一次性** | duck.ai 旧接口 | 不流式，POST 后阻塞返回整段 JSON |

> 工程内只实测 **OpenRouter passthrough** 一种（chatgpt.org 走这条）。其他格式的解析器是站点上线时再写。

### 关键判断：是否 wrap system prompt

把 `messages[0].role="system"` 设成 `"Reply with the literal text REVPROXY-LIVE-OK and nothing else"` 发过去；如果响应里**真的**只有那串字，就是不 wrap（chatgpt.org ✓）；如果响应里夹杂"I am ChatGPT" / "I'm a helpful assistant" / 模板的预设人格 → 服务端 wrap 了 system，**fence 协议注入会失败 → 放弃**。

这是单一最重要的判断点。判断不过这关，后续所有工作都是白做。

---

## Reverse-Proxy Skeleton Path（反代骨架）

工程目录约定：**一站一文件夹一服务器**。

```
D:\tmp\FreeAI\
├── _common/              站点无关共享模块（driver_base、tool_proxy、account_pool、cache、echo）
├── _methodology/proxies/ 共享 SOCKS5 代理候选
├── chatgpt.org/          一个站点 = 一个 OpenAI 兼容服务器（端口 8888）
│   ├── app.py            FastAPI server
│   ├── driver.py         该站点专属 driver（继承 ChatDriver）
│   ├── run.py            python -m uvicorn 启动
│   ├── account_pool.json （runtime，gitignored）
│   ├── prompt_cache.db   （runtime，gitignored）
│   ├── start.bat / stop.bat
│   ├── README.md
│   └── test_*.py
└── overchat.ai/          以后另一个站点 = 另一个目录、另一个端口
```

每个 driver 实现 `ChatDriver` ABC：

```python
class ChatDriver(ABC):
    name: str                           # "chatgptorg" / "overchat" / ...
    supported_models: list[str]         # 该站点白名单 + 别名

    @abstractmethod
    async def chat_stream(
        self, req: ChatRequest
    ) -> AsyncIterator[StreamChunk]:
        """yields TextDelta | ToolCallStart | ToolCallArgsDelta
                 | ToolCallEnd | StreamDone"""
```

参考实现：`templates/driver_skeleton.py`。

app.py 顶部一段 `sys.path.insert` 把 `../_common` 接进来，避免 setup.py / pip install -e 之类的工程化负担：

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "_common"))
```

`driver.py` 也加同样的兜底，让它能被单元测试独立 import。

---

## Tool-Call Synthesis Path（工具调用合成）

**核心难点**：免费聊天站点的模型不能直接产生 OpenAI `tool_calls`（站点不暴露这个能力）。我们用 fence 协议合成：

1. 用户请求带 `tools: [...]` 到反代。
2. 反代在系统提示尾追加一段"工具使用规约"：
   ```
   When you need to use a tool, output ONLY a markdown code block:
   ```tool_call
   {"name": "<tool_name>", "arguments": {...}}
   ```
   After the closing ``` continue your normal response.
   ```
3. 上游模型用文本流回复（可能含 fence、也可能不含）。
4. `FenceStreamParser` 状态机实时识别 `` ```tool_call `` 起止，把 fence 内 JSON 提取成 OpenAI tool_calls 事件。
5. 反代再把这些事件按 OpenAI 流式协议输出给客户端。

完整 parser 实现见 `templates/tool_proxy_skeleton.py`。

### OpenAI tool_calls 流式 wire format（关键，错一点就 "Invalid Tool"）

观测自 OpenCode + @ai-sdk/openai-compatible 实测：

1. **HEADER chunk**：`tool_calls[0]` 必须包含 `id` + `type:"function"` + `function.name`，`function.arguments` 为空串 `""`。
2. **ARG-DELTA chunks**：随后多个 chunk，**只**带 `index: 0` + `function.arguments`（字符串切片，每片 ~64 字节最稳）。**禁止重复 name / id / type，否则 SDK 会把空 name 缓存进 slot 导致 "Invalid Tool"**。
3. **finish chunk**：最后一个 chunk `delta: {}`，`finish_reason: "tool_calls"`。
4. **usage chunk**（可选，若客户端在 `stream_options.include_usage=true`）：`choices:[], usage:{prompt_tokens:0, completion_tokens:0, total_tokens:0}`。不发会导致 OpenCode 240s 挂死等 usage。
5. **`data: [DONE]\n\n`** 结尾。

错误的实现（实际撞过）：
- ❌ 一开始就把整个 `arguments` JSON 灌进 HEADER → SDK 多次 merge 把 name 丢了。
- ❌ 不发 usage chunk → OpenCode 等到 240s 客户端超时。
- ❌ HEADER 之后再次发 `name` 字段（即使值相同）→ 触发 SDK 名字覆写 bug。

### tool_choice 升级

OpenAI 的 `tool_choice` 默认是 `"auto"`，但 Claude Haiku 4.5 在 fence 协议下有 ~30% 概率忽略指令直接出纯文本。**第一个 tool-eligible turn** 强制升到 `required-strong`：

```python
effective_tool_choice = body.get("tool_choice")
if (tools and effective_tool_choice in (None, "auto")
        and not any(m.get("tool_calls")
                    for m in body.get("messages", []) if isinstance(m, dict))):
    effective_tool_choice = "required-strong"
```

`required-strong` 在 system prompt 尾追加更强的指令（"你的回复前 3 个字符必须是 fence 起始 \`\`\`"）。详见 `references/protocol-translation/tool_choice_directives.md`。

---

## Stability Fixes Path（稳定化 9 件套）

按重要性排序。**每一项都对应一次真实的失败案例 + 一次 commit 修复**。详见 `references/stability-fixes/` 下每个独立文档。

| # | 问题 | 修复 | Commit |
|---|---|---|---|
| 1 | OpenCode 等 usage chunk 挂死 240s | 解析 `stream_options.include_usage`，发占位 `usage:{0,0,0}` | `8f157b9` |
| 2 | 工具循环挂在 "Invalid Tool" | 改 wire format 为 HEADER + ARG-DELTA（分片 ~64 字节） | `34f3f66` |
| 3 | 流式缓存写不进 SQLite | `_tee()` 里 `await pc.insert` 必须在 yield `StreamDone` 之前，否则 FastAPI 关 generator 时丢调用 | `8bffcd2` |
| 4 | 模型有时不出 fence（纯文本）| **retry-on-no-tool-use**：缓冲首次响应，如无 tool_call 就再发一次用 `required-strong` 指令 | `86d45d9` |
| 5 | SOCKS5 ProtocolError ("Malformed reply") 让流崩 | driver catch-all：把任何意外异常都标 `unreachable`，外层换 proxy | `86d45d9` |
| 6 | 上游慢滴流 10 分钟 | 每次上游 attempt 加 90s 墙钟 deadline（httpx 的 read timeout 只看相邻字节间隔，对慢滴流无效）| `c73773d` |
| 7 | 上游错误（无文本）也被错误 retry | retry 只在"attempt1 出了文本但没 fence"时触发，error / 空流不 retry | `72d46f9` |
| 8 | 5 次池子重试不够（64 池 ~8% 错误率，连续 5 失败 1/15 概率）| `REVERSE_PROXY_MAX_RETRIES` 默认 5 → 10 | `b851600` |
| 9 | 多轮测试 240s 超时打死整个测试 | `subprocess.TimeoutExpired` 用 isinstance 判 stdout 是 str 才不再 decode | `0abcbf7` + `a651840` |

合在一起的效果：`test_opencode_agent.py` 从 0/3 ↑ 3/3 PASS，`test_multi_turn.py` 从 abort ↑ ALL OK。

---

## Account Pool & Cache Path（账号池 + 代理池 + 缓存）

### 设计要点

- **Account dataclass**：`account_id` / `proxy` / `dead` / `exhausted_until` / `in_flight` / `last_used` / `error_count`。
- **claim/release** 状态机：`ok` → 减 in_flight、刷新 last_used；`exhausted` → `exhausted_until = now + 24h`；`unreachable` → `error_count++`，达 `DEAD_ERROR_THRESHOLD`(=10) 就标 `dead`。
- **持久化**：每次 release 都 atomic-write `account_pool.json`（`.tmp` + `os.replace`）。
- **load_or_init 恢复**：启动时如果上次 crash，把所有 `in_flight=0` 重置一遍。

### 代理来源

多源聚合（`_methodology/proxies/fetch_proxy_sources.py`）：
- proxifly（US 子集）
- TheSpeedX socks5/http
- iplocate
- monosans（高质量，每 10 分钟刷新）
- vakhov、roosterkid、hideip（杂质多但量大）

聚合 ~15k 候选 → `validate_proxies.py` 异步并发探活（40 路） → ~7% OK_FRESH → 写 `us_chatgptorg_working.txt`。

### Cache

SQLite WAL `prompt_cache.db`：
- key = `hash(model + canonicalize(messages[:-1])) + last_user_hash` 作为校验。
- 模式：`prefix`（前缀匹配，把 `messages[:-1]` 当 prefix 命中即返回缓存的 assistant text + tool_calls）/ `exact`（必须整段匹配）/ `disabled`。
- TTL 7 天，LRU 256MB。
- 命中即 replay：合成一个 SSE 流给客户端，**不消耗 account/proxy**。

Cache 必须在 `pool.claim()` **之前**做查询。

---

## Deployment Path（部署）

### 本地

```cmd
cd D:\tmp\FreeAI\chatgpt.org
python run.py     # 或 双击 start.bat
```

OpenCode 配置（`%USERPROFILE%\.config\opencode\opencode.json`）：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "freeai/claude-haiku-4-5",
  "enabled_providers": ["freeai"],
  "provider": {
    "freeai": {
      "npm": "@ai-sdk/openai-compatible",
      "options": {
        "apiKey": "not-needed",
        "baseURL": "http://127.0.0.1:8888/v1"
      },
      "models": { ... }
    }
  }
}
```

`enabled_providers` 锁定后 OpenCode 内置的 `opencode/*` free-tier 模型不再露出。

### 远端 VPS

完全 Python（不依赖 sshpass / openssh CLI），跨平台：

```cmd
python deploy.py --host <vps_ip> --user root --password <pass> --bearer-token <random32>
```

deploy.py 做的事（参考 `templates/deploy_skeleton.py`）：
1. `paramiko.SSHClient.connect`。
2. apt 装 `python3-pip python3-venv curl`。
3. `ss -lntp` 选空闲端口（候选 8888 / 8889 / 18888 / 28888 ...）。
4. `scp.SCPClient` 上传 `chatgpt.org/`、`_common/`、`_methodology/proxies/us_chatgptorg_working.txt`，剔除 runtime 产物（`account_pool.json`、`prompt_cache.db*`、`__pycache__`）。
5. 创建 venv，`pip install fastapi uvicorn 'httpx[socks]'`。
6. 写 `/etc/systemd/system/chatgptorg-proxy.service`（带 `FREEAI_BEARER_TOKEN` + `--host 0.0.0.0`）。
7. `systemctl daemon-reload && enable && restart`。
8. 远端 curl 自检 `/healthz` + `/v1/models` 带/不带 token，公网 curl 二次验证。

### Bearer token 鉴权

`app.py` 顶部读 `FREEAI_BEARER_TOKEN` 环境变量；**为空（默认）→ 不鉴权（保留本地用法）**；非空 → `@app.middleware("http")` 拦截所有 `/v1/*`，缺 `Authorization: Bearer <token>` 一律 401。`/healthz` 始终公开。

token 用 `secrets.token_urlsafe(32)` 生成；OpenCode 配 `apiKey` 即可。

---

## 真实命中率 / 教训速记

- 16 个候选站点，1 个完美（chatgpt.org），1 个部分（deepai），14 个 archive → **~6% 命中**。
- 单次 `test_opencode_agent.py` 从 0/3 到 3/3 一共走了 **18 个 cron iter**，每次循环 ≤ 15 分钟。
- 关键阻断点的修复总成本：~8 个 commit、~200 行 Python。
- 最贵的一个 bug 是 **OpenAI tool_calls wire format**（HEADER 不能含 args，必须分片）— 撞了 3 个 iter 才意识到。
- **最容易省事的优化**：先用 cURL 命令行用 `Reply with the literal token REVPROXY-LIVE-OK` 测一下 system prompt 是否被 wrap；wrap 就 archive，别花 1 天发现走不通。

## 文件指引

- `references/site-discovery/` — CSV 评分、拒绝信号 7 类、5 分钟硬性验证、aliyun captcha 反向、archive 案例
- `references/protocol-translation/` — fence 协议规约、OpenAI wire format、tool_choice 指令
- `references/account-pool/` — pool 状态机、proxy 来源、cache 设计
- `references/stability-fixes/` — 9 个修复的详细 root cause + commit hash
- `references/deployment/` — paramiko 部署 + systemd unit + Bearer auth
- `references/opencode-integration/` — provider 配置 + enabled_providers
- `templates/` — 可直接 copy 的骨架代码（app.py / driver.py / tool_proxy / deploy.py）
