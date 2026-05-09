# 国际验证码：reCAPTCHA / hCaptcha / Arkose Labs FunCAPTCHA - notes

## 一、Google reCAPTCHA v2/v3/Enterprise

### 签名
- iframe `anchor.html` + `bframe.html`。
- POST `/recaptcha/api2/reload?k=...`。
- v2 用图形/复选框；v3 给"分数"（0~1，越接近 1 越像真人）；Enterprise 是付费版+风险分析。

### 还原思路
- **v2**：图像识别（YOLOv8 + CLIP），但成本高且不稳。
- **v3 score warming**：稳定 cookie + 真人鼠标轨迹+老 session → 分数能升到 0.7+。
- **付费 API**：anti-captcha、CapSolver、2captcha、yescaptcha、xCaptcha、CapMonster 都支持。

### URL
- [Python 爬虫绕过 Google reCAPTCHA (CSDN 2025-10)](https://blog.csdn.net/SUEJESDA/article/details/153252940)
- [绕过 reCAPTCHA V2/V3 (掘金 2024-10)](https://juejin.cn/post/7420718445191364623)
- [Python 绕过 reCAPTCHA v3 高分 (nextcaptcha)](https://nextcaptcha.com/zh/blog/bypass-recaptcha-v3-with-high-scores-using-python)
- [NodeJS+Puppeteer 绕过 v3 (anti-captcha)](https://anti-captcha.com/zh/tutorials/how-to-bypass-recaptcha-v3)
- [xHossein/PyPasser (GitHub)](https://github.com/xHossein/PyPasser)
- [高分破解 v3 (CapSolver)](https://www.capsolver.com/zh/blog/reCAPTCHA/how-to-bypass-recaptchav3-with-capsolver)

## 二、hCaptcha (含 Enterprise)

### 签名
- 主域 `hcaptcha.com/captcha/v1/api.js`。
- 参数：`siteKey`+`token` 64 字符。
- Cloudflare 在弃用 reCAPTCHA Enterprise 后切到 hCaptcha。

### 还原思路
- 基本只能用付费 API（YesCaptcha、CapSolver、Bright Data）。
- Bright Data 提供机器学习+IP 轮换+代理基础设施，是较稳的方案。
- 2captcha 与 anti-captcha 用真人池。

### URL
- [如何优雅破解 HCaptcha (博客园)](https://www.cnblogs.com/cuihongyu3503319/p/17620426.html)
- [hcaptcha 无感验证码逆向闲谈 (CSDN 2025-03)](https://blog.csdn.net/qq_45696543/article/details/146364872)
- [绕过 hCaptcha & Cloudflare Captcha (skk.moe)](https://blog.skk.moe/post/bypass-hcaptcha/)
- [bright-cn/hcaptcha-solver (GitHub 2025-09)](https://github.com/bright-cn/hcaptcha-solver)
- [hcaptcha 逆向分析 (REXiaoHe 2025-04)](https://yxc.net.cn/index.php/2025/04/03/hcaptcha逆向分析/)

## 三、Arkose Labs FunCAPTCHA

### 签名
- 主域 `funcaptcha.com`。
- 接口：`/fc/gt2/public_key/{public_key}`、`/fc/a/`、`/fc/gc/`。
- 关键参数：`bda`（浏览器指纹+token 协商）、`token` 形如 `26318777fbd628c58.timestamp|...`。
- 类型：3D 旋转图、Match Game、拼图。
- 部署：Twitter/X、Roblox、Steam 等。

### 还原思路
- **bda 算法**：浏览器指纹+key 协商，公开实现 `unfuncaptcha-bda` PyPI。
- **3D 旋转图**：YOLO 训练 + 角度回归神经网。
- **Match Game**：图像分类。
- **付费**：CapSolver 等都支持。

### URL
- [ArkoseLabs FunCaptcha 协议逆向 (haloowhite 2025-11)](https://haloowhite.com/2025/11/13/arkose-funcaptcha-reverse-tutorial/)
- [arkose-funcaptcha-reverse-tutorial.md (GitHub)](https://github.com/haloowhite/blog/blob/main/_posts/2025-11-13-arkose-funcaptcha-reverse-tutorial.md)
- [基于易语言 ArkoseLabs BDA (CSDN 文库)](https://wenku.csdn.net/doc/3dq3nydraq)
- [x 账号注册解锁 funcaptcha 逆向 (知乎)](https://zhuanlan.zhihu.com/p/1928982270292754609)
- [unfuncaptcha-bda PyPI](https://pypi.org/project/unfuncaptcha-bda/)
- [SpiderAPI: Arkose Labs FunCAPTCHA](https://spiderapi.cn/captcha/funcaptcha/)
- [2captcha Arkose Labs API](https://2captcha.com/api-docs/arkoselabs-funcaptcha)

## raw-hits 来源

- reCAPTCHA：[captcha-batch1.md Q3](../raw-hits/captcha-batch1.md)。
- hCaptcha：[captcha-batch1.md Q4](../raw-hits/captcha-batch1.md)。
- Arkose：[captcha-batch1.md Q5](../raw-hits/captcha-batch1.md)。

## 通用建议

1. 国际三大 captcha 几乎都不支持单纯纯算（Google/hCaptcha/Arkose 持续更新模型）。
2. 实战靠组合拳：真浏览器+真人轨迹+stable cookie+住宅 IP+付费 API 兜底。
3. 行为模型很重要：reCAPTCHA v3 score 与历史 session 强相关，warming session 比直接刷分更稳。
