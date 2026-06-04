# AccountPool 设计

> 单账号配额有限 → 用一组等价的"账号 / 出口 IP"轮换。即使你的站点不需要登录（如 chatgpt.org），上游通常按出口 IP 限速，所以"账号"实际上等于"SOCKS5 代理出口 IP"。

## Account 数据结构

```python
@dataclass
class Account:
    account_id: str                # 唯一 ID（hash(proxy) 或自增）
    proxy: str = ""                # "socks5://host:port"，空串=直连
    dead: bool = False             # 多次失败永久标死
    exhausted_until: float = 0.0   # unix ts；0=未耗尽；>now=配额耗尽 24h
    in_flight: int = 0             # 当前并发占用数
    last_used: float = 0.0         # 用于 LRU
    error_count: int = 0           # 累计错误；到阈值就 dead
```

## claim / release 状态机

```
                ┌─────────────┐
                │   live      │ ← claim 时选 LRU + in_flight 最少的
                └──┬──┬──┬────┘
       ok          │  │  │     exhausted
       ┌───────────┘  │  └───────────┐
       ▼              │              ▼
  in_flight--    unreachable    exhausted_until = now + 24h
  last_used=now      │
  error_count=0      ▼
                error_count++
                if error_count >= DEAD_ERROR_THRESHOLD:
                    dead = True
```

四种 `outcome` 值：

| outcome | 触发 | 处理 |
|---|---|---|
| `ok` | 成功返回（即使响应慢）| in_flight--, error_count=0, last_used=now |
| `exhausted` | 上游 429 / "limit reached" | exhausted_until=now+24h |
| `unreachable` | 连不上 / 超时 / SOCKS error | error_count++; 到阈值标 dead |
| `dead` | 永久失败（手动标记或 error_count 达 DEAD_ERROR_THRESHOLD=10） | dead=True，永不 claim |

## 持久化

每次 release **同步**写 `account_pool.json`（atomic：`.tmp` + `os.replace`）。

启动时 `load_or_init()`：
1. 如果 JSON 存在 → 加载，**把所有 `in_flight=0` 强制重置**（上次 crash 时漏 release 的恢复）。
2. 如果不存在 → 从 seed 文件（如 `_methodology/proxies/us_chatgptorg_working.txt`）批量创建。

seed 文件格式（一行一个 proxy 或注释）：

```
# generated YYYY-MM-DD ...
socks5://1.2.3.4:1080   # 100ms
socks5://5.6.7.8:4145   # 220ms
http://9.10.11.12:8080  # 350ms
```

## TTL 与并发

- `EXHAUSTED_TTL_SECONDS = 24*3600`（环境变量 `REVERSE_PROXY_EXHAUSTED_TTL` 可覆盖）
- `DEAD_ERROR_THRESHOLD = 10`
- claim 是 async（`asyncio.Lock` 保护），高并发下不会两个请求拿到同一个账号
- 内部用 LRU + 最少 in_flight 排序选 account，避免热点

## stats 输出（healthz）

```json
{
  "pool": {
    "live": 46,
    "exhausted": 18,
    "dead": 0,
    "in_flight": 2,
    "total": 64,
    "last_refresh_at": 0.0
  }
}
```

`live + exhausted + dead == total`，`in_flight` 独立计算。

## 配额耗尽时的客户端体验

如果 `live == 0`（所有账号都 exhausted 或 dead）：
- 立即 raise `NoAccountsAvailable`
- driver 转 fallback：用 `HTTPS_PROXY` 环境变量裸连，或直接 fail。
- 客户端收到 5xx 错误。

## 重要陷阱

1. **`in_flight` 必须用 try/finally 包**，否则 driver 异常时漏 release，账号被永久标 occupied。
2. **JSON 持久化不能用 buffered IO**，要 `_persist_sync()` 每次 release 都 atomic write，否则 crash 后状态丢。
3. **不要在 claim 时锁全局**，只锁选 account 的 critical section（~1 µs），否则高并发立刻挂。
4. **dead 账号要写日志**，因为 dead 不可逆，不知道为啥死的就难恢复。

## 完整实现

见 `_common/account_pool.py`（~250 行）或 `templates/account_pool_skeleton.py`。
