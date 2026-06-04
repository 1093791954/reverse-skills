# DataDome

## 1. 产品形态
- 边缘 + 客户端混合反爬：
  - **JS Challenge**（无感）：注入 `<sitekey>.captcha-delivery.com/c.js`，收集环境与行为，POST 验证；通过后下发 `datadome` cookie。
  - **Slider Captcha**：`captcha-delivery.com/captcha/?initialCid=...`，几何缺口滑块。
  - **WASM/VMP 加固**：客户端关键 payload 在 WASM 里，并叠加 VMP-style 字节码解释器（看作迷你虚拟机）。
- 客户：Hermes（爱马仕）、Vinted、Reddit 部分页面、ticketmaster 区域、Foot Locker。

## 2. 检测维度
- **datadome cookie**：服务器签名，绑定 IP+UA+TLS。
- **dd / ddm / plv3 / cid**：客户端生成 payload，参与 cookie 派生。
- **指纹**：Canvas/WebGL/Audio/Font/UA-CH，UA 与 JA3 必须一致。
- **行为**：滑块 traceData，`movePath` 二阶差分；纯算研究表明可用真人录制做种子库。
- **AI 引擎**：DataDome 主打实时机器学习；多维 feature 上送至边缘做评分。

## 3. 关键端点与字段
| 端点 | 字段 |
|------|------|
| `<host>/c.js`（403 重定向触发） | 主 JS，混淆 + WASM glue |
| `geo.captcha-delivery.com/captcha/check` | `cid`, `icid`, `ccid`, `s`, `referer`, `parent_url`, `dd_cookie`, `hash`(payload), `ua` |
| `/captcha/?initialCid=...&hash=...&cid=...&t=fe&referer=...` | 滑块页面 |
| `/captcha/check?cid=...` POST | `payload=base64`, `pow=...`, `solution=...`(滑块答案), `motion`(轨迹) |

**payload**：先 JSON → 修改版 SipHash/RC4 → base64；新版用 WASM 函数包装，再叠 VMP bytecode。

## 4. 已公开研究
- CSDN「最新 Datadome 逆向 支持 Hermes、vinted」(144714365)：TLS 指纹 + cookie 校验流程。
- CSDN「逆向工程师视角：拆解 DataDome 滑块验证码的 3 层防护机制」(150596576)。
- CSDN「datadome 无感 jspl 逆向」(156131046)：JSPL 中间语言还原思路。
- CSDN「JS 逆向 - datadome（无感）补环境、纯算」(158962041)：三次请求流程，403 → ddm/WASM/VMP。
- CSDN「DataDome AI 引擎深度逆向：智能反爬虫算法」(150546710)。
- GitHub `glizzykingdreko/datadome-documentation`：协议级文档。
- 多个滑块研究：模板匹配 + Bezier 轨迹 + IP 信誉栈。

## 5. 防御性分析思路
1. 触发：直接请求业务接口，遇 403 返回 `<script src="...captcha-delivery.com/c.js">` 时进入 challenge。
2. WASM dump：`hsw`-类思路，wabt 反汇编 → 找 `__indirect_function_table`, 标识关键 hash 函数（多为修改版 SipHash 或 SHA1）。
3. VMP 字节码：常驻字符串数组 + opcode dispatcher；用脚本枚举 opcode → handler 对照表。
4. 滑块缺口距离 CV：模板匹配（背景被涂色干扰，需先去噪）。
5. cookie 复用窗口非常短（多在 1-3 分钟），频控严格。

## 6. 已知缓解 / 更新历史
- 2022 引入 WASM 强化。
- 2023 JSPL（Java-Script-Polish-Like）中间表示，对纯算逆向是大障碍。
- 2024 滑块底图加 noise + alpha 通道扰动，传统模板匹配失效率上升。
- 对 curl_cffi 之外的 client（aiohttp/requests）几乎全拦。

## 7. 待研究问题
- VMP 不同站点是否共享 opcode set？
- `plv3` payload 内部分段含义。
- AI 引擎评分中 IP 历史权重占比。
