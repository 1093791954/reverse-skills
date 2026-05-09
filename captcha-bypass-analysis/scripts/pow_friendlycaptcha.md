# PoW 计算示例（FriendlyCaptcha 类）

配套 SKILL.md Path 12。本文档说明 Proof-of-Work 验证码的"客户端解题"原理与等价代码。

合规边界：FriendlyCaptcha / mCaptcha 都是开源 PoW 实现，本身无任何"反爬服务"性质；
本笔记仅作算法教学；不针对任何具体网站做"过码服务"。

---

## FriendlyCaptcha 协议（开源，可在自有站点部署）

服务器下发挑战：
```json
{
  "puzzle_id": "abc123",
  "puzzles": [
    {"d": 6, "n": 51, "t": "..."},
    ...
  ]
}
```
- `d`（difficulty）：要求 SHA-256 输出的前 d 位为 0
- `n`：要 求解的 puzzle 数量（通常 51 个）
- `t`：每个 puzzle 的输入前缀

客户端要做的事：
```python
import hashlib

def solve_puzzle(prefix: bytes, difficulty: int) -> int:
    """找到 nonce，使 SHA256(prefix || nonce_bytes) 前 difficulty 位为 0。"""
    target_bytes = difficulty // 8
    target_remainder = difficulty % 8
    nonce = 0
    while True:
        # 8 字节 little-endian nonce（FriendlyCaptcha 规范）
        candidate = prefix + nonce.to_bytes(8, "little")
        h = hashlib.sha256(candidate).digest()
        # 前 target_bytes 字节必须全 0
        if all(b == 0 for b in h[:target_bytes]):
            if target_remainder == 0:
                return nonce
            # 余位也要 0
            if h[target_bytes] >> (8 - target_remainder) == 0:
                return nonce
        nonce += 1


def solve_friendlycaptcha(challenge: dict) -> str:
    """返回 base64 编码的解。"""
    import base64
    solutions = []
    for p in challenge["puzzles"]:
        prefix = bytes.fromhex(p["t"])
        nonce = solve_puzzle(prefix, p["d"])
        solutions.append(nonce.to_bytes(8, "little"))
    return base64.b64encode(b"".join(solutions)).decode()
```

可用 multiprocessing.Pool 把每个 puzzle 派给不同 CPU 核（PoW 天然并行）。

---

## mCaptcha 协议

类似 FriendlyCaptcha，区别在于 mCaptcha 的 difficulty 通常更低（在自托管站点常见 5~7 位 0）。

---

## Cloudflare Turnstile 中的"PoW 类挑战"

Turnstile 不是纯 PoW，但在某些"managed challenge"分支会让 V8 跑一段计算密集脚本，
并通过执行时长 / V8 特征 来识别"是不是真 Chrome 引擎"。
分析方向：定位 challenge.js 中的循环 → 在脱机 V8 中运行 → 抓返回 token。

---

## 极验 v4 PoW

参数：`pow_msg` + `pow_sign` + `pow_detail`（来自 captcha-id 的 captcha_load 接口下发）。
算法：HMAC-SHA256(pow_msg, key) + 难度位检查；每次 ~50ms 开销。

---

## 参考链接（待重启联网后验证补全）

- [NEEDS_VERIFICATION] friendlycaptcha.com/docs/protocol
- [NEEDS_VERIFICATION] github.com/FriendlyCaptcha/friendly-captcha
- [NEEDS_VERIFICATION] github.com/mCaptcha/mCaptcha
- [NEEDS_VERIFICATION] developers.cloudflare.com/turnstile/concepts/widget
