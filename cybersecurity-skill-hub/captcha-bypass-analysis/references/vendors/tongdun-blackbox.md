# 同盾 BlackBox（TongDun BlackBox / fp）

## 1. 产品形态
- **同盾 BlackBox / 黑盒指纹（fp.tongdun.net 域）**：用作业务前端"行为+设备+环境"采集 SDK，落地为一个 base64 token，业务端调用风控决策 API（`fp_dispatcher` / `partner` 等）拿评分。
- 常与"同盾滑块/同盾点选"组合：滑块/点选只产生缺口答案，BlackBox 才是真正的指纹载体。
- 部署形态：JS SDK（PC/H5）、Android/iOS Native SDK、小程序版本。
- 多家金融/电商接入；典型 host：`fp.tongdun.net`、`fp.fraudmetrix.cn`、`static.tongdunczb.com`。

## 2. 检测维度
- **设备指纹**：Canvas/WebGL/Audio/Font/UA-CH/Battery/Permissions 五维交叉。
- **行为埋点**：mousemove / touchstart / scroll / keydown 时序队列，进 token 之前先做差分压缩 + 修改版 base64。
- **环境一致性**：window/document 关键属性 toString 校验、Function.prototype.toString 链路校验、Worker self.navigator 与主线程对齐。
- **加密栈**：JSON → 修改版 RC4 → AES-GCM（密钥 RSA 协商或时间派生） → 修改版 base64。
- **WASM token 段**：新版（v3）把"魔改 SHA-256 + AES" 推到 WASM，AST 解混淆失效。
- **频率/IP 信誉**：同 IP 短窗口大量 token 触发降级到滑块/点选。

## 3. 关键端点与字段
| 端点 | 用途 | 关键字段 |
|------|------|---------|
| `fp.tongdun.net/<partner>/<sub>` | 加载 SDK | partnerCode/appName/version |
| `fp.tongdun.net/.../v1/web/load` | 拉配置 | sign（HMAC）, ts |
| `fp.tongdun.net/.../v1/web/event` | 上报指纹 | blackBox（核心 token，base64+RC4+AES） |
| 业务侧 `/risk/check` | 决策 | blackBox + 业务签名 |

**blackBox 结构**：`版本字节(1) + 时间戳(4) + 随机IV(8/16) + 密文体(变长) + checksum(4)`，密文里是 JSON 行为数组 + 多维指纹。

## 4. 已公开研究
- CSDN「逆向实战：新版同盾 BlackBox 环境补全与指纹对抗解析」(159074707)：BlackBox WASM Token、AES-GCM/RSA、请求载荷解密；本技能已在 fingerprint-bypass / netease-yidun 笔记复用。
- CSDN「最新某星球同盾 blackbox 逆向，亲测有效」(138467655)。
- CSDN「【JS 逆向百例】某盾 Blackbox 逆向分析」(145267241)。
- CSDN「某盾 Blackbox 算法逆向分析」(145068193)。
- CSDN「同盾滑块 + blackbox 指纹，逆向协议通过」(142761535)：滑块+黑盒联用案例。
- CSDN「某盾 blackBox 逆向——纯算」(130794263)：脱离浏览器纯算实现。
- CSDN「某岛的某盾 blackbox 逆向与分析」(139996926)。
- CSDN「SO 逆向入门实战教程九——blackbox」(118115569)：Native SO 层的 BlackBox。

## 5. 防御性分析思路（授权审计）
1. 抓 fp.tongdun.net 三段请求（load → event → risk/check），用 mitmproxy 录制。
2. 找 SDK 入口 webpack chunk → 全局 hook `XMLHttpRequest.prototype.send` 看 blackBox 拼装位置。
3. AST 解 control-flow flatten + string array rotate；定位 RC4 修改版（key-schedule 顺序变动），再定位 AES-GCM 与 IV 来源。
4. WASM 段（v3）：用 wabt + wasm-decompile 抽 dispatcher，标注 native 函数表。
5. 行为 payload：录制真人轨迹做种子，不要纯函数生成。
6. Native SDK：unidbg 黑盒模拟 + Frida 拦关键 SO 导出；常见函数名 `Java_com_tongdun_..._collect`。

## 6. 已知缓解 / 更新历史
- 2021 改 RC4 修改版 → 2022 引入 WASM。
- 2023 v3 加 Function.prototype.toString native code 校验，简单 Proxy 补环境失效。
- 2024 加 OffscreenCanvas / Worker 维度交叉校验。
- 2025 reportedly 引入 `fp_v4`（部分客户灰度），加 RSA 协商对称密钥。

## 7. 待研究问题
- v3 WASM 内 AES key 与时间戳/RSA 协商的具体派生公式。
- BlackBox token 不同 partner 是否复用同一密钥族（推测分 partner 派生）。
- Android SDK 与 Web SDK token 内部字段差异。
