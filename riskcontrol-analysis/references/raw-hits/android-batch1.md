# Android Native 风控 - 摸底 raw-hits 批次 1

> 这份文件是**原始搜索命中**，未经炼化。每个 ## 段落是一个 query，下面列出 Bing 真实结果的 title / URL / snippet。后续会基于这些原始命中做炼化进 `references/android/<topic>-notes.md`。

---

## Q1: `"x-gorgon" 算法 还原 douyin` (Bing, 2026-05)

- **douyin algorithm, X-Ladon, X-Argus, X-Gorgon, X-Khronos, X ...** — https://github.com/huaerxiela/douyin-algorithm
  - 仓库不再更新了，有我开源的这些，有需求的自己分析算法也没啥问题了。另外 douyin 和 tiktok 算法都差不多，分析一份，改改就能适配另一个。仓库代码中 sm3 的算法有点问题…
- **抖音TikTok算法分析 X-Gorgon X-Ladon X-Argus XG TikTok ...** — https://zhuanlan.zhihu.com/p/499766958
- **抖音xgorgon03，含java、python、js版源码 - 代码先锋网** — https://www.codeleading.com/article/98445177429/
  - 前言：抖音xgorgon算法是核心算法（其他常用的还有设备注册算法deviceid、xlog算法等），基本每一个接口都需要用到xgorgon…
- **抖音短视频x-gorgon算法入口定位查找过程笔记 - CSDN** — https://blog.csdn.net/2403_87731058/article/details/144614392
  - 抖音作为目前流量最大、日活跃最高的平台，目前也有很多不同行业的人对它进行逆向分析研究…
- **最新app逆向——抖音app逆向 X-gorgon加密字段算法解析** — https://www.bilibili.com/video/BV1Lp421X79b/
  - 21 条视频，UP 主完整逆向课程
- **[原创]抖音短视频x-gorgon算法入口定位查找过程笔记 (看雪)** — https://bbs.kanxue.com/thread-259906.htm
- **a20201212-111126-124: 抖音 xgorgon 0408 数据加密算法 (Gitee)** — https://gitee.com/liqiumeng/a20201212-111126-124
  - 关键算法被 VM，只能动态分析去理解
- **[原创]某音APP逆向关键参数 (X-Ladon、X-Gorgon、X-Argus) (sechub.in)** — https://sechub.in/view/2653727
- **tiktok逆向 四神算法寻找 - 博客园** — https://www.cnblogs.com/aayr/articles/18534131
- **抖音xgorgon、device_id、xlog (易百纳)** — https://www.ebaina.com/articles/140000005158


## Q2: `"x-argus" protobuf douyin tiktok reverse` (Bing, 2026-05)

- **TikTok Reverse Engineering - Mobile and Web API (GitHub armxe/tiktok-api)** — https://github.com/armxe/tiktok-api
- **X-Argus X-Gorgon X-Ladon 抖音 tiktok 头条 ida 反反调试 (知乎)** — https://zhuanlan.zhihu.com/p/625877787
- **TikTok APP加密算法 / TikHub.io docs** — https://docs.tikhub.io/224648349e0
- **tiktok逆向 四神算法寻找 - 博客园** — https://www.cnblogs.com/aayr/articles/18534131
- **tiktok最新版四神算法36.7.4：x-argus、x-gorgon (CSDN)** — https://blog.csdn.net/qq_48840175/article/details/141783427
  - tk 四神 xa 参数数据结构与 dy 六神有所不同，时区/时差/系统语言等需要相应修改
- **[原创] 某音 APP 逆向关键参数 (sechub.in)** — https://sechub.in/view/2653727
- **抖音 TikTok 算法分析 X-Gorgon X-Ladon X-Argus (icode.best)** — https://icode.best/i/07074645385525
- **Need iOS Developer for MSSDK, X-Ladon, X-Argus (BlackHatWorld)** — https://www.blackhatworld.com/seo/need-ios-developer-for-mssdk-x-ladon-x-argus-algorithm-generation-reverse-engineering-tiktok-api.1743565/
- **unidbg 主动调用 tiktok so 生成签名 (逆想技术)** — https://nixiang.tech/forum.php?mod=viewthread&tid=401

## Q3: `美团 mtgsig 算法 还原 native so` (Bing, 2026-05)

- **逆向实战：解开美团外卖 App mtgsig3.0 签名 (CSDN)** — https://blog.csdn.net/weixin_42533120/article/details/160788291
  - 抓包→Frida Hook 动态调试→算法还原→绕过检测
- **【无逆向不爬虫】最新美团外卖逆向实战——MTGSIG (知乎)** — https://zhuanlan.zhihu.com/p/1957878843739178008
- **爬虫js逆向实战美团外卖 MTGSIG 全流程 (B 站视频)** — https://www.bilibili.com/video/BV1n4nMz8Emw/
- **[原创] 某团 App mtgsig2.4 算法分析 (看雪)** — https://bbs.kanxue.com/thread-280779.htm
  - 评论：3.0 关键函数还多了多个 CSEL 混淆，重点是风控
- **某团小程序 _token、Mtgsig 分析流程 (博客园)** — https://www.cnblogs.com/zichliang/p/18868079
- **[原创] Web 美团 mtgsig 算法逆向分析 (教书先生)** — https://blog.oioweb.cn/121.html
- **dogsoft1990/mtgsig: 美团外面算法 mtgsig 3.0 大致算法 (GitHub)** — https://github.com/dogsoft1990/mtgsig
- **美团 mtgsig 4.03 算法分析 (51CTO)** — https://blog.51cto.com/u_15835408/14542925
- **爬虫 某团外卖 mtgsig 逆向分析 (灰信网)** — https://www.freesion.com/article/72012626135/
- **看不懂混 js 代码怎么逆向美团 mtgsig (网易号)** — https://www.163.com/dy/article/HVFRLL3A05561QYO.html

## Q4: `京东 h5st 算法 还原 jsvmp x-api-eid-token` (Bing, 2026-05)

- **某东签名算法 jsvmp 插桩法的纯算还原（舟涯 2025-11）** — https://blog.zhx47.top/archives/1762148186443
  - 老版本 h5st + jsvmp 混淆，时间戳格式化、fp 指纹拆解
- **京东 h5st 5.3.2 生成方式与逆向经验 (CSDN)** — https://blog.csdn.net/kevinsir2003/article/details/131904373
  - h5st 8 段结构拆解，核心加密字符串生成流程
- **爬虫&逆向 京东 h5st 案例解析 (博客园)** — https://www.cnblogs.com/352387312-dada/p/19109300
  - paramsH5sign 体内 SHA256 处理流程
- **某东 4.7 jsvmp 算法还原 (skuukzky 2024-08)** — https://lpy30m.github.io/skuukzky.github.io/2024/08/23/%E9%80%86%E5%90%91/%E6%9F%90%E4%B8%9C4-7jsvmp-%E7%AE%97%E6%B3%95%E8%BF%98%E5%8E%9F/
  - 京东 h5st 4.7.4，AES 加密用 fp 需与第二段保持一致
- **京东 web 端 h5st—4.7 逆向分析 (知乎)** — https://zhuanlan.zhihu.com/p/694854392
- **【JS 逆向-京东】最新 H5ST 算法 (B 站视频)** — https://www.bilibili.com/video/BV1gE4m1d7n6/
- **爬虫&逆向 京东 h5st (技术栈)** — https://jishuzhan.net/article/1974643694654521345
- **京东 h5st 4.7 逆向分析 (腾讯云开发者社区)** — https://cloud.tencent.com/developer/article/2417063
- **京东 h5st 4.7 逆向分析 (idocdown)** — https://idocdown.com/app/articles/blogs/detail/8691
- **京东 h5st 4.7 逆向分析 (FreeBuf)** — https://www.freebuf.com/articles/web/400807.html
  - 含 x-api-eid-token 风控参数，a/d 由浏览器环境+指纹生成

## Q5: `拼多多 anti_content 算法 还原 wasm` (Bing, 2026-05)

- **js 逆向实战之某多多 anti_content 加密 (博客园 sbhglqy)** — https://www.cnblogs.com/sbhglqy/p/18919287
  - CSP-Report-Only 触发问题
- **千千之中-最新拼多多 anti-content (CSDN 2025-07)** — https://blog.csdn.net/qq_48435967/article/details/148953108
  - 动态采集环境指纹+动态行为建模+参数混淆加密
- **拼多多 anti_content 逆向分析 (51CTO huangliang)** — https://blog.51cto.com/u_12929/14223672
- **gitbenxing/anti-content: 拼多多 Anti-Content 加密 (GitHub)** — https://github.com/gitbenxing/anti-content
- **【拼多多爬虫逆向】25 年最新 anti-content 参数分析 (B 站视频)** — https://www.bilibili.com/video/BV1QKbxzLEqG/
- **【JavaScript 逆向】拼多多 anti_content 参数 (知乎)** — https://zhuanlan.zhihu.com/p/654954767
- **某多多 anti_content 逆向（补环境） (技术栈)** — https://jishuzhan.net/article/1853028973185863681
- **拼夕夕小程序 anti_content 算法逆向思路 (看雪)** — https://bbs.kanxue.com/thread-283125.htm
- **拼多多 anti-content 全链路解析与动态对抗 (东大)** — http://www.chinadongda.com/j/?weixin_29323365/article/details/158958178
- **拼多多 anti-content 核心算法完全解密+修复 (术之多)** — https://www.shuzhiduo.com/A/lk5aZjpod1/

## Q6: `淘宝 sign wua 算法 libsgmain mtop 逆向` (Bing, 2026-05)

- **淘宝 app 逆向 x-sgext, x-umt, x-mini-wua, x-sign 实战 (CSDN 2025-05)** — https://blog.csdn.net/2501_92178017/article/details/148240665
- **淘系算法 淘宝 app 协议四神加密 (知乎)** — https://zhuanlan.zhihu.com/p/1910467398500348477
- **[原创] 淘宝长 x-mini-wua 分析与破解 (看雪)** — https://bbs.kanxue.com/thread-274616.htm
  - x-mini-wua 中带硬件参数，新设备可不带账号
- **电视淘宝 x-sign x-umt wua x-mini-wua 签名算法 (灰信网)** — https://www.freesion.com/article/10951592141/
  - 淘宝 h5 与客户端 sign 不同；mtop 随机分配令牌
- **淘宝评论接口 sign 参数逆向 (SegmentFault)** — https://segmentfault.com/a/1190000043885537
- **app 安卓逆向 x-sign/x-sgext/x_mini_wua/x_umt (IoTWord)** — https://www.iotword.com/13150.html
  - 阿里 6.3 版本，frida-rpc 主动调用法
- **淘宝评论抓取 (博客园)** — https://www.cnblogs.com/steed4ever/p/17471118.html
- **app 安卓逆向 x-sign 等阿里系 (ewbang)** — https://www.ewbang.com/community/article/details/961865719.html
  - 阿里系（淘宝/咸鱼）通用一套：x-sign, x-sgext, x_mini_wua, x_umt

## Q7: `bilibili wbi 签名 w_rid 算法 还原` (Bing, 2026-05)

- **【JS 逆向】B 站 WBI 签名鉴权 w_rid+密钥 a (e-com-net)** — https://www.e-com-net.com/article/2037839201197678592.htm
- **WBI 签名 (BAC Document)** — https://sessionhu.github.io/bilibili-API-collect/docs/misc/sign/wbi.html
  - 自 2023.3 起，B 站 Web 端开始 WBI 签名（query 加 w_rid+wts）
- **爬虫与 B 站的"顶级智斗" Wbi 与其破解 (知乎)** — https://zhuanlan.zhihu.com/p/1961014749807513938
- **bilibili-api/docs/misc/sign/wbi.md (GitHub mirror)** — https://github.com/youfengknight/bilibili-api/blob/main/docs/misc/sign/wbi.md
- **B 站 WBI 签名逆向实战 w_rid + Python (CSDN 2026-03)** — https://blog.csdn.net/weixin_29323365/article/details/158674255
  - imgKey + subKey 混合 + mixinKey 计算
- **WBI 签名 mirror (hey99)** — https://www.hey99.cn/shot/CSDN_158674255
- **wbi.md mirror (Gitee 星痕Sky)** — https://gitee.com/Starry-Trace-Sky/bilibili-API-collect/blob/master/docs/misc/sign/wbi.md
- **B 站 Wbi 鉴权方式分析 (掘金)** — https://juejin.cn/post/7278129589518991397
- **WBI 签名算法 (晚风 API doc)** — https://s.apifox.cn/apidoc/docs-site/3455036/api-289557769
- **浅度剖析 B 站新 -352 风控策略 (Salty Fish blog)** — https://im.salty.fish/index.php/archives/revengr-bilibili-352.html

## Q8: `快手 __NS_sig3 算法 还原 native so` (Bing, 2026-05)

- **逆向实战：用 Python 复现快手 sig3 和 tokensig (CSDN 2026)** — https://blog.csdn.net/weixin_26757939/article/details/160879607
  - Java 层 → Native 层逆向，sig / __NS_sig3 / __NStokensig 三件套
- **快手 __NS__sig3 接口动态参数 (掘金)** — https://juejin.cn/post/7490973048242749490
- **快手 __NS__sig3 逆向分析 (技术栈)** — https://jishuzhan.net/article/1909895685819924481
- **快手极速版逆向 sig & NStokensig (YBlog)** — https://blog.2zxz.com/archives/nebula_sig_nstokensig
  - QUIC 降级 HTTP 通用方案 + 请求参数详解
- **ks/sig3 分析 (x14nuy Hexo blog)** — https://x14nuy.github.io/2025/07/01/ks-sig3%E5%88%86%E6%9E%90/
- **gaozhenqiang/kwai-ns_sig3 (GitHub)** — https://github.com/gaozhenqiang/kwai-ns_sig3
  - 快手 ns_sig3 web 签名实现
- **[原创] 某手 910 版本 sig3 48 位算法逆向 (看雪)** — https://bbs.kanxue.com/thread-271489.htm
  - libsgmain.so 0x2d4b6 sha256 魔改特征
- **快手 __NS__sig3 逆向分析 (B 站视频 古月)** — https://www.bilibili.com/video/BV1oG6pYeE5o/
- **快手 __NS_sig3 sig3 算法分析 (CFANZ)** — https://www.cfanz.cn/mobile/resource/detail/DoqWOxGoQzkyp
  - sha256 → sub_3FDA4 → base64 → base64 = sig3
- **某手 app __NS_sig3, sig, __NStokensig (代码先锋网)** — https://www.codeleading.com/article/50226543549/

## Q9: `知乎 x-zse-96 算法 还原 逆向` (Bing, 2026-05)

- **保姆级教程：Node.js+jsdom 复现知乎 x-zse-96 (CSDN 2026)** — https://blog.csdn.net/weixin_42531925/article/details/160814927
- **Ai 还原 x-zse-96 vmp 纯算 (ZONE.CI)** — https://zone.ci/secarticles/wx/522564.html
  - 插桩绕过 JSVMP + SM4 + 自定义编码规则
- **Ai 还原 x-zse-96 vmp 纯算 (CN-SEC)** — https://cn-sec.com/archives/5184884.html
  - SM4-CBC + 位混洗公式 + 常量验证 + ZK 篡改发现
- **知乎 x-zse-96 参数逆向实战 Python (hey99 mirror 2026)** — https://www.hey99.cn/shot/CSDN_158014576
  - 由版本号+路径+cookie_d_c0+x-zst-81 拼接 MD5 后加密
- **知乎 x-zse-96 逆向分析 TNanko (博客园)** — https://www.cnblogs.com/tnanko/p/18164834
- **分析知乎加密算法最新 x-zse-96 (知乎专栏)** — https://zhuanlan.zhihu.com/p/419576219
- **知乎 x-zse-96 参数逆向实战 Python+execjs (e-com-net)** — https://www.e-com-net.com/article/2028874487788789760.htm
- **知乎评论爬取 x-zse-96 (掘金)** — https://juejin.cn/post/7471620402487672871
- **Ai 还原 x-zse-96 vmp 纯算 (gm7 信息安全知识库)** — https://www.gm7.org/archives/90355
- **知乎 x-zse-96 算法 (二进制之旅 2026-03)** — https://blog.xzregister.cn/2026/03/18/zh/
  - okhttp3 Hook + com.zhihu.android.o.a.a 方法定位

## Q10: `网易云音乐 encSecKey params 算法 还原` (Bing, 2026-05)

- **网易云音乐 params 与 encSecKey 参数逆向 (CSDN 2025-08)** — https://blog.csdn.net/chuanl5949/article/details/149885558
  - 评论接口需 csrf_token + params + encSecKey
- **网易云音乐搜索接口 JS 逆向 (阿里云开发者)** — https://developer.aliyun.com/article/1596740
  - AES 加密原理 + Python 完整复现
- **网易云音乐 api params/encSecKey 抓取分析 (冰月)** — https://blog.bingyue.top/2024/06/08/wyy_sign/
- **【JS 逆向】网易云音乐全流程视频 (B 站)** — https://www.bilibili.com/video/BV1NhjGzBEk5/
- **Python 逆向爬虫入门教程：网易云音乐加密 (博客园 hahaa)** — https://www.cnblogs.com/hahaa/p/17962426
- **网易云 JS 解密 (知乎 老网抑云)** — https://zhuanlan.zhihu.com/p/227900268
- **JS 逆向之网易云参数 (掘金)** — https://juejin.cn/post/7023252269952925733
- **网易云音乐 params/encSecKey JS 整合版 (GitHub golangboy/wangyiyuncore)** — https://github.com/golangboy/wangyiyuncore
- **网易云搜索接口 JS 逆向 (技术栈)** — https://jishuzhan.net/article/1824450650881134593
- **JS 逆向网易云音乐 (Cytrogen 个人博客)** — https://blog.cytrogen.icu/posts/f8ce.html
