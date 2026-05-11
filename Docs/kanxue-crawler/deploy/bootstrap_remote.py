"""一次性部署脚本：通过 paramiko 把项目推到 VPS、装环境、起 systemd。

目标 VPS 关掉了 SFTP 子系统（open_sftp 报 EOFError），所以这里全部用
exec_command + base64 走 ssh 主信道传文件。
"""
import base64
import io
import os
import shlex
import sys
import tarfile
from pathlib import Path

import paramiko

HOST = os.environ.get("KANXUE_VPS_HOST", "")
USER = "root"
PASSWORD = os.environ.get("KANXUE_VPS_PASS", "")
PROJECT = Path(__file__).resolve().parent.parent
REMOTE_ROOT = "/opt/kanxue-crawler"

# QQ 邮箱配置（部署时一次性写入 /etc/kanxue-crawler.env）
SMTP_HOST = os.environ.get("KANXUE_SMTP_HOST", "smtp.qq.com")
SMTP_PORT = "465"
SMTP_USER = os.environ.get("KANXUE_SMTP_USER", "")
SMTP_PASS = os.environ.get("KANXUE_SMTP_PASS", "")
NOTIFY_TO = os.environ.get("KANXUE_NOTIFY_TO", SMTP_USER)


# ---------------- ssh helpers ----------------

def run(c: paramiko.SSHClient, cmd: str, *, check=True, get_pty=False, hide=False):
    if not hide:
        print(f"$ {cmd}")
    stdin, stdout, stderr = c.exec_command(cmd, get_pty=get_pty)
    out = stdout.read().decode(errors="replace")
    err = stderr.read().decode(errors="replace")
    rc = stdout.channel.recv_exit_status()
    if out and not hide:
        print(out, end="" if out.endswith("\n") else "\n")
    if err and not hide:
        print(f"[stderr] {err}", end="" if err.endswith("\n") else "\n")
    if check and rc != 0:
        raise RuntimeError(f"command failed (rc={rc}): {cmd}")
    return rc, out, err


def reconnect(c: paramiko.SSHClient | None = None) -> paramiko.SSHClient:
    """有些服务器会主动 kick 频繁建连。这里在每次 run_batch 之间允许重连。"""
    if c is not None:
        try:
            c.close()
        except Exception:
            pass
    nc = paramiko.SSHClient()
    nc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    nc.connect(HOST, username=USER, password=PASSWORD, timeout=20,
               look_for_keys=False, allow_agent=False,
               banner_timeout=30, auth_timeout=20)
    nc.get_transport().set_keepalive(15)
    return nc


def run_script(c: paramiko.SSHClient, script: str, *, check=True, hide=False) -> tuple[int, str, str]:
    """把多条命令拼成一个 bash 脚本，**只走一次 exec_command**，避免高频建 channel。"""
    if not hide:
        print(f"$ <multi-line script, {len(script.splitlines())} lines>")
    # 用 here-doc 注入；用 base64 来传 script 内容避免 shell 转义问题
    b64 = base64.b64encode(script.encode("utf-8")).decode("ascii")
    cmd = f"bash -c \"$(printf %s {shlex.quote(b64)} | base64 -d)\""
    stdin, stdout, stderr = c.exec_command(cmd, get_pty=False)
    out = stdout.read().decode(errors="replace")
    err = stderr.read().decode(errors="replace")
    rc = stdout.channel.recv_exit_status()
    if out and not hide:
        print(out, end="" if out.endswith("\n") else "\n")
    if err and not hide:
        print(f"[stderr] {err}", end="" if err.endswith("\n") else "\n")
    if check and rc != 0:
        raise RuntimeError(f"script failed (rc={rc})")
    return rc, out, err


def upload_bytes(c: paramiko.SSHClient, data: bytes, remote_path: str) -> None:
    """通过 base64 + exec 上传二进制。把整个内容拼成一条命令一次 exec，避免多 channel。"""
    print(f"uploading {len(data)/1024:.1f} KB -> {remote_path}")
    b64 = base64.b64encode(data).decode("ascii")
    # 用 here-string 避免命令行参数过长。把 b64 通过 stdin 喂入 base64 -d。
    cmd = f"base64 -d > {shlex.quote(remote_path)}"
    stdin, stdout, stderr = c.exec_command(cmd)
    stdin.write(b64)
    stdin.flush()
    stdin.channel.shutdown_write()
    err = stderr.read().decode(errors="replace")
    rc = stdout.channel.recv_exit_status()
    if rc != 0:
        raise RuntimeError(f"upload failed (rc={rc}): {err}")
    # 校验大小（一次额外 exec）
    rc, out, _ = run(c, f"stat -c %s {shlex.quote(remote_path)}", hide=True)
    remote_size = int(out.strip() or 0)
    if remote_size != len(data):
        raise RuntimeError(f"size mismatch: local={len(data)} remote={remote_size}")
    print(f"  upload OK ({remote_size} bytes)")


def upload_text(c: paramiko.SSHClient, text: str, remote_path: str, mode: int = 0o644) -> None:
    upload_bytes(c, text.encode("utf-8"), remote_path)
    run(c, f"chmod {mode:o} {shlex.quote(remote_path)}")


# ---------------- packing ----------------

def make_tar() -> bytes:
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for root, dirs, files in os.walk(PROJECT):
            rel_root = Path(root).relative_to(PROJECT).as_posix()
            dirs[:] = [
                d for d in dirs
                if d not in ("output", ".venv", "__pycache__", ".pytest_cache", ".mypy_cache")
            ]
            if rel_root == "state":
                files = [f for f in files if f == "cookies.json"]
            elif rel_root.startswith("state/"):
                continue
            for fn in files:
                full = Path(root) / fn
                arcname = full.relative_to(PROJECT).as_posix()
                tar.add(full, arcname=arcname)
    buf.seek(0)
    return buf.read()


# ---------------- main ----------------

def main() -> int:
    required = {
        "KANXUE_VPS_HOST": HOST,
        "KANXUE_VPS_PASS": PASSWORD,
        "KANXUE_SMTP_USER": SMTP_USER,
        "KANXUE_SMTP_PASS": SMTP_PASS,
        "KANXUE_NOTIFY_TO": NOTIFY_TO,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        print("missing required environment variables: " + ", ".join(missing), file=sys.stderr)
        return 2

    print(f"connecting to {USER}@{HOST} ...")
    c = reconnect(None)

    try:
        # 1) 打包并上传 tar
        print("packing local project ...")
        tar_bytes = make_tar()
        print(f"  tar size: {len(tar_bytes)/1024:.1f} KB")
        upload_bytes(c, tar_bytes, "/tmp/kanxue-crawler.tar.gz")

        # 2) 写 SMTP env 文件
        env_content = (
            f"KANXUE_SMTP_HOST={SMTP_HOST}\n"
            f"KANXUE_SMTP_PORT={SMTP_PORT}\n"
            f"KANXUE_SMTP_USER={SMTP_USER}\n"
            f"KANXUE_SMTP_PASS={SMTP_PASS}\n"
            f"KANXUE_NOTIFY_TO={NOTIFY_TO}\n"
        )
        upload_bytes(c, env_content.encode("utf-8"), "/etc/kanxue-crawler.env")

        # 3) 一次性跑 解包 + chmod + install + 验证
        big_script = f"""
set -e
chmod 600 /etc/kanxue-crawler.env
mkdir -p {REMOTE_ROOT}
tar xzf /tmp/kanxue-crawler.tar.gz -C {REMOTE_ROOT}
chmod +x {REMOTE_ROOT}/deploy/install.sh
DEBIAN_FRONTEND=noninteractive NEEDRESTART_MODE=a NEEDRESTART_SUSPEND=1 \
  bash {REMOTE_ROOT}/deploy/install.sh

echo
echo '=== verifying ==='
systemctl is-enabled kanxue-crawler.timer || true
systemctl status kanxue-crawler.timer --no-pager || true
ls -la {REMOTE_ROOT}/state/ || true

echo
echo '=== check_login ==='
sudo -u kanxue {REMOTE_ROOT}/.venv/bin/python -m src.check_login || true
"""
        run_script(c, big_script)

    finally:
        c.close()
    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
