# PerimeterX / HUMAN（_px3 / _pxhd / _pxvid）

## 1. 产品形态
- 边缘 + 客户端 SDK，被 HUMAN Security 收购后整合在 BotDefender / HumanDefend 产品线下。
- 提供「press & hold」按钮交互式验证（按住 5-10s）+ 若干被动检测。
- 客户：StubHub、Booking.com 部分、SSENSE、Crunchbase、电商及票务行业。
- 域名：`<sitekey>.captcha-px.com`、`collector-<region>.perimeterx.net`、`px-cdn.net`。

## 2. 检测维度
- **环境**：UA-CH、Canvas、WebGL、Audio、Font、`navigator` 全集、`window.chrome` 详细字段。
- **行为**：mousemove dx/dy/t、touchmove、focus、scroll；press & hold 按住的力度抖动 + 停留时长。
- **TLS / HTTP2** 指纹必须与 UA 匹配。
- **IP 信誉 + ASN**：HUMAN 维护大型黑名单。
- **多域 collector**：客户端会请求 collector 域多次上报，cookie chain 含 `_pxvid`(visitor id), `_pxhd`(host data), `_px3`(session token), `_px2`/`_pxff_*` 等。
- **PoW**：部分场景启用 SHA-256 短 PoW。

## 3. 关键端点与字段
| 端点 | 字段 |
|------|------|
| `<host>/init.js` | 主 JS（client.js 混淆，AST 含字符串数组 + flatten） |
| `collector-<region>.perimeterx.net/api/v2/collector` | POST sensor data, `appId`, `tag`, `uuid`, `ft`, `vid`, `seq`, `fp_hash` |
| `captcha-px.com/blocked.js` 或 `/api/v1/collector/captcha` | 触发交互式 captcha |
| `/api/v1/collector/PX...` | 提交答案 |

**Sensor 上报字段**：`data` 为 JSON.stringify 的大对象 → AES-CBC + base64；含分段 `PX0`/`PX1`/...，每段一组 fingerprint or behavior。

## 4. 已公开研究
- CSDN「perimeterx 逆向」相关讨论帖（多见各厂商对比综述）。
- GitHub `glizzykingdreko/PerimeterX-Documentation`、`px-bypass-research`：协议级整理。
- 多篇 medium/dev.to 文章「Bypassing PerimeterX press-and-hold」(2022-2024)，使用真浏览器 + 注入修改 timing。
- 看雪与吾爱 RPC + 浏览器一体化方案讨论。
- HUMAN 官方 blog 多次披露过他们如何 detect Botright / camoufox。

## 5. 防御性分析思路
1. 解混淆 `client.js`：jscrambler + 字符串 array rotate；用 `babel-plugin-jscrambler-deobf` + 自写 unflatten。
2. 关注 `seq` 单调递增、`vid` 一致性；session 粘性强。
3. press & hold 不能瞬时（< 800ms 必失败），且要带轻微抖动。
4. `_px3` 的 ttl 通常 30-60 分钟。
5. mobile（PXM SDK）和 web 上报字段不一样，但共享同一 collector。

## 6. 已知缓解 / 更新历史
- 2021 引入 press & hold。
- 2022-2023 强化 fingerprint 段，加入 `Permissions.query` 五项交叉。
- 2024 对 patchright/camoufox 上线针对性 detector（`evaluate` 调用栈检测）。
- HUMAN 整合后引入「Aggregate threat scoring」跨网络评分。

## 7. 待研究问题
- `_pxhd` 的内容是否是浏览器组合的稳定哈希？
- press & hold 接受的最小/最大时长边界。
- `seq` 字段是否参与 server-side replay 检测。
