# Prompt-Prefix SQLite WAL 缓存

> OpenAI 服务端有 "prompt caching" 给你的同前缀请求打折。我们的反代也可以做本地版，把"同前缀 + 同最后一条 user message"的请求直接命中，**不消耗 account/proxy**。

## 设计

### Key 计算

```python
key = sha256(
    model +
    canonicalize(messages[:-1])  # 所有除最后一条以外的 messages
)
verifier = sha256(messages[-1].content)  # 最后一条 user message
```

两步：
1. **prefix key** 用于查找候选条目。
2. **verifier** 防止前缀偶然碰撞导致错答。

`canonicalize()` 把 messages 规范化（dict 的 key 排序、空白 strip），保证逻辑上相同的 prompt 总产生相同 key。

### 三种模式

环境变量 `REVERSE_PROXY_CACHE_MODE`：

| 模式 | 含义 |
|---|---|
| `disabled` | 禁用 cache |
| `exact` | 必须 messages 完全一致才命中 |
| `prefix` | （**默认**）`messages[:-1]` 一致 + `messages[-1]` 的 hash 用 verifier 校对 |

`prefix` 模式适合 agent 工具循环：前 N 条历史不变，只有最后一条 user 在变，命中率更高。

### 存储

SQLite WAL：

```sql
CREATE TABLE prompt_cache (
  key TEXT PRIMARY KEY,
  verifier TEXT NOT NULL,
  text BLOB,            -- gzip 压缩的 assistant text
  tool_calls TEXT,      -- JSON list
  created_at REAL,
  last_used REAL,
  byte_size INTEGER
);
CREATE INDEX idx_last_used ON prompt_cache(last_used);
```

WAL 模式（PRAGMA journal_mode=WAL）：并发读不阻塞写、写不阻塞读。

### LRU + TTL 清理

- TTL：7 天（`created_at < now - 7*86400` 删）
- 容量：256 MB（`byte_size` 累计超过就按 `last_used` 升序删）
- 清理在 `lookup` 时机会型触发（不专门起 task）

## API

```python
# 查找
async def lookup(model: str, messages: list[Message]) -> CachedResponse | None: ...

# 插入
async def insert(model: str, messages: list[Message], resp: CachedResponse): ...
```

`CachedResponse(text: str, tool_calls: list[dict])`。

## 流式 cache 的陷阱

最大的坑（见 `stability-fixes/streaming-cache-insert.md`）：

```python
# 错的（FastAPI 关 generator 时这行可能不跑）
async def _tee():
    async for ch in driver.chat_stream(req):
        yield ch
        if isinstance(ch, StreamDone):
            await cache.insert(...)  # ← 丢
```

正确：

```python
async def _tee():
    async for ch in driver.chat_stream(req):
        if isinstance(ch, StreamDone) and not had_error:
            await cache.insert(...)  # ← 先写
        yield ch  # ← 再 yield
```

## 命中验证

curl 同一个 prompt 两次：

```cmd
curl -s -X POST http://127.0.0.1:8888/v1/chat/completions \
  -d '{"model":"claude-haiku-4-5","messages":[{"role":"user","content":"hi"}],"stream":false}'
# → cache miss，慢

curl -s -X POST http://127.0.0.1:8888/v1/chat/completions \
  -d '{"model":"claude-haiku-4-5","messages":[{"role":"user","content":"hi"}],"stream":false}'
# → cache hit，响应里有 "x_freeai_cache": "HIT"
```

`/healthz` 里 `cache.hit_count_total` 会增加。

## 完整实现

`_common/cache.py`（~300 行）或 `templates/cache_skeleton.py`。
