# OpenCode 集成

OpenCode CLI（`@opencode-ai/cli`）可以通过 `@ai-sdk/openai-compatible` 接任意 OpenAI 协议的反代。

## 配置位置

| 平台 | 路径 |
|---|---|
| Windows | `C:\Users\<you>\.config\opencode\opencode.json` |
| macOS / Linux | `~/.config/opencode/opencode.json` |

## 完整示例

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "freeai/claude-haiku-4-5",
  "enabled_providers": ["freeai"],
  "mcp": {},
  "permission": "allow",
  "provider": {
    "freeai": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "FreeAI Reverse Proxy (chatgpt.org / Claude Haiku 4.5)",
      "options": {
        "apiKey": "REPLACE_WITH_BEARER_TOKEN_OR_not-needed",
        "baseURL": "http://127.0.0.1:8888/v1"
      },
      "models": {
        "claude-haiku-4-5":  { "name": "Claude Haiku 4.5 (chatgpt.org)" },
        "gpt-4o-mini":       { "name": "GPT-4o mini (chatgpt.org)" },
        "gemini-2.0-flash":  { "name": "Gemini 2.0 Flash (chatgpt.org)" },
        "deepseek-v3":       { "name": "DeepSeek V3 (chatgpt.org)" },
        "qwen-2.5-72b":      { "name": "Qwen 2.5 72B (chatgpt.org)" },
        "grok-3-mini-beta":  { "name": "Grok 3 mini beta (chatgpt.org)" },
        "moonlight-16k":     { "name": "Moonshot Moonlight 16K (chatgpt.org)" },
        "perplexity-sonar":  { "name": "Perplexity Sonar (chatgpt.org)" }
      }
    }
  }
}
```

## 关键字段

### `model` — 默认模型

不写 `-m` 时用哪个。推荐 `freeai/claude-haiku-4-5`（这是唯一在 `test_opencode_agent.py` PASS 3/3 实测过的）。

### `enabled_providers` — 锁定到本地反代

```json
"enabled_providers": ["freeai"]
```

OpenCode 1.14+ 自带 `opencode/*` 免费模型（big-pickle / minimax / nemotron / ring-2.6），不锁定的话它们会出现在 `opencode models` 列表里。

也支持 `disabled_providers: [...]` 做反向屏蔽。

### `npm: "@ai-sdk/openai-compatible"`

不需要自己 install，OpenCode 会按需 pull。

### `options.baseURL`

注意 `/v1` 后缀，不能漏。OpenCode 把它和 `/chat/completions` 拼接。

本地：`http://127.0.0.1:8888/v1`
远端 VPS（带鉴权）：`http://<vps_ip>:<port>/v1`

### `options.apiKey`

- 本地反代不鉴权时随便填（`"not-needed"` 之类）
- 远端反代有 `FREEAI_BEARER_TOKEN` 时填那个 token

### `models`

每个 key 必须和反代 `/v1/models` 输出的 `id` 字段对应。不在表里的 model 不能用。

## 命令速查

```cmd
opencode models           # 列出所有可用 (provider/model)
opencode auth list        # 列出登录凭证
opencode run "task"       # 用默认 model 跑
opencode run -m freeai/deepseek-v3 "task"   # 指定 model
opencode --help
```

## 备份

每次改配置先备份：

```cmd
copy %USERPROFILE%\.config\opencode\opencode.json %USERPROFILE%\.config\opencode\opencode.json.bak.YYYYMMDD_HHMMSS
```

OpenCode 升级（如 1.3 → 1.14）有时会引入新字段或 schema 变更，备份能秒回滚。

## 升级 OpenCode

```cmd
npm install -g opencode-ai
opencode --version
```

`opencode upgrade` 也行（CLI 自带 self-update）。

## 实测验证

```cmd
mkdir /tmp/test
cd /tmp/test
echo "hello" > a.txt
opencode run "Use the read tool to read a.txt and tell me what it says."
```

应该看到 OpenCode：
1. 用 read tool 读 a.txt
2. 输出 "The file says: hello"

如果挂死或报错，看反代 `server.log` 或 `journalctl -u chatgptorg-proxy -f` 排查。

## 常见错误

| 错误 | 原因 | 修复 |
|---|---|---|
| `404 Not Found` | baseURL 漏了 `/v1` 后缀 | 加 `/v1` |
| `401 Unauthorized` | apiKey 没设 / 错 | 检查 deploy.py 输出的 token |
| `Invalid Tool` | wire format bug | 参考 `protocol-translation/openai-wire-format.md` |
| 卡 240s 超时 | 没发 usage chunk | 见 `stability-fixes/nine-fixes.md` 第 1 项 |
| `opencode/big-pickle` 等出现 | 没 `enabled_providers` | 加上 |
