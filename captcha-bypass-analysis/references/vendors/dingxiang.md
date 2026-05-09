# 顶象 Dingxiang（DX / constId）

## 1. 产品形态
- 顶象「无感验证」、滑块、文字点选、图标点选、推理。
- 配套设备指纹 SDK：`Constant ID (constId)` 是核心，跨域稳定。
- 域名：`cap.dingxiang-inc.com`、`tcaptcha.dingxiang-inc.com`、`ctu.dingxiang-inc.com`。

## 2. 检测维度
- **constId**：长字符串，浏览器指纹聚合。生成时收集 Canvas/WebGL/Audio/Font/UA/Screen/Plugins/`navigator` 详细字段，中间用魔改算法（多为修改版 MD5/CRC）。
- **挑战 token**：`/api/captcha/get` 返回 `captcha_id`, `bg`, `slice` 等，提交时带 `tk`。
- **轨迹**：mouse/touch 序列，含 `pressure`(触摸压力，PC 默认 0)。
- **请求频次/IP/UA 黑名单**。
- **环境多态**：WASM 局部加密；JS 主体强混淆（OB/jscrambler）。

## 3. 关键端点与字段
| 端点 | 字段 |
|------|------|
| `/api/captcha/get` | `appId`, `token`, `version`, `language` |
| `/api/captcha/verify` | `captcha_id`, `slide` 距离, `track`(轨迹)，`constId`, `tk` |
| `/captcha-static/...` | 图片资源 |

## 4. 已公开研究
- CSDN「DX 算法还原」(130499340)：顶象 `const_id` 生成机制；JS 频繁变动。
- CSDN「顶象点选验证码」(135934417)：文字点选还原方法。
- 多个 GitHub `dingxiang-bypass` / `constid-research` 协议研究仓库。
- 看雪「顶象 const_id 还原」与「DX 滑块验证码 OpenCV 缺口识别」帖。

## 5. 防御性分析思路
1. constId 是高价值目标：可以 dump 一段时间内的所有指纹字段，做相关性分析（哪些组合稳定）。
2. JS 经常变 → 建议每天定时拉一份 `cap.dingxiang-inc.com/static/<hash>.js` 做 diff。
3. 滑块 CV：背景图较干净，ddddocr `slide_match` 表现好。
4. 文字点选：YOLOv5/v8 训练 1k+ 样本即可达 95%+。
5. 注意 `tk` 是一次性，重复用必失败。

## 6. 已知缓解 / 更新历史
- 2022 引入 WASM 部分。
- 2023 推理题上线，配合 LLM-style prompt（"找出第二个戴红帽子的"）。
- 2024 强化 constId 抗污染，引入 cross-tab 一致性校验。
- 持续刷新 JS 命名空间防 RPC。

## 7. 待研究问题
- constId 在不同浏览器内核（Chromium/WebKit/Gecko）下的稳定性。
- 推理题候选集生成的语义模板。
- WASM 内部加解密算法是否使用了非标准 S-box。
