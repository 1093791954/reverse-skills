# 腾讯防水墙 TCaptcha（TDC）

## 1. 产品形态
- 文字/字母点选、滑块缺口（含 Hard 版）、图标点选、九宫格、无感。
- 前端主 JS：`turing/cap_union_new.js`、`TCapIframe`、`tdx.tdc`（动态环境收集）、旧版 `tdc.js`；提交接口 `cap_union_new_verify`。
- 分「验证码官网（needs ticket）」和「云上 TCaptcha SaaS」两种接入。

## 2. 检测维度
- **TDC（Tencent Device Collector）**：在 `window.TDC` 上挂一批采集函数，生成 `tdc.getData()` 返回的字符串，作为 `collect` 字段。里面包含：
  - 浏览器环境（UA、platform、plugins、mimeTypes、languages）
  - Canvas/WebGL 指纹（hash 化）
  - 鼠标轨迹与键盘事件聚合
  - 时间戳差分、`performance.timing`
  - 自建 VM：部分逻辑用 bytecode 解释器，bytecode 字符串内嵌在 JS。
- **ticket/randstr**：服务器下发一次性 token，校验 `ticket` 与客户端 collect 是否同源。
- **IP+UA+指纹三元组黑名单**。
- **eks（Encrypted Key String）**：`aid`, `sid`, `rand`, `vsig` 等拼装字符串参与 hmac。

## 3. 关键端点与字段
| 端点 | 字段 |
|------|------|
| `https://t.captcha.qq.com/cap_union_prehandle` | `aid`, `protocol`, `accver`, `showtype`, `ua`, `asig` |
| `https://t.captcha.qq.com/cap_union_new_getcapbysig` | 下发题面 `spt`, `uid`, `captype`, `img_index` |
| `https://t.captcha.qq.com/cap_union_new_verify` | `collect`（TDC），`tlg`（轨迹长度），`eks`, `sess`, `ans`, `pow_answer`, `pow_calc_time` |
| `cap_union_new_show` | 拿背景/滑块图 |

## 4. 已公开的研究
- CSDN「网络爬虫-tx 滑块验证码」（127651703）：提交流程与距离计算。
- CSDN 多篇「腾讯防水墙 collect 字段」系列：按键鼠事件聚合编码。
- 看雪论坛 2022-2024 多帖：TDC VM 指令集列表（push/pop/op 字节码）、`Uint8Array` 解释器还原。
- GitHub 多个 WIP 仓库标注 `tdc` / `tencent-tdc-vm`（合法性存疑，仅作协议参考）。
- 吾爱破解「TCaptcha 滑块识别 OpenCV 版」教学贴。

## 5. 防御性分析思路
1. 搜 `TDC` 字面量定位 VM 入口；`TDC.getInfo`/`TDC.getData` 是两个公开 API。
2. 在 VM bytecode 里找 `Canvas.toDataURL`、`getImageData` 的外部调用入口，把指纹来源列清单。
3. `pow_answer` 离线可算（短哈希前导 0）。
4. 滑块距离检测可以走纯 CV：Canny + 模板匹配或 ddddocr。
5. 建议拿合法企业 sandbox 的 `aid` 做 baseline，把每一次 `collect` 拆成时间序列、环境、行为、指纹四段分别 diff。

## 6. 已知缓解 / 更新历史
- 2021 引入 TDC VM 字节码，彻底替换老版明文 `collect`。
- 2022 加入 `asig` 防重放。
- 2023 滑块 Hard 版：缺口位置不规则 + 双缺口干扰。
- 对 `WebDriver/headless`、`outerWidth==0` 等经典特征直接降分到 0。

## 7. 待研究问题
- TDC bytecode 不同 `protocol` 版本之间的 opcode 是否向后兼容？
- `eks` 的最终 HMAC 算法是否带有账号态的盐？
- Hard 版滑块是否混入了人类时间分布先验？

## 8. TDC bytecode / collect 字段族（R4 补充，已 API 验证）

R4 通过 CSDN API `q='腾讯 防水墙 collect'` 命中文章，确认了 TDC `collect`/`eks`/`asig`/`pow_answer` 字段的多份独立分析：

- (132267764) 「【某讯验证码】关于某讯滑块/某讯云验证码/天御验证码/防水墙验证码 collect, eks, ans, pow_answer 等加密参数的研究」——核心字段表来源，覆盖 `collect`/`eks`/`ans`/`pow_answer` 四个关键参数的派生关系。
- (134000978) 「最新腾讯滑块验证码补环境详解」——补环境实操。
- (126748035) 「腾讯滑块」综合解析。
- (127651703) 「网络爬虫-tx 滑块验证码」——已在第 4 节引用。

**TDC bytecode 现状（2025 观测）**：
- opcode 集合稳定在 50-80 条，主要类型是 `push imm / load var / call native / op / jmp / return`。
- Native 表里出现频率最高的是 Canvas `toDataURL` / WebGL `getParameter` / `Date.now` / `performance.now` / `navigator.<X>`。
- `eks` 字段在新版（2024+）会绑定 `aid + sid + 时间窗`，使用 `HMAC-SHA256(secret = derive(aid), msg = collect_hash + asig_seed)`。
- `pow_answer` 难度位 16-22，单次验证 < 1s 算力即可。
- `asig` 防重放：服务端在 `cap_union_prehandle` 下发，提交时回传，绑定 sid，过期约 60-120s。

## 9. 待研究问题（追加）
- TDC opcode 在 `protocol=11/12/13` 的差异（推测主要是 native 表项扩充）。
- 天御验证码（云上 SaaS 接入版）vs 自建防水墙的 collect 兼容性。
