#!/usr/bin/env bash
# 把本机 state/cookies.json 同步到 VPS。
# 在本机 git-bash / WSL / Linux / macOS 跑都行。
#
# 用法（一次性配置 SSH 别名，然后直接跑）：
#   ./deploy/push_cookies.sh kanxue-vps
# 等同于：
#   scp state/cookies.json kanxue-vps:/opt/kanxue-crawler/state/cookies.json
#
# 也可以传完整 host：
#   ./deploy/push_cookies.sh user@vps.example.com
#   ./deploy/push_cookies.sh user@vps.example.com /opt/kanxue-crawler

set -euo pipefail

HOST="${1:-}"
REMOTE_ROOT="${2:-/opt/kanxue-crawler}"

if [[ -z "$HOST" ]]; then
  echo "usage: $0 <ssh-host> [remote-project-dir]" >&2
  echo "example: $0 kanxue-vps" >&2
  exit 1
fi

LOCAL_FILE="$(dirname "$0")/../state/cookies.json"
if [[ ! -f "$LOCAL_FILE" ]]; then
  echo "local cookies file missing: $LOCAL_FILE" >&2
  exit 1
fi

echo "[1/3] uploading cookies to $HOST:$REMOTE_ROOT/state/cookies.json"
scp "$LOCAL_FILE" "$HOST:$REMOTE_ROOT/state/cookies.json"

echo "[2/3] fixing permissions on remote (600 + chown kanxue)"
ssh "$HOST" "sudo chown kanxue:kanxue '$REMOTE_ROOT/state/cookies.json' && sudo chmod 600 '$REMOTE_ROOT/state/cookies.json'"

echo "[3/3] verifying login on remote"
ssh "$HOST" "sudo -u kanxue bash -c 'cd $REMOTE_ROOT && .venv/bin/python -m src.check_login'"

echo "OK. cookies pushed and verified."
