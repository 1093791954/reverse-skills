# TLS / HTTP2 指纹（JA3 / JA4 / JA4H / JA4S / JARM / HTTP2 SETTINGS）

## 1. 指纹标准
| 名称 | 范围 | 计算 |
|------|------|------|
| JA3 | TLS Client Hello | 拼 (version, ciphers, extensions, ec_curves, ec_point_fmts) → MD5 |
| JA3S | TLS Server Hello | 同思路服务端版 |
| JA4 | TLS Client Hello（升级版） | 三段：JA4_a 可读、JA4_b 密码套件 SHA256 前 12 位、JA4_c 扩展 SHA256 前 12 位；排序后哈希 |
| JA4H | HTTP/1.1+2 头部顺序 | 头字段顺序 + cookie/auth 存在性 |
| JA4S | TLS Server Hello（JA4 版） | 服务端 |
| JA4SSH | SSH | 类似 |
| JA4D | DHCP | 类似 |
| JARM | TLS 服务器栈指纹 | 多次 ClientHello 探测 |
| HTTP/2 fingerprint | SETTINGS frame 顺序、WINDOW_UPDATE、PRIORITY、HEADERS pseudo-header 顺序 | "akamai_h2_fingerprint" 一类 |
| HTTP/3 fingerprint | QUIC TPP / 加密参数 | 新兴 |

## 2. 检测点
- 同一声称 UA 必须配套合理的 JA3/JA4。例如 UA 是 Chrome 131 但 JA3 是 Go default → 直接拒。
- HTTP/2 SETTINGS：浏览器顺序与 lib（Go/Python/Java）顺序差异巨大。
- header 顺序：浏览器 `accept` / `accept-encoding` / `accept-language` / `cache-control` 顺序固定。
- ALPN 顺序：`h2,http/1.1` vs `http/1.1,h2`。
- 0-RTT、PSK、key share groups 顺序。

## 3. 工具栈（合规授权场景）
- **curl_cffi**（Python，基于 libcurl-impersonate fork）：`browser="chrome131"` 一行配齐 TLS+HTTP2。最受推荐。
- **tls-client**（Go + Python binding，bogdanfinn/tls-client）：profile 库丰富。
- **hrequests**（Python，async）：基于 tls-client。
- **azuretls**（Go）：可定制 ClientHello。
- **cycletls**（Node）：JA3 自定义。
- **node-fetch + js-fetch-mod**：复杂但可控。
- **Go `utls`**（refraction-networking）：底层 TLS impersonation 库，所有上层 Go 工具的根。
- **curl --tls13-ciphers** / **openssl s_client** 配合：调试用。

## 4. 已公开研究
- CSDN「HTTPS 中的 JA3，JA4，JA3S 介绍及计算」(160122496)：算法 step by step。
- CSDN「别再只用 JA3 了！聊聊 JA4 指纹的独特之处」(98420939)：Chromium 源码层 JA4 随机化方案。
- CSDN「TLS 指纹技术深度解析：JA3 与 JA4 的原理、演进与实战应用」(150550044)。
- CSDN「Python 爬虫进阶：TLS 指纹对抗，彻底解决 JA3/JA4 指纹被识别问题（2026 终极版）」(159254518)：curl_cffi 一行绕过 + Scrapy 集成 + 动态指纹池 + 高匿代理。
- CSDN「浅聊报文指纹 JA3 JA4」(144562731)：openssl 自签证书与 Hello 报文。
- CSDN「JA4+ vs JA3：为什么 JA4+ 成为新一代网络指纹识别标准？」(153803853)：JA4 / JA4D / JA4H / JA4SSH 多协议。
- CSDN「Cloudflare TLS 指纹识别反爬终极对抗方案」。
- GitHub `salesforce/ja3`、`FoxIO-LLC/ja4`：标准实现。
- GitHub `lwthiker/curl-impersonate`、`lexiforest/curl_cffi`：fork 浏览器 TLS。

## 5. 防御性分析步骤
1. 检测目标 IP 的 JA3/JA4：用 `tlsfp.dev`、`tls.peet.ws`、`browserleaks.com/tls`、`ja4db.com` 拿目标 baseline。
2. 测试自己的客户端：访问同样的 fingerprint 测试服务，比对差异。
3. 选 lib：`curl_cffi`（最快上手）→ `tls-client`（profile 多）→ `utls` 自写（最灵活）。
4. HTTP/2 settings：注意 SETTINGS_INITIAL_WINDOW_SIZE / SETTINGS_HEADER_TABLE_SIZE 顺序。
5. 与 UA-CH/真 cookie/真 referer 联动；TLS 对了但 UA-CH 错也会被识别。

## 6. 缓解 / 趋势
- 浏览器持续动态化（Chrome 启用 GREASE 随机扩展位）让 JA3 不稳定 → 推动 JA4 排序后哈希。
- 厂商引入 JA4+ 多协议联合，单 JA3 远远不够。
- 越来越多服务在边缘做 ML 打分（不只是黑白名单）。

## 7. 待研究
- HTTP/3 QUIC fingerprint 大规模部署后的检测点。
- curl_cffi 与真 Chrome 在 GREASE 随机化上的差异。
- 各 lib 在 Linux/Mac/Windows 上 JA3 是否一致（OpenSSL/BoringSSL 影响）。

## 8. JA4+ 全协议矩阵（R4 补充，已 API 验证）

R4 通过 CSDN API `q='JA4D JA4SSH'` / `q='JA4H JA4T JA4L'` 抽 51 篇，按 FoxIO-LLC/ja4 标准整理：

| 标识 | 协议层 | 输入要素 | 用途场景 |
|------|--------|----------|---------|
| JA4 | TLS Client Hello | version + cipher + ext + ALPN | Web/API 反爬 |
| JA4S | TLS Server Hello | server hello extensions | 探测目标侧栈 |
| JA4H | HTTP/1.1+2 请求 | 方法 + 头序 + Accept-Language + cookie 存在 | UA-CH 联合校验 |
| JA4T | TCP | TCP options + window size | 操作系统侧识别（区分容器/虚机） |
| JA4L | TCP latency | 三次握手 RTT 特征 | 区分代理链 |
| JA4SSH | SSH client | KEX + cipher 顺序 | 反扫描器/反 botnet |
| JA4X | X.509 证书 | issuer + subject + ext + sig alg | 自签证书识别 |
| JA4D | DHCP | DHCP option 顺序 | 内网设备识别 |
| JA4R | TLS Client Hello（raw 序）| 同 JA4 但保留扩展原始顺序 | 抓包分析时与 JA4 对照 |

新增 articleid 入口（已 API 验证）：
- (153804215) 零基础学习 JA4+：从安装到分析的入门教程
- (153804470) JA4+ 在恶意软件检测中的应用：5 个真实案例解析
- (133747866) tls 指纹之 ja4 发布！！！
- (148993129) JA4+ 数据库完全指南：如何利用 ja4db.com 查询指纹信息
- (143099496) 【编程笔记】libpcap 应用之 JA3 指纹

## 9. 待研究（追加）
- JA4T / JA4L 在 Cloudflare / Akamai 边缘的实际启用率（推测 < 5%，多用于 IDS）。
- curl_cffi 是否覆盖 JA4R（保留扩展原始顺序）；目前观测到对 JA4 主指纹覆盖较好，JA4R 还在 GREASE 上有差异。
