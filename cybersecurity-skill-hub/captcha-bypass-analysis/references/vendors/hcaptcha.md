# hCaptcha（含 Enterprise）

## 1. 产品形态
- 经典图块选择（"select all images with..."）9 格 / 18 格变种；图标点选；私有 Enterprise 题型（passive）。
- 域名：`hcaptcha.com`、`js.hcaptcha.com`、`api.hcaptcha.com`、`newassets.hcaptcha.com`。
- 核心 JS：`hcaptcha.js` + `hsw.js`（WASM 包，签名计算）+ `hsl.js`（题型 logic）。

## 2. 检测维度
- **WASM 签名（N-data / motionData）**：`hsw.js` 加载 WASM，输入 `req`(从 checksiteconfig 拿) + 当前页环境 + motionData，返回 `hsw` token。
- **motionData**：鼠标轨迹 + 触摸 + 焦点切换；以列结构 base64。
- **指纹**：UA-CH、Canvas、WebGL、Audio、字体；hCaptcha 对比同 IP 历史 motion 分布。
- **IP 信誉 + ASN**：和 datadome 一样住宅段优先。
- **TLS JA3/JA4**：和浏览器声明的 UA 必须匹配。

## 3. 关键端点与字段
| 端点 | 字段 |
|------|------|
| `/checksiteconfig` | `host`, `sitekey`, `sc`, `swa`，返回 `c`(req nonce), `pass`, `features` |
| `/getcaptcha/<sitekey>` | `v`, `host`, `sitekey`, `hl`, `motionData`, `n`(hsw 输出), `c`, `pst`(passive flag) |
| `/checkcaptcha/<id>` | 答案数组 + `motionData`(选答阶段) + `n` |
| `/hsw.js` | WASM 模块入口，被 `hCaptcha.execute` 内部调用 |

**hsw 输入 req 结构**：JWT-like，`alg=HS256`，payload 含 `s`(siteKey hash), `t`(ts), `e`(过期), `d`(domain hash)。
**N 字段**：是 `hsw(req)` 的输出，再次 JWT-like base64。

## 4. 已公开研究
- CSDN「hcaptcha 逆向」(141957797)：`checksiteconfig` → 注入 hsw.js 拿 N。
- CSDN「hcaptcha(hcp)无感验证码逆向闲谈」(146364872)：WASM 加密总览。
- CSDN「hcaptcha 无感逆向 P1」(143582573)：二进制流定位与 N 验证。
- CSDN「hcaptcha 纯算法逆向 steam 可高并发」(148101100)：纯算工程化。
- GitHub `xrip/hcaptcha-solver`、`Vinyzu/hCaptcha-Challenger`：研究项目，含图块训练数据集与 ONNX 模型。
- Twitter `@hCaptcha` 官方对历次绕过事件的回应贴。

## 5. 防御性分析思路
1. 在合法授权站点把 `hsw.js` dump 出来，先 wabt → wat 反汇编，找 `__wbindgen_*` 与 export 函数。
2. 关键 export：`hs_make_hsw(req_ptr, env_ptr) -> string`，env 是 stringify 的 motionData+UA+timing。
3. 补环境主要是 motionData 字段顺序与浮点精度（必须用 IEEE754 64bit 精确）。
4. 图块识别：YOLOv8 + CLIP（针对「select all <语义>」）效果优于纯 CNN 分类。
5. Enterprise passive 模式：服务端自动判分，无 UI；要看是否启用 `pst=true`。

## 6. 已知缓解 / 更新历史
- 2021 推 WASM hsw，杀掉了之前 JS 直跑的 motionData。
- 2022 引入 N 字段二段验证。
- 2023 motionData 字段重排（v0 → v1），加 `dr` 加速度差分。
- 对 `playwright`、`puppeteer-extra-stealth` 直接特征匹配 `__playwright_evaluation_script__`。

## 7. 待研究问题
- WASM 内部是否使用 SIMD 指令做行为聚合？
- `swa`（site-wide assessment）开启后，N 是否带账号态？
- Enterprise passive 的最低评分阈值。
