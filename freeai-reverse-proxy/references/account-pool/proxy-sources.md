# 代理源聚合 + 探活

> 单一公开 SOCKS5 代理源命中率极低（< 1%）。多源聚合 + 异步探活后能稳定拿到 ~7% OK_FRESH。

## 已用的源（9 家）

详见 `_methodology/proxies/sources.md`。质量从高到低：

| 名字 | URL | 刷新 | 格式 | 可靠度 |
|---|---|---|---|---|
| monosans_s5 | github.com/monosans/proxy-list/.../socks5.txt | 10 min | host:port | 高 |
| iplocate_s5 | github.com/iplocate/free-proxy-list/.../socks5.txt | per commit | host:port | 高（声称）|
| proxifly_us | jsdelivr.net/gh/proxifly/.../US/data.txt | 5 min | scheme://host:port | 中 |
| speedx_socks5 | github.com/TheSpeedX/PROXY-List/.../socks5.txt | hourly | host:port | 中 |
| hideip_s5 | github.com/zloi-user/hideip.me/.../socks5.txt | 不定 | host:port:Country | 低 |
| roosterkid_s5 | github.com/roosterkid/.../SOCKS5_RAW.txt | 不定 | host:port | 低 |
| vakhov_s5 | github.com/vakhov/fresh-proxy-list/.../socks5.txt | 不定 | host:port | 低 |
| monosans_http | github.com/monosans/proxy-list/.../http.txt | 10 min | host:port | 中 |
| speedx_http | github.com/TheSpeedX/PROXY-List/.../http.txt | hourly | host:port | 中 |

## 聚合脚本

`_methodology/proxies/fetch_proxy_sources.py`：

1. 并发 `httpx.AsyncClient` 下载 9 个源。
2. normalize 到 `scheme://host:port` 格式（统一）。
3. dedupe（用 set）。
4. 写 `us_all.txt`（~15k unique 候选）。

跑：

```cmd
cd _methodology\proxies
python fetch_proxy_sources.py
# → us_all.txt (~15000 lines)
```

## 探活脚本

`_methodology/proxies/validate_proxies.py`：

1. 随机抽样 / 取 head N（一般 500-1500）。
2. 异步并发（默认 40 路）跑 `POST chatgpt.org/api/chat` 简单 prompt。
3. 分类：
   - `OK_FRESH`：200 + 拿到 token + 不显示"limit reached" → 即时可用
   - `OK_QUOTA_EXHAUSTED`：200 + "limit reached" → 该 IP 今天已用完
   - `UNREACHABLE`：连不上 / SOCKS error / 5xx
4. 按 latency 排序写 `mega_working_<n>.txt`。

```cmd
python validate_proxies.py us_all.txt mega_working.txt
# → 大概 3-5 分钟跑完 500 个候选
```

## 命中率（真实数据，2026-05-11）

| 日期 | 样本数 | OK_FRESH | OK_QUOTA | UNREACHABLE | 命中率 |
|---|---|---|---|---|---|
| 2026-05-11 | 500 | 38 | 0 | 462 | **7.6%** |

意味着每 30 分钟做一次 500 样本扫描可期望 ~30-50 个 fresh。

## seed 文件结构

`_methodology/proxies/us_chatgptorg_working.txt`：

```
# chatgpt.org-validated proxies generated at Mon May 11 01:05:02 2026
# OK_FRESH: 34  OK_QUOTA_EXHAUSTED: 0

# --- OK_FRESH (quota usable now, fastest first) ---
socks5://1.2.3.4:1080   # 100ms
socks5://5.6.7.8:4145   # 220ms
...

# --- OK_QUOTA_EXHAUSTED (proxy works but quota used today) ---
（空 — 不用 quota-exhausted 的）
```

AccountPool 启动时 `_seed_from_file()` 读这个文件创建账号。

## 后续策略

- pool_refresher 后台任务每 30 分钟自动重跑 validate 一次，把新 OK_FRESH append 进 pool。
- 但 default `REVERSE_PROXY_DISABLE_REFRESHER=1`（在 systemd 里），因为 refresh 会消耗带宽 + 上游配额。手动重跑就行。

## 常见问题

- **某些"OK_FRESH" 其实是地理位置坏**：proxy 在中国 → chatgpt.org 拒绝。validate 时已经能识别（POST 会 timeout / SOCKS error）。
- **socks5h vs socks5**：`socks5h://` 用 proxy 端 DNS（推荐）；`socks5://` 用客户端 DNS（可能泄露真实位置）。我们统一用 `socks5://` 因为 httpx 现在对 hostname proxy 处理是一致的。
- **HTTP proxy**：偶尔有用，但 chatgpt.org 走 HTTPS，HTTP CONNECT 隧道经常被中间盒劫持。优先 socks5。
