# Web 风控 - 摸底 raw-hits 批次 1（国际反爬厂商 + 国内大站参数）

## Q1: `akamai sensor_data _abck 逆向 jsvmp 算法` (Bing, 2026-05)

- **Akamai 3.0 反爬分析与 sensor-data 算法 (CSDN 2025-01)** — https://blog.csdn.net/weixin_43845191/article/details/144977354
  - Akamai 3.0 每一两天换 js 文件
- **Akamai 3.0 反爬分析镜像 (kuazhi)** — https://www.kuazhi.com/post/716083219.html
- **xiaoweigege/akamai2.0-sensor_data: bypass (GitHub)** — https://github.com/xiaoweigege/akamai2.0-sensor_data
- **Akamai 2.0 sensor_data 参数及 akamai-bm (博客园)** — https://www.cnblogs.com/xiaoweigege/p/17455532.html
- **akamai 3.0 反爬 sensor_data 主流程 (B 站)** — https://www.bilibili.com/video/BV1bAifYkE7i/
- **Akamai 反爬 JS 逆向 抓包到分析 (知乎)** — https://zhuanlan.zhihu.com/p/1953445818599180205
- **[原创] Akamai 逆向分析 part1 (看雪 2025-07)** — https://bbs.kanxue.com/thread-287819.htm
  - 同版本 akamai cKH 类周变动，纯算可行
- **Akamai 3.0 反爬 sensor_data (ldpk mirror)** — https://www.ldpk.cn/news/435340.html
- **akamai 2.0 cookie 反爬 上 (CN-SEC)** — https://cn-sec.com/archives/3471249.html
- **Akamai 某环境 VMP 算法分析 (吾爱破解)** — https://www.52pojie.cn/thread-2009699-1-1.html

## Q2: `cloudflare turnstile cf_clearance __cf_bm 逆向 绕过` (Bing, 2026-05)

- **Cloudflare 防护技术解析与 Turnstile 验证实战 (CSDN 2025-09)** — https://blog.csdn.net/qq_33253945/article/details/152059625
  - cf_clearance 与 __cf_bm cookie 模式
- **r0vx/turnstile cf-clearance-scraper-go (GitHub 2025-08)** — https://github.com/r0vx/turnstile
  - puppeteer-real-browser-go 实现
- **取巧绕过 Cloudflare v2 验证 (林伟源 2023-03)** — https://linweiyuan.github.io/2023/03/14/一种取巧的方式绕过-Cloudflare-v2-验证.html
- **Cloudflare Turnstile CSP doc** — https://developers.cloudflare.com/turnstile/reference/content-security-policy/
- **cloudflare 五秒盾突破 (掘金)** — https://juejin.cn/post/7238920970563027003
- **Cloudflare Turnstile 验证码插件 (linux.do 2025-10)** — https://linux.do/t/topic/1010988
  - MITM 劫持 challenges.cloudflare.com，逆向后返回
- **cloudflare 5s 盾解密 (dairoot 2024-08)** — https://dairoot.cn/2024/08/05/cloudflare5s-bypass/
- **Cloudflare Turnstile 演示 (2captcha)** — https://2captcha.com/zh/demo/cloudflare-turnstile
- **Cloudflare 逆向 JS 加密第一步 (resourch.com 2022)** — https://www.resourch.com/archives/19.html
- **过 cf turnstile 与五秒盾 (小河守候)** — https://zhun.org/archives/293
  - DrissionPage 过 5 秒盾

## Q3: `datadome cookie slider 逆向 bypass` (Bing, 2026-05)

- **ellisfan/bypass-datadome (GitHub)** — https://github.com/ellisfan/bypass-datadome
- **Datadome 2026 最新逆向分析 支持 Hermes (CSDN)** — https://blog.csdn.net/m0_66839504/article/details/129361471
- **某旅行网站 datadome 初尝试 (知乎)** — https://zhuanlan.zhihu.com/p/1921367769292714269
- **datadome 3.40 分钟解混淆 (B 站墨竹_zs)** — https://www.bilibili.com/video/BV1Jj3Hz3E96/
  - 包含 reese84/淘系 231/akamai 教程
- **How to Bypass DataDome 2026 (ZenRows)** — https://www.zenrows.com/blog/datadome-bypass
- **chrisyp/nocaptcha datadome zh-CN** — https://chrisyp.github.io/zh-CN/datadome.html
- **Guide to Bypassing DataDome 2025 (kameleo)** — https://kameleo.io/blog/guide-to-bypassing-datadome
- **绕过 Cloudflare 和 DataDome (lxspider 2024-08)** — http://www.lxspider.com/?p=1098
- **如何绕过 DataDome 保护的网站 (姚伟斌)** — https://yaoweibin.cn/datadome-bypass/
- **Bypass DataDome with Python 2026 Guide (data-journal)** — https://www.data-journal.org/cn/data-scraping/bypass-datadome-with-python/

## Q4: `perimeterx px _px2 _px3 逆向 bypass` (Bing, 2026-05)

- **Pr0t0ns/PerimeterX-Reverse (GitHub)** — https://github.com/Pr0t0ns/PerimeterX-Reverse
- **如何绕过 PerimeterX (姚伟斌)** — https://yaoweibin.cn/perimeterx-bypass/
- **PerimeterX 逆向分析 (二进制之旅 2026-04)** — https://blog.xzregister.cn/2026/04/18/px/
  - 4 次请求(3 bundle + 1 g)，main.min.js 混淆，AI 解混淆
- **绕过 PerimeterX 6 种方法 (集蜂云)** — https://www.beeize.com/tecShare/article/perimeterx-bypass/
- **PX3 按压反混淆+逆向 (yazong 1997.pro 2024-03)** — https://www.1997.pro/archives/1711604818499
- **chrisyp/nocaptcha perimeterx zh-CN** — https://chrisyp.github.io/zh-CN/perimeterx.html
  - cookie _px2/_px3 三种验证模式
- **SpiderAPI: PerimeterX/HUMAN Challenge** — https://spiderapi.cn/captcha/perimeterx/
- **【perimeterx】px3 逆向分析 (icode)** — https://icode.best/i/98248060793566
- **Reversing PerimeterX Web Sensor (autodev 2026-02)** — https://autodev.blog/posts/px-web-sensor-article/

## Q5: `瑞数 5代 6代 逆向 动态 jsvmp 算法` (Bing, 2026-05)

- **瑞数 6 代 JS 逆向分析 (K 哥爬虫 博客园)** — https://www.cnblogs.com/ikdl/p/17778885.html
  - 动态值匹配：5 代 vs 6 代差异
- **瑞数 6 代 JS 逆向 (腾讯云开发者)** — https://cloud.tencent.com/developer/article/2348357
- **pysunday/rs-reverse 瑞数 vmp 纯算法 (GitHub)** — https://github.com/pysunday/rs-reverse
- **某期刊瑞数 6 代 JSVMP 原型链检测+补环境 (B 站)** — https://www.bilibili.com/video/BV1QEwReKEWB/
- **jsvmp 逆向实战 x-s/x-t 算法还原 (51CTO)** — https://blog.51cto.com/u_16213567/14308914
- **某标局最新瑞数 6 vmp 破解分析 (掘金 2024-07)** — https://juejin.cn/post/7392070976060031012
- **js 逆向思路-区分瑞数 vmp/6/5/4/3 反爬 (CN-SEC)** — https://cn-sec.com/archives/1882149.html
- **海关征信瑞数 6 vmp 算法深度解析 (百度开发者 2025-10)** — https://developer.baidu.com/article/detail.html?id=4107009

## Q6: `微信小程序 wxapkg 解包 逆向 加密` (Bing, 2026-05)

- **微信小程序+反编译+AES 加解密爬虫 (CSDN 2025-12)** — https://blog.csdn.net/huagangwang/article/details/135013405
- **微信小程序逆向解密实战 (博客园 2026-01)** — https://www.cnblogs.com/jzssuanfa/p/19455255
- **微信小程序抓包解密与反编译工具 (掘金 2023-12)** — https://juejin.cn/post/7312678013559636006
- **2025 年最新反编译微信小程序教程 (SegmentFault)** — https://segmentfault.com/a/1190000046438288
- **See Wxapkg 在线反编译工具** — https://seewxapkg.keepbuild.cn/
- **分包的微信小程序解包反编译 (知乎)** — https://zhuanlan.zhihu.com/p/719729034
- **小程序反编译+最新存储位置 (FreeBuf 2025-08)** — https://www.freebuf.com/articles/sectool/443248.html
- **wxapkg 文件解析工具 unwxapkg (GitCode)** — https://blog.gitcode.com/ec16be06c7e4ea114ba23769830c875b.html
- **[原创] 微信小程序反编译/解包 (看雪)** — https://bbs.kanxue.com/thread-281804.htm

## Q7: `jsvmp 补环境 纯算 还原 逆向 头绪` (Bing, 2026-05)

- **JS 逆向 JSVMP 纯算法还原 (CSDN 2024-03)** — https://blog.csdn.net/zlc1990628/article/details/136558267
  - 三种方法：RPC/补环境/日志断点
- **TK X-Gnarly：AI 辅助 JSVMP 纯算还原 (zeeklog 2026-04)** — https://zeeklog.com/tk-x-gnarly-ji-yu-ai-fu-zhu-de-jsvmp-chun-suan-huan-yuan-fang-an-2
  - Webmssdk.js + 日志挂钩
- **知乎 jsvmp 纯算还原 (B 站)** — https://www.bilibili.com/video/BV1Vjhvz7EN1/
- **某音 X-Bogus JSVMP 纯算 (K 哥爬虫 博客园 2022)** — https://www.cnblogs.com/ikdl/p/16807224.html
- **某东签名 jsvmp 插桩纯算还原 (舟涯 2025-11)** — https://blog.zhx47.top/archives/1762148186443
- **pysunday/sdenv 补环境框架 (GitHub)** — https://github.com/pysunday/sdenv
- **jsvmp 逆向实战 x-s/x-t (51CTO 2025-11)** — https://blog.51cto.com/u_16213567/14308914
- **JSVMP 补环境 (ycxlo blog 2025-08)** — https://ilikeoyt.github.io/2025/08/22/JSVMP补环境/
- **X-Bogus JSVMP 纯算 (腾讯云)** — https://cloud.tencent.com/developer/article/2208864
- **xhs jsvmp 逆向记录 (掘金 2023)** — https://juejin.cn/post/7238539643947778109

## Q8: `kasada x-kpsdk-ct ips.js 逆向 bypass wasm` (Bing, 2026-05)

- **chrisyp/nocaptcha kasada zh-CN** — https://chrisyp.github.io/zh-CN/kasada.html
- **kasada 代码分析+插桩点+反编译 (yazong 2024-02)** — https://1997.pro/archives/1708325827794
- **新一代 vmp 混淆保护 Kasada (知乎 2025-07)** — https://zhuanlan.zhihu.com/p/1923793309379309941
  - ips.js 是 vmp，生成 X-Kpsdk-Ct/Dt 和 payload
- **lktop/kpsdk: Kasada x (GitHub 2021-06)** — https://github.com/lktop/kpsdk
- **Kasada (Spider-乾坤 sakura-luo)** — https://sakura-luo.top/kasada
- **Kasada Solver API (CaptchaSolv)** — https://captchasolv.com/zh/captcha/kasada
- **Kasada-kpsdk p.js+ips.js (Gitee zhzhsgg)** — https://gitee.com/zhzhsgg/kasada-kpsdk
- **如何绕过 Kasada (姚伟斌)** — https://yaoweibin.cn/kasada-bypass/
- **Kasada 任务 (EzCaptcha Confluence 2025-11)** — https://ezcaptcha.atlassian.net/wiki/spaces/IS/pages/38338692/Kasada

## Q9: `imperva incapsula reese84 逆向 bypass` (Bing, 2026-05)

- **BottingRocks/Incapsula payload (GitHub)** — https://github.com/BottingRocks/Incapsula
- **reese84 Bypass Solution (TakionAPI doc)** — https://docs.takionapi.tech/incapsula/reese84
- **绕过 Incapsula (姚伟斌 2023-11)** — https://yaoweibin.cn/incapsula-bypass/
- **Deobfuscating Imperva utmvc Anti-Bot (yoghurtbot 2023-03)** — https://yoghurtbot.github.io/2023/03/04/Deobfuscating-Incapsula-s-UTMVC-Anti-Bot/
- **Incapsula Reese84 最新版 JSVMP (rhkb 2026-04)** — http://www.rhkb.cn/news/198799
- **Bypass Incapsula/Imperva 96% (Scrapfly)** — https://scrapfly.io/bypass/incapsula
- **Bypass Imperva Incapsula 2025 (ZenRows)** — https://www.zenrows.com/blog/incapsula-bypass
- **reese84 及 _utmvc 逆向流程分析 (吾爱破解 2024-04)** — https://www.52pojie.cn/thread-1912763-1-1.html
- **补环境框架测试 inCaplusa reese84 (阿龙 2024-02)** — http://program.robinjia.cc/2024/02/24/用补环境框架测试inCaplusa之reese84/
