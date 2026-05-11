# Kanxue Crawler — 看雪安全社区抓取工具

合法授权下抓取看雪安全社区（`bbs.kanxue.com`）公开帖子的爬虫工具，把帖子整理成 Markdown 归档到本地，供个人技术资料检索/沉淀。

> **账号优先原则**：本工具一切默认参数都向"绝不被风控封号"倾斜，速率比真人浏览还慢。任何修改 `config.toml` 加快速度的行为都需要使用者自己评估风险。

---

## 0. 30 秒上手（之后忘了直接看这一段就够）

```bash
cd D:\tmp\SKILLS\Docs\kanxue-crawler

# 第一次：装依赖（只需要做一次）
python -m pip install -r requirements.txt

# 1) 验证 cookies 还有效（如果失败请看 §5 重新登录流程）
python -m src.check_login

# 2) 收集某个版块的帖子列表（不会下正文，只把 url+标题写入数据库）
#    fid=4 是"逆向工程"版块；其它 fid 见 config.toml [forums] 段。
python -m src.crawl_list --forum 4 --max-pages 2

# 3) 真正下载帖子内容（默认按非常慢的节流跑）
python -m src.crawl_thread --limit 5 --fid 4

# 结果在：output/4_逆向工程/<tid>_<标题>/post.md
```

抓出来的每个帖子都是一个目录，含 `post.md`（人读的 Markdown）+ `meta.json`（元数据）+ `raw/page-N.html`（原始 HTML 备份）。

---

## 1. 项目目录

```
D:\tmp\SKILLS\Docs\kanxue-crawler\
├── README.md              ← 你正在读的文件
├── requirements.txt       ← Python 依赖
├── config.toml            ← 节流参数 + 版块白名单
├── src\
│   ├── core.py            ← 核心：KxClient（带风控防御的 httpx 客户端）+ RequestLedger（每日请求计数器）+ Config 加载
│   ├── check_login.py     ← 验证 cookies 是否还登录
│   ├── crawl_list.py      ← 抓版块帖子列表（只收集 url+标题，不下正文）
│   └── crawl_thread.py    ← 抓帖子详情，落盘到 output/
├── state\
│   ├── cookies.json       ← 登录 cookies（核心是 passport_token），失效需重新 dump
│   ├── threads.sqlite     ← 抓取进度：待抓/已抓的帖子清单（断点续爬靠它）
│   └── ledger.sqlite      ← 每日全局 GET 计数（跨进程持久化，重启不重置）
└── output\<fid>_<版块名>\<tid>_<安全标题>\
    ├── meta.json          ← 帖子元数据
    ├── post.md            ← Markdown 化的主楼正文 + 楼层回复
    └── raw\page-N.html    ← 每一页的原始 HTML（爬虫升级后可重解析）
```

---

## 2. 三个脚本分别做什么

### 2.1 `check_login.py` — 健康检查

```bash
python -m src.check_login
```

GET 一次首页，检查响应里是否含登录态标志（`user-tasks-` / `退出` / `我的会员` / `user-center`）。
- 输出 `OK: cookies are still valid.` → 一切正常
- 输出 `FAIL: cookies expired ...` → 看 §5 重新 dump cookies

每跑一次会消耗 1 次今日请求额度（默认 600/天）。

---

### 2.2 `crawl_list.py` — 收集帖子列表

```bash
python -m src.crawl_list --forum <fid> [--forum <fid> ...] [--max-pages N]
```

把 `forum-{fid}-{page}.htm` 的列表页爬下来，把每条帖子的 `(tid, fid, title, url)` 写进 `state/threads.sqlite`。**不下正文**。

- `--forum` 可重复指定，如 `--forum 4 --forum 161`（同时收集"逆向工程"+"Android 安全"）
- `--max-pages` 默认 3，意味着每个版块抓最近 3 页 ≈ 120 帖

例子：

```bash
# 抓"逆向工程"版块最新 5 页帖子的索引
python -m src.crawl_list --forum 4 --max-pages 5

# 抓 3 个版块各 2 页
python -m src.crawl_list --forum 4 --forum 161 --forum 168 --max-pages 2
```

可重复运行：已记录在数据库里的帖子会更新 `list_seen_at` 时间戳，不会重复增加。

> 📌 fid 在哪查：浏览器打开 https://bbs.kanxue.com/list.htm 点版块名，URL 里 `forum-XX.htm` 的 XX 就是 fid。常用 fid 已经在 `config.toml [forums]` 里维护好了。

---

### 2.3 `crawl_thread.py` — 下载帖子正文

```bash
python -m src.crawl_thread [--limit N] [--fid <fid>] [--tid <tid>]
```

从 `state/threads.sqlite` 里挑 `crawled_at IS NULL`（即还没下过正文）的帖子，逐个抓首页 + 后续分页，落盘到 `output/`。

- `--limit N`：本次最多抓多少帖。默认 10。**保守起见每次先跑小数量**。
- `--fid X`：只挑某些版块的（与 `crawl_list` 的版块对应）；可重复。
- `--tid Y`：只抓单个 tid（用于调试）。`--tid` 可以抓不在数据库里的帖子。

例子：

```bash
# 从数据库里挑 5 个还没抓的逆向工程版帖子下载
python -m src.crawl_thread --limit 5 --fid 4

# 单帖调试
python -m src.crawl_thread --tid 291077

# 不限版块，把数据库里待抓的清掉 20 个
python -m src.crawl_thread --limit 20
```

支持 **断点续爬**：随时 Ctrl-C 中断，下次再跑会自动跳过 `crawled_at` 已设置的帖子。

落盘结构：

```
output/4_逆向工程/286611_[原创] 微信4.0防撤回带提醒 (符号恢复和字符串解密)/
├── meta.json    # tid/fid/title/作者/时间/楼层数/页数/附件链接
├── post.md      # 主楼 + 全部楼层回复，Markdown 化（保留代码块/图片/链接）
└── raw/
    ├── page-1.html
    ├── page-2.html
    ...
    └── page-7.html
```

---

## 3. 配置文件 `config.toml`

### 3.1 `[network]` — 风控节流（默认值已经非常保守，**一般不要改**）

| 字段 | 默认 | 含义 |
|---|---|---|
| `min_delay` / `max_delay` | 8.0 / 22.0 秒 | 每个 HTTP 请求间随机停顿 |
| `post_thread_min_delay` / `post_thread_max_delay` | 30 / 90 秒 | 抓完一帖再抓下一帖之间的额外停顿 |
| `daily_request_cap` | 600 | 每天全局 GET 上限。超过抛 `DailyCapReached` 立刻退出 |
| `session_thread_cap` | 20 | 单次会话默认最多抓多少帖（被 `--limit` 覆盖） |
| `timeout` | 30 秒 | 单请求超时 |
| `max_retries` | 4 | 网络失败重试次数 |

按当前默认值的实际产出 ≈ **150~200 帖/天**（取决于帖子分页数）。

### 3.2 `[forums]` — 版块白名单

记录 `fid -> 中文名` 映射，仅用于：
- 给 `--forum` 提供合法 fid 参考
- 输出目录命名（`output/<fid>_<中文名>/...`）

如果想加新版块就在这里追加一行：

```toml
[forums]
4   = "逆向工程"
161 = "Android安全"
# 新增一行：
200 = "我自定义的版块"
```

---

## 4. 输出格式

### 4.1 `meta.json` 字段

```json
{
  "tid": 286611,
  "fid": 4,
  "title": "[原创] 微信4.0防撤回带提醒 (符号恢复和字符串解密)",
  "url": "https://bbs.kanxue.com/thread-286611.htm",
  "forum_name": "逆向工程",
  "pages": 7,
  "author": "0xEEEE",
  "author_url": "https://bbs.kanxue.com/user-home-901761.htm",
  "created_at": "2025-4-25 11:07",
  "floors_count": 170,
  "attachments": [],
  "crawled_at": 1778413487
}
```

### 4.2 `post.md` 结构

```markdown
# <帖子标题>

- **链接**: https://bbs.kanxue.com/thread-XXXXX.htm
- **版块**: 逆向工程 (fid=4)
- **作者**: ...
- **发表**: 2026-x-x
- **楼层数**: 170    **页数**: 7

---

## #1  作者名    时间
（主楼 Markdown 正文，保留代码块、图片、超链接）

---

## #2  回复者    时间
...
```

图片地址会被自动补全为绝对 URL（`https://bbs.kanxue.com/upload/attach/...`），目前**不下载图片本体**，只保留链接（避免大量额外 GET 触发风控）。

### 4.3 `raw/page-N.html`

每页原始 HTML 都保留，万一爬虫的解析逻辑以后要升级，可以离线重跑解析、不需要再请求服务器。

---

## 5. 重新 dump cookies（cookies 失效时用）

`state/cookies.json` 里最关键的是 `passport_token`，看雪基本上是几周到几个月才会过期。`check_login` 报错时按下面流程重新生成：

1. 在外层（你和我对话的）Claude 里说一句"打开 playwright 登录看雪"，我会用 MCP 工具开浏览器到 `https://bbs.kanxue.com/`。
2. 你在那个浏览器里手动点登录 → 输入账号密码 → 完成（如果有滑块自己拖）。
3. 我用 `mcp__playwright__browser_evaluate` 跑：
   ```js
   () => ({ cookieFull: document.cookie, ua: navigator.userAgent })
   ```
   把整段 cookie 字符串拿回来。
4. 我把它写回 `state/cookies.json`，结构如下（注意是把 cookie 字符串拆成键值对放到 `cookies` 字典里）：
   ```json
   {
     "_user_agent": "Mozilla/5.0 ...",
     "domain": ".kanxue.com",
     "cookies": {
       "passport_token": "...",
       "__snaker__id": "...",
       ...其它 cookie
     }
   }
   ```
5. 跑 `python -m src.check_login` 验证 OK。

> ⚠️ 如果只想自己手动做：F12 打开看雪登录后的页面 → Application → Cookies → 复制对应字段，按上面 JSON 结构写进去。最关键的字段就是 `passport_token`。

---

## 6. 故障排查

| 现象 | 原因 / 处理 |
|---|---|
| `check_login` 输出 FAIL | cookies 失效 → 见 §5 重新 dump |
| `Throttled: captcha page at ...` | 触发了人机验证。**立即停止**，去浏览器手动打开看雪过验证码，过完再 dump 一次新 cookie，然后等 1~2 天再恢复抓取 |
| `Throttled: too many blocks ...` | 连续 3 次 403/429/5xx。最常见原因：cookie 失效；其次是被风控临时降权。停掉，等几小时再试 |
| `DailyCapReached: daily cap 600 reached` | 今天的额度用完了。等到第二天 0 点 ledger 自动按 `YYYY-MM-DD` 切到新一天 |
| 同一帖反复抓 | `state/threads.sqlite` 里那条记录的 `crawled_at` 字段被清掉了。可以 `sqlite3 state\threads.sqlite "UPDATE threads SET crawled_at=NULL WHERE tid=XXXX"` 强制重抓 |
| 解析后楼层数=1 但实际不止 | 可能看雪改版了 HTML 结构。先看 `output/.../raw/page-1.html` 确认原始 HTML 是不是变了，然后改 `crawl_thread.py` 里的 selectolax 选择器（`tr.post`、`.message[isfirst="1"]`、`.card.message_card`） |
| 抓到的标题尾巴还带 `-XXX` 版块名 | 看 `crawl_thread.py` 的 `parse_thread_page`，它已经会用 breadcrumb 自动剥版块尾。如果出现新形态可以再扩展 |

### 看进度 / 数据库速查

```bash
# 看今天用了多少额度
sqlite3 state\ledger.sqlite "SELECT * FROM req_count;"

# 看数据库里多少帖待抓 / 已抓
sqlite3 state\threads.sqlite "SELECT fid, COUNT(*) total, SUM(crawled_at IS NOT NULL) done FROM threads GROUP BY fid;"

# 看最近 10 个抓完的
sqlite3 state\threads.sqlite "SELECT tid, title FROM threads WHERE crawled_at IS NOT NULL ORDER BY crawled_at DESC LIMIT 10;"
```

### 想完全重置数据库

```bash
del state\threads.sqlite
del state\ledger.sqlite
```

`output/` 不会被脚本自动删，需要的话手动 `rmdir /s output`。

---

## 7. 边界与原则（**别越界**）

- ✅ 只抓**已登录可见**的公开帖子。
- ❌ 不尝试绕过付费/隐藏内容、不撞解付费章节。
- ❌ 不并发、不堆 IP 池、不做账号轮换。一旦封号就再也爬不到，**保账号优先级 > 抓取效率**。
- ❌ 不下载附件（attach 链接保留在 `meta.json` 里，需要时人工去下）。
- ❌ 不下载图片本体（同上）。
- 🛑 一旦遇到验证码/异常跳转，立即停止，让用户人工介入。

---

## 8. 加新功能的入口（开发者备忘）

- **想抓新版块**：`config.toml [forums]` 加一行；用 `--forum <fid>` 跑 `crawl_list`。
- **想改解析逻辑**：所有解析在 `src/crawl_thread.py: parse_thread_page()`，依赖 selectolax 的 CSS 选择器。raw HTML 已落盘，改完代码可以离线重跑（写一个 reparse 脚本读 `raw/page-*.html`）。
- **想下载附件 / 图片**：在 `crawl_one` 抓完正文那段后追加 GET 流，注意 **每个附件 GET 也要走 `cli.get()` 才会算进 ledger 节流**，别绕过 KxClient。
- **想搬到 Linux / WSL**：路径用 `Path` 都是跨平台的，唯一注意是 `safe_name` 把 `\\/:*?"<>|` 都干掉了（按 Windows 最严标准），Linux 上反而能多保留 `:` 但不必管。

---

## 9. 法律与道德

仅用于个人学习、安全研究归档。**不得**：
- 将抓取结果再分发到公开渠道（看雪原创内容版权属于原作者）
- 用于商业用途
- 大批量爬取后做镜像站

如果看雪官方对此有异议，立刻停止使用并删除已抓数据。
