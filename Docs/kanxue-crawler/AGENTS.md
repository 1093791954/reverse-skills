# 给 Claude 看的 — 项目交接说明

> 这份文档是给后续接手这个项目的 Claude（也包括我自己重启会话后）看的。
> 用户每次进来不会重复解释项目背景，请你先读完这份再动手。

## 项目是什么

`D:\tmp\SKILLS\Docs\kanxue-crawler` — 看雪安全社区（bbs.kanxue.com）登录态帖子抓取工具。
用户的目标：**把感兴趣的帖子按版块归档到本地的 Markdown 资料库**，用于以后检索/阅读。

## 用户的硬性要求（**最重要**）

1. **绝不能让账号被封**。账号难弄，封了就再也没法继续。
2. 不做任何形式的压力测试 / 探测风控阈值。
3. 速率必须模拟正常用户，**慢就慢**。用户明确表示能接受非常缓慢的进度。
4. 见到验证码、未登录跳转、连续 4xx/5xx → 立刻停，让用户介入。

## 当前状态（2026-05-10）

- 工程骨架已搭完，三个脚本都跑通了：`check_login` / `crawl_list` / `crawl_thread`
- cookies 已经 dump 到 `state/cookies.json`，登录有效
- 已经抓完 5 个真实帖子（output/4_逆向工程/ 下面）作为验证
- 节流参数已经按"账号优先"调到非常保守：每 GET 8~22s + 每帖间 30~90s + 日上限 600 GET

## 用户接下来可能让你做什么

### 情景 A：让你继续抓某些版块

```bash
cd D:\tmp\SKILLS\Docs\kanxue-crawler
python -m src.check_login                                    # 先确认 cookies 还有效
python -m src.crawl_list --forum <fid> --max-pages <N>       # 收集索引
python -m src.crawl_thread --limit <小数字，如 5~20> --fid <fid>  # 下正文
```

**永远先 check_login。永远把 `--limit` 控制在用户给的数字以内**，不要自作主张加大。

### 情景 B：cookies 失效

按 README §5 流程：
1. 用 `mcp__playwright__browser_navigate` 打开 `https://bbs.kanxue.com/`
2. 让用户在浏览器里手动登录（不要尝试自动填账密）
3. 用 `mcp__playwright__browser_evaluate` 跑 `() => document.cookie` 拿回 cookie 字符串
4. 解析成键值对写回 `state/cookies.json`，结构参考现有文件
5. 跑 `check_login` 验证

### 情景 C：解析逻辑要改

- 看雪的 HTML 关键 selector（已实测）：
  - 主楼正文：`.card.message_card .message[isfirst="1"]`
  - 主楼作者：`.card.message_card a[href*="user-home"]` 里**第一个有文字的** anchor
  - 回复楼：`tr.post`（注意是 `tr` 不是 `div`），属性 `data-pid`
  - 回复楼作者：`tr.post` 内第一个有文字的 `a[href*="user-home"]`
  - 楼层号：`tr.post .floor`
  - 时间：在 `.card.message_card`（OP）或 `tr.post` 里搜 `^\d{4}-\d{1,2}-\d{1,2}` 的 span 文本
  - 总页数：扫所有 `a[href]` 里 `thread-{tid}-{p}.htm` 的最大 p
  - 列表页 thread 链接：`table.threadlist a[href*="thread-"]`，正则 `thread-(\d+)\.htm$`
- raw HTML 都存了，可以离线 debug 不用再请求服务器
- 解析后楼层数 ≠ 实际数 → 99% 是看雪改版，去看 `raw/page-1.html`

### 情景 D：用户问"现在抓了多少 / 还有多少"

```bash
sqlite3 state\threads.sqlite "SELECT fid, COUNT(*) total, SUM(crawled_at IS NOT NULL) done FROM threads GROUP BY fid;"
sqlite3 state\ledger.sqlite "SELECT * FROM req_count;"
```

## 不要做的事

- ❌ 不要并发（不要用 asyncio gather / 多进程 / 多线程同时跑多个 GET）
- ❌ 不要在没明确得到允许的情况下跑 `--limit` > 20
- ❌ 不要试图绕过看雪的付费/隐藏内容
- ❌ 不要去碰 `passport_token` 之外的鉴权机制（不要试图自动登录、不要弄账号轮换）
- ❌ 不要把抓下来的内容用任何形式发到外网
- ❌ 收到 captcha / 403 不要 retry 一万次，立刻 raise Throttled 退出

## 文件清单

- `README.md` — 给人看的完整使用文档
- `CHEATSHEET.md` — 命令速查卡
- `AGENTS.md` — 你正在读的这份，给 AI agent 的交接文档
- `config.toml` — 配置（节流 + 版块白名单）
- `requirements.txt` — Python 依赖
- `src/core.py` — KxClient + Config + Ledger + Throttled/DailyCapReached
- `src/check_login.py` — 健康检查
- `src/crawl_list.py` — 列表爬虫
- `src/crawl_thread.py` — 详情爬虫 + Markdown 渲染
