# 浏览器指纹 / TLS 指纹 - notes

## 一、JavaScript 端浏览器指纹

### 主要熵源（按熵从高到低）

1. **Canvas**：`canvas.toDataURL()` 渲染同一图形，硬件 GPU+驱动差异让结果有微差。`fingerprintjs2` 用一段固定文字+emoji，结果熵 ≈ 8-10 bit。
2. **WebGL**：`getParameter(GL_VENDOR/GL_RENDERER)`、`UNMASKED_VENDOR_WEBGL`、`UNMASKED_RENDERER_WEBGL`、`getSupportedExtensions()`、`getShaderPrecisionFormat`。GPU 名字（`Apple M2`、`NVIDIA GeForce RTX 4090`、`Mali-G78`）。
3. **AudioContext**：`OfflineAudioContext` 跑一段 oscillator → `getChannelData()` → 哈希。差异来自浮点 + DSP 实现。
4. **Font**：`measureText` 量字宽 / `FontFaceSet.check()` 探针。
5. **WebRTC IP leak**：暴露真实 IP（即使开了代理）。
6. **TLS 指纹**：见下文。
7. **navigator.* / screen.***：`userAgent`、`platform`、`languages`、`hardwareConcurrency`、`deviceMemory`、`maxTouchPoints`、`screen.width`/`height`/`colorDepth`/`pixelDepth`。
8. **Permissions**：`Permissions.query({name:'notifications'})` 与 `Notification.permission` 矛盾时暴露 headless。
9. **UA-CH**：`Sec-CH-UA-Full-Version-List`、`Sec-CH-UA-Platform`、`Sec-CH-UA-Mobile` 等。

### Headless / WebDriver 检测点

- `navigator.webdriver` 属性（Chrome 默认 true）。
- `window.chrome.runtime` headless 时缺失。
- `Permissions.query({name:'notifications'})` 返回 `denied` 但 `Notification.permission` 是 `default` → 矛盾。
- `languages` 长度 0 / `plugins` 空数组。
- `outerHeight==0` / `outerWidth==0`。
- UA 含 `HeadlessChrome`。
- CDP `Runtime.evaluate` 留下的痕迹（hard to spoof）。
- `Function.prototype.toString.call(window.x)` 与原生不一致。
- `Object.getOwnPropertyDescriptor(navigator, 'webdriver')` 在 Chrome >=89 有特殊处理。

### 隐藏库

- `puppeteer-extra-plugin-stealth`：18 种规避，但有时被 fingerprint.com 等检测到。
- `playwright-stealth` (`AtuboDad/playwright_stealth`)：playwright 版。
- `undetected-chromedriver`：基于 patchright 的 Chrome driver。
- `stealth.min.js`：把 puppeteer-extra-plugin-stealth 提取成独立 js，可注入任何无头浏览器。
- `kameleo`：商业指纹浏览器。
- `Bright Data Scraping Browser`：基于 puppeteer-real-browser，有真实指纹池。

### 自检站点

- [bot.sannysoft.com](https://bot.sannysoft.com/)
- [creepjs.abrahamjuliot.io](https://abrahamjuliot.github.io/creepjs/)
- [browserleaks.com](https://browserleaks.com/)
- [amiunique.org](https://amiunique.org/)
- [tls.peet.ws](https://tls.peet.ws/)

## 二、网络层 TLS / HTTP/2 指纹

### JA3 / JA3S
- JA3 = MD5(`SSLVersion,Cipher,Extensions,EllipticCurves,EllipticCurvePointFormats`)。
- JA3S = 服务器响应的指纹。
- 缺点：MD5 易碰撞，且简单字段顺序变化会导致 hash 完全变。

### JA4 / JA4+
- 拓展化、模块化、可读化。
- JA4 = `q13d_1717_8daaf6152771_e5627efa2ab1`（协议+ALPN+cipher+extension+SNI）。
- JA4+ 是一系列指纹（JA4S/JA4H/JA4L/JA4X）。
- 服务器端 2024 后大量切到 JA4。

### JARM
- 服务器端 TLS 指纹，反向探测 server。
- 用于识别 CDN 后真实源站、识别已知 C2 服务器。

### HTTP/2 SETTINGS / PRIORITY
- Akamai 用 HTTP/2 帧序列+SETTINGS 值组合作为指纹。
- Chrome 的 `INITIAL_WINDOW_SIZE=6291456`、`HEADER_TABLE_SIZE=65536`、`MAX_HEADER_LIST_SIZE=262144`、PRIORITY 树形结构都有特征。
- `requests`/`httpx` 在 HTTP/2 帧序上与 Chrome 完全不同，绕不过去。

### HTTP/3 QUIC
- TLS 1.3 帧顺序、`quic-transport-parameters`。
- 越来越多站点（Google/Cloudflare）默认走 HTTP/3。

### 绕过工具

| 工具 | 语言 | 优点 | 缺点 |
|---|---|---|---|
| `curl-impersonate` | C | 模拟 Chrome/FF/Safari/Edge 完整 TLS+HTTP/2 | 编译复杂 |
| `curl_cffi` | Python | curl-impersonate 的 Py 封装，最常用 | 跟 curl-impersonate 同步更新 |
| `tls-client` (bogdanfinn) | Go | 高性能 + 多浏览器 profile | Go 调用 |
| `utls` (refraction-networking) | Go | 底层 TLS 库，可深度定制 | 较复杂 |
| `impersonator` (zhkl0228) | Java | Java 生态用 | Java 限定 |
| `cycletls` | Node.js | JS 生态 | 性能一般 |

### TLS 自检

- [tls.peet.ws](https://tls.peet.ws/) — 看你 client 的 JA3/JA4/HTTP2 指纹。
- [tls.browserleaks.com](https://tls.browserleaks.com/) — 测 SSL/TLS 配置。
- [scrapfly.io/web-scraping-tools](https://scrapfly.io/web-scraping-tools) — Scrapfly 提供的指纹检测工具集。

## 三、移动 App 端设备指纹

### Android 关键采集点（200+ 字段）
- **Build.\***：MODEL、SERIAL、FINGERPRINT、PRODUCT、BRAND、HARDWARE、IS_EMULATOR。
- **Settings.Secure.ANDROID_ID**。
- **GSF ID**：Google 服务框架。
- **IMEI**：API 29+ 受限，需要 READ_PHONE_STATE。
- **MEID/MAC**：API 23+ 也受限。
- **Widevine `getPropertyByteArray("deviceUniqueId")`** + L 级别（L1/L2/L3）。
- **MediaDrm**：DRM session UUID。
- **GPU 字符串**：真机 `Mali-G78`、`Adreno 750`、`Apple A17`；模拟器 `Swiftshader`、`ANGLE`、`VirGL`、`llvmpipe`。
- **传感器字段**：accelerometer/gyro/magnetometer 厂商。
- **网络字段**：MAC（API 23+ 受限）、SSID、cellular network type。
- **运行环境**：cgroup `/proc/self/cgroup`、selinux 状态、Verified Boot、Build.IS_EMULATOR、`getprop ro.kernel.qemu`、`/dev/qemu_pipe`、`/dev/socket/qemud`。

### iOS 关键采集点
- IDFA / IDFV / `UIDevice.identifierForVendor`。
- `sysctl(KERN_OSVERSION)`、`Mach exception ports`。
- AppAttest assertion / DeviceCheck 2-bit。
- SEP key 派生指纹。

### 典型 SDK
- 阿里 wua/x5sec
- 字节 x-helios
- 美团 mtguard
- 京东 eid
- 快手 sigsdk
- 网易盾 yidun
- 数美 ishumei smid
- 顶象 constid
- 同盾 blackbox
- 瑞数 RASP
- 蚂蚁 mPaaS APDID

## 四、防御侧产品

- [fingerprint.com](https://fingerprint.com/) — 商业指纹识别，识别率 ~99%。
- [Castle.io](https://castle.io/) — 账号风控+指纹综合。
- [HUMAN](https://www.humansecurity.com/) — 反 bot 巨头，原 PerimeterX。
- [Spur.us](https://spur.us/) — 住宅代理识别。
- [IPQualityScore](https://www.ipqualityscore.com/) — IP+设备综合分。
- [MaxMind GeoIP2 Anonymous IP](https://www.maxmind.com/en/geoip-anonymous-ip) — VPN/代理 DB。

## raw-hits 来源

- TLS：[fingerprint-batch1.md Q1](../raw-hits/fingerprint-batch1.md)
- Stealth：[fingerprint-batch1.md Q2](../raw-hits/fingerprint-batch1.md)
- Canvas/WebGL/Audio：[fingerprint-batch1.md Q3](../raw-hits/fingerprint-batch1.md)

## 工作流建议

1. 拿到目标 → 用 `tls.peet.ws` 看你 client 的指纹是什么。
2. 比对 Chrome 真实指纹（chrome 直连 tls.peet.ws）。
3. 用 `curl_cffi`+`impersonate="chrome120"` 或类似选项把 client 指纹对齐。
4. JS 层：先看 `bot.sannysoft.com` 是否标红→开 stealth → 测 `creepjs.abrahamjuliot.io`。
5. App 端：先把 200 字段的设备指纹完整采集（必须真机 dump）→ 再考虑伪造。
6. 注意：单独欺骗 JS 不够，要 JS+TLS+HTTP2+IP 多层一致。
