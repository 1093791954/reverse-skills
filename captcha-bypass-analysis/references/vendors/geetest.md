# 极验 GeeTest（v3 / v4）

## 1. 产品形态（哪些版本 / 题型）
- **v3**：三段式接口（`gettype.php` / `get.php` / `ajax.php`），题型有经典滑块、滑动拼图、点选汉字、图标点选、空间推理、语义点选。
- **v4**：统一 `adaptive-captcha`／`nine-captcha` 前端容器，同一入口动态下发题型（slide、click、nine、winlinze、iconcrush），接口为 `/load`、`/verify`（POST，payload 形如 `{lot_number, payload, process_token, payload_protocol, pow_msg, pow_sign, ...}`）。
- 还有「极验无感（behaviour v4）」——不弹窗，埋点收集后直接 `/verify`，失败再降级到带交互的题型。

## 2. 检测维度
- **行为流水线**：v3 `w` 里编码了鼠标按下/移动/抬起时间戳、鼠标轨迹差分、滚轮、键盘。
- **指纹**：Canvas、WebGL vendor、AudioContext、UA-CH、`navigator.webdriver`、iframe 位置、screen 尺寸。
- **PoW**：v4 带 `pow_msg` + `pow_sign`（SHA-256，难度前导 4 位 0）。
- **频率/IP**：同一 `gt`/`challenge` 对同一出口 IP 的错误次数触发强校验。
- **环境一致性**：`lang`、`platform`、时区、`performance.now()` 抖动。

## 3. 关键端点与字段
| 接口 | 作用 | 关键字段 |
|------|------|---------|
| `/gettype.php` | 下发题型 | `gt`, `callback`, `is_next` |
| `/get.php` | 获取挑战 | `challenge`, `gt`, `lang`, `pt`, `w` |
| `/ajax.php` | 提交答案 | `challenge`, `w`（AES-CBC+RSA，用户答案/轨迹/环境），`userresponse` |
| v4 `/load` | 初始化 | `captcha_id`, `challenge`, `client_type`, `lang` |
| v4 `/verify` | 提交 | `payload`（AES），`pow_msg`, `pow_sign`, `process_token`, `captcha_output` |

**v3 w 结构**：外层 `AES.encrypt(plaintext, aesKey)` + `RSA.encrypt(aesKey, pubKey)` 拼成 base64url；plaintext 是 JSON（含 `lang, userresponse, passtime, imgload, aa`(加密轨迹), `ep`(环境), `em`(event meta)）。
**v4 payload**：AES-CBC，key 是 `process_token` 派生，IV 固定或随请求。

## 4. 已公开的研究 / 文章 / commit
- CSDN「极验4最新逆向」（articleid 147063867）：讲 `w` 定位与缺口识别。
- CSDN「极验滑块四代w值逆向」（138268546）：对比三代与四代加密差异，重点轨迹参数 `e`。
- CSDN「极验3代前两个参数w逆向分析」（142301806）：`r / o / i` 三段的分析。
- CSDN「极验4滑块验证码 pow_sign 参数逆向实战」：SHA-256 爆破难度位。
- CSDN「JS 逆向 03-某站的极验第一个 w 值的逆向分析」（147285020）：RSA 公钥定位 + 魔改 base64 + AST 还原。
- CSDN「某网站极验逆向」（148239186）：jscrambler 混淆器通用处理模板。
- GitHub `sml2h3/ddddocr`：滑块缺口匹配 + 点选 OCR 一体化。
- 看雪《GeeTest v4 jscrambler 解混淆》系列帖子（关键词：jscrambler dispatch）。

## 5. 防御性分析思路（授权审计场景）
1. 把三个 stage（`load` / `verify` / `ajax`）的 payload 全抓下来做差分，看哪些字段在多次失败里保持不变——这些通常是静态指纹。
2. 定位 `w` 生成函数：对 `XMLHttpRequest.prototype.send` 下 conditional breakpoint，回溯 call stack 到混淆根函数。
3. AST 层面先跑 `control-flow-flattening unflatten + string array rotate` 两个常用 pass，再 rename。
4. RSA 公钥是硬编码的，找到 `bigInt` 库的 `encrypt` 入口即可反推拼装顺序。
5. 轨迹 `aa` 部分：把 `mousedown/move/up` 的 dx,dy,dt 差分 → Caesar/ROT 变体 → base64 变种。
6. v4 pow 单独离线可跑：纯 SHA-256 前导 0 搜索，不必在浏览器里做。

## 6. 已知缓解 / 厂商更新历史
- v3 2019 增加 jscrambler 强化、`em` 环境段扩字段。
- v4 2021 上线，引入 PoW + WASM 轻量计算，题型池大幅扩展（icon-crush、winlinze 空间推理）。
- 2023 后多次刷新 AES key 派生算法；`payload_protocol` 版本号变化（1 → 3）。
- 出现「guard」检测：window 上挂了很多 native 函数的 toString 校验，`Proxy` 补环境需极精细。

## 7. 待研究问题
- v4 `payload_protocol=3` 的 AES key 派生是否与 `process_token` 完全确定性相关？
- `em` 字段里新加的 `pow_detail` 用途？
- winlinze（空间推理）题目的客户端答案编码格式。

## 8. v4 PoW + payload 完整字段表（R4 补充）

提交 `/verify` 时 POST body 标准字段集合（按时间序排列）：

| 字段 | 含义 | 加密 |
|------|------|------|
| `captcha_id` | sitekey 的字符串别名 | 明文 |
| `client_type` | `web` / `h5` / `native` | 明文 |
| `lot_number` | 服务端在 `/load` 时下发的本次会话编号 | 明文 |
| `risk_type` | 服务端指定题型 (`slide`/`click`/`nine`/`winlinze`/`iconcrush`) | 明文 |
| `pow_msg` | 服务端给的 PoW 输入串（含 `lot_number`） | 明文 |
| `pow_sign` | 客户端算出的 PoW 结果（SHA-256 前导若干 0） | 明文 |
| `process_token` | 服务端在 `/load` 给的会话密钥派生种子 | 明文 |
| `payload` | 加密后的完整答题 + 行为 + 环境 数据块 | AES-CBC，密钥从 `process_token` 派生 |
| `payload_protocol` | 当前协议版本（1/3 等），决定 AES 派生算法 | 明文 |
| `captcha_output` | 服务端响应字段，验证成功后下发，业务侧用 | 明文（含 `lot_number` + 通过签名） |

**payload 内层 JSON（明文）字段示例**：
```
{
  "device_id": "<本地 fp 哈希>",
  "passtime": <ms>,
  "userresponse": <用户应答>,
  "track": <轨迹列表>,
  "em": {<环境 meta>},
  "ep": <环境快照>,
  "geetest": {<内部统计>},
  "pow_detail": {"diff": <难度位>, "raw": <pow_msg>, "version": <int>}
}
```

**PoW 算法**：客户端在 `pow_msg + nonce` 上 sha256，难度位由服务端控制（通常 14-22）。新版 v4（`payload_protocol=3`）AES key 由 `KDF(process_token + version)` 派生，IV 随机但塞在 payload 头部 16 字节。

## 9. v4 PoW 相关 articleid（R4 补充，已 API 验证）

- (147063867) 极验 4 最新逆向
- (138268546) 极验滑块四代 w 值逆向
- (138847340) 极验四代滑块验证码逆向学习
- (139360661) 极验 4 滑块逆向
- (154240738) 极验 4-滑块逆向分析
- (142767556) 极验四代滑块协议逆向
- (148630543) 某网站极验 4 验证码纯算逆向分析
- (135728692) 极验 4 代滑块分析

以上文章覆盖：`pow_sign` SHA-256 难度位枚举、`process_token` 派生 AES 还原、`payload_protocol=3` 的字段差异、`device_id` 本地 fp 生成。

## 10. 待研究问题（追加）
- `payload_protocol=4` 是否存在（若存在）AES key 派生差异。
- `pow_detail.version` 当前可能取值与含义。
- `captcha_output` 在不同站点的字段顺序差异（疑似与 sitekey 的"模板"配置相关）。
