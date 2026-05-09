# Android Native 风控 - 摸底 raw-hits 批次 2

## Q11: `小红书 x-s x-s-common 算法 还原 逆向` (Bing, 2026-05)

- **Cloxl/xhshow: 小红书 xs 纯算 (GitHub)** — https://github.com/Cloxl/xhshow
- **【JS 逆向】2024-09 小红书 x-s-common 算法还原 (CSDN)** — https://blog.csdn.net/YCHMBb/article/details/142391556
- **小红书 X-s X-common 算法还原 202409 更新 (ITADN)** — https://itadn.com/i0_95642614292/3518771
  - signSvn 55 版本，重新混淆+注释抹除
- **小红书加密分析 X-S 与 X-S-Common 参数生成 (B 站)** — https://www.bilibili.com/video/BV1MsakezEnG/
- **某红书 Js 逆向思路 (掘金)** — https://juejin.cn/post/7563139451804254258
  - eval 运行两段代码初始化 window.mnsv2
- **某红书 X-s X-s-common VMP 逆向算法还原 (技术栈 2026-04)** — https://jishuzhan.net/article/2047492177362747393
- **某红书 x-s、x-s-common 参数分析与纯算 (kuazhi)** — https://www.kuazhi.com/post/713748134.html
- **小红书 x-s、x-s-common 算法研究 docx (book118)** — https://max.book118.com/html/2023/1205/7132162056006014.shtm
- **小红书 X-S(X-t,x-common) JS 纯算逆向 2024.8 (Gitee cornanluwei/xiaohongshu)** — https://gitee.com/cornanluwei/xiaohongshu


## Q12: `抖音 X-Bogus _signature x-tt-params 算法 还原` (Bing, 2026-05)

- **抖音 _signature 和 X-Bogus 还原 Python (CSDN 文库 2026)** — https://wenku.csdn.net/column/jk2q4626c7w
  - JSVMP→Python 全流程
- **x-bogus 逆向 抖音 _signature (知乎)** — https://zhuanlan.zhihu.com/p/634864314
- **B1gM8c/X-Bogus: 抖音 X-Bogus 生成接口 (GitHub)** — https://github.com/B1gM8c/X-Bogus
- **【JS 逆向】抖音巨量 X-Bogus 与 _signature (B 站)** — https://www.bilibili.com/video/BV1aF4m1P7un/
- **抖音下载视频+X-Bogus 参数 JS 逆向 (博客园)** — https://www.cnblogs.com/fuchangjiang/p/17891223.html
- **JS 逆向 某音 X-Bogus 补环境 (lyy077 博客)** — https://lyy077.github.io/JS%E9%80%86%E5%90%91%E6%A1%88%E4%BE%8B%E2%80%94%E2%80%94%E6%9F%90%E9%9F%B3X-Bogus%E5%8F%82%E6%95%B0%E9%80%86%E5%90%91%E5%88%86%E6%9E%90%E4%B9%8B%E8%A1%A5%E7%8E%AF%E5%A2%83/
- **Python 逆向 TikTok msToken+X-Bogus+signature (e-com-net)** — https://www.e-com-net.com/article/1902557145006665728.htm
- **[原创] WEB 逆向 X-Bogus 纯算+补环境 (看雪)** — https://bbs.kanxue.com/thread-281237.htm
- **使用 Python 和 JS 逆向抖音 X-Bogus (econow.cn)** — https://econow.cn/2023/11/22/【爬虫实战】使用Python和JS逆向抖音X-Bogus参数获取N条视频/
- **抖音 signature/ac_signature/X-Bogus 综合 (新码农博客)** — https://blog.addcoder.com/blog/article_detail/35a10144/

## Q13: `boss直聘 __zp_stoken__ zp_token 逆向 算法` (Bing, 2026-05)

- **boss 直聘 __zp_stoken__ 生成补环境 (CSDN 2024-02)** — https://blog.csdn.net/qq_57325259/article/details/136320269
  - 12 月更新后特征：动态代码每次请求不同
- **[原创] boss 直聘 __zp_stoken__ 控制平坦流纯算逆向 (看雪 2025-09)** — https://bbs.kanxue.com/thread-288403-1.htm
- **boss 直聘 __zp_stoken__ 逆向 (博客园 TNanko)** — https://www.cnblogs.com/tnanko/p/18156580
- **Boss 直聘 cookie 字段 __zp_stoken__ (腾讯云开发者)** — https://cloud.tencent.com/developer/article/2014566
- **boss 直聘最新版 zp_stoken 逆向分析 (知乎)** — https://zhuanlan.zhihu.com/p/425180886
  - nodejs 检测：__filename / Buffer 浏览器为 undefined
- **【JS】逆向实战 Boss 直聘 cookie/zp_stoken (B 站)** — https://www.bilibili.com/video/BV1UF3FeAEFe/
- **逆向破解 boss 直聘 __zp_stoken__ JS 混淆 + AST (阿里云开发者)** — https://developer.aliyun.com/article/1328914
- **boss 直聘 __zp_stoken__ 分析 (51CTO)** — https://blog.51cto.com/u_15835408/14542326
- **DrissionPage 爬 boss 直聘绕 __zp_stoken__ (技术栈)** — https://jishuzhan.net/article/2032643926889398273
- **zwgFF/zp_stoken_jsLearn (GitHub)** — https://github.com/zwgFF/zp_stoken_jsLearn

## Q14: `12306 RAIL_DEVICEID RAIL_EXPIRATION 逆向 算法` (Bing, 2026-05)

- **获取 RAIL_EXPIRATION 和 RAIL_DEVICEID (geekdaxue 12306-api-doc)** — https://geekdaxue.co/read/12306-api-doc/2.logdevice.md
  - hashAlg 函数返回 dict 拆解
- **12306 抢票系列：RAIL_DEVICEID 来源 (博客园 snowdreams1006)** — https://www.cnblogs.com/snowdreams1006/p/12316951.html
- **JS 逆向：分析 12306 设备码 RAIL_DEVICEID (CSDN)** — https://blog.csdn.net/weixin_31211821/article/details/117686084
- **12306 抢票 RAIL_DEVICEID 来源 (腾讯云开发者)** — https://cloud.tencent.com/developer/article/1588600
- **RAIL_EXPIRATION 已失效，更新获取设备信息 (GitHub J12306 issue)** — https://github.com/kalvinGit/J12306/issues/10
- **12306 抢票系列 RAIL_DEVICEID (bytezonex)** — https://www.bytezonex.com/archives/sJgQ1gvP.html
- **python-js 逆向破解 12306 cookie RAIL_DEVICEID (johnjgh)** — https://johnjgh.github.io/2019/11/13/python-js%E9%80%86%E5%90%91%E7%A0%B4%E8%A7%A312306%E7%BD%91%E7%AB%99%E5%B9%B6%E8%8E%B7%E5%8F%96cookie%E5%AD%97%E6%AE%B5RAIL-DEVICEID/
- **12306 抢票 RAIL_DEVICEID (开源中国)** — https://my.oschina.net/u/4348357/blog/3240538
- **12306 抢票 RAIL_DEVICEID (术之多)** — https://www.shuzhiduo.com/A/6pdDxkEOdw/
- **GitHub 开源抢票插件 (知乎)** — https://zhuanlan.zhihu.com/p/100530628

## Q15: `微博 aid 击客 算法 逆向 sina_visitor` (Bing, 2026-05)

- **[原创] 微博 12.5.1 算法研究 (看雪)** — https://bbs.kanxue.com/thread-272984.htm
  - DeviceId.getDeviceIdNative native 方法
- **微博完整逆向分析和数据抓取 (CSDN 专栏)** — https://download.csdn.net/blog/column/12440659/138464798
- **【某博系列 app 逆向】aid 参数 (B 站)** — https://www.bilibili.com/video/BV17Xj2zHEKX/
- **pokerfaceSad/SinaNetSpider 新浪微博关系网 (GitHub)** — https://github.com/pokerfaceSad/SinaNetSpider
  - 绕过新浪访客系统
- **从零开始逆向分析 APP 微博 APP 协议 (吾爱破解)** — https://www.52pojie.cn/thread-1370540-1-1.html
- **Android 新浪微博逆向 (51CTO)** — https://blog.51cto.com/u_16175451/13765283
- **微博登录流程逆向 + 加密参数 (极客日志 2025-01)** — https://zeeklog.com/-js-ni-xiang-bai-li-fu-za-de-deng-lu-guo-cheng-zui-xin-wei-bo-ni-xiang
  - 9 步登录流程，密码 RSA 加密
- **新浪微博逆向总结 (GitCode 项目)** — https://gitcode.com/Open-source-documentation-tutorial/1b891/tree/main

## Q16: `百度 acsToken 逆向 算法 zid` (Bing, 2026-05)

- **百度指数 Cipher-Text 与百度翻译 Acs-Token 逆向 (百度云开发者 2025-10)** — https://cloud.baidu.com/article/3866832
- **百度翻译 Acs-Token 调试 (CSDN Not__Cry)** — https://blog.csdn.net/Not__Cry/article/details/139726675
- **【JS 逆向百例】某度 Acs-Token、ab_sr (腾讯云 2025-12)** — https://cloud.tencent.com/developer/article/2606384
  - AES 加密+环境检测，AST 解混淆
- **某度 Acs-Token、ab_sr (K 哥爬虫 博客园)** — https://www.cnblogs.com/ikdl/p/19386049
  - 22 年新增 Acs-Token，加密 js 自注释为"玉门关"
- **百度指数 Cipher-Text、百度翻译 Acs-Token (掘金 K 哥)** — https://juejin.cn/post/7133151365806686245
- **逆向某平台发帖接口 Acs-Token (知乎)** — https://zhuanlan.zhihu.com/p/1953560209537611152
- **百度指数 Cipher-Text、百度翻译 Acs-Token (zeeklog mirror)** — https://zeeklog.com/bai-du-zhi-shu-cipher-text-bai-du-fan-yi-acs-token-ni-xiang-fen-xi/
- **超详细百度翻译 js 逆向 token+sign (51CTO)** — https://blog.51cto.com/u_16128190/6345223
- **百度指数+百度翻译 Acs-Token (小猿 1024)** — https://www.xiaoyuan1024.com/5631.html
- **百度翻译逆向之 Acs-Token (雷神 nb)** — https://www.leishennb.icu/article/687ca2bbbdf21c32e5ca2dd2
