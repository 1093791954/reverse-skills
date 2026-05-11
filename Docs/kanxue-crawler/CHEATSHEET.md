# Kanxue Crawler — 命令速查卡

> 完整文档见 `README.md`。这里只放最常用的命令，方便以后忘了直接 copy。

## 进入项目

```bash
cd D:\tmp\SKILLS\Docs\kanxue-crawler
```

## 第一次（只装一次依赖）

```bash
python -m pip install -r requirements.txt
```

## 健康检查

```bash
# 验证 cookies 还登录有效（消耗 1 次今日额度）
python -m src.check_login
```

## 收集帖子列表（不下正文）

```bash
# 抓"逆向工程"版（fid=4）最近 3 页帖子的索引
python -m src.crawl_list --forum 4 --max-pages 3

# 多版块一起抓（每版各 2 页）
python -m src.crawl_list --forum 4 --forum 161 --forum 168 --max-pages 2
```

常用 fid（详见 `config.toml [forums]`）：

| fid | 版块 |
|-----|------|
| 4   | 逆向工程 |
| 161 | Android 安全 |
| 163 | iOS 安全 |
| 168 | Web 安全 |
| 123 | 二进制漏洞 |
| 178 | AI 安全 |
| 41  | 工具发布 |
| 88  | 病毒分析 |
| 132 | 外文翻译 |

## 下载帖子正文

```bash
# 从数据库挑 5 个还没抓的逆向工程版帖子下载
python -m src.crawl_thread --limit 5 --fid 4

# 单帖调试（不需要先 crawl_list）
python -m src.crawl_thread --tid 291077

# 把数据库里所有版块的 20 个待抓帖一起抓
python -m src.crawl_thread --limit 20
```

## 看进度

```bash
# 今天用了多少 GET 额度（默认上限 600）
sqlite3 state\ledger.sqlite "SELECT * FROM req_count;"

# 数据库里每个版块多少帖、抓完多少
sqlite3 state\threads.sqlite "SELECT fid, COUNT(*) total, SUM(crawled_at IS NOT NULL) done FROM threads GROUP BY fid;"

# 最近抓完的 10 个
sqlite3 state\threads.sqlite "SELECT tid, title FROM threads WHERE crawled_at IS NOT NULL ORDER BY crawled_at DESC LIMIT 10;"

# 强制重抓某帖
sqlite3 state\threads.sqlite "UPDATE threads SET crawled_at=NULL WHERE tid=XXXXX"
```

## 出问题怎么办

| 现象 | 处理 |
|------|------|
| `check_login` 输出 FAIL | cookies 过期，重新 dump（README §5） |
| `Throttled: captcha page` | **立即停**，浏览器手动过验证码 + dump 新 cookie，等 1~2 天再恢复 |
| `Throttled: too many blocks` | 连续 3 次 403/429。停掉，等几小时再试 |
| `DailyCapReached` | 今日额度用完，等明天 |
| 解析失败 / 楼层数不对 | raw HTML 已存 `output/.../raw/page-*.html`，离线 debug |

## 重置（慎用）

```bash
# 清空进度库（output/ 不会被动）
del state\threads.sqlite
del state\ledger.sqlite

# 清空已抓内容
rmdir /s output
```

## 风控基本盘（**不要随便加快**）

- 每 GET 间停 8~22 秒
- 每帖之间额外停 30~90 秒
- 每天最多 600 GET ≈ 150~200 帖/天
- 单线程，永不并发
- 见到验证码立刻停
