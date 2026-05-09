# Kasada（x-kpsdk-* 系列）

## 1. 产品形态
- 纯无感、强 PoW、强 WASM/VMP 的反爬产品。
- 主要客户：澳大利亚票务（Ticketmaster AU）、银行、北美电商部分。
- 关键 header：`x-kpsdk-ct`（client token，含指纹 + 行为 hash）、`x-kpsdk-cd`（compute data，PoW + payload）、`x-kpsdk-v`（版本）、`x-kpsdk-im`（implementation flag）。

## 2. 检测维度
- **PoW**：SHA-256 双重哈希前导 N 位 0，难度由服务端动态调整，CPU 消耗大；纯算可做但服务端会校验 timing（太快太慢都拒）。
- **WASM/VMP**：核心计算包在 WebAssembly 中，外层 JS 是 packed VMP，opcode dispatcher 难还原。
- **指纹**：Canvas/WebGL/Audio/Font/Hardware/UA-CH。
- **行为**：mouse/scroll/keyboard 序列。
- **TLS JA3 / JA4 / HTTP2 SETTINGS** 强校验。
- **服务端打分**：边缘 worker，不通过直接 429。

## 3. 关键端点与字段
| 端点 | 字段 |
|------|------|
| `/<random>/api/v1/sensor/...`（按客户路径变） | POST sensor 上报 |
| `https://<host>/<path>` 业务接口 | header `x-kpsdk-ct`, `x-kpsdk-cd`, `x-kpsdk-v` |
| 主 JS：`fp.js` / `ips.js`（名字按租户随机） | WASM 引导 |

**x-kpsdk-cd**：JSON `{"workTime":<ms>,"id":<n>,"answers":[hex...],"version":"...", "duration":<ms>}` 的 base64。`answers` 是多次 PoW 的解。

## 4. 已公开研究
- 中文：CSDN 关于 Kasada 的中文资料较少（命中 ~20 篇但深入度不高）；多在英文圈讨论。
- GitHub 多个 `kasada-bypass`、`kasada-solver` 项目（合法性需谨慎）。
- 商业方案：CapSolver `KasadaCaptchaSolver`、2captcha `kasada` 任务类型。
- 看雪零星英文翻译贴：详解 PoW 难度计算与 timing 检查窗口。

## 5. 防御性分析思路
1. 抓 sensor 主 JS，先做 prettify + AST unpack；定位 WASM 加载入口（多用 `WebAssembly.instantiate` 配合 base64 字节）。
2. WASM 反汇编（wabt → wat）：找 export `pow`, `compute`, `sign`；多为 SHA-256 + 自定义 mix。
3. PoW timing：实测 < 800ms 或 > 5s 都被服务端打分降低，需要按真机分布投递。
4. `x-kpsdk-ct` 一次有效，跨请求需重新生成。
5. 调研建议：用真浏览器 + stealth 拿 token，再持久化短窗口（10-30s）。

## 6. 已知缓解 / 更新历史
- 2022 PoW 难度从固定升级为动态。
- 2023 加入 WASM 内部反调试（计算时检测 `performance.now()` 抖动）。
- 2024 与 Cloudflare/AWS 集成，沿用 IP 信誉。
- 客户路径前缀（`/<random>/api/...`）随租户与日期变化，需先 prefetch HTML。

## 7. 待研究问题
- 服务端 timing 容忍窗口的精确边界。
- WASM 内反调试的具体实现。
- `x-kpsdk-im` 各值含义与对应版本。
