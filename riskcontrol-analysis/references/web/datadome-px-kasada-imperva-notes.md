# DataDome / PerimeterX (HUMAN) / Kasada / Imperva - notes

> 把四家国际反爬合并成一份是因为它们的还原思路非常相似（jsvmp+设备指纹+滑块+IP 信誉），实战时按签名快速判断厂商→选对应工具/付费 API 即可。

## 一、DataDome

### 签名
- Cookie `datadome=...` 长串。
- 滑块/拼图域 `captcha-delivery.com`。
- POST `/js/...` 提交 `payload`、`tagsId`。
- 拦截页含 `tags.js`。

### 还原
- 真浏览器+stealth：80% 网站可过。
- `pynocaptcha` / `chrisyp/nocaptcha` / `kameleo` / `Bright Data`：付费方案。
- 纯算少见，重在**指纹真实性 + 真人轨迹**。

### URL
- [Datadome 2026 最新逆向 (CSDN)](https://blog.csdn.net/m0_66839504/article/details/129361471)
- [datadome 3.40 分钟解混淆 (B 站墨竹_zs)](https://www.bilibili.com/video/BV1Jj3Hz3E96/)
- [How to Bypass DataDome 2026 (ZenRows)](https://www.zenrows.com/blog/datadome-bypass)
- [chrisyp/nocaptcha datadome zh-CN](https://chrisyp.github.io/zh-CN/datadome.html)
- [ellisfan/bypass-datadome (GitHub)](https://github.com/ellisfan/bypass-datadome)

## 二、PerimeterX (HUMAN)

### 签名
- Cookie `_px2`/`_px3`/`_pxhd`/`_pxvid`。
- challenge 域 `captcha.px-cdn.net`。
- 主 JS：`PXxxxx.js`+`init.js`+`main.min.js`。
- 4 次请求模型：3 次 bundle + 1 次 g。

### 还原
- 主流：`Pr0t0ns/PerimeterX-Reverse` 是公开实现框架。
- **AI 解混淆 + 一段段抠**：main.min.js 混淆力度大，2026 年常见用 AI 辅助还原。
- **PX3 vs PX2**：PX3 现在是主流，每天换 main.min.js 内容。

### URL
- [PerimeterX 逆向分析 (二进制之旅 2026-04)](https://blog.xzregister.cn/2026/04/18/px/)
- [Reversing PerimeterX Web Sensor (autodev 2026-02)](https://autodev.blog/posts/px-web-sensor-article/)
- [PX3 按压反混淆+逆向 (yazong 2024-03)](https://www.1997.pro/archives/1711604818499)
- [chrisyp/nocaptcha perimeterx zh-CN](https://chrisyp.github.io/zh-CN/perimeterx.html)
- [Pr0t0ns/PerimeterX-Reverse (GitHub)](https://github.com/Pr0t0ns/PerimeterX-Reverse)

## 三、Kasada

### 签名
- Header `x-kpsdk-ct` / `x-kpsdk-cd` / `x-kpsdk-im` / `x-kpsdk-v`。
- POST `/tl` 接口。
- 主 JS：`/ips.js`，是一个迷你 vmp，专门做 PoW。
- 客户端跑 `/ips.js` → 算出 payload + ct + cd → POST `/tl` → 服务器赋 cookie。

### 还原
- `lktop/kpsdk` 是 2021 年的公开实现，参考思路。
- 现在主流：`pynocaptcha` 付费 / 自己解 ips.js（vmp 较小，可纯算）。
- ips.js 内部走类寄存器的程序行为，断点定位即可分析。

### URL
- [新一代 vmp 混淆保护 Kasada (知乎 2025-07)](https://zhuanlan.zhihu.com/p/1923793309379309941)
- [kasada 代码分析+插桩 (yazong 2024-02)](https://1997.pro/archives/1708325827794)
- [Kasada 任务 (EzCaptcha 2025-11)](https://ezcaptcha.atlassian.net/wiki/spaces/IS/pages/38338692/Kasada)
- [chrisyp/nocaptcha kasada](https://chrisyp.github.io/zh-CN/kasada.html)
- [lktop/kpsdk (GitHub)](https://github.com/lktop/kpsdk)
- [zhzhsgg/kasada-kpsdk (Gitee)](https://gitee.com/zhzhsgg/kasada-kpsdk)

## 四、Imperva (Incapsula)

### 签名
- Cookie `incap_ses_*` / `visid_incap_*` / `reese84`。
- 路径 `/_Incapsula_Resource?...`。
- 双层 challenge：utmvc（前置）+ reese84（高级风控）。

### 还原
- `___utmvc` 是 ob 混淆，用蔡老板/webcrack 工具能解。
- `reese84` 是新一代 JSVMP，2024 后越来越多航空/酒店站启用。
- `BottingRocks/Incapsula` 是公开 payload 实现起点。
- `TakionAPI` / `Scrapfly` / `ZenRows` 都提供 reese84 求解 API。

### URL
- [reese84 及 _utmvc 逆向 (吾爱破解 2024-04)](https://www.52pojie.cn/thread-1912763-1-1.html)
- [Deobfuscating utmvc (yoghurtbot 2023-03)](https://yoghurtbot.github.io/2023/03/04/Deobfuscating-Incapsula-s-UTMVC-Anti-Bot/)
- [Incapsula Reese84 JSVMP (rhkb 2026-04)](http://www.rhkb.cn/news/198799)
- [BottingRocks/Incapsula (GitHub)](https://github.com/BottingRocks/Incapsula)
- [Bypass Incapsula 96% (Scrapfly)](https://scrapfly.io/bypass/incapsula)
- [reese84 Bypass Solution (TakionAPI)](https://docs.takionapi.tech/incapsula/reese84)

## raw-hits 来源

- 见 [raw-hits/web-batch1.md Q3-Q4, Q8-Q9](../raw-hits/web-batch1.md)。

## 通用建议

1. **先识别厂商**：看 cookie 名 → 决定攻击面。
2. **真浏览器优先**：除非要批量，不要一上来就纯算。
3. **付费 API 是兜底**：CapSolver/2captcha/yescaptcha/anti-captcha/CapMonster 价格 1-3 美元/1000 次。
4. **指纹真实性**：所有四家都重度依赖浏览器指纹真实性（Canvas/WebGL/AudioContext + 鼠标事件 timing）。
5. **TLS 与 IP**：四家都校验 JA3/JA4 + IP 信誉（Spur.us 数据源）。机房 IP 必拒，住宅代理才行。
