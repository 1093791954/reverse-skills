#!/usr/bin/env bash
# 在 VPS 上一键安装 kanxue-crawler 服务。
#
# 假设：
# - 你已经把整个项目 rsync / scp 到了 /opt/kanxue-crawler
# - 你已经按 deploy/kanxue-crawler.env.example 准备好了 /etc/kanxue-crawler.env
# - Ubuntu / Debian 系统
#
# 用法（在服务器上以 root 跑）：
#   sudo bash /opt/kanxue-crawler/deploy/install.sh

set -euo pipefail

ROOT=/opt/kanxue-crawler
USER=kanxue
GROUP=kanxue

if [[ $EUID -ne 0 ]]; then
   echo "请用 sudo / root 跑这个脚本" >&2
   exit 1
fi

echo "[1/7] 安装系统依赖"
export DEBIAN_FRONTEND=noninteractive
export NEEDRESTART_MODE=a
export NEEDRESTART_SUSPEND=1
apt-get update -y
apt-get install -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" \
    python3 python3-venv python3-pip ca-certificates sqlite3

echo "[2/7] 创建专用用户 $USER（已存在则跳过）"
if ! id "$USER" &>/dev/null; then
    useradd --system --home "$ROOT" --shell /usr/sbin/nologin "$USER"
fi

echo "[3/7] 修复目录权限"
mkdir -p "$ROOT/output" "$ROOT/state"
chown -R "$USER:$GROUP" "$ROOT"
chmod 700 "$ROOT/state"
[[ -f "$ROOT/state/cookies.json" ]] && chmod 600 "$ROOT/state/cookies.json" || true

echo "[4/7] 创建虚拟环境并装依赖"
sudo -u "$USER" python3 -m venv "$ROOT/.venv"
# 配置 pypi 镜像（清华源），加快国内服务器拉包
sudo -u "$USER" "$ROOT/.venv/bin/pip" config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple || true
sudo -u "$USER" "$ROOT/.venv/bin/pip" install --upgrade pip
sudo -u "$USER" "$ROOT/.venv/bin/pip" install -r "$ROOT/requirements.txt"

echo "[5/7] 校验 SMTP env 文件"
if [[ ! -f /etc/kanxue-crawler.env ]]; then
    echo "WARNING: /etc/kanxue-crawler.env 不存在，先 cp $ROOT/deploy/kanxue-crawler.env.example /etc/kanxue-crawler.env 并填好密码"
fi
chmod 600 /etc/kanxue-crawler.env 2>/dev/null || true

echo "[6/7] 安装 systemd 单元"
install -m 644 "$ROOT/deploy/kanxue-crawler.service" /etc/systemd/system/kanxue-crawler.service
install -m 644 "$ROOT/deploy/kanxue-crawler.timer"   /etc/systemd/system/kanxue-crawler.timer
systemctl daemon-reload
systemctl enable --now kanxue-crawler.timer

echo "[7/7] 状态自检"
systemctl status kanxue-crawler.timer --no-pager || true
echo
echo "==========================================="
echo " 安装完成。"
echo " 立刻手动跑一次（不等 timer）："
echo "   sudo systemctl start kanxue-crawler.service"
echo " 看日志："
echo "   journalctl -u kanxue-crawler -n 200 -f"
echo " 看下次什么时候触发："
echo "   systemctl list-timers kanxue-crawler.timer"
echo "==========================================="
