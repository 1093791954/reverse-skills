# Templates — 可复用代码骨架

> 这些是从工程 `D:\tmp\FreeAI\` 抠出来的**实际跑通的代码**（PASS 3/3 + multi-turn ALL OK），不是伪代码。每个文件都有完整的 cron iter 修复链。

## 文件清单

| 文件 | 行数 | 是否站点专属 | 用法 |
|---|---|---|---|
| `app_skeleton.py` | ~780 | 否 | 直接 `cp <new-site>/app.py`，改顶部 driver import 即可 |
| `driver_skeleton.py` | ~250 | **是** | `cp <new-site>/driver.py`，改 `SITE_API_URL` / `MODEL_MAPPING` / `_headers()` 三处 |
| `driver_base.py` | ~100 | 否 | 直接放 `_common/`，不需要改 |
| `tool_proxy.py` | ~350 | 否 | 直接放 `_common/`，包含 FenceStreamParser 完整状态机 |
| `account_pool.py` | ~275 | 否 | 直接放 `_common/`，包含 LRU + JSON 持久化 + exhausted TTL |
| `cache.py` | ~265 | 否 | 直接放 `_common/`，包含 SQLite WAL + 流式 insert 修复 |
| `deploy.py` | ~322 | 否 | 直接放工程根，按 `--host / --user / --password / --bearer-token` 跑 |

## 推荐目录结构

```
<your-project-root>/
├── _common/                 ← 站点无关共享
│   ├── driver_base.py       (copy from templates)
│   ├── tool_proxy.py        (copy from templates)
│   ├── account_pool.py      (copy from templates)
│   ├── cache.py             (copy from templates)
│   └── echo.py              (自检 driver，可写一个最简的或复用工程内的)
├── _methodology/proxies/    ← 站点无关共享
│   ├── us_<sitename>_working.txt
│   └── fetch_proxy_sources.py
├── deploy.py                (copy from templates，放工程根)
└── <sitename>/              ← 一站一文件夹
    ├── app.py               (copy from templates/app_skeleton.py)
    ├── driver.py            (copy from templates/driver_skeleton.py，改 3 处)
    ├── run.py               (3 行：uvicorn.run("app:app", host="127.0.0.1", port=8888))
    ├── start.bat / stop.bat (双击启动 / 停止)
    ├── README.md
    └── test_*.py            (参考工程内 chatgpt.org/test_*.py)
```

## 新站点上线 checklist

1. **5 分钟硬性验证**通过 → 才动这些代码（参考 `references/site-discovery/5-minute-triage.md`）。
2. `mkdir <sitename>/` + 复制 6 个 template 文件。
3. 在 `driver_skeleton.py` 改 3 处：`SITE_API_URL`、`MODEL_MAPPING`、`_headers()`。
4. 在 `app_skeleton.py` 改 1 处：`from drivers.chatgptorg import ChatGPTOrgDriver` → `from driver import MyDriver`。
5. `_methodology/proxies/` 跑一次 `fetch_proxy_sources.py` + `validate_proxies.py <sitename>`。
6. 本地 `python run.py` → `curl /healthz` → `curl /v1/chat/completions`。
7. 跑 `test_app_e2e.py` 单元层 → `test_opencode_agent.py` E2E（必须 3/3）。
8. 远端 `python deploy.py --host <vps> ...`。
9. OpenCode 配置改 baseURL 到远端 → 实测 `opencode run "task"`。

## 关键注意点

- **`_common/` 不能用 `pip install -e`** — 每个 site 服务器在 `app.py` 顶部 `sys.path.insert(0, str(Path(__file__).parent.parent / "_common"))` 直接 sibling import。这是有意为之，避免任何 setup.py / pyproject.toml 工程化负担。
- **driver 文件名建议固定为 `driver.py`**（不是 `<sitename>_driver.py`），因为 app.py 里 `from driver import ...` 是硬路径，目录已经隔离了站点。
- **每个 site 用不同端口**：chatgpt.org 8888，下一个站点（如果做的话）用 8889 / 18888，避免冲突。
- **runtime 产物 gitignore**：`account_pool.json` / `prompt_cache.db*` / `server.log` 每个 site 目录都各自有，不要 commit。

## 站点专属修改点（driver_skeleton.py 的 3 处）

```python
# ============================ SITE-SPECIFIC ============================
SITE_API_URL = "https://chatgpt.org/api/chat"   # 改这里

MODEL_MAPPING = {
    "claude-haiku-4-5": "anthropic/claude-haiku-4-5",
    # 改这里
}

def _headers():
    return {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "Origin": "https://chatgpt.org",           # 改这里
        "Referer": "https://chatgpt.org/chat",     # 改这里
        "User-Agent": "Mozilla/5.0 ...",
    }
# ======================================================================
```

3 个地方加起来不超过 10 行。其他全部是通用的（重试、墙钟、SOCKS catch-all、池子集成等）。

## 验证清单

template 拿去用之前，**先**在本地跑一次原版工程的 `test_app_e2e.py`：

```cmd
cd D:\tmp\FreeAI\chatgpt.org
python test_app_e2e.py
# expect: All end-to-end app tests passed.
```

如果工程内的 PASS，但你 copy 出来的不 PASS → 大概率是 sys.path 没配对。检查 `_common/` 路径相对位置。
