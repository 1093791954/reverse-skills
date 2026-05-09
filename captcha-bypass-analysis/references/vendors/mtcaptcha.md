# MTCaptcha

## 1. 产品形态
- 2017 年成立、欧洲背景的合规导向 captcha 厂商，主打"低数据收集 + GDPR / SOC2 合规"。
- 题型：图片字符（distorted text）、4 字符变形 + 干扰线，标准 v1；2023 起新增"PoW + 图标"轻量版。
- 集成域：`service.mtcaptcha.com`、`service.mtcaptcha.io`。
- 客户类型：合规要求高的 SaaS、欧洲银行、政府站点；面向中国大陆站点不多，因此中文圈讨论少。

## 2. 检测维度
- **OCR 难度**：4-6 字符强变形（rotation、warp、噪线），ddddocr 默认权重命中率 ~25-50%；要训自有数据集。
- **token 链路**：客户端拿到 `mtcaptcha-verifiedtoken-vXXX`，服务端用 secret 调 `/api/checktoken` 校验。
- **指纹**：Canvas/UA-CH/JS 内 timer 抖动；非主流的是它显式声明"不收集 mouse trace"，故行为段较弱。
- **PoW**：可选，开通后客户端做 SHA-256 前导 0。

## 3. 关键端点与字段
| 端点 | 用途 | 关键字段 |
|------|------|---------|
| `service.mtcaptcha.com/mtcv1/api/getchallenge` | 拉题 | `sitekey`, `lang`, `customparam` |
| `service.mtcaptcha.com/mtcv1/api/verifytoken` | 提交 | `vt`(verifyToken), `vsig` |
| 服务端 `service.mtcaptcha.com/mtcv1/api/checktoken` | 二次校验 | `privatekey`, `vt`, `tokenInfo` |
| 字符串 `mtcaptcha-verifiedtoken-v1:<base64>` | 通行证 | base64 内嵌 sitekey/expire/sig |

## 4. 已公开研究
- CSDN「10 款行为验证码平台排行榜，选型必备参考」(146397133)：MTCaptcha 与 reCAPTCHA / hCaptcha / 极验对比。
- CSDN「行为式验证码与传统验证码的区别，以及主流产品盘点」(147077448)。
- CSDN「自动化测试中几种常见验证码的处理方式及如何实现？」(134983064)。
- CSDN「逆向工程验证码」(137153740)。
- CSDN「如何自动化解决或破解文字、图像、滑块、点选等验证码问题」(131476509)：含 MTCaptcha 一节。
- 2Captcha 文档：`MTCaptchaTaskProxyless`，5-15s 平均答题时间。

## 5. 防御性分析思路（授权审计）
1. token 是 server-signed，一次性，不能纯客户端伪造，必须真把图给打出来。
2. 训练 OCR：用 CRNN + CTC，自采 5k-10k 张样本可达 90%+。
3. PoW 段（如开启）：纯算 SHA-256 暴搜，CPU 可承受。
4. UA-CH/Canvas 校验弱，但 IP 信誉高敏，建议住宅代理。
5. 不可靠：mtcaptcha 在 Tor 出口几乎全拒。

## 6. 已知缓解 / 更新历史
- 2022 增加干扰线密度与字符 warp。
- 2023 开放 PoW 选项。
- 2024 加 sitekey 级别难度档位（easy/medium/hard）；hard 档 ddddocr 默认权重低于 20%。

## 7. 待研究问题
- 不同档位字符集差异（是否有 case-sensitive）。
- 服务端 checktoken 的 sig 算法（推测 HMAC-SHA256，但参与字段未公开）。
- 训练 OCR 时干扰线最有效的 augmentation 顺序。
