# 浏览器指纹对抗（Canvas / WebGL / Audio / Font / UA-CH / Permissions）

## 1. 维度清单（合规授权研究）
| 维度 | 关键 API | 检测点 |
|------|---------|--------|
| Canvas 2D | `toDataURL`, `getImageData` | 渲染 hash 一致性 |
| WebGL | `getParameter(UNMASKED_VENDOR/RENDERER)`, `readPixels` | GPU vendor/renderer 字符串、shader 渲染特征 |
| AudioContext | `OfflineAudioContext` 输出累加 | 浮点求和 hash |
| Font | `measureText('')`, 字体可用性 | 系统字体列表 hash |
| UA-CH | `navigator.userAgentData.getHighEntropyValues()` | brands/mobile/platform/full-version-list |
| Permissions | `navigator.permissions.query({name:'X'})` | notifications / midi / geolocation 等返回值组合 |
| Battery | `navigator.getBattery()` | 已废弃但仍读 |
| HW | `navigator.hardwareConcurrency`, `deviceMemory` | 与 UA 匹配（手机端 UA 下却返回 16 → 异常） |
| Screen | `screen.{width,height,availWidth,availHeight,colorDepth,pixelDepth}` | 比例 + dpr 一致性 |
| Intl | `Intl.DateTimeFormat().resolvedOptions().timeZone` | 与 IP 地区匹配 |
| Media | `navigator.mediaDevices.enumerateDevices()` | mic/cam 列表 |

## 2. 检测策略
- **一致性交叉**：UA、UA-CH、TLS、Permissions、HW 多个维度交叉，单点伪装会被任意 mismatch 抓住。
- **真值校验**：服务端有真实硬件分布数据，对每条 (UA, GPU, fontList) 做联合概率打分。
- **熵值**：Canvas hash 太常见（千万人共享）反而可疑；要分布在常见区间。
- **toString 检测**：被改写的 native 函数 `getParameter.toString()` 不再返回 `[native code]`。
- **Proxy 痕迹**：`Object.getOwnPropertyDescriptor` 检测到 proxy。

## 3. 工具与方法
- **Stealth 浏览器**（推荐）：`patchright` (Python) > `nodriver` > `camoufox` (Firefox) > `botright` > `undetected-chromedriver`；2024-2026 多次迭代，需关注是否在维护。
- **playwright-stealth / puppeteer-extra-stealth**：早期方案，对新版 detector 已力不从心，但作为基线可用。
- **指纹浏览器**（商业）：Multilogin、AdsPower、Nstbrowser、Hidemyacc、BitBrowser、Gologin。
- **Node 补环境**：在 Node 模拟 Canvas/WebGL/Audio，配合 jsdom；常用 `canvas`、`gl`、`web-audio-api` 包。
- **CDP 检测对抗**：`Runtime.evaluate` 触发某些 console 异常；用真浏览器+native event 投递更稳。

## 4. 已公开研究
- CSDN「JS 逆向补环境 ===＞＞＞ Canvas」(157131057)：模拟 Canvas 指纹原理。
- CSDN「JS 逆向新手也能搞定：手把手教你用 Node.js 补全 ali140 滑块 canvas」(159607511)。
- CSDN「JS 逆向实战：补环境框架对抗浏览器指纹与反混淆」(154904175)：Proxy 兜底原理。
- CSDN「JS 逆向进阶：ali140 滑块验证码的 Canvas 环境精准模拟」(158903755)：WebGL UNMASKED_VENDOR/RENDERER + 2D toDataURL。
- CSDN「逆向实战：新版同盾 BlackBox 环境补全与指纹对抗解析」(159074707)：Canvas/WebGL/Audio + WASM Token 全流程。
- CSDN「浏览器指纹解读」：Header / Canvas / Audio 综述。
- CSDN「006.指纹浏览器编译-随机 audio 指纹」：随机化思路。
- CSDN「天外客翻译机 AudioContext 指纹采集」(AudioContext)：硬件级指纹。
- CSDN「前端指纹技术是如何实现的？」：Canvas/Audio + 硬件 API + Battery + concurrency。
- CSDN「你的爬虫被识别了？...用 Playwright 伪装 Canvas/WebGL 指纹」。
- CSDN「CreepJS 浏览器指纹技术深度解析」系列四篇 (149826297/156743339/159642016/155302069)：检测能力 + Blink 引擎特性清单 + 局限性 + 替代方案。
- CSDN「CreepJS 快速上手：10 分钟」(156743339)：WebRTC/WebGL/Canvas 2D/字体/时区/屏幕/无头检测。
- CSDN「别再只改版本号了！深入 CreepJS 源码，看它如何识破伪造的 Chromium 106」(159642016)：Blink 引擎 API 一致性校验。

## 5. 防御性分析步骤
1. 用 CreepJS / FpJS 测试当前环境，列「trust 0」字段。
2. 针对每个 0 字段补环境（一致化）。
3. 用同一组 UA + UA-CH + TLS + 字体打到目标厂商 baseline，观察评分。
4. 长期：把指纹与代理/账号绑定，避免跨 session 漂移。

## 6. 缓解 / 趋势
- UA-CH（Sec-CH-UA-Full-Version-List）成为标配。
- Permissions 五项交叉是新热点（notifications + midi + geolocation + camera + microphone）。
- Privacy Sandbox 后 Canvas hash 熵下降，但新引入 Topics API 与 PAT 替代。

## 7. 待研究
- Chromium 110+ Canvas 噪声化特性对 hash 稳定性的影响。
- UA-CH `Sec-CH-UA-Full-Version-List` 各厂商解析差异。
- 移动浏览器（Safari iOS）指纹熵更低导致的「群体匿名」效应。

## 8. Chromium Canvas 噪声化 / 指纹随机化（R4 补充）

R4 通过 `q='Chromium Canvas 噪声'` / `q='Chromium Canvas randomization'` 命中 ~50 篇文章，集中在"Chromium 源码定制 + Canvas/Audio/WebGL 随机化"主题，是当前防爬反向工程领域热点：

新增 articleid（已 API 验证）：
- (159489997) 别再只盯着 Canvas 了！聊聊 Audio 指纹的"可塑性"与 Chromium 定制浏览器的隐私增强思路
- (159787987) 从源码到实战：编译 Chromium 实现 Canvas 指纹随机化防御
- (97490940) Chromium 指纹浏览器开发实战：对抗 canvas 指纹追踪的深度定制方案
- (147342815) 13. Chromium 指纹浏览器开发教程之 canvas 指纹定制
- (160168545) 003. 深入 Chromium 源码：编译时注入 Canvas 指纹随机化策略
- (157352566) 从零构建：如何为 Chromium 注入动态音频指纹的魔法
- (158992383) Canvas 指纹检测避坑指南：为什么你的 Chromium 随机画布总被 browserleaks 识破？
- (159075481) 手把手教你绕过网站追踪：Chromium 浏览器 canvas 指纹伪装技巧
- (160079938) 保姆级教程：修改 Chromium 源码，让 Canvas 指纹随机化以应对 creepjs 和 browserscan 检测
- (159230090) 013. 指纹浏览器进阶 - 对抗 creepjs 与 browserscan 的 canvas 色彩指纹检测
- (159848369) 逆向思维：如何像 creepjs 一样检测浏览器指纹？从检测原理看指纹浏览器的伪装策略

**关键技术点（汇总自上述文献）**：
1. 直接改 `Source/platform/graphics/skia/SkiaCanvas.cpp`、`Source/modules/canvas/canvas2d/CanvasRenderingContext2D.cpp`，在 `toDataURL`/`getImageData` 之前插入像素级 ±1 噪声。
2. 噪声必须 session-stable（同 session 输出一致），否则 CreepJS 会用 "trust" 试两次发现差异。
3. 仅做颜色噪声不够，CreepJS / browserleaks 还检 `measureText` / `BlobCreator` / Canvas 整体一致性，需要全链路统一打过。
4. WebGL 需同时改 `getParameter` 字符串（vendor/renderer）+ shader 渲染输出 + GPU vendor 派生噪声。
5. Audio 指纹：直接改 `OfflineAudioContext` 累加节点，否则与 Canvas 一改 Audio 露馅。

## 9. Permissions.query 五项交叉（R4 补充）

CreepJS / FpJS Pro 的核心交叉校验：依次 query `notifications` / `midi` / `geolocation` / `camera` / `microphone`，五个返回值组合成"权限指纹"。常见反模式：
- `notifications: granted` + `geolocation: prompt` 同时出现 → 真人或正常浏览器
- 全部 `denied` → headless / 自动化 / Tor
- `notifications: prompt` + `geolocation: granted` 但无地理位置请求历史 → 异常
- 五个 API 在同一栈帧内被依次调用且 0ms 内全部返回 → 自动化扫描

R4 检索（`q='Permissions.query 验证码'` / `q='navigator.permissions 检测'`）显示中文圈对此点专题文章较少（多与短信/SMS 验证码关键字撞车），主要在 CreepJS 系列里讨论。

## 10. CreepJS Blink API 真实性校验（R4 补充）

R4 命中 26 篇 `q='CreepJS Blink API'` 强相关：
- (149958105) CreepJS 浏览器指纹技术深度解析——自动化工具集成实践（三）
- (150000567) CreepJS 浏览器指纹技术深度解析——高级反检测技术与替代方案（四）
- (159642016) 别再只改版本号了！深入 CreepJS 源码，看它如何识破伪造的 Chromium 106
- (159848369) 逆向思维：如何像 creepjs 一样检测浏览器指纹？
- (95675152) 指纹浏览器避坑指南：为什么只改 UserAgent 伪装 macOS 会失败？
- (98015611) 别再让网站追踪你的显卡了！手把手教你用 Chromium 源码修改 WebGPU 指纹

**Blink 真实性校验的核心套路**：
1. 在不同 Chromium 版本里，某些 API 是阶段性添加的（如 `OffscreenCanvas` 在 89 引入、`Sec-CH-UA-Full-Version-List` 在 100 引入）。如果 UA 声称 Chrome 106 但缺该 API → 露馅。
2. 反向：声称 Chrome 89 但出现 117 才有的 API → 同样露馅。
3. CreepJS 维护一份"版本 → 必有 API 表"（在源码 `getEngine`/`getJSEngine` 内）；伪装时必须按 UA 版本号同步移除/添加。
4. 二次校验：`Function.prototype.toString` 链路（被 Proxy 劫持后会变 native code 字符串异常）。

## 11. 待研究（追加）
- WebGPU API（`navigator.gpu`）作为"下一个 Canvas"的指纹熵评估。
- Chromium 噪声化是否能稳定打过 browserleaks Canvas Trust = 100%（社区结论：能但需 session 持久 + 全链路）。
