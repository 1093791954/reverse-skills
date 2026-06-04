# Imperva Incapsula（reese84 / utmvc）

## 1. 产品形态
- 边缘 WAF + 反爬，主要 cookie：`incap_ses_*`, `visid_incap_*`, `reese84`, `___utmvc`。
- reese84 是核心客户端 token，对应 Imperva BotManager 客户端 JS。
- 客户：金融、电商、传媒、票务（含部分美区与日韩站点）。

## 2. 检测维度
- **reese84**：长字符串 cookie，由前端 JS 上报后服务端签发。前端在 `/`+空白页或专用路径 GET 一段强混淆 JS（每天可能换 hash），运行后 POST `_Incapsula_Resource` 之类的端点。
- **utmvc / ___utmvc**：第二段 token，覆盖部分场景。
- **指纹**：Canvas/WebGL/Audio/Font/UA-CH，与 reese84 payload 关联。
- **TLS JA3/JA4**：必须匹配 UA。
- **行为**：少量鼠标/键盘事件采集（不是核心，主要靠指纹）。

## 3. 关键端点与字段
| 端点 | 字段 |
|------|------|
| `/<random>.js?[d=...]` 或专门路径 | 主 JS（混淆，每日 rotate） |
| `/_Incapsula_Resource?...` 或 `/<host>/<path>` POST | 上报 sensor → 拿 reese84 |
| 业务请求 | header/cookie `reese84` 必带 |

**reese84 payload**：JSON 多字段（Canvas/WebGL/Audio hash, navigator, screen, performance, plugins）→ AES + base64；服务端验证签发新的 reese84 cookie。

## 4. 已公开研究
- CSDN「Imperva incapsula 逆向分析」：JS 加密分析与 token 获取。
- CSDN「Incapsula(reese84) 逆向分析」：动态文件，编码函数多变；多接口逐步绕过。
- CSDN「reese84 加密」：详解 JS 挑战流程，多维指纹采集，4 种典型场景（普通短链、长链、84+utmvc 联用）。
- CSDN「Incapsula reese84 防护机制深度解析」：3 重验证体系（指纹/动态 JS/加密令牌）。
- GitHub 多个 `reese84-research` / `imperva-bypass` 项目（协议研究为主）。

## 5. 防御性分析思路
1. JS 文件名 hash 每天 rotate：先做日级 prefetch + diff，重点关注新引入的字符串数组。
2. 主 JS 混淆是「字符串数组 + control-flow flatten + dead code」典型组合，babel-pass 三连。
3. AES key 派生：从 `Math.fround` / `parseInt` 类的种子算出，注意浮点精度。
4. 长链场景 `reese84 + utmvc`：两个 cookie 共同生效；只解一个不够。
5. 频率：单 IP 单 UA 失败几次后强制升级到 captcha。

## 6. 已知缓解 / 更新历史
- 2022 reese84 升级，加入 `Permissions.query` 多项一致性。
- 2023 主 JS 启用 jscrambler-style 强混淆。
- 2024 与 Imperva DDoS 模块整合，对短时高并发段直接 block。

## 7. 待研究问题
- reese84 与 utmvc 各自的 ttl 与覆盖场景边界。
- 主 JS 字符串数组的轮换周期（1d / 7d）。
- 新版指纹采集是否包含 GPU compute fingerprint。

## 8. CSDN 文章 articleid 表（R4 补充，已 API 验证）

- (158508337) 「reese84 加密」
- (158141101) 「Incapsula reese84 防护机制深度解析：为什么你的爬虫总是被封？」
- (142337871) 「Incapsula（reese84）逆向分析」
- (152127264) 「Incapsula 智能防护系统 reese84 算法深度解析与实战」
- (152211572) 「Incapsula 智能防护机制技术解析：reese84 算法与企业级安全架构」
- (154643043) 「手把手教你绕过 Incapsula reese84 验证：从 cookie 生成到实战破解」
- (128136632) 「Imperva incapsula 逆向分析」
- (152177763) 「Incapsula UTMVC 参数处理技术深度解析：__utmvc 生成算法与实现方案」

以上 8 篇覆盖：reese84 token 字段表、JS 混淆规律、UTMVC 与 reese84 联用场景、各 cookie ttl、AES key 派生定位。可作为 R5 进一步深读的入口。

## 9. 待研究问题（追加）
- ___utmvc 在何种场景下被服务端忽略（仅 reese84 场景）。
- IP 信誉对 reese84 自动升级到 captcha 的具体阈值。
