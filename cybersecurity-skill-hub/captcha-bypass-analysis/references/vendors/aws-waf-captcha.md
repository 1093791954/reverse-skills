# AWS WAF Captcha / AWS WAF Challenge

## 1. 产品形态
- AWS 自研边缘人机验证，2022 上线，配合 WAF Web ACL 使用。两类规则：
  - **WAF Captcha Rule**：触发后返回 `text/html` 带 JS challenge + 九宫格点选/简单滑块。
  - **WAF Challenge Rule**（CHA）：纯 JS PoW + 指纹，无人机交互。
- 客户：Amazon 自家、Audible、Twitch 部分接口、AWS 控制台登录后端、不少使用 CloudFront 的 SaaS。
- 客户端 JS 来自 `https://<aws-region>.captcha.awswaf.com/<token>/jsapi.js`。

## 2. 检测维度
- **aws-waf-token cookie**：服务器签名（包含 IP+UA+TLS+签发时间）；过期 ~30 min。
- **aws-waf-token header**：API 调用回放时塞到 `x-aws-waf-token`。
- **指纹采集**：Canvas、WebGL、Audio、Plugin、screen、字体；UA-CH 严格校验。
- **PoW**：SHA-256 hashCash，难度难度位 18-24 不等。
- **题型**：九宫格图像点选（"Pick all squares with traffic lights"），偶尔出现旋转拖拽。
- **TLS 指纹**：必须 ALPN h2，curl/python-requests 默认 JA3 几乎必拦。

## 3. 关键端点与字段
| 端点 | 用途 | 关键字段 |
|------|------|---------|
| `<region>.captcha.awswaf.com/<token>/jsapi.js` | 加载 SDK | inline cdn token |
| `<region>.captcha.awswaf.com/<token>/<endpoint>/verify` | 提交答案 | `metrics`, `existing_token`, `client`, `solution`, `domain` |
| `<region>.token.awswaf.com/<token>/<endpoint>/inputs` | 上报指纹 | `inputs`(base64+rc4 类) |
| Cookie `aws-waf-token` | 通行证 | server-signed 不可伪造 |
| Header `x-amzn-waf-action` | 服务器侧指示 | `captcha`/`challenge`/`block` |

## 4. 已公开研究
- CSDN「【JS 逆向百例】aws-waf-token 算法与九宫格验证码分析」(149171547)：完整逆向 token 生成 + 九宫格答案提交。
- CSDN「FunCaptcha 解决方案」(150269212)：与 AWS WAF Captcha 的对比。
- CSDN「AWS WAF Captcha 与 reCAPTCHA / hCaptcha 对比」(类似综述类文章 4-5 篇出现在 q="AWS WAF Captcha 逆向" 命中里)。
- CapSolver / 2Captcha 文档：`AntiAwsWafTaskProxyLess` 任务类型，按调用计费。
- GitHub 关键词：`aws-waf-token bypass`、`awswaf challenge solver`，多个开源 PoC 仓库（部分已下架）。

## 5. 防御性分析思路（授权审计）
1. 触发：业务接口 405/202 + `x-amzn-waf-action: captcha` 即进入。
2. 抓 jsapi.js → 通常 1.4MB+，含 wasm 与 hash 逻辑；用 wabt 解 wasm，用 webpack-unpacker 拆 chunk。
3. token 解码：base64URL → 修改版 base64 → struct（version|ts|nonce|payload|hmac）。
4. 九宫格 OCR：CLIP / OpenAI Vision / Gemini Vision 都能稳定打过；`AntiAwsWafTask` 即云端代解。
5. 用 curl_cffi `impersonate=chrome131` 直接打 Verify 端点；TLS 指纹必须吻合，否则即使 token 正确也 403。
6. cookie 复用：拿到一次 `aws-waf-token` 在过期前可全站走，注意 IP 不变。

## 6. 已知缓解 / 更新历史
- 2022 上线时 token 仅 HMAC-SHA256，社区两周内出 PoC。
- 2023 加 Plain JS challenge（无交互 PoW），PoW 难度位增加。
- 2024 引入 wasm 校验段；UA-CH `Sec-CH-UA-Full-Version-List` 必须真实。
- 2025 部分 region 加 IP 信誉评分，云手机/数据中心 IP 直接 block。

## 7. 待研究问题
- `inputs` payload 内 RC4-like 函数的 key 派生（疑似从 token 第一段裂出）。
- WASM 模块在不同 region 是否共享同一份字节码。
- 难度位是否随站点风险等级动态调整。
