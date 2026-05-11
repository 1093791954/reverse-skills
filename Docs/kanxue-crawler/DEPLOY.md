# 部署到 Linux VPS（Ubuntu 22.04）

> 当前部署目标：`YOUR_VPS_HOST`，Ubuntu 22.04 LTS。
> 邮件告警：QQ 邮箱 `your-mail@qq.com` → 自身 SMTP 发送。

## 整体架构

```
本机 (你的笔记本)                          VPS (YOUR_VPS_HOST)
┌────────────────────────┐                ┌──────────────────────────────────┐
│ playwright 浏览器登录  │                │ /opt/kanxue-crawler/             │
│   ↓                    │                │   ├ src/                          │
│ dump cookies.json      │  scp/sftp →    │   ├ state/cookies.json (600)      │
│                        │                │   ├ state/threads.sqlite          │
│ deploy/push_cookies.sh │                │   └ output/                       │
└────────────────────────┘                │                                  │
                                          │ /etc/kanxue-crawler.env (600)    │
                                          │   SMTP 凭证                      │
                                          │                                  │
                                          │ systemd:                         │
                                          │   kanxue-crawler.timer (每天 03:17)│
                                          │   kanxue-crawler.service          │
                                          │     ↓                            │
                                          │   python -m src.scheduled_run    │
                                          │     ├ check_login                │
                                          │     │   ↓ 失败                   │
                                          │     │   send_email() → QQ 邮箱  │
                                          │     ├ crawl_list (1 页/版块)     │
                                          │     └ crawl_thread (≤10 帖)     │
                                          └──────────────────────────────────┘
```

## 一次性部署（按顺序做）

### Step 1：本机打包 + 上传

在本机项目目录执行（git-bash / WSL 都行）：

```bash
cd D:\tmp\SKILLS\Docs\kanxue-crawler
# 排除 output/raw 太大、state 仅服务器需要新建
tar --exclude='output' --exclude='__pycache__' --exclude='.venv' \
    --exclude='state/threads.sqlite' --exclude='state/ledger.sqlite' \
    -czf /tmp/kanxue-crawler.tar.gz .
scp /tmp/kanxue-crawler.tar.gz root@YOUR_VPS_HOST:/tmp/
```

### Step 2：在 VPS 上解包

```bash
ssh root@YOUR_VPS_HOST
mkdir -p /opt/kanxue-crawler
tar xzf /tmp/kanxue-crawler.tar.gz -C /opt/kanxue-crawler
```

### Step 3：配置 SMTP 凭证（千万别漏 chmod）

```bash
cp /opt/kanxue-crawler/deploy/kanxue-crawler.env.example /etc/kanxue-crawler.env
nano /etc/kanxue-crawler.env
# 当前 QQ 邮箱配置：
#   KANXUE_SMTP_HOST=smtp.qq.com
#   KANXUE_SMTP_PORT=465
#   KANXUE_SMTP_USER=your-mail@qq.com
#   KANXUE_SMTP_PASS=
#   KANXUE_NOTIFY_TO=your-mail@qq.com
chmod 600 /etc/kanxue-crawler.env
```

### Step 4：跑安装脚本（建用户 + venv + systemd）

```bash
sudo bash /opt/kanxue-crawler/deploy/install.sh
```

脚本会自动：
1. apt 装 python3 / venv / sqlite3
2. 创建 `kanxue` 系统用户
3. 创建 `/opt/kanxue-crawler/.venv` 虚拟环境并装依赖
4. 把 `kanxue-crawler.service` / `kanxue-crawler.timer` 装到 `/etc/systemd/system/`
5. `systemctl enable --now kanxue-crawler.timer`

### Step 5：把 cookies 推上去

cookies 不在压缩包里（避免误传旧的）。从本机推：

```bash
# 本机
cd D:\tmp\SKILLS\Docs\kanxue-crawler
bash deploy/push_cookies.sh root@YOUR_VPS_HOST
# 或 PowerShell:
.\deploy\push_cookies.ps1 -RemoteHost root@YOUR_VPS_HOST
```

脚本会：上传 → chmod 600 → 在 VPS 上跑一次 `check_login` 验证。

### Step 6：手动跑一次确认链路通

```bash
ssh root@YOUR_VPS_HOST
systemctl start kanxue-crawler.service
journalctl -u kanxue-crawler.service -n 200 --no-pager
```

预期看到：
- `login OK`
- `forum=4 page=1 got 32 threads`
- 几行 `OK 2912XX  floors=N pages=M  ...`
- `summary` 段

定时器：

```bash
systemctl list-timers kanxue-crawler.timer
# NEXT 应该是明天 03:17 ± 15 min
```

## 日常运维

### 看抓取状态

```bash
ssh root@YOUR_VPS_HOST
sudo -u kanxue bash -c '
  cd /opt/kanxue-crawler
  echo === 今天用了多少 GET ===
  sqlite3 state/ledger.sqlite "SELECT * FROM req_count ORDER BY day DESC LIMIT 7;"
  echo
  echo === 各版块抓取进度 ===
  sqlite3 state/threads.sqlite "SELECT fid, COUNT(*) total, SUM(crawled_at IS NOT NULL) done FROM threads GROUP BY fid ORDER BY fid;"
  echo
  echo === 最近抓完的 5 个 ===
  sqlite3 state/threads.sqlite "SELECT tid, title FROM threads WHERE crawled_at IS NOT NULL ORDER BY crawled_at DESC LIMIT 5;"
'
```

### 拉日志

```bash
journalctl -u kanxue-crawler.service -n 500 --no-pager
journalctl -u kanxue-crawler.service --since '24 hours ago'
```

### 把抓到的内容拉回本机

```bash
# 全量
rsync -avz root@YOUR_VPS_HOST:/opt/kanxue-crawler/output/ D:/tmp/SKILLS/Docs/kanxue-crawler/output/

# 仅某版块
rsync -avz root@YOUR_VPS_HOST:/opt/kanxue-crawler/output/4_逆向工程/ D:/tmp/SKILLS/Docs/kanxue-crawler/output/4_逆向工程/
```

### 临时停掉爬虫

```bash
sudo systemctl disable --now kanxue-crawler.timer
# 恢复
sudo systemctl enable --now kanxue-crawler.timer
```

## cookies 失效处理流程

收到 `[kanxue-crawler] cookies 失效` 邮件时：

1. 在本机 playwright 浏览器登录 `https://bbs.kanxue.com/`
2. 用 MCP 工具跑一次 `() => document.cookie` 拿到新 cookie 字符串
3. 解析成 JSON 写回本机 `state/cookies.json`
4. 跑 `bash deploy/push_cookies.sh root@YOUR_VPS_HOST`，自动同步 + 验证
5. 立即手动 `ssh root@YOUR_VPS_HOST systemctl start kanxue-crawler.service` 看一次能跑通即可

## 常见故障速查

| 现象 | 处理 |
|---|---|
| `journalctl` 看到 exit 3 | cookies 失效。看上面的"cookies 失效处理流程" |
| 看到 `Throttled: captcha page` | 触发风控！立刻 `disable timer`、本机浏览器人工过滑块、过完再开 |
| `DailyCapReached` | 今日额度 600 用完，正常现象 |
| 邮件没收到 | 检查 `/etc/kanxue-crawler.env` 凭证；qq 邮箱授权码不是登录密码 |
| 时间不对 | `timedatectl set-timezone Asia/Shanghai` |
| 磁盘越占越大 | `output/raw/*.html` 占空间最多。可以加 cron `find ... -name 'page-*.html' -mtime +30 -delete` |

## 安全清单（部署完检查一遍）

- [ ] `/etc/kanxue-crawler.env` 权限是 600，所有者是 root
- [ ] `/opt/kanxue-crawler/state/cookies.json` 权限是 600，所有者是 kanxue
- [ ] `/opt/kanxue-crawler` 整体所有者是 kanxue
- [ ] 改了系统 root 密码（**对话历史里的明文密码请立刻改**）
- [ ] 关闭 root 密码登录，只允许 SSH key（`/etc/ssh/sshd_config: PermitRootLogin prohibit-password`）
- [ ] 防火墙只开 22/443/80（如果不需要服务对外，关 80/443 也行）
