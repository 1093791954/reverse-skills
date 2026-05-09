# References Index — riskcontrol-analysis

本目录是 `riskcontrol-analysis` Skill 的"知识炼化"主索引：每个主题/平台/厂商一份 `*-notes.md`，`SKILL.md` 提供通用工作流，本目录提供细节。

## 目录结构

```
references/
├── README.md                       # 本文件（索引）
├── android/                        # Android 大站参数 + 加固壳
├── ios/                            # iOS 越狱 / AppAttest / 反 hook
├── web/                            # Web 反爬厂商 + 国内大站参数
├── captcha/                        # 人机验证 / 滑块 / 点选
├── fingerprint/                    # 浏览器指纹 / TLS 指纹
├── toolchain/                      # Frida / Magisk / unidbg / OLLVM / SSL Pinning
├── hw-system/                      # Play Integrity / TEE Attestation / AVB
├── crypto/                         # （预留）魔改 AES/MD5/HMAC 抽象总结
├── schema/                         # （预留）通用上传 schema 模板
└── raw-hits/                       # 摸底搜索原始命中（500+ writeup URL，按 batch 分文件）
```

## 案例索引（按主题）

### Android Native 风控

| App / 厂商 | 关键参数 | 主 SO / 入口 | 笔记 |
|---|---|---|---|
| 小红书（深度逐字笔记，932 行） | x-mini-mua/s1/sig, shield | libtiny.so | [android/xhs-libtiny-notes.md](android/xhs-libtiny-notes.md) |
| 字节系 抖音/TikTok | X-Gorgon/X-Khronos/X-Argus/X-Ladon/X-Helios | libmsaoidsec.so / libsscronet.so | [android/bytedance-x-gorgon-x-argus-notes.md](android/bytedance-x-gorgon-x-argus-notes.md) |
| 美团 / 大众点评 | mtgsig (1→2.4→3.0→4.0+) | libmtguard.so / rohr.js | [android/meituan-mtgsig-notes.md](android/meituan-mtgsig-notes.md) |
| 京东 | h5st (3→5.x), x-api-eid-token | jsvmp + AES + fp | [android/jd-h5st-notes.md](android/jd-h5st-notes.md) |
| 拼多多 | anti_content (base64+zlib+WASM) | jsvmp + WASM | [android/pdd-anti-content-notes.md](android/pdd-anti-content-notes.md) |
| 淘宝 / 阿里系 | x-sign, x-sgext, x-mini-wua, x-umt | libsgmain.so | [android/taobao-libsgmain-notes.md](android/taobao-libsgmain-notes.md) |
| 快手 | __NS_sig3, __NStokensig | libsgmain.so（同名不同实现） | [android/kuaishou-ns-sig3-notes.md](android/kuaishou-ns-sig3-notes.md) |
| QQ / 微信 / 支付宝 | wtlogin sign / mmtls / APDID | 各自 SO | [android/tencent-alipay-protocols-notes.md](android/tencent-alipay-protocols-notes.md) |
| **加固壳 + wxapkg** | 360/爱加密/梆梆/乐固/聚安全/几维/娜迦 + 微信小程序 wxapkg | libjiagu/libsecexe/libshellx 等 | [android/packers-and-wxapkg-notes.md](android/packers-and-wxapkg-notes.md) |

### Web / H5 风控

| 厂商 / 站 | 关键参数 | 笔记 |
|---|---|---|
| Akamai Bot Manager | sensor_data, _abck, bm_sz | [web/akamai-sensor-data-notes.md](web/akamai-sensor-data-notes.md) |
| Cloudflare Turnstile | cf_clearance, __cf_bm | [web/cloudflare-turnstile-notes.md](web/cloudflare-turnstile-notes.md) |
| **DataDome / PerimeterX (HUMAN) / Kasada / Imperva** | 4 家国际反爬合并 | [web/datadome-px-kasada-imperva-notes.md](web/datadome-px-kasada-imperva-notes.md) |
| 抖音 Web | X-Bogus, _signature, msToken, X-Argus | [web/douyin-x-bogus-notes.md](web/douyin-x-bogus-notes.md) |
| 小红书 Web | x-s, x-t, x-s-common, x-mns | [web/xhs-x-s-common-notes.md](web/xhs-x-s-common-notes.md) |
| 知乎 Web | x-zse-96, x-zst-81, d_c0 | [web/zhihu-x-zse-96-notes.md](web/zhihu-x-zse-96-notes.md) |
| 网易云音乐 | params, encSecKey | [web/netease-music-encseckey-notes.md](web/netease-music-encseckey-notes.md) |
| bilibili Web | w_rid, wts, mixin_key | [web/bilibili-wbi-notes.md](web/bilibili-wbi-notes.md) |
| Boss 直聘 | __zp_stoken__, zp_token | [web/boss-zhipin-zp-stoken-notes.md](web/boss-zhipin-zp-stoken-notes.md) |
| 百度 / 12306 / 微博 | Acs-Token / RAIL_DEVICEID / sina_visitor | [web/baidu-12306-weibo-notes.md](web/baidu-12306-weibo-notes.md) |

### Captcha / 人机验证

| 笔记 | 覆盖 |
|---|---|
| [captcha/cn-vendors-summary-notes.md](captcha/cn-vendors-summary-notes.md) | 瑞数 5/6/7、极验 v3/v4、网易盾 NECaptcha、数美、顶象、同盾、阿里 x5sec |
| [captcha/intl-recaptcha-hcaptcha-arkose-notes.md](captcha/intl-recaptcha-hcaptcha-arkose-notes.md) | reCAPTCHA v2/v3/Enterprise、hCaptcha、Arkose Labs FunCAPTCHA |

### Fingerprint（浏览器/TLS/硬件指纹）

- [fingerprint/browser-tls-fingerprint-notes.md](fingerprint/browser-tls-fingerprint-notes.md) — Canvas/WebGL/Audio + JA3/JA4/JARM + UA-CH + Stealth 库 + 自检站点

### iOS 风控

- [ios/ios-jailbreak-attestation-notes.md](ios/ios-jailbreak-attestation-notes.md) — 越狱生态 + Hook 框架 + 反越狱探针 + Mach-O + 砸壳 + AppAttest/SEP + 加密参数 + 网络指纹

### 工具链 / Hook / 模拟 / 反混淆

| 笔记 | 覆盖 |
|---|---|
| [toolchain/frida-anti-detect-notes.md](toolchain/frida-anti-detect-notes.md) | Frida 6 大检测面 + strongR-frida 魔改 + Magisk/Zygisk/Shamiko + KernelSU/APatch |
| [toolchain/unidbg-recipes-notes.md](toolchain/unidbg-recipes-notes.md) | unidbg 黑盒模拟 + qiling + AndroidNativeEmu + unidbg-boot-server 工业化 |
| [toolchain/ollvm-deobfuscation-notes.md](toolchain/ollvm-deobfuscation-notes.md) | OLLVM 三大 Pass (BCF/FLA/SUB) + D-810/Triton/Miasm/angr 工具链 |
| [toolchain/ssl-pinning-bypass-notes.md](toolchain/ssl-pinning-bypass-notes.md) | Android (TrustManager/OkHttp/Conscrypt) + iOS (Security/BoringSSL/Network.framework) |

### 硬件 / 系统层

- [hw-system/play-integrity-tee-attestation-notes.md](hw-system/play-integrity-tee-attestation-notes.md) — Play Integrity 当前 + TEE Key Attestation 5 级证书链 + Verified Boot/AVB + ARM PAC/BTI/MTE

### 摸底原始命中（raw-hits/）

50+ Bing query × 10 真实 URL = ~500 个 writeup 链接，按平台分批：

- `raw-hits/android-batch1.md`：抖音/美团/京东/拼多多/淘宝/B 站/快手/知乎/网易云（10 query）
- `raw-hits/android-batch2.md`：小红书/X-Bogus/boss/12306/微博/百度（6 query）
- `raw-hits/android-batch3.md`：360 加固/爱加密/数美/顶象/同盾/微信 mmtls/支付宝/QQ（8 query）
- `raw-hits/web-batch1.md`：Akamai/CF/DataDome/PerimeterX/瑞数/wxapkg/jsvmp/Kasada/Imperva（9 query）
- `raw-hits/captcha-batch1.md`：网易盾/极验/recaptcha/hcaptcha/arkose/ddddocr/阿里 x5sec（7 query）
- `raw-hits/fingerprint-batch1.md`：JA3/JA4 + stealth + Canvas/WebGL/Audio（3 query）
- `raw-hits/toolchain-batch1.md`：Frida 反检测/Magisk DenyList/unidbg/OLLVM/SSL Pinning/LSPosed/IL2CPP（7 query）
- `raw-hits/hw-system-batch1.md`：Play Integrity/TEE Key Attestation/AVB Verified Boot（3 query）
- `raw-hits/ios-batch1.md`：iOS Frida/AppAttest/SEP/砸壳/Mach-O/SSL Pinning（5 query）

加载策略：raw-hits 仅当需要"该话题更多 writeup 链接"时再 Read；常规对话只 Read 对应的 `<topic>-notes.md`。

## 如何新增条目

1. 选一个 `references/<dir>/` 子目录（android/ios/web/captcha/fingerprint/toolchain/hw-system/crypto/schema 之一）。
2. 新建 `<topic>-notes.md`，文件首部放：
   - 摘要（参数对照表+识别签名）
   - 算法/工作流/坑点
   - raw-hits 来源指向（注明对应 batch+Q 编号）
   - 关键 URL（按入门→进阶分类）
   - 关键术语
3. 在本 README 索引里追加一行。
4. 若该话题引入"全新工作流环节"，在 `../SKILL.md` 里**只补一节** Path，不重写已有路径。
5. 通用规律写进 `SKILL.md`，样本细节写进 `references/<dir>/<topic>-notes.md`——这是 Skill 持续扩张不臃肿的关键。

## 文件命名约定

- `bytedance-`、`xhs-`、`douyin-`、`meituan-`、`jd-`、`pdd-`、`taobao-`、`bilibili-`、`kuaishou-`、`zhihu-`、`netease-` 等平台前缀。
- 后接关键参数或 SO 名或 SDK 名，例：
  - `xhs-libtiny-notes.md`（小红书 + libtiny.so + notes）
  - `meituan-mtgsig-notes.md`（美团 + mtgsig + notes）
  - `bytedance-x-gorgon-x-argus-notes.md`（字节 + x-gorgon + x-argus + notes）
- 主题文件用 `<theme>-notes.md`，例 `cn-vendors-summary-notes.md`、`browser-tls-fingerprint-notes.md`、`play-integrity-tee-attestation-notes.md`。
