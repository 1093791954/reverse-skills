# Captcha 风控 - 摸底 raw-hits 批次 1（人机验证：滑块/点选/无感/三方厂商）

## Q1: `网易盾 NECaptcha 滑块 逆向 算法` (Bing, 2026-05)

- **逆向网易易盾滑块+生成 JS 滑动轨迹 (CSDN)** — https://blog.csdn.net/weixin_42524276/article/details/160848618
- **Python 爬虫逆向：网易易盾滑块验证码请求参数分析 (zeeklog 2024-02)** — https://zeeklog.com/python-pa-chong-ni-xiang-an-li-wang-yi-yi-dun-hua-kuai-qing-qiu-can-shu-fen-xi-hua-kuai-yan-zheng-ma
- **最新版网易易盾滑块验证码解析 cb 硬扣 JS (B 站)** — https://www.bilibili.com/video/BV1b4P2e1EkZ/
- **网易易盾验证码核心参数全攻略 无感滑块点选 (ttocr 2026-03)** — https://www.ttocr.com/word/article.php?slug=article-20260319082005
  - id/token/fp/actoken/data/validate/NECaptchaValidate 各参数生成
- **【web js 逆向分析易盾滑块 fp 参数】(技术栈)** — https://jishuzhan.net/article/1887060578627751937
- **【验证码识别】绕过网易滑动验证码 (掘金)** — https://juejin.cn/post/6916052135310262279
  - java + selenium + OpenCV
- **网易易盾滑块逆向分析 (易微帮)** — https://www.ewbang.com/community/article/details/961865456.html
  - 轨迹数组 a，固定取前 50 位加密
- **网易易盾滑块 (overfit mirror)** — https://avoid.overfit.cn/post/02fa625ef00d45c38b94e199d093b6ab
- **网易滑块 data 与 cb 参数逆向 (知乎)** — https://zhuanlan.zhihu.com/p/624860656
- **0xAllenChen/spider_reverse 综合案例 (GitHub)** — https://github.com/0xAllenChen/spider_reverse
  - TLS 指纹/瑞数/网易易盾/微信小程序反编译/极验/Boss 直聘/qq 音乐

## Q2: `极验 geetest v4 w 参数 逆向 算法` (Bing, 2026-05)

- **极验 4 滑块验证码逆向与纯算实现 (CSDN 2025-12)** — https://blog.csdn.net/weixin_35906794/article/details/156308786
- **Geetest 极验 4 代滑块验证算法逆向 (B 站)** — https://www.bilibili.com/video/BV1USScBrEtH/
- **parasyte-x/GeetestReverseEngineering (GitHub)** — https://github.com/parasyte-x/GeetestReverseEngineering
- **【逆向案例】不能再细的极验滑块 w 值逆向 (知乎)** — https://zhuanlan.zhihu.com/p/583603620
- **极验滑块验证码新思路 (lyy077 何仕鹏)** — https://lyy077.github.io/JS%E9%80%86%E5%90%91%E6%A1%88%E4%BE%8B%E2%80%94%E2%80%94%E6%9E%81%E9%AA%8C%E6%BB%91%E5%9D%97%E9%AA%8C%E8%AF%81%E7%A0%81%E6%96%B0%E6%80%9D%E8%B7%AF/
- **极验四代滑块验证码逆向学习 (SegmentFault)** — https://segmentfault.com/a/1190000044880224
  - w = 轨迹+滑动时间+滑动距离+userresponse+device_id+pow_msg 加密
- **极验 4.0 滑动验证码逆向 (博客园 是四不是十)** — https://www.cnblogs.com/FlowerNotGiveYou/p/18872578
- **【Web 逆向】极验 4 代九宫格协议分析 (CN-SEC)** — https://cn-sec.com/archives/4449663.html
- **某验四代动态参数逆向详解 (掘金)** — https://juejin.cn/post/7469666524258500660
- **某验四代动态参数逆向 (搜狐)** — https://www.sohu.com/a/855862633_120818776

## Q3: `recaptcha v3 score bypass 绕过 构造` (Bing, 2026-05)

- **Python 爬虫绕过 Google reCAPTCHA 终极指南 (CSDN 2025-10)** — https://blog.csdn.net/SUEJESDA/article/details/153252940
- **绕过 reCAPTCHA V2/V3 (掘金)** — https://juejin.cn/post/7420718445191364623
- **绕过 reCAPTCHA V2/V3 Python+Selenium (技术栈)** — https://jishuzhan.net/article/1904726362508832770
- **xHossein/PyPasser: Bypassing reCaptcha V3 (GitHub)** — https://github.com/xHossein/PyPasser
- **高分破解 reCAPTCHA v3 (CapSolver)** — https://www.capsolver.com/zh/blog/reCAPTCHA/how-to-bypass-recaptchav3-with-capsolver
- **Python 绕过 reCAPTCHA v3 高分 (nextcaptcha)** — https://nextcaptcha.com/zh/blog/bypass-recaptcha-v3-with-high-scores-using-python
- **NodeJS + Puppeteer 绕过 Recaptcha V3 (anti-captcha)** — https://anti-captcha.com/zh/tutorials/how-to-bypass-recaptcha-v3
- **绕过谷歌验证码新方案 (知乎 2021)** — https://zhuanlan.zhihu.com/p/388628182
- **绕过 reCAPTCHA V2/V3 实战指南 (iotword)** — https://www.iotword.com/39754.html
- **绕过 reCAPTCHA V2/V3 (易微帮)** — https://www.ewbang.com/community/article/details/1000187497.html

## Q4: `hcaptcha 逆向 bypass token enterprise` (Bing, 2026-05)

- **如何优雅的破解 HCaptcha (博客园 宏宇 2023)** — https://www.cnblogs.com/cuihongyu3503319/p/17620426.html
- **hcaptcha (hcp) 无感验证码逆向闲谈 (CSDN 2025-03)** — https://blog.csdn.net/qq_45696543/article/details/146364872
- **绕过 hCaptcha & Cloudflare Captcha (skk.moe)** — https://blog.skk.moe/post/bypass-hcaptcha/
- **bright-cn/hcaptcha-solver (GitHub 2025-09)** — https://github.com/bright-cn/hcaptcha-solver
- **绕过 reCAPTCHA V2/V3 (掘金)** — https://juejin.cn/post/7420718445191364623
- **HCaptcha 破解 (知乎)** — https://zhuanlan.zhihu.com/p/521583792
- **简单绕过 hCaptcha 验证 (万里淘知 2024-06)** — https://www.hovthen.com/hCaptcha.html
- **Python 绕开 hcaptcha (PingCode)** — https://docs.pingcode.com/baike/800332
- **hcaptcha 逆向分析 (REXiaoHe 2025-04)** — https://yxc.net.cn/index.php/2025/04/03/hcaptcha逆向分析/
- **绕过 hCaptcha (linux.do 2025-01)** — https://linux.do/t/topic/377328

## Q5: `arkose labs funcaptcha 逆向 bda token` (Bing, 2026-05)

- **ArkoseLabs FunCaptcha 协议逆向 (haloowhite 2025-11)** — https://haloowhite.com/2025/11/13/arkose-funcaptcha-reverse-tutorial/
- **基于易语言 ArkoseLabs BDA + FunCaptcha (CSDN 文库)** — https://wenku.csdn.net/doc/3dq3nydraq
- **arkose-funcaptcha-reverse-tutorial.md (GitHub)** — https://github.com/haloowhite/blog/blob/main/_posts/2025-11-13-arkose-funcaptcha-reverse-tutorial.md
- **x 账号注册解锁 funcaptcha 逆向 (知乎)** — https://zhuanlan.zhihu.com/p/1928982270292754609
- **Arkose FunCaptcha 参数逆向 (V2EX 2025-11)** — https://www.v2ex.com/t/1174536
- **SpiderAPI: Arkose Labs FunCAPTCHA** — https://spiderapi.cn/captcha/funcaptcha/
- **FunCaptcha 自动识别 (Capmonster doc)** — https://docs.capmonster.cloud/zh/docs/captchas/funcaptcha-task/
- **arkoselabs 的 bda + FunCaptcha (精易论坛)** — https://bbs.ijingyi.com/thread-14655213-1-1.html
- **unfuncaptcha-bda PyPI** — https://pypi.org/project/unfuncaptcha-bda/
- **2captcha Arkose Labs API 文档** — https://2captcha.com/api-docs/arkoselabs-funcaptcha

## Q6: `ddddocr 滑块 点选 验证码 识别` (Bing, 2026-05)

- **ddddocr 库全攻略 (百度云开发者 2025-10)** — https://cloud.baidu.com/article/4202705
- **ddddocr 库的使用 图片/滑块/坐标 (CSDN 2025-10)** — https://blog.csdn.net/m0_64408930/article/details/149200690
- **Python 识别图片/滑块验证码 (博客园 huangcong)** — https://www.cnblogs.com/huangcong/p/18288175
- **sml2h3/ddddocr (GitHub)** — https://github.com/sml2h3/ddddocr
- **DdddOcr 滑块验证码使用 (知乎)** — https://zhuanlan.zhihu.com/p/1931104560073646236
- **ddddocr 通用验证码 OCR pypi (Gitee mirror)** — https://gitee.com/fkgeek/ddddocr
- **极验滑动验证码 ddddocr 免费方案 (技术栈 2026-04)** — https://jishuzhan.net/article/2041389302135980033
- **带带弟弟 ddddocr 各种类型 (掘金)** — https://juejin.cn/post/7278286913944289340
- **Pytorch+ddddocr 点选验证码 (灰信网)** — https://www.freesion.com/article/69122634328/
- **python ddddocr 点选验证码 (51CTO)** — https://blog.51cto.com/u_16213306/9025503

## Q7: `阿里 x5sec _bx-v 逆向 nocaptcha 滑块` (Bing, 2026-05)

- **某里 v2 滑动验证码分析 (K 哥爬虫 博客园 2024-11)** — https://www.cnblogs.com/ikdl/p/18576586
  - 1.1.0 到 1.1.10 滑块版本演进
- **阿里系 x5sec 逆向 (icode.best 2025-06)** — https://icode.best/i/659939405503278
  - bx-pp, bx-et, slidedata 加密参数
- **daxiongaijingxiang/x82y 阿里滑块 (GitHub)** — https://github.com/daxiongaijingxiang/x82y
- **阿里 v2 滑块 sg.js 设备指纹 (掘金 2025-04)** — https://juejin.cn/post/7489362433359036443
  - F017 动态 key 错误的处理
- **淘宝 x5sec 普通滑块分析 (51CTO 2026-04)** — https://blog.51cto.com/u_15835408/14545164
- **阿里 1688 阿里滑块 231 x5sec (技术栈 2024-11)** — https://jishuzhan.net/article/1856050465993658369
- **阿里 227 x82y 纯算 (知乎)** — https://zhuanlan.zhihu.com/p/706291170
- **C 阿里淘宝滑块工具 (GitCode 68bbd)** — https://gitcode.com/open-source-toolkit/68bbd/blob/main/README.md
  - x5sec 协议 + 226 + slidedata
- **阿里 taobao 滑条验证码 x5sec slidedata (overfit 2023)** — https://avoid.overfit.cn/post/5c46c1aa94c545829cb8a3269d20f62a
