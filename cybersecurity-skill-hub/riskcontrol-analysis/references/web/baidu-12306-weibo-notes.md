# 国内 Web 中等案例：百度 / 12306 / 微博 - notes

## 一、百度 Acs-Token / ab_sr / Cipher-Text

### 签名
- 百度翻译：Header `Acs-Token`+POST `ab_sr`。
- 百度指数：`Cipher-Text` 加密 query。
- `BAIDUID`/`BAIDUID_BFESS` cookie 是设备/会话指纹。

### 算法
- AES + 环境检测。
- 22 年 Acs-Token 加密 js 自注释为"玉门关"（K 哥爬虫考古发现）。
- AST 解混淆后是相对清晰的逻辑。

### URL
- [深入解析 Cipher-Text 与 Acs-Token (百度云开发者 2025-10)](https://cloud.baidu.com/article/3866832)
- [某度 Acs-Token、ab_sr 逆向 (腾讯云 2025-12)](https://cloud.tencent.com/developer/article/2606384)
- [某度 Acs-Token 玉门关 (K 哥爬虫 博客园)](https://www.cnblogs.com/ikdl/p/19386049)
- [百度指数 + 百度翻译 Acs-Token (掘金 K 哥)](https://juejin.cn/post/7133151365806686245)
- [百度翻译逆向 Acs-Token 调试 (CSDN)](https://blog.csdn.net/Not__Cry/article/details/139726675)
- [逆向某平台 Acs-Token (知乎)](https://zhuanlan.zhihu.com/p/1953560209537611152)

### 工作流
1. 抓包 → 看 Header 是否有 `Acs-Token`。
2. 搜 `acs_token` → 找加密函数（多走 AES）。
3. AST 解混淆（webcrack 等）。
4. Python 复现，注意 `ab_sr` 是会话级 cookie，需要刷新。

## 二、12306 RAIL_DEVICEID / RAIL_EXPIRATION

### 签名
- Cookie `RAIL_DEVICEID`（设备指纹）+`RAIL_EXPIRATION`（过期时间）。
- 必带 cookie 才能登录/查票/预订。
- 接口 `/otn/HttpZF/logdevice`（生成 RAIL_DEVICEID）。

### 算法
- JS 收集浏览器指纹（UA/语言/screen/canvas）→ hashAlg dict → 拼接 → 上送。
- 服务器返回包含 `dfp`（设备指纹码）+ exp。
- `RAIL_DEVICEID = dfp` 拷贝到 cookie。

### URL
- [获取 RAIL_EXPIRATION 和 RAIL_DEVICEID (geekdaxue)](https://geekdaxue.co/read/12306-api-doc/2.logdevice.md)
- [12306 抢票 RAIL_DEVICEID 来源 (博客园 snowdreams1006)](https://www.cnblogs.com/snowdreams1006/p/12316951.html)
- [JS 逆向 12306 设备码 (CSDN)](https://blog.csdn.net/weixin_31211821/article/details/117686084)
- [12306 RAIL_DEVICEID 来源 (腾讯云)](https://cloud.tencent.com/developer/article/1588600)
- [J12306 issue: RAIL_EXPIRATION 失效](https://github.com/kalvinGit/J12306/issues/10)
- [12306 RAIL_DEVICEID (bytezonex 2024-01)](https://www.bytezonex.com/archives/sJgQ1gvP.html)

### 工作流
1. 入门级，公开方案多。
2. 用 Python+execjs 跑 hashAlg.js 即可得 RAIL_DEVICEID。
3. RAIL_EXPIRATION 是 base64 timestamp，可解码后调整。
4. 跨 IP 复用要谨慎，12306 反爬比较严。

## 三、微博 aid / sina_visitor / sig

### 签名
- 访客系统：`tid` + 访客 cookie（先访问 `https://passport.weibo.com/visitor/visitor` 得到 sub/subp）。
- 主签名：`sig`/`from`/`gsid`+设备 ID。
- 登录：9 步流程含预登陆 → 取 token → 验证码 → RSA 加密密码 → 提交。
- App 端：`com.sina.weibo`，DeviceId.getDeviceIdNative JNI 调用。

### URL
- [[原创] 微博 12.5.1 算法研究 (看雪)](https://bbs.kanxue.com/thread-272984.htm)
- [微博完整逆向分析 (CSDN 专栏)](https://download.csdn.net/blog/column/12440659/138464798)
- [从零开始逆向 APP 微博协议 (吾爱破解)](https://www.52pojie.cn/thread-1370540-1-1.html)
- [Android 新浪微博逆向 (51CTO 2025-04)](https://blog.51cto.com/u_16175451/13765283)
- [微博登录流程逆向+加密参数 (极客日志 2025-01)](https://zeeklog.com/-js-ni-xiang-bai-li-fu-za-de-deng-lu-guo-cheng-zui-xin-wei-bo-ni-xiang)
- [pokerfaceSad/SinaNetSpider (GitHub)](https://github.com/pokerfaceSad/SinaNetSpider)
- [新浪微博逆向总结 (GitCode)](https://gitcode.com/Open-source-documentation-tutorial/1b891/tree/main)

### 工作流
1. Web 访客系统先走通：访问 visitor.do 取 sub/subp cookie。
2. 登录用 RSA pub key（接口返回）+RSA 加密密码。
3. App 端用 jadx 跟 DeviceId.getDeviceIdNative。
4. 微博风控对账号+IP 联合判断比较敏感，建议小流量 + 真号。

## raw-hits 来源

- 百度：[android-batch2.md Q16](../raw-hits/android-batch2.md)
- 12306：[android-batch2.md Q14](../raw-hits/android-batch2.md)
- 微博：[android-batch2.md Q15](../raw-hits/android-batch2.md)
