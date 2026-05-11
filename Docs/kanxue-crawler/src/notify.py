"""邮件告警。配置在 config.toml [notify.email] 或环境变量里。

环境变量优先（部署到服务器时把密码放 env 而不是落盘到 config.toml 更安全）：
- KANXUE_SMTP_HOST
- KANXUE_SMTP_PORT
- KANXUE_SMTP_USER
- KANXUE_SMTP_PASS  (邮箱"应用专用密码"/授权码，不是登录密码)
- KANXUE_NOTIFY_TO  (收件人，多个用逗号分隔)
"""
from __future__ import annotations

import logging
import os
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

try:
    import tomllib
except ImportError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

log = logging.getLogger("kanxue.notify")


class NotifyConfig:
    def __init__(self, host: str, port: int, user: str, password: str,
                 to_addrs: list[str], from_addr: str, use_starttls: bool):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.to_addrs = to_addrs
        self.from_addr = from_addr or user
        self.use_starttls = use_starttls

    @classmethod
    def load(cls, project_root: Path) -> "NotifyConfig | None":
        # 1) 环境变量优先
        if os.environ.get("KANXUE_SMTP_HOST"):
            host = os.environ["KANXUE_SMTP_HOST"]
            port = int(os.environ.get("KANXUE_SMTP_PORT", "465"))
            user = os.environ.get("KANXUE_SMTP_USER", "")
            password = os.environ.get("KANXUE_SMTP_PASS", "")
            to_raw = os.environ.get("KANXUE_NOTIFY_TO", user)
            from_addr = os.environ.get("KANXUE_SMTP_FROM", user)
            use_starttls = os.environ.get("KANXUE_SMTP_STARTTLS", "0") == "1"
            return cls(host, port, user, password,
                       [x.strip() for x in to_raw.split(",") if x.strip()],
                       from_addr, use_starttls)
        # 2) 退到 config.toml
        cfg_path = project_root / "config.toml"
        if not cfg_path.exists():
            return None
        with open(cfg_path, "rb") as f:
            cfg = tomllib.load(f)
        n = cfg.get("notify", {}).get("email")
        if not n:
            return None
        to_raw = n.get("to", n.get("user", ""))
        if isinstance(to_raw, list):
            to_addrs = to_raw
        else:
            to_addrs = [x.strip() for x in str(to_raw).split(",") if x.strip()]
        return cls(
            host=n["host"],
            port=int(n.get("port", 465)),
            user=n.get("user", ""),
            password=n.get("password", ""),
            to_addrs=to_addrs,
            from_addr=n.get("from", n.get("user", "")),
            use_starttls=bool(n.get("starttls", False)),
        )


def send_email(subject: str, body: str, project_root: Path) -> bool:
    """发邮件。返回 True 表示发送成功。失败只打 log，不向上抛（告警失败不应该影响主流程）。"""
    cfg = NotifyConfig.load(project_root)
    if cfg is None:
        log.warning("notify config missing, skip sending: %s", subject)
        return False
    if not cfg.to_addrs:
        log.warning("no recipient configured, skip: %s", subject)
        return False
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = cfg.from_addr
    msg["To"] = ", ".join(cfg.to_addrs)
    msg.set_content(body)
    try:
        ctx = ssl.create_default_context()
        if cfg.use_starttls:
            with smtplib.SMTP(cfg.host, cfg.port, timeout=30) as s:
                s.ehlo()
                s.starttls(context=ctx)
                s.login(cfg.user, cfg.password)
                s.send_message(msg)
        else:
            with smtplib.SMTP_SSL(cfg.host, cfg.port, context=ctx, timeout=30) as s:
                s.login(cfg.user, cfg.password)
                s.send_message(msg)
        log.info("email sent: %s", subject)
        return True
    except Exception as e:
        log.exception("failed to send email '%s': %s", subject, e)
        return False
