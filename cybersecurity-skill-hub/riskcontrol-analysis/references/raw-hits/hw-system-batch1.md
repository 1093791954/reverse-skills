# HW-System - 摸底 raw-hits 批次 1（TEE/Play Integrity/Verified Boot/PAC/MTE）

## Q1: `play integrity api bypass strong integrity kernelsu` (Bing, 2026-05)

- **tryigit/PlayIntegrityFix (GitHub)** — https://github.com/tryigit/PlayIntegrityFix
  - 模块内 fingerprints 被 ban 因测试过多
- **Fixing Play Integrity with KernelSU (XDA Forums)** — https://xdaforums.com/t/a-guide-to-fixing-play-integrity-with-kernelsu.4759925/
- **Play Integrity Fork (KernelSU Modules)** — https://modules.kernelsu.org/module/playintegrityfix/
  - <A13 PI STRONG，A13+ DEVICE/STRONG integrity 推荐
- **KernelSU+PlayIntegrityFix 解决 ChatGPT 报错 (CSDN 2025-06)** — https://blog.csdn.net/qq_45797625/article/details/148975330
- **Play Integrity PASS on KernelSU 2026-02 (gizdev)** — https://www.gizdev.com/pass-play-integrity-on-kernelsu/
  - Susfs + ZygiskNext + Play Integrity Fork
- **修复 Play Integrity / SafetyNet Attestation (dkrain 2023)** — https://dkrain.com/posts/在已root设备上修复play-integrity-safetynet-attestation验证/
- **Magisk 防 Root 偵測 + 通過 Play Integrity (ivonblog)** — https://ivonblog.com/posts/magisk-hide-root/
- **Android 进阶：Play Integrity 与 Strong Integrity 之殇 (cloudflush 2025-11)** — https://blog.cloudflush.win/article/000019/.html
- **ROOT & Play Integrity 解決方案 (PTT Android 2024)** — https://www.ptt.cc/bbs/Android/M.1725672033.A.187.html
  - APatch + KernelSU GKI mode

## Q2: `tee key attestation android keystore 5级证书链 strongbox` (Bing, 2026-05)

- **数字凭据硬件证明 (Android 官方 dev doc)** — https://developer.android.google.cn/identity/digital-credentials/credential-issuer/keystore-attestation?hl=zh-CN
- **使用密钥认证验证硬件支持的密钥对 (Android 官方)** — https://developer.android.com/privacy-and-security/security-key-attestation?hl=zh-cn
- **[原创] Key Attestation 原理理解 (看雪 2024-08)** — https://bbs.kanxue.com/thread-283191.htm
- **第 14 章 密钥管理与硬件安全 (zsc android_os)** — https://zsc.github.io/android_os/chapter14.html
- **密钥证明验证硬件支持的密钥对 (android-docs.cn)** — https://android-docs.cn/privacy-and-security/security-key-attestation
- **Strongbox 和 Weaver keymint (CSDN 2023-06)** — https://blog.csdn.net/baidu_25966105/article/details/130775176
- **密钥和 ID 认证 (AOSP 中文)** — https://aosp.org.cn/docs/security/features/keystore/attestation
- **vvb2060/KeyAttestation (GitHub)** — https://github.com/vvb2060/KeyAttestation
- **Key Attestation 密钥认证流程和绕过思路 (知乎 2024-01)** — https://zhuanlan.zhihu.com/p/675905006
- **Android Keystore 技术演进与 Key Attestation (阿里云开发者 2024-01)** — https://developer.aliyun.com/article/1411710

## Q3: `verified boot avb vbmeta 风控 检测 ramdisk` (Bing, 2026-05)

- **AVB vbmeta 结构浅析 (CSDN 2025-08)** — https://blog.csdn.net/anjiyufei/article/details/150499666
- **Magisk 刷入 vbmeta.img 关闭 avb2.0 (知乎)** — https://zhuanlan.zhihu.com/p/500410873
- **AVB 2.0 工作原理 vbmeta chain (阿里云 2024)** — https://developer.aliyun.com/article/1411150
- **救砖 boot/vbmeta/fastboot 工具箱 (星苒鸭 2026-02)** — https://xingranya.cn/android-backup-unbrick-fastboot-partitions/
- **AVB 2.0 (魅族内核团队 2023)** — https://kernel.meizu.com/2023/07/04/Android-R-AVB2-0/
- **AVB 2.0 详解 Android P (博客园 schips)** — https://www.cnblogs.com/schips/p/what_is_android_verified_boot.html
- **Magisk 刷入 vbmeta + 关闭 avb2.0 (看雪)** — https://bbs.kanxue.com/thread-265792.htm
- **secureboot 入门 6 安卓 AVB (掘金 2024-08)** — https://juejin.cn/post/7407256931394289675
- **Magisk vbmeta.img + AVB 2.0 (百度文库)** — https://wenku.baidu.com/view/92fd4bb361ce0508763231126edb6f1aff0071d9.html
- **Android AVB 与启动校验 (初然の博客 2026-04)** — https://blog.crneko.top/posts/android-avb/
