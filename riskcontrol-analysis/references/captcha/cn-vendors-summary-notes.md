# 国产 Web 三巨头：瑞数 / 极验 / 网易盾 / 数美 / 顶象 / 同盾 / 阿里盾 - notes

> 国产风控/验证码生态的"七剑客"。识别签名 → 选 SDK → 走对应工具流即可。

## 一、瑞数 RASP（5/6/7 代）

### 签名
- Cookie 含 `FSSBBIl1UgzbN7N80T` 类别（每个站名字不一样）+`MmEwMD`。
- HTML 内嵌 `<meta name="@@HuYan">` 或 `<script>$_ts={...}; eval(...)</script>`。
- 错误码 `412` 是瑞数典型拦截。
- 页面初次访问会被 202 拦截（瑞数）。

### 演进
- 4 代：明文 + 简单混淆。
- 5 代：jsvmp 字节码 + 动态值匹配（正则可解）。
- 6 代：字节码升级 + 更严格匹配。
- VMP 代：完全 vmp 化，每隔几天换一次。

### 还原
- 思路：抓静态 JS → AST 解混淆 → 找 dispatcher → 还原 cookie 生成。
- 公开实现：`pysunday/rs-reverse`（瑞数 vmp 纯算）+ `pysunday/sdenv`（补环境）。
- AI 辅助：CN-SEC 等 2026 年开始用 AI 辅助原型链检测+补环境。

### URL
- [瑞数 6 代 JS 逆向 (K 哥爬虫 博客园)](https://www.cnblogs.com/ikdl/p/17778885.html)
- [pysunday/rs-reverse (GitHub)](https://github.com/pysunday/rs-reverse)
- [某期刊瑞数 6 代 JSVMP 原型链检测+补环境 (B 站)](https://www.bilibili.com/video/BV1QEwReKEWB/)
- [js 逆向思路-区分瑞数 vmp/6/5/4/3 (CN-SEC)](https://cn-sec.com/archives/1882149.html)
- [海关征信瑞数 6 vmp (百度开发者 2025-10)](https://developer.baidu.com/article/detail.html?id=4107009)

## 二、极验 GeeTest v3 / v4

### 签名
- v3：`gt`/`challenge`/`w`，POST `/api.geetest.com/...`。
- v4：`lot_number`/`payload`/`process_token`/`pow_msg`/`pow_sign`，POST `/load`+`/verify`。
- 三种类型：滑块、图标点选、九宫格、空间推理（无感）。

### 还原
- v3 已被破解多年，公开实现充足。
- v4 关键是 `w` 参数：`w = encrypt(轨迹+滑动距离+timing+device_id+pow_msg)`。
- pow_msg 需要 CPU 暴力搜索（PoW），写个简单循环即可。

### URL
- [极验 4 滑块逆向与纯算实现 (CSDN 2025-12)](https://blog.csdn.net/weixin_35906794/article/details/156308786)
- [Geetest 极验 4 代滑块逆向 (B 站)](https://www.bilibili.com/video/BV1USScBrEtH/)
- [极验四代滑块验证码逆向学习 (SegmentFault 2024-05)](https://segmentfault.com/a/1190000044880224)
- [parasyte-x/GeetestReverseEngineering (GitHub)](https://github.com/parasyte-x/GeetestReverseEngineering)
- [极验 4.0 滑动验证码逆向 (博客园)](https://www.cnblogs.com/FlowerNotGiveYou/p/18872578)
- [【Web 逆向】极验 4 代九宫格协议 (CN-SEC 2025-09)](https://cn-sec.com/archives/4449663.html)
- [验证码逆向专栏 某验四代 (掘金 2025-02)](https://juejin.cn/post/7469666524258500660)

## 三、网易易盾 NECaptcha

### 签名
- POST `/api/v2/{init,get,check}`。
- 参数：`id`/`token`/`fp`/`actoken`/`data`/`validate`/`NECaptchaValidate`。
- 滑块取轨迹前 50 位加密。
- 类型：滑块、文字点选、九宫格、空间推理、无感。

### URL
- [逆向网易易盾滑块+JS 轨迹 (CSDN 2026)](https://blog.csdn.net/weixin_42524276/article/details/160848618)
- [网易易盾验证码核心参数全攻略 (ttocr 2026-03)](https://www.ttocr.com/word/article.php?slug=article-20260319082005)
- [Python 爬虫逆向：网易易盾 (zeeklog 2024-02)](https://zeeklog.com/python-pa-chong-ni-xiang-an-li-wang-yi-yi-dun-hua-kuai-qing-qiu-can-shu-fen-xi-hua-kuai-yan-zheng-ma)
- [网易易盾滑块逆向 (易微帮)](https://www.ewbang.com/community/article/details/961865456.html)
- [网易滑块 data 与 cb (知乎)](https://zhuanlan.zhihu.com/p/624860656)
- [0xAllenChen/spider_reverse (GitHub 综合)](https://github.com/0xAllenChen/spider_reverse)

## 四、数美 ishumei

### 签名
- POST `/v3/profile.json`。
- 参数：`smid`/`organization`/`tokenId`+设备指纹+RC4+3DES+RSA。
- BlackBox 是数美主签名，跨 web/Android/iOS/小程序。

### URL
- [数美 SDK 设备指纹 ID 生成规则（上）(CSDN 2025-12)](https://blog.csdn.net/luomao2012/article/details/155806403)
- [东某航空数美指纹 v4 设备 ID (K 哥爬虫 博客园 2024-12)](https://www.cnblogs.com/ikdl/p/18596626)
- [新版同盾 BlackBox 环境补全 (CSDN 2026-03)](https://blog.csdn.net/weixin_29322553/article/details/159074707)
- [某盾 blackbox 指纹分析 (博客园 郭楷丰 2025-04)](https://www.cnblogs.com/guokaifeng/p/18829332)
- [数美官方 fp-android (GitHub)](https://github.com/ishumei/fp-android)

## 五、顶象 Dingxiang

### 签名
- 参数：`constId`/`bx-pp`/`bx-et`/`slidedata`。
- 滑块用 canvas 切割 + 动态混淆 + 图像识别。
- 接入面：web/Android/iOS/微信小程序/支付宝小程序。

### URL
- [顶象官方 const-id 文档](https://www.dingxiang-inc.com/docs/detail/const-id)
- [设备指纹系列前端篇 (看雪 2023)](https://bbs.kanxue.com/article-23478.htm)
- [顶象设备指纹 PDF](https://netmarket.oss-cn-hangzhou.aliyuncs.com/3b5818e35b0f490282633248cf748f1d.pdf)
- [decodecaptcha/DingxiangCaptchaBreak (GitHub)](https://github.com/decodecaptcha/DingxiangCaptchaBreak)
- [顶象滑块 js 逆向 (imSpm)](https://www.imspm.com/dev/686063.html)

## 六、同盾 Tongdun

### 签名
- BlackBox 算法（v2 2025+ 版本走 WASM）。
- 接入：web/小程序/App，跨平台。

### URL
- [某盾 Blackbox 算法逆向 (腾讯云 2025-01)](https://cloud.tencent.com/developer/article/2486648)
- [同盾 v2 2025 blackbox WASM (技术栈 2025-03)](https://jishuzhan.net/article/1900133381028040706)
- [山姆会员商店 T 盾风控 (看雪 2025-03)](https://bbs.kanxue.com/thread-286243.htm)
- [某盾 blackbox 二次分析 (hzhcontrols 2025-05)](https://www.hzhcontrols.cn/new-7196806.html)

## 七、阿里盾 NoCaptcha / x5sec

### 签名
- Cookie `x5secdata`。
- POST `/_____tmd_____/punish`。
- 参数：`bx-pp`/`bx-et`/`slidedata` + sg.js（设备指纹）。
- v2 滑块从 1.1.0 → 1.1.10 一直在演进。
- F001/F017 错误码标志参数错误。

### URL
- [某里 v2 滑动验证码 (K 哥爬虫 博客园 2024-11)](https://www.cnblogs.com/ikdl/p/18576586)
- [阿里系 x5sec 逆向分析 (icode.best 2025-06)](https://icode.best/i/659939405503278)
- [阿里 v2 滑块 sg.js 设备指纹 (掘金 2025-04)](https://juejin.cn/post/7489362433359036443)
- [淘宝 x5sec 普通滑块 (51CTO 2026-04)](https://blog.51cto.com/u_15835408/14542925)
- [阿里 1688 阿里滑块 231 x5sec (技术栈 2024-11)](https://jishuzhan.net/article/1856050465993658369)
- [daxiongaijingxiang/x82y (GitHub)](https://github.com/daxiongaijingxiang/x82y)

## raw-hits 来源

- 瑞数：[web-batch1.md Q5](../raw-hits/web-batch1.md)
- 极验：[captcha-batch1.md Q2](../raw-hits/captcha-batch1.md)
- 网易盾：[captcha-batch1.md Q1](../raw-hits/captcha-batch1.md)
- 数美/同盾：[android-batch3.md Q3, Q5](../raw-hits/android-batch3.md)
- 顶象：[android-batch3.md Q4](../raw-hits/android-batch3.md)
- 阿里 x5sec：[captcha-batch1.md Q7](../raw-hits/captcha-batch1.md)

## 通用建议

1. **先识别厂商**：看 cookie/参数前缀 + 接口路径。
2. **滑块类**走 OCR + 真人轨迹拟合（ddddocr 是必备）。
3. **PoW 类**直接暴力搜索。
4. **WASM 类**先 wabt 反编译看小模块是否纯计算（90% 是）。
5. **指纹类**（数美/顶象/同盾/blackbox）依赖端到端真实采集，纯算往往要"指纹快照+回放"。
