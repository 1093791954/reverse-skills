# FriendlyCaptcha / mCaptcha / Cap（PoW 验证码）

## 1. 产品形态
- 三款无认知交互的 PoW 类验证码，主打"不收集任何指纹 + 隐私优先 + GDPR-friendly"。
  - **FriendlyCaptcha**：德国背景，客户多为欧洲 SMB；sitekey 申请后嵌 widget。
  - **mCaptcha**：开源（MIT）+ 自托管，纯 PoW，社区活跃。
  - **Cap / Cap-Worker**：Cloudflare Workers 上跑的开源 PoW 实现；更轻量。
- 共同点：客户端做大约 0.3-2s 的 SHA-256 前导 0 搜索，得到 `solution` 后提交；服务端 verify 通过即放行。
- 弱点：纯 PoW 对真人友好但无法检测 botnet（攻击者只要肯花算力都能过）。

## 2. 检测维度
- **难度位**：FriendlyCaptcha 默认 18-22 位、mCaptcha 可调（推荐 20-24）、Cap 默认 18。
- **挑战时效**：通常 60-120s，过期作废。
- **重放保护**：每个 challenge 一次性，sitekey + nonce 绑定。
- **指纹/行为**：均不采集，纯 PoW + 时间窗。
- **服务端速率限制**：mCaptcha 内置 rate-limit 模块，按 IP/sitekey 限请求。

## 3. 关键端点与字段
| 厂商 | 端点 | 关键字段 |
|------|------|---------|
| FriendlyCaptcha | `api.friendlycaptcha.com/api/v1/puzzle` | `sitekey`, `puzzle`(base64) |
| FriendlyCaptcha | `api.friendlycaptcha.com/api/v1/siteverify` | `solution`, `secret`, `sitekey` |
| mCaptcha | 自托管 `<host>/api/v1/pow/config` | `key`, `pow_config` |
| mCaptcha | `<host>/api/v1/pow/verify` | `string`, `key`, `nonce`, `result` |
| Cap | Workers `<host>/.well-known/cap.json` | `puzzle`, `difficulty` |

**puzzle 结构**：`base64(version | difficulty | timestamp | nonce | sitekey)`，客户端在 `nonce` 上爆破 SHA-256。

## 4. 已公开研究
- CSDN「pow-bot-deterrent：轻量级证明工作量反机器人解决方案」(146642443)：综述 PoW 方案。
- CSDN「推荐开源项目：Friendly Challenge - 友好验证码解决方案」(139164280)。
- CSDN「mCaptcha 与竞争对手对比：为什么 PoW 验证码是未来趋势」(156501865)。
- CSDN「如何快速部署 mCaptcha：10 分钟搭建隐私优先的 PoW 验证系统」(143559110)。
- CSDN「mCaptcha 开源项目常见问题解决方案」(144391770)。
- CSDN「mCaptcha 统计功能使用指南」(156502105)。
- CSDN「mCaptcha API 使用教程：5 个步骤实现无缝网站集成」(156500663)。
- CSDN「通过 JavaScript 能力表征钓鱼页面」(151802284)：在 PoW captcha 站点的滥用风险一节。
- GitHub `mCaptcha/mCaptcha`、`FriendlyCaptcha/friendly-challenge`、`tiagorangel1/cap`：源码可读。

## 5. 防御性分析思路（授权审计）
1. PoW 全部纯算可写：拿 puzzle → for nonce in counter: hash = sha256(puzzle + nonce); if hash[:diff_bits]==0: break。
2. 难度 22 位平均 ~1s（Python `hashlib.sha256`），可多核并发。
3. solution 提交后 token 时效短，必须立即用。
4. 不可滥用：开源协议下，无授权大量请求等于 DDoS；研究阶段限速到每秒 1 个。
5. PoW 类对 IP 信誉无依赖，住宅代理与数据中心 IP 通过率近似。
6. 主要缺陷研究：Cap-Worker 早期版本 nonce 范围窄，曾被预计算 rainbow table（已修复）。

## 6. 已知缓解 / 更新历史
- 2023 FriendlyCaptcha 加 sitekey 维度难度自适应。
- 2024 mCaptcha 增加 visual-pow（可选展示进度条提升用户感知）。
- 2025 Cap 引入 multi-puzzle 模式（一次签发多个 puzzle 减少 round-trip）。
- PoW 方案的根本缓解：上层套 IP 信誉/速率限制，纯 PoW 对自动化威慑有限。

## 7. 待研究问题
- mCaptcha PoW 的内存难度变种（argon2 etc.）落地情况。
- Cap 与 Cloudflare Turnstile 的差异点（Turnstile 也声称"PoW + 行为"）。
- PoW + behavioral 联用方案的工业化案例。
