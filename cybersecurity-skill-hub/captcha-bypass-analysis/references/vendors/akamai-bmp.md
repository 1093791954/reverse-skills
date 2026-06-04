# Akamai Bot Manager（BMP / BMM / sensor_data + _abck）

## 1. 产品形态
- **Web BMP**：浏览器场景，下发 `<hash>.js`（多以路径包含 `_bm` 或随机 hash），收集 sensor_data，post 到 `/_bm/_data` 类端点。
- **Mobile BMP（BMM）**：iOS/Android SDK，使用 `bmak` / `bmcm` 收集设备指纹 + 行为，签名后跟随业务请求头 `x-acf-sensor-data`。
- 大客户：DHL、KAYAK、UA、JetBlue、众多航司、Nike、Walmart。

## 2. 检测维度
- **sensor_data**：`<n>;<n>;<n>;<n>;<...>` 多段以 `,` 与 `;` 分隔的字符串，含：
  - 行为段（鼠标/触摸/键盘/滚轮，dx,dy,t,event_type）
  - 环境段（UA, screen, plugins, languages, do not track, hardwareConcurrency, deviceMemory）
  - 时间段（performance.timing 各阶段）
  - 指纹段（Canvas hash, WebGL renderer/vendor, AudioContext sum, font 列表 hash）
  - 异常段（webdriver、permissions、iframe 嵌套）
- **_abck cookie**：服务端发，本地不可改；多次刷新 + 行为合规后 `~0~` 三个 0 改成 `~-1~` / `~0~-1~-1~` 视为有效会话。
- **bm_sz / ak_bmsc / bm_sv**：辅助节流与 session 标识。
- **TLS JA3/JA4 + HTTP/2 SETTINGS + ALPN 顺序**。
- **frequency / IP**：CDN 边缘统计高频 sensor_data 异常率。

## 3. 关键端点与字段
| 端点 | 字段 |
|------|------|
| `/<hash>.js` 或 `/_bm/get_params` | 下发 JS，里面有 `bd`, `bod`, `n` 等动态参数 |
| `/_bm/_data` 或站点专属 POST 路径 | body=sensor_data, header=`X-Akamai-...` |
| 业务 GET | 校验 `_abck`，无效返回 403 + Set-Cookie 重置 |

**sensor_data 解码**：第 1 段是 `version;0;<...>`；以 `-` 后的负整数（-105、-101、-115、...）做 type id 区段切分。

## 4. 已公开研究
- CSDN「阿卡迈 Akamai 逆向分析」(142049165)：三次请求生成 `_abck`/`ak_bmsc`/`bm_sz` 流程。
- CSDN「2024-12 月 akamai_2.0-sensor-data 之 cookie 反爬分析详细教程（上）」(144276074)：DHL 案例 sensor_data 还原。
- CSDN「Akamai 最新逆向分析，sensor_data，阿卡迈，abck」(134553689)：AST 定位 58 位关键数组。
- CSDN「Akamai JS _abck sensor_data 第三个参数 20%（18）」(120672379)：参数变化对比。
- CSDN「Akamai 阿卡迈 _abck 逆向 sensor_data（一）：从韩亚航空案例」(91390254)：核心数组与多段标识详细分析。
- 看雪「Akamai 反爬虫绕过实战」多帖。
- GitHub `Akamai-Bypass`、`akamai-sensor-data-research`（仅协议研究）。

## 5. 防御性分析思路
1. 抓 `_bm` JS 直接保存，`prettify + AST unflatten` 后搜 `bd=`, `bot=`, 数字字面量大数组，是 sensor_data 拼装的位运算字典。
2. 把 sensor_data 拆成 `events`、`fingerprint`、`timing` 三类，对比真人浏览器的实际值（在合法授权环境下采集 baseline）。
3. `_abck` 的「~0~」校验位很关键：第三个 `~` 后值非 `-1` 时未通过，需多次行为合规请求。
4. UA-CH 必须填全 (`Sec-CH-UA`, `Sec-CH-UA-Platform`, `Sec-CH-UA-Mobile`)；与 sensor_data 内字段保持一致。
5. TLS 层强烈推荐 `curl_cffi browser="chrome131"`，纯 requests 几乎一定 403。

## 6. 已知缓解 / 更新历史
- 2.0 sensor_data：2022 引入更长字段、加入加密段。
- 2024 起字符串数组动态化（每天 hash 变化），AST 还原难度上升。
- 增加对 `Notification.permission`、`Permissions.query` 的真实性校验。
- BMP Pro 模型：用 LightGBM 做实时打分。

## 7. 待研究问题
- sensor_data 各段间的 checksum 算法（是否每段独立 CRC）。
- BMM mobile 的 `x-acf-sensor-data` header 与 web 是否同源？
- _abck 三段 ttl 的实际过期边界。

## 8. Akamai BMP Mobile / BMM 子产品（R4 补充）

- **BMP** 全称 *Bot Manager Premier*，覆盖 Web；**BMM**（Bot Manager Mobile）面向原生 App，2021 年正式商品化。中文圈也称"akamai 移动端"、"Akamai 移动 BMP"。
- BMM 的核心载荷：Native SDK（iOS .framework / Android .aar）输出一段 base64 token，名为 **`x-acf-sensor-data`**（部分客户用 `X-Sensor-Data`），与 Web 端 `_abck`/`bm_sz` 不同字段，但内部同样是经修改版 RC4 + AES-CCM + SHA-256 包装的事件流。
- 关键差异（vs Web BMP）：
  - 移动端 sensor 收集陀螺仪/加速度计/Wi-Fi BSSID/电池/语言设置等 Web 没有的维度；
  - SDK 内部直接读 `Build.MODEL`、`Settings.Secure.ANDROID_ID`、`getSimSerialNumber`；
  - 提交频次更低（多在 App 启动 + 关键接口前），所以风控阈值比 Web 严。
- **akamai-bm-telemetry** 是 Web 侧 sensor 上送途中常见 query 名。
- **akamai___sensor_data___**（带连续下划线）是 v2 sensor_data 的"已编码"变体，长度可达 4000-8000 字节。

## 9. 移动端逆向研究（R4 补充）

- CSDN「akamai 指纹和 akamai BMP 移动端 sensor 风控分析」(104104680)：综合介绍 Web vs Mobile sensor。
- CSDN「【亲测免费】探秘 Akamai BMP 生成器：绕过机器人检测的新利器」(139821325)：商业 BMP 生成器接入说明。
- CSDN「Akamai 移动端 Sensor 数据采集与 BMP 风控机制深度解析」(154627447)。
- CSDN「如何优雅的绕过 Akamai 验证」(140620829)：含 mobile sensor 一节。
- CSDN「【观察】Akamai：做中国泛娱乐企业出海的"加速器"」(102493250)：业务背景。
- 推荐工具链：unidbg / Frida + objection；定位 native 函数 `Java_com_akamai_botman_*` 与 iOS `_aks*`。
- 商业方案：CapSolver / Sadcaptcha 提供 `AkamaiBMPTask`，输入 device profile + endpoint，返回 sensor token。

## 10. 待研究问题（追加）
- BMM SDK 各版本（v3 → v4）字段对照与签名算法变化点。
- Akamai 服务端是否对 mobile token 与 IP/UA-CH 一致性做交叉评分。
