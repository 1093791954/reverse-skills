# 无感行为验证（Invisible / Passive）

## 1. 题型描述
- 用户视觉无感知，全靠后台对环境与行为打分；无法通过即降级到弹题。
- 代表：reCAPTCHA v3 / Cloudflare Turnstile（managed 模式） / hCaptcha Enterprise passive / Akamai BMP / Imperva BotManager / DataDome / PerimeterX / Kasada / 极验无感 / 网易易盾 inline / Vaptcha invisible。

## 2. 检测维度（最广覆盖的合集）
- **指纹**：UA-CH、Canvas、WebGL、AudioContext、Font 列表、navigator/window 全集、HardwareConcurrency、DeviceMemory、Battery（已弃但仍被读）、Permissions API 五项交叉、`screen` 全字段、`Intl` 时区、Media devices。
- **TLS / HTTP2 / HTTP3**：JA3/JA4/JA4H/JA4S、HTTP/2 SETTINGS frame 顺序、ALPN 顺序、HTTP/3 QUIC 指纹。
- **行为**：mouse/wheel/touch/keystroke 时序与分布（最少 1~3s 静默观察）；focus/blur/visibilitychange。
- **页面 timing**：performance.timing/resourceTiming，加载时序与真人分布对比。
- **session 链**：cookie chain（cf_clearance、_abck、reese84、_px3、datadome 等）。
- **网络层**：IP 信誉、ASN、出口 ASN 与 client 声明地区一致性。
- **历史**：同 visitor id 的累积可信分。

## 3. 关键参数 / 字段
- reCAPTCHA v3 `g-recaptcha-response`（含 score 后端可见）。
- Turnstile `cf-turnstile-response`（边缘验证后下发 cf_clearance）。
- hCaptcha Enterprise passive `swa=true`，只下发 N，UI 隐藏。
- Akamai `_abck` 三段（最关键的第三段必须为 -1）。
- DataDome `datadome` cookie。
- PerimeterX `_px3`（session）+ `_pxhd`（host data）。
- 极验 v4 invisible `lot_number/captcha_output` 直传。

## 4. 已公开研究
- 主要看各厂商笔记 (`vendors/recaptcha.md`、`vendors/cloudflare-turnstile.md`、`vendors/akamai-bmp.md`、`vendors/datadome.md`、`vendors/perimeterx-human.md`、`vendors/kasada.md`、`vendors/imperva-incapsula.md`)。
- arxiv「Invisible CAPTCHA Bypass」综述论文。
- CreepJS（GitHub abrahamjuliot/creepjs）：测自己浏览器在哪些字段上"露马脚"，用于评估补环境完整度。
- BrowserGap / FpJS Pro 厂商博客：他们公开的检测项清单。

## 5. 防御性分析步骤
1. 用 CreepJS 跑一遍当前浏览器/补环境，列「lies」清单 → 这就是检测点画像。
2. 对每个目标厂商，看被检测的字段子集 + 优先级。
3. 真浏览器（patchright/camoufox/nodriver/botright）+ 优质代理（住宅）+ 真实 UA 是最低门槛。
4. 评估 token 复用窗口：拿到一个高分 token 可重复多少次（多在 30s ~ 30min）。

## 6. 缓解 / 趋势
- 模型从 GBDT 走向深度学习实时打分。
- 多厂商 IP 信誉数据交换（HUMAN/Cloudflare 等）。
- Apple Private Access Token (PAT) 给 Safari 用户「攻击成本」加权。
- 越来越多对 stealth 工具的针对性 detector（playwright 特征字符串）。

## 7. 待研究
- 各厂商的 token 复用窗口的实测分布。
- IP 信誉评分 API（Spur、IPQS、IP2Proxy）的覆盖差异。
- HTTP/3 QUIC fingerprint 在 2025+ 的部署情况。

## R5 追加：Apple PAT / Privacy Pass IETF draft

### 外部 API 检索结果（R5 新增）

**IETF datatracker** （`curl https://datatracker.ietf.org/api/v1/doc/document/?name__contains=privacy-pass`）成功返回 24 篇文档：
- `slides-120-privacypass-privacy-passbbs` rev 00
- `slides-107-privacypass-privacy-pass-ecosystem` rev 00
- `slides-107-privacypass-privacy-pass-use-cases` rev 02
- `slides-110-privacypass-privacy-pass-feedback-from-use-cases` rev 00
- `slides-110-privacypass-privacy-pass-redemption-contexts` rev 00
- `slides-122-privacypass-privacy-pass-reverse-flow` rev 01
- `slides-122-privacypass-privacy-pass-for-tls` rev 00
- `draft-ietf-moq-privacy-pass-auth` rev 02

**关键 RFC**（已落地）：
- RFC 9576/9577/9578（Privacy Pass 协议族，2024 完成）
- HTTP 头：`Authorization: PrivateToken token=<base64url>`
- `WWW-Authenticate: PrivateToken challenge=<base64url>, token-key=<base64url>`

### CSDN 中文资料（R5 新增）

- CSDN 141150612：Privacy Pass 扩展——隐私增强浏览器套装使用指南
- CSDN 134754060：Aggregate Signatures with Versatile Randomization and Issuer-Hiding 多作者方案
- CSDN 129221188 / 145988440：iOS16 私密访问令牌（PAT）专题
- CSDN 115258127：苹果 M1 隐私 vs 矛盾分析（含 PAT）
- CSDN 158831301：GitHub 2FA 与 PAT 类似机制对比

### 与本技能的关联

1. **Apple PAT 充当"无验证码通道"**：当 Cloudflare / Fastly 站点检测到 Safari + Apple PAT 头，**直接放行无需任何验证码**
2. **跨厂商支持**：Cloudflare（2022-08 起）、Fastly、Akamai 部分客户支持 PAT
3. **本技能的影响**：研究滑块/极验时，若目标是 Safari/iOS 真机流量，只要走真机 PAT 即可绕过验证码层
4. **Issuer/Attester 模型**：Apple 充当 Attester（验证设备真实性），Cloudflare 充当 Issuer（签发 token）

### 协议级要点（与 PoW 验证码对比）

| 维度 | Apple PAT | mCaptcha PoW | FriendlyCaptcha PoW |
|------|-----------|-------------|---------------------|
| 用户成本 | 0（设备已签名） | CPU ~200ms | CPU ~500ms |
| 隐私性 | ⭐⭐⭐⭐⭐（盲签名） | ⭐⭐⭐ | ⭐⭐⭐ |
| 防机器人 | ⭐⭐⭐⭐⭐（Apple 设备证明） | ⭐⭐⭐ | ⭐⭐⭐ |
| 可批量伪造 | ❌（需要真 Apple 设备） | ✅（CPU 暴力） | ✅ |

[NEEDS_VERIFICATION] CSDN 中文圈对 PAT 专题文章稀少（多噪声 Apple ID 注册），主要资料源仍为 IETF datatracker + Cloudflare 官方博客 + Apple WWDC22 视频（CSDN 125719212 提及）。
