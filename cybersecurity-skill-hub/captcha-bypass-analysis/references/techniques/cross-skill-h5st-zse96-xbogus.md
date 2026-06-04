# 跨技能联动笔记：京东 h5st / 知乎 zse-96 / 抖音 x-bogus

> 本笔记记录三个**大站签名参数**与本技能的"指纹/轨迹/PoW"如何配合使用。
> 这三个参数在 `riskcontrol-analysis` 与 `web-keygen-analysis` 技能中已有专章；本技能（captcha-bypass-analysis）只关心它们与 **验证码触发点 / 设备指纹 / PoW** 的交叉。

## 1. 三参数定位与本技能交集

| 参数 | 站点 | 本技能交集点 | CSDN 命中量级 |
|------|------|-------------|--------------|
| `h5st` | 京东 H5（m.jd.com / api.m.jd.com） | 触发风控时跳转到滑块/极验，h5st 与 sliderToken 同框生成 | 130 篇 |
| `x-zse-96` | 知乎（www.zhihu.com / api.zhihu.com） | 风控降级到极验/瑞数 v6 题；zse-96 中含 d_c0 设备指纹哈希片段 | 144 篇 |
| `X-Bogus` + `msToken` | 抖音/TikTok（aweme/douyin.com） | 触发后弹出 verify_center 滑块/点选，X-Bogus 计算依赖 Canvas 指纹 hash | 427 篇 |

## 2. 京东 h5st × 滑块 sliderToken

**典型链路**：用户访问 m.jd.com → 风控判定可疑 → 服务器在响应里下发 `H5_LOGIN_VERIFY` flag → 前端唤起极验 v3/v4 滑块 → 提交时 `h5st` 头 + 滑块的 `validate / sliderToken` 同时校验。

**生成结构**（参考 CSDN 160164511、`new window.ParamsSignMain({appId,...}).sign(params)`）：
- `h5st = ts.appId.token.sign1.sign2`
- `sign1` = HmacSHA256(token, body)
- `token` 来自首屏 `/genToken` 接口，**该接口本身受滑块保护**

**与本技能的联动点**：
- 极验滑块通过后产生的 `validate` 字段需要回传到下一次调用 `/genToken` 的请求体里
- token 一旦绑定 IP/UA，就长期有效（与本技能 `replay-token.md` 关联）
- 设备指纹（eid / pdid / `_jdb`）参与 sign2 计算 → 与 `fingerprint-bypass.md` 联动

**已存档 articleid**：160164511（H5ST 完整逆向 + Node 补环境）。

## 3. 知乎 x-zse-96 × 瑞数 v6

**典型链路**：登录/搜索接口 → 触发瑞数 v6 wasm 校验 → cookie `__zse_ck` + header `x-zse-96` 同时校验。

**生成结构**（参考 CSDN 120891620、138296549）：
- `x-zse-96 = "2.0_" + sign`
- `sign = MD5( "101_3_3.0+" + path + "+" + d_c0 + "+" + cookie_z_c0 + "+" + body )` （早期版本）
- 新版本：webpack 加密器 + AES + RC4，需要补环境

**与本技能的联动点**：
- `d_c0` 是知乎的设备指纹 cookie，**首次访问由瑞数 v6 wasm 算出**（属于本技能 `vendors/ruishu.md` 范畴）
- `__zse_ck` 包含 Canvas 指纹哈希（`fingerprint-bypass.md`）
- 触发"图形验证码"时跳转 `/captcha/api/v3/captcha/v_token` → 点选汉字（`types/click-character.md`）

**已存档 articleid**：120891620（早期 MD5 版）、138296549（webpack 反调试新版）。

## 4. 抖音 X-Bogus × 风控滑块

**典型链路**：aweme API → 必带 `X-Bogus` 头 + `msToken` cookie → 触发后跳 verify_center → 滑块/点选/旋转三选一。

**生成结构**（参考 CSDN 137170043 + 公开公众号文章）：
- 19 字节数组 → 4 位编码表 base 转换 → 28 位 X-Bogus
- 数组前 4 位固定，5-10 位由 MD5 hex 切片，11-18 位由时间戳 + Canvas 固定值拼接
- Canvas 固定值 = `canvas.toDataURL()` 的某段 hash（**直接命中本技能 `fingerprint-bypass.md` 的 Canvas 主题**）

**与本技能的联动点**：
- X-Bogus 内嵌的 Canvas hash 必须和当次 verify_center 内嵌的 fingerprint hash 一致 → 不一致直接拒绝（无滑块界面）
- 滑块通过后回传 `did_token`，下一次 X-Bogus 的"环境快照"会引用此 did_token
- 与 `web-keygen-analysis` 技能 `webmssdk.js` 共享 jsvmp 调度器 → 使用本技能时若需要补 jsvmp，应转交那个技能

**已存档 articleid**：137170043（X-Bogus 19 位编码 + 解码表 `Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=`）。

## 5. 跨站点共性总结

三参数与本技能验证码模块的交叉规律：
1. **指纹一致性**：签名参数内嵌的指纹（Canvas / d_c0 / eid）必须与验证码 SDK 上报的指纹完全一致，否则即便滑块通过也会被风控判失败。
2. **token 链式绑定**：`genToken` / `verify_center` / `__zse_ck` 等接口本身受验证码保护，形成"必须先解一次验证码才能拿到生成签名所需的 token"的循环。
3. **PoW 借用**：抖音风控部分版本会让 X-Bogus 末尾几位作为简易 PoW 校验位（前 4 字节哈希前缀 = 0），与 `types/pow-friendly.md` 思路相通但远更轻量。

## 6. 推荐工作流（联合 web-keygen-analysis）

1. 先在 `web-keygen-analysis` 技能里把 h5st/zse-96/X-Bogus 的"纯算"或"补环境"版本跑通
2. 跳到本技能：分析触发后的滑块/点选验证码（按各自 vendor 笔记走）
3. 把"验证码通过得到的 validate"接回到第 1 步生成签名
4. 完整闭环 = (h5st_node.js / zse96_node.js / xbogus_node.js) + (滑块 OCR 方案)

## 7. 来源

- CSDN 160164511：京东 H5ST 完整 Node 补环境实战
- CSDN 120891620 / 138296549：知乎 x-zse-96 两代版本
- CSDN 137170043：抖音 X-Bogus 19 位编码与算法
- 旧技能 `web-keygen-analysis` 同主题段落（h5st / x-zse-96 / x-bogus）
