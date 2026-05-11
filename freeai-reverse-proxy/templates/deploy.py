"""Deploy chatgpt.org/ reverse-proxy to a Linux VPS via paramiko + scp.

Uses pure-Python SSH/SCP (no sshpass / openssh CLI) so it works
identically on Windows hosts.

Usage:
    set DEPLOY_HOST=38.76.215.105
    set DEPLOY_USER=root
    set DEPLOY_PASS=...
    python deploy.py
        --bearer-token <random32>
        [--port 0]      # 0 = auto-pick a free port on the remote
        [--remote-base /opt/freeai]

The script is idempotent: re-running redeploys the latest code
without re-installing apt/pip deps when not needed.

What gets deployed
------------------
- chatgpt.org/        → <remote-base>/chatgpt.org/
- _common/            → <remote-base>/_common/
- _methodology/proxies/us_chatgptorg_working.txt
                      → <remote-base>/_methodology/proxies/

What gets installed
-------------------
- apt: python3-pip, python3-venv
- venv at <remote-base>/.venv with: fastapi, uvicorn, httpx, httpx[socks]
- systemd unit /etc/systemd/system/chatgptorg-proxy.service
  with FREEAI_BEARER_TOKEN + listen-on-0.0.0.0 + port
"""
from __future__ import annotations

import argparse
import os
import posixpath
import secrets
import socket
import sys
import time
from pathlib import Path

import paramiko
from scp import SCPClient


HERE = Path(__file__).parent.resolve()
LOCAL_REPO_ROOT = HERE  # we're running this script from D:\tmp\FreeAI


def _log(msg: str):
    print(f"[deploy] {msg}", flush=True)


def open_ssh(host: str, user: str, password: str) -> paramiko.SSHClient:
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    _log(f"connecting to {user}@{host} ...")
    cli.connect(hostname=host, username=user, password=password,
                timeout=30, banner_timeout=30, allow_agent=False,
                look_for_keys=False)
    _log("ssh OK")
    return cli


def run(cli: paramiko.SSHClient, cmd: str, *, check: bool = True,
        quiet: bool = False) -> tuple[int, str, str]:
    if not quiet:
        _log(f"$ {cmd}")
    stdin, stdout, stderr = cli.exec_command(cmd, get_pty=False, timeout=600)
    rc = stdout.channel.recv_exit_status()
    out = stdout.read().decode("utf-8", "replace")
    err = stderr.read().decode("utf-8", "replace")
    if not quiet and out.strip():
        for line in out.rstrip().splitlines():
            print(f"        {line}")
    if rc != 0 and not quiet:
        for line in err.rstrip().splitlines():
            print(f"   ERR: {line}")
    if check and rc != 0:
        raise RuntimeError(
            f"remote command failed ({rc}): {cmd}\n"
            f"stdout: {out}\nstderr: {err}")
    return rc, out, err


def pick_free_port_remote(cli: paramiko.SSHClient,
                          candidates: list[int]) -> int:
    """Pick the first candidate port that nothing is listening on."""
    for p in candidates:
        rc, out, _ = run(cli, f"ss -lntp 2>/dev/null | grep ':{p} ' || true",
                         check=False, quiet=True)
        if out.strip():
            continue
        # Also avoid TIME_WAIT clutter
        rc, out2, _ = run(cli, f"ss -ant 2>/dev/null | grep ':{p} ' || true",
                          check=False, quiet=True)
        if out2.strip():
            continue
        _log(f"port {p} is free")
        return p
    raise RuntimeError(f"no free port in {candidates}")


def ensure_apt_deps(cli: paramiko.SSHClient):
    _log("apt: ensuring python3-pip + python3-venv ...")
    # apt-get update can be slow / fail on flaky mirrors — don't fail hard
    run(cli, "DEBIAN_FRONTEND=noninteractive apt-get update -y || true",
        check=False)
    run(cli,
        "DEBIAN_FRONTEND=noninteractive apt-get install -y "
        "python3-pip python3-venv curl")


def make_remote_dirs(cli: paramiko.SSHClient, base: str):
    _log(f"mkdir -p {base}/{{chatgpt.org,_common,_methodology/proxies}}")
    run(cli, f"mkdir -p {base}/chatgpt.org "
             f"{base}/_common "
             f"{base}/_methodology/proxies")


def upload_tree(cli: paramiko.SSHClient, local_dir: Path, remote_dir: str,
                *, excludes: set[str] | None = None):
    excludes = excludes or set()
    _log(f"upload {local_dir} -> {remote_dir}")
    # Pre-create the destination (scp -r requires the parent to exist)
    run(cli, f"mkdir -p {remote_dir}", quiet=True)
    transport = cli.get_transport()
    assert transport is not None
    # Build a flat file list (we want to skip excludes & __pycache__)
    files_to_upload = []
    for root, dirs, files in os.walk(local_dir):
        # prune
        dirs[:] = [d for d in dirs
                   if d not in ("__pycache__", ".pytest_cache",
                                "req_dump", "req_dump_v2")
                   and not d.endswith(".egg-info")]
        for fn in files:
            full = Path(root) / fn
            rel = full.relative_to(local_dir).as_posix()
            if rel in excludes:
                continue
            if fn.endswith((".pyc", ".pyo")):
                continue
            if fn in ("account_pool.json", "prompt_cache.db",
                      "prompt_cache.db-shm", "prompt_cache.db-wal",
                      "server.log"):
                # Runtime artifacts — don't ship our local state
                continue
            files_to_upload.append((full, rel))

    with SCPClient(transport, socket_timeout=60) as scp:
        for full, rel in files_to_upload:
            dst = posixpath.join(remote_dir, rel)
            # Make sure parent exists
            parent = posixpath.dirname(dst)
            run(cli, f"mkdir -p {parent}", quiet=True)
            scp.put(str(full), dst)
    _log(f"  uploaded {len(files_to_upload)} files")


def upload_one(cli: paramiko.SSHClient, local_path: Path, remote_path: str):
    _log(f"upload {local_path} -> {remote_path}")
    transport = cli.get_transport()
    assert transport is not None
    parent = posixpath.dirname(remote_path)
    run(cli, f"mkdir -p {parent}", quiet=True)
    with SCPClient(transport, socket_timeout=60) as scp:
        scp.put(str(local_path), remote_path)


def setup_venv(cli: paramiko.SSHClient, base: str):
    _log("creating venv + pip install ...")
    venv = f"{base}/.venv"
    run(cli, f"test -d {venv} || python3 -m venv {venv}")
    pip = f"{venv}/bin/pip"
    run(cli, f"{pip} install --upgrade pip 2>&1 | tail -3", check=False)
    run(cli, f"{pip} install fastapi uvicorn 'httpx[socks]' 2>&1 | tail -5")


SYSTEMD_UNIT = """\
[Unit]
Description=FreeAI chatgpt.org reverse-proxy
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory={base}/chatgpt.org
Environment=PYTHONUNBUFFERED=1
Environment=FREEAI_BEARER_TOKEN={token}
Environment=REVERSE_PROXY_DISABLE_REFRESHER=1
ExecStart={base}/.venv/bin/python -m uvicorn app:app --host 0.0.0.0 --port {port}
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""


def install_systemd(cli: paramiko.SSHClient, base: str, port: int,
                    token: str, service_name: str):
    unit = SYSTEMD_UNIT.format(base=base, port=port, token=token)
    unit_path = f"/etc/systemd/system/{service_name}.service"
    _log(f"writing {unit_path}")
    # Write via heredoc-style cat to avoid scp permission edges
    # (we're root, so a plain cat redirect is fine).
    # Escape any single-quotes in token (we generated it from
    # token_urlsafe which is alnum + -_, but be defensive).
    safe_unit = unit.replace("'", "'\"'\"'")
    run(cli, f"cat > {unit_path} <<'UNITEOF'\n{safe_unit}\nUNITEOF")
    run(cli, f"chmod 644 {unit_path}")
    run(cli, "systemctl daemon-reload")
    run(cli, f"systemctl enable {service_name}")
    run(cli, f"systemctl restart {service_name}")
    _log(f"systemd unit {service_name} started")


def verify(cli: paramiko.SSHClient, host: str, port: int, token: str,
           service_name: str):
    _log("waiting 3s for service to spin up ...")
    time.sleep(3)
    rc, out, _ = run(cli, f"systemctl is-active {service_name}", check=False)
    _log(f"systemctl is-active → {out.strip()}")

    # Check the port is bound
    rc, out, _ = run(cli, f"ss -lntp 2>/dev/null | grep ':{port} ' "
                          f"|| echo 'NOT BOUND'", check=False)

    # Hit /healthz locally
    rc, out, _ = run(
        cli, f"curl -s -m 5 http://127.0.0.1:{port}/healthz", check=False)
    _log(f"/healthz → {out.strip()[:200]}")

    # Hit /v1/models with auth
    rc, out, _ = run(
        cli, f"curl -s -m 5 -H 'Authorization: Bearer {token}' "
             f"http://127.0.0.1:{port}/v1/models | head -c 200",
        check=False)
    _log(f"/v1/models (with token) → {out.strip()[:200]}")

    # Hit /v1/models WITHOUT auth — should 401
    rc, out, _ = run(
        cli, f"curl -s -m 5 -o /dev/null -w '%{{http_code}}' "
             f"http://127.0.0.1:{port}/v1/models",
        check=False)
    _log(f"/v1/models (no token) HTTP status → {out.strip()}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default=os.environ.get("DEPLOY_HOST", ""))
    ap.add_argument("--user", default=os.environ.get("DEPLOY_USER", "root"))
    ap.add_argument("--password",
                    default=os.environ.get("DEPLOY_PASS", ""))
    ap.add_argument("--bearer-token", default="",
                    help="leave empty to auto-generate")
    ap.add_argument("--port", type=int, default=0,
                    help="0 = auto-pick from a candidate list")
    ap.add_argument("--remote-base", default="/opt/freeai")
    ap.add_argument("--service-name", default="chatgptorg-proxy")
    args = ap.parse_args()

    if not args.host or not args.password:
        ap.error("--host and --password are required "
                 "(or via DEPLOY_HOST / DEPLOY_PASS env vars)")

    token = (args.bearer_token or secrets.token_urlsafe(32)).strip()

    cli = open_ssh(args.host, args.user, args.password)
    try:
        ensure_apt_deps(cli)

        # Pick a port if user didn't.  Avoid common ones; prefer "obvious"
        # spots so we / the user remember it.
        if args.port == 0:
            port = pick_free_port_remote(
                cli, [8888, 8889, 18888, 28888, 38888, 48888])
        else:
            port = args.port

        make_remote_dirs(cli, args.remote_base)
        upload_tree(cli, LOCAL_REPO_ROOT / "chatgpt.org",
                    f"{args.remote_base}/chatgpt.org")
        upload_tree(cli, LOCAL_REPO_ROOT / "_common",
                    f"{args.remote_base}/_common")
        upload_one(cli,
                   LOCAL_REPO_ROOT / "_methodology" / "proxies"
                   / "us_chatgptorg_working.txt",
                   f"{args.remote_base}/_methodology/proxies/"
                   f"us_chatgptorg_working.txt")

        setup_venv(cli, args.remote_base)
        install_systemd(cli, args.remote_base, port, token,
                        args.service_name)
        verify(cli, args.host, port, token, args.service_name)

        print()
        print("=" * 64)
        print(" DEPLOY OK")
        print("=" * 64)
        print(f"  endpoint:     http://{args.host}:{port}/v1")
        print(f"  bearer token: {token}")
        print(f"  remote base:  {args.remote_base}")
        print(f"  systemd:      systemctl status {args.service_name}")
        print(f"  journal:      journalctl -u {args.service_name} -f")
        print()
        print("Configure OpenCode with:")
        print(f'  "options": {{')
        print(f'    "apiKey": "{token}",')
        print(f'    "baseURL": "http://{args.host}:{port}/v1"')
        print(f'  }}')
        print("=" * 64)
    finally:
        cli.close()


if __name__ == "__main__":
    main()
