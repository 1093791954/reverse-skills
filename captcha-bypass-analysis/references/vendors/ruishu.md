# 瑞数信息（Botgate / 动态安全 / VMP cookie）

## 1. 产品形态
- 国内反爬厂商，独立部署在客户站点，主打动态 JS+ 双 cookie：
  - 第一次请求拿 cookie-A（多为 `T1` / `FSSBBIl1UgzbN7N80T` 之类）
  - 第二次请求自执行 JS 生成 cookie-B（`FSSBBIl1UgzbN7N80S` 等）
- 各大期刊/政府/银行/医保接口常见。
- 版本：4 / 5 / 6 代，6 代引入 VM 字节码解释器。

## 2. 检测维度
- **JS 动态生成 cookie**：每页面下发不同 JS，里面包含一个 packed VM 解释器，运行后 `document.cookie = '<name>=<...>'`。
- **环境探针**：navigator/window/document 大量字段被取用，缺一个补一个就会无限报错（"缺啥补啥"是社区共识）。
- **HTML 中 meta 与脚本顺序**：第一次返回的 HTML 含特定 base 字符串数组，被 JS 用作 VM 字节码源。
- **二次请求前的 SET-COOKIE 顺序**。
- **TLS / UA 一致性**。

## 3. 关键端点与字段
| 端点 | 字段 |
|------|------|
| 业务 GET（首次） | 返回 200/202 + `<script>` 包含 VM bytecode + Set-Cookie A |
| 业务 GET（二次，带 Cookie A） | 校验 cookie B 是否生成 |
| 业务接口 | header/cookie 必带两个 cookie |

## 4. 已公开研究
- CSDN「【瑞数 VMP】中期刊服务平台逆向」(150556922)：完整流程清 cookie/抓包/扣代码。
- CSDN「[逆向知识] 瑞数补环境：公式与逻辑深挖」(149048509)：VM 关键变量补全。
- CSDN「瑞数 5 逆向过程（纯补环境）」(136632868)：cookie-A → cookie-B 全过程。
- CSDN「js 逆向：瑞数」(147122772)：动态安全技术综述。
- CSDN「瑞数(6 代)逆向分析.part1」(149752567)：VM 代码生成分析。
- CSDN「瑞数 4 代逆向学习」(138604767)：Hook + RPC + 硬扣代码三种方法对比。
- 看雪、吾爱大量瑞数 4/5/6 代分析帖。

## 5. 防御性分析思路
1. 瑞数补环境 = 「缺啥补啥」+ Proxy 兜底；先用 `document = new Proxy({}, {get(t,k){console.log(k); return '';}})` 把所有访问字段记下来。
2. VM 字节码：先识别 dispatcher（switch/case 主循环），再列 opcode → handler 表；同一站点 opcode 集稳定。
3. Cookie B 生成函数最终落到 `document.cookie = ...` 赋值，可以 hook 这一句反推。
4. 6 代 VM 引入更多花指令，建议先做 `dead branch elimination`。
5. 注意首次 HTML 带的字符串数组：是 VM 的 bytecode 源，每次 rotate。

## 6. 已知缓解 / 更新历史
- 4 代：JS 直跑生成 cookie。
- 5 代：引入分段 cookie 与 packed JS。
- 6 代：完整 VM 字节码 + 反调试探针。
- 持续打 `Function.prototype.toString` 检测、`debugger` 检测、`performance.now()` 时差检测。

## 7. 待研究问题
- 6 代 opcode 是否随站点变化（多客户共享 vs 各自独立）。
- VM 内部反调试触发后是否会污染 cookie。
- 与移动端 SDK 是否共享指纹算法。

## 8. 别名与产品矩阵（R4 补充）

- **Botgate（瑞数 Botgate）**= 瑞数信息官方面向云上/SaaS 客户的"动态防爬虫网关"商品名；与本笔记中的 cookie A/B 双段动态 JS 是同一套技术栈，只是部署形态从私有化转到 SaaS。
- 中文圈 CSDN 用关键词 `Botgate 逆向`（命中 ~55 篇）查到的多数文章实际就是瑞数 4/5/6 代 cookie 的逆向教程，可以并入本笔记的同一思路。
- 瑞数其它别名：
  - **River Security（瑞数海外品牌）**：英文资料标题更易出现"River Bot Defense"。
  - **5G WAF / 动态安全 WAF**：在通信运营商客户里的话术。
  - **瑞数云盾**：私有化产品名（vs Botgate 的 SaaS 版）。
- 与 F5 Shape、Akamai BMP 的差异：瑞数主打"双 cookie + VM 字节码"，几乎完全跑在客户端 JS；不像 Akamai/F5 那样要 server-side 强签名。这导致瑞数比同等价位竞品**更可纯算还原**，但 6 代 VM 后还原成本上升明显。
- 接入域示例：`<custom-domain>/<random>.js`（无固定 CDN 域名，因为它可私有化部署）；最稳的特征是首次返回 HTML 里的 base64-like 字符数组 + 特定形态的 packed JS 头。

## 9. 待研究问题（追加）
- Botgate SaaS 版与私有化版 VM opcode 是否分裂演进。
- 移动端 SDK（瑞数 App Defense）与 Web cookie 是否共享 RNG/指纹采集逻辑。
