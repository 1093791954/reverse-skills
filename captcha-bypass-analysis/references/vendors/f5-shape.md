# F5 Shape Security（__TS01__ / TS01* cookie）

## 1. 产品形态
- F5 收购 Shape Security 后整合的边缘反爬产品，企业线名称：**F5 Distributed Cloud Bot Defense**（前身 Shape Enterprise Defense）。
- 客户端表征：cookie 头 `__TS01XXXX=...`、`TSXXXXXXXX=...`、`TS_XXXXXXX=...`（XXXX 是 8 位 hash 化的客户标识）。
- 部署方式：JS Snippet + iRule（F5 BIG-IP 模块），少量站走纯边缘。
- 客户：航空、银行、零售（American Airlines / Delta / Walmart 部分接口）。

## 2. 检测维度
- **TS01 cookie**：长度 50-200 字节，base64-like，内嵌时间戳/IP/UA/事件统计；服务端硬签名。
- **TLS 指纹**：JA3/JA4 + ALPN h2 强校验。
- **行为**：mousemove/touch 事件被采集，时序压缩后塞 cookie payload。
- **指纹**：Canvas/WebGL/Audio + Permissions + Battery；Chromium native code 校验严格。
- **频率/IP 信誉**：明显基于 IP 历史；数据中心 IP 即使指纹完美也降级到强校验。
- **环境一致性**：Function.prototype.toString 链路被多次校验，简单 Proxy 兜底失效。

## 3. 关键端点与字段
| 标识 | 含义 |
|------|------|
| Cookie `__TS01XXXX` / `TSXXXXXXXX` | 通行证（核心） |
| Cookie `TS_XXXXXXX` | 二级会话信息 |
| Header `x-shape-pi` / `x-shape-tk` | （部分客户）业务接口签名 |
| Endpoint 客户私域 `/<random>/sjs.js` | 注入 SDK，1MB+ 大文件 |
| Endpoint `/<random>/te-fp` | 上报指纹 payload |

**__TS01 内容**：约 50-200 字节，前 4 字节 magic，随后是 timestamp + nonce + 多段 RC4-like 编码体；最末 16 字节为 HMAC。

## 4. 已公开研究
- 中文圈在 CSDN/52pojie 几乎没有公开成体系的逆向（`F5 Shape __TS01` 命中数极少，且大多被搜索引擎噪音文章占据）。
- 英文 GitHub：`shape-security-bypass`、`f5-shape-bypass` 等关键词存在零星 PoC，多被 takedown。
- ScrapingBee / ZenRows / Bright Data 商业代理普遍以"F5/Shape 兼容"为卖点，是黑盒方案。
- 推测中文文章用别名（"F5 边缘"、"Shape 防护"、"绿盾代爬"）发表，需用更广关键词扫。

## 5. 防御性分析思路（授权审计）
1. 触发：业务 401/403，响应包含 `Set-Cookie: __TS01XXXX=` 和带 sjs.js 的 HTML。
2. 拉 sjs.js 并先做 webpack 拆解 + AST flatten 还原；体积大、字符串数组多。
3. 定位 RC4-like 编码：通常在 `function _0xXXXX(a, b)` + 256-byte permutation 数组。
4. HMAC 末段：找 `crypto.subtle.sign("HMAC", ...)` 或纯 JS HMAC-SHA256 实现，secret 来自 cookie 第二段。
5. 因 cookie 必须 server-signed → 必须真跑客户端逻辑或商业代爬代理；纯静态算法还原难度高。
6. 实操常用：商业指纹浏览器（Multilogin、AdsPower）+ 住宅代理 + curl_cffi `chrome131` 拼出方案。

## 6. 已知缓解 / 更新历史
- 2021 cookie 名加 client-specific suffix（变成 `__TS01XXXX`，XXXX 客户专属），扫描类工具失效。
- 2023 加 native code 链路校验。
- 2024 强化 IP/历史评分，无 history 的"干净"IP 第一次访问基本必经强校验。
- 2025 reportedly 灰度 wasm 段。

## 7. 待研究问题
- 不同客户的 cookie 格式版本号是否一致。
- HMAC secret 的 server / client 协商时机。
- wasm 段的 dispatcher 是否复用 DataDome 风格的 VMP。

## 8. R5 深化：英文检索与 GitHub 兜底

### 8.1 GitHub API 检索（本轮 R5 新增）

```
GET https://api.github.com/search/repositories?q=f5+shape+__TS01
→ total_count: 0
```

GitHub 上**无公开标注 "f5+shape+__TS01" 的活跃仓库**（已被 takedown 或本就不存在）。
CSDN 同关键词 "F5 Shape __TS01" 命中 4936 篇但绝大多数为噪声（"f5 刷新键"等）。
**结论：GitHub 公开层面不可用，只能依赖商业指纹浏览器/住宅代理黑盒方案，仍标 [NEEDS_VERIFICATION]。**

### 8.2 R5 新命中的 CSDN 真专题（共 ~10 篇）

| articleid | 标题 | 备注 |
|-----------|------|------|
| 127145748 | f5 shape 逆向 | 早期版本 |
| 128136145 | f5 shape 最新版逆向分析 | |
| 96071901 | 不只是 TikTok：解构 F5 Shape 在国际航空大厂的应用与逆向成本 | 综述 ⭐ |
| 141189815 | f5 shape 逆向 | |
| 133108236 | F5 shape 逆向分析 | |
| 128675914 | F5 shape 最新版逆向分析（航空类）xbk | xbk = 飞机航空头 |
| 138187743 | F5 Shape 最新版逆向分析 — 加解密和补环境 | ⭐ 含补环境 |
| 129356868 | F5 shape 最新版逆向分析（达美航空、TikTok） | ⭐ |
| 158247140 | F5 Shape 逆向工程实战：解析航空类的 xbk 反风控机制 | 2025 新版 ⭐ |
| 96713800 | F5 Shape 逆向实战：完整破解某达美航空 header 加密的过程与避坑指南 | 完整过程 ⭐⭐ |
| 158753473 | F5 Shape：JSVMP 二次加密的无敌 Header 反爬实战（TikTok/航司） | ⭐⭐ JSVMP 主题 |

### 8.3 关键发现（R5 新增）

1. **航空业是 F5 Shape 主战场**：达美 (Delta) / 美联 / 韩亚 等航司明确出现在中文资料里
2. **TikTok 部分接口走 F5 Shape**：与抖音 X-Bogus 不冲突，是不同接口分别防护
3. **2025 版引入 JSVMP**：158753473 表明最新版加了 jsvmp 二次加密，与 DataDome / hCaptcha 趋同
4. **xbk** 是社区对"航空类 F5 客户端"的简称，可作为搜索关键词

[NEEDS_VERIFICATION] 上述 articleid 仍待人工验证全文质量，但标题与本厂商主题强相关。
