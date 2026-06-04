# 远程部署（paramiko + scp + systemd）

> 全 Python（无 sshpass / openssh CLI 依赖），Windows / Linux 都能跑。

## 总览

```
本地（Windows / mac / Linux）              远端（Linux VPS）
    │
    │  paramiko.SSHClient.connect (password)
    ├──────────────────────────────────────►  sshd
    │
    │  apt install python3-pip python3-venv curl
    │  ss -lntp → 选空闲端口
    │
    │  scp.SCPClient.put  (chatgpt.org/, _common/,
    │                      us_chatgptorg_working.txt)
    │
    │  python3 -m venv .venv
    │  .venv/bin/pip install fastapi uvicorn 'httpx[socks]'
    │
    │  cat > /etc/systemd/system/<name>.service <<EOF
    │   [Service] Env=FREEAI_BEARER_TOKEN=<token> ...
    │  EOF
    │
    │  systemctl daemon-reload && enable && restart
    │
    │  curl /healthz → 验证
    │  curl /v1/models (with token) → 验证
    │  curl /v1/models (no token)   → 验证 401
    └──────────────────────────────────────►
```

## 完整脚本

`templates/deploy_skeleton.py`（或工程内 `deploy.py`，~250 行）。

## systemd unit 模板

```ini
[Unit]
Description=FreeAI chatgpt.org reverse-proxy
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/opt/freeai/chatgpt.org
Environment=PYTHONUNBUFFERED=1
Environment=FREEAI_BEARER_TOKEN=<32-char-base64url>
Environment=REVERSE_PROXY_DISABLE_REFRESHER=1
ExecStart=/opt/freeai/.venv/bin/python -m uvicorn app:app --host 0.0.0.0 --port 8888
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

注意：
- `Type=simple` 不要用 `forking`（uvicorn 不 daemonize）
- `Environment=` 一行一个（不要用引号包整个值）
- `After=network-online.target` + `Wants=network-online.target` 保证有网络
- `Restart=on-failure` + `RestartSec=5` 处理偶发崩溃

## 上传时剔除项

不要把这些上传到远端：
- `account_pool.json` — 远端要自己 seed
- `prompt_cache.db*` — 远端独立的 cache
- `server.log` — 本地调试痕迹
- `__pycache__/` / `*.pyc` — Python 字节码
- `.pytest_cache/`
- `req_dump*/` — 调试 dump

deploy.py 的 `upload_tree()` 在 `os.walk` 时直接 prune。

## Bearer token 鉴权

`app.py` 顶部：

```python
_AUTH_TOKEN = os.environ.get("FREEAI_BEARER_TOKEN", "").strip()

@app.middleware("http")
async def _bearer_auth(request: Request, call_next):
    if not _AUTH_TOKEN:
        return await call_next(request)
    path = request.url.path
    if path in ("/healthz", "/") or path.startswith(("/docs", "/openapi")):
        return await call_next(request)
    auth = request.headers.get("authorization") or ""
    if auth != f"Bearer {_AUTH_TOKEN}":
        return JSONResponse(
            {"error": {"message": "missing or invalid Bearer token",
                       "type": "auth_error", "code": "unauthorized"}},
            status_code=401)
    return await call_next(request)
```

特点：
- 空 token = 不鉴权（本地默认 / 测试兼容）
- `/healthz` 始终公开（运维 / load-balancer 探活）
- `/v1/*` 必须带 `Authorization: Bearer <token>`
- 缺 / 错 → 401 + OpenAI 错误 schema

## 探活脚本（部署后）

```bash
# SSH 上去看
systemctl status chatgptorg-proxy
journalctl -u chatgptorg-proxy -n 50 --no-pager
journalctl -u chatgptorg-proxy -f

ss -lntp | grep :8888

curl http://127.0.0.1:8888/healthz
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8888/v1/models
```

公网验证：

```bash
curl http://<vps_ip>:<port>/healthz
curl -o /dev/null -w "%{http_code}\n" http://<vps_ip>:<port>/v1/models   # 应 401
curl -H "Authorization: Bearer $TOKEN" http://<vps_ip>:<port>/v1/models  # 应 200
```

## 防火墙建议

- `ufw allow ssh`
- `ufw allow from <你的家用 IP> to any port 8888`
- `ufw enable`

或更严：把 8888 只让 127.0.0.1 听 + 用 SSH `-L 8888:127.0.0.1:8888` 隧道访问。

## 安全速记

- **不要**在脚本里硬编码 root 密码 / token。统一用环境变量 / argv。
- 一旦在聊天历史里泄露 token，**立刻重跑 deploy.py 生成新 token**。
- VPS root 密码也要定期换。
- `apt update` 前先看 `/etc/apt/sources.list` 是否被改过（极端场景）。
