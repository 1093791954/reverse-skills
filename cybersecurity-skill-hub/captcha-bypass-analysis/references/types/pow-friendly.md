# PoW 验证码（Proof-of-Work）

## 1. 题型描述
- 客户端做 SHA-256 / Scrypt 等哈希难题搜索（前导 N 位 0），提交解作为通过凭证。
- 代表：FriendlyCaptcha、mCaptcha、Cap（基于 SHA-256）、Cloudflare Turnstile（混合）、极验 v4（pow_sign）、Kasada（双重 SHA-256）。
- 优点：无需 UI 交互，对盲人/老人友好；对纯数据中心爬虫成本指数级。
- 缺点：低端设备体验差；GPU/服务器侧搜索几乎无成本。

## 2. 检测维度
- **难度（leading zero bits）**：4~28 位不等。
- **timing**：解出耗时必须在 [t_min, t_max] 区间内（否则判作脚本/特殊硬件）。
- **payload 绑定**：哈希输入含 server-issued challenge + ts + sitekey；challenge 一次性。
- **指纹关联**：与设备指纹一起评估，避免单纯 PoW 被算力穿。

## 3. 算法骨架
```
challenge = server_random  # base64
prefix = SHA256(siteKey || challenge || ts)
for nonce in 0..N:
    h = SHA256(prefix || nonce)
    if leading_zero_bits(h) >= difficulty:
        answer = (nonce, h)
        break
```
- FriendlyCaptcha：Scrypt-based（更慢但更难 GPU 加速）。
- 极验 v4 pow_sign：明文是若干字段拼接 + ts，求 SHA-256 前 4 位 0 的 nonce。
- Kasada：双重 SHA-256 + 多任务并发（answers 是数组）。

## 4. 已公开研究
- CSDN「【探索】无形验证码 —— PoW 算力验证」：Hashcash、设计原理。
- CSDN「工作量证明在验证码中的实际应用」：极验场景。
- CSDN「极验4滑块验证码 pow_sign 参数逆向实战」：调试 + SHA256 多参数拼接。
- CSDN「【黑产攻防道04】利用 pow 工作量证明降低黑产的破解效率」。
- CSDN「干掉图形验证码！基于 PoW 的 Cap 验证码集成指南」：Cap + Vue3 + Nestjs。
- CSDN「pow-bot-deterrent：轻量级证明工作量反机器人解决方案」：多线程 WASM + Scrypt。
- CSDN「推荐开源项目：Friendly Challenge」。
- CSDN「终极 Cap 隐私保护指南」：自托管 CAPTCHA。
- 论文 "Proof-of-Work as Anti-Sybil Tool"。
- mCaptcha 官方文档（开源 Rust 实现）。

## 5. 防御性分析步骤
1. 找到 PoW 端点：抓包看 request 中是否有 ts/nonce/zeros/answer 之类字段。
2. 离线复现：把 challenge + 拼接逻辑用 Python/Go/Rust 重写，纯 SHA-256 暴力。
3. timing 控制：人为延迟到合理区间，否则被服务端打回。
4. 多 worker 并行：同一 challenge 不能复用，注意 idempotency。
5. 与指纹联动：单 PoW 通过不够，整体行为评分仍要过线。

## 6. 缓解 / 趋势
- Scrypt / Argon2 替代 SHA-256，让 GPU 加速困难。
- 难度动态化：根据 IP 信誉/历史评分实时调整。
- 与 WASM 紧耦合，让纯算实现需要复刻 WASM 行为。
- Apple Private Access Token (PAT) / Privacy Pass：用证书替代 PoW 给苹果设备打分。

## 7. 待研究
- Argon2 在客户端的可用难度上限（兼顾低端设备）。
- 极验 v4 pow_sign 难度的服务端调度策略。
- Privacy Pass IETF draft 进展与浏览器实现现状。
