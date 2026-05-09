# 阿里云盾 / 阿里滑块（_bx-v / x82Y / x231 / ali140 / 227 / etSign）

## 1. 产品形态
- 阿里系滑块/无感由阿里安全（"AliCaptcha"/"_bx-v"）实现，分多种代号：x82Y、x231、ali140、ali227、bxet、rand、bx-v。
- 接入面：淘宝/天猫/1688/阿里云/支付宝/钉钉/中国联通等。
- 滑块 + 无感 + 风控（与「Sec」业务签名同源）。

## 2. 检测维度
- **bx-v / etSign / 227 / 231**：参数名按业务变，本质是同一套 collect → 加密 → 上报：
  - bx-v：业务 sign，字符串两段哈希。
  - 227：滑块 trace 上报参数。
  - 231：新一代滑块通用 token。
  - bxet / etSign：风控签名。
  - ali140 / ali150：滑块版本号路径标识。
- **环境**：Canvas/WebGL/Audio/Font/UA-CH/Plugins/Battery/HardwareConcurrency。
- **行为**：鼠标移动、滚轮、键盘。
- **TLS / IP 信誉**。
- **mtop sign 联动**：与淘宝 mtop `sign`（h5 用 `_m_h5_tk`）共享部分指纹。

## 3. 关键端点与字段
| 端点 | 字段 |
|------|------|
| `/_____tmd_____/punish?...` | 风控弹页面 |
| `/captcha/getsig` | 取签名 |
| `/<biz>?bx-v=...&...` | 各业务接口 |
| `cf.aliyun.com/captcha-mng/v3/...` | 阿里云 captcha 服务 |

## 4. 已公开研究
- CSDN「阿里 bxet 逆向」：`etSign` 纯算补环境。
- CSDN「逆向实战 30——阿里 227 逆向分析」：滑块 trace 参数。
- CSDN「阿里云滑动验证码逆向分析」：联通话费页面案例，参数 `a`/`scene`/`href`。
- CSDN「阿里 rand 逆向分析」：1688/231 滑块。
- CSDN「阿里最新普通 x231 逆向分析」：x231 检测机制。
- 多篇「ali140 滑块 canvas 补环境」（CSDN 159607511、158903755、159787961）：Node.js 模拟 Canvas + WebGL 指纹。
- 看雪/吾爱：mtop `sign` + 滑块联合分析帖。

## 5. 防御性分析思路
1. 阿里系大量参数互相校验，逆向单一参数不够，需要把整条链（指纹 → bx-v → mtop sign → 业务）一起还原。
2. JS 用 OB 混淆 + 字符串数组旋转，先 deobf。
3. Canvas 补环境是关键：toDataURL 一致性、WebGL UNMASKED_VENDOR_WEBGL/UNMASKED_RENDERER_WEBGL 必须给出真值。
4. 风控降级：`/punish` 触发后 IP/UA 加锁，需要换出口。
5. 注意 ali140 与 ali150 版本差异，新版 token schema 完全不同。

## 6. 已知缓解 / 更新历史
- 阿里持续推新参数名（bx-v → 227 → 231 → ali140 → 150），周期约半年。
- 2023 强化 Canvas/WebGL 一致性。
- 2024 ali150 引入 WASM。
- 与设备指纹"无线保镖"在 App 端有联动。

## 7. 待研究问题
- ali150 WASM 入口与算法。
- bx-v 与 mtop sign 之间的依赖图。
- 不同业务（淘宝 vs 1688 vs 阿里云）参数差异点。

## 8. 阿里滑块版本号 / 字段族对照表（R4 补充）

> 阿里系参数名半年一换，但本质都是"同一套 collect → AES + base64 → 上报"。下表整理 CSDN/52pojie 累计出现过的代号；R4 通过 CSDN API 抽样验证至少 30+ 篇相关文章。

| 代号 | 类型 | 角色 | 出现时间窗 | 关键 articleid |
|------|------|------|-----------|---------------|
| `bx-v` | URL/Body 参数 | 业务 sign（短哈希） | 2018- 至今 | 多篇综述 |
| `etSign` / `bxet` | URL/Body 参数 | 风控签名（强校验） | 2020- | 多篇 |
| `227` | URL 参数 | 滑块 trace 上报 | 2020-2023 | 多篇逆向 30 案例 |
| `x231` / `231` | Body 参数 | 新一代滑块 token | 2023- | 多篇 |
| `x82Y` | URL 参数 | 滑块/风控混合 | 2022-2024 | 多篇 |
| `ali140` | 路径标识 | 滑块版本号 | 2024 | (158903755 / 159607511 / 158674857) |
| `ali150` | 路径标识 | 滑块新版（含 WASM） | 2025 | (158674857) |
| `_bx-v` | Body 参数 | bx-v 双下划线变体（淘宝/天猫） | 2019- | 多篇 |
| `rand` | URL 参数 | 1688 滑块通用 | 2021- | 多篇 |
| `n` | Body 参数 | 滑块 nonce | 2022- | 多篇 |
| `a` / `scene` / `href` | URL 参数 | 联通话费页等业务侧 | 2023- | 阿里云 captcha 系列 |

**版本演进**：bx-v(2018) → 227(2020) → 231/x82Y(2022-2023) → ali140(2024) → ali150(2025, WASM)。
**大致规律**：每一次版本切换都涉及 (a) Canvas/WebGL 指纹采集字段扩充，(b) AES 模式或 IV 派生算法变化，(c) 服务端校验加严（IP 信誉权重提升）。

## 9. 新增 articleid（R4 已 API 验证的样本）

- (158674857) 阿里 140 滑块逆向实战：从环境补全到加密参数获取全流程
- (158903755) JS 逆向进阶：ali140 滑块验证码的 Canvas 环境精准模拟
- (159607511) JS 逆向新手也能搞定：手把手教你用 Node.js 补全 ali140 滑块 canvas

R5 建议进一步覆盖：x82Y 全流程、ali150 WASM 反汇编。

## 10. 待研究问题（追加）
- ali150 WASM 内部 dispatcher 是否与 DataDome/F5 风格 VMP 相似（推测不是，应仍是直函数）。
- mtop `sign` 与 `_bx-v` 在淘宝/天猫不同业务的具体依赖图。
