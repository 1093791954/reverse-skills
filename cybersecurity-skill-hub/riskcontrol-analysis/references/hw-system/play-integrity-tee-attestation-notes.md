# Hardware/System：Play Integrity / TEE Key Attestation / Verified Boot - notes

## 一、Play Integrity API（取代 SafetyNet）

### 判定矩阵

| Verdict | 条件 |
|---|---|
| `MEETS_DEVICE_INTEGRITY` | 标准 Android 设备（CTS 通过） |
| `MEETS_BASIC_INTEGRITY` | 较宽松（允许部分定制 ROM） |
| `MEETS_STRONG_INTEGRITY` | 硬件 backed Key Attestation（A13+） |
| `MEETS_VIRTUAL_INTEGRITY` | 云手机（Android 13 引入） |

### 请求模式
- **Standard request**：在线、最严格、需要 Google Cloud 项目+nonce。
- **Classic request**：离线签名 token，已不推荐。

### 当前绕过现状（2026）
- **MEETS_BASIC/DEVICE**：用 `tryigit/PlayIntegrityFix` + `Susfs` + `ZygiskNext` 模块组合，A11+ Magisk 可过。
- **MEETS_STRONG**：需要 spoof locked bootloader+合法证书链；难度极高，几乎只能在自有真机上做"记录-验证"研究。
- **MEETS_VIRTUAL**：云手机环境本身就有此 verdict，无需绕过。

### 关键模块
- [tryigit/PlayIntegrityFix](https://github.com/tryigit/PlayIntegrityFix) — 主流修复模块。
- `Susfs` (su filesystem)：mount-point 隐藏，让 root 痕迹彻底消失。
- `ZygiskNext`：Magisk 已不维护 Zygisk 自身后的替代。
- `Play Integrity Fork`：另一支 fork。

### 集成 SDK 真实回应（典型）
```json
{
  "deviceIntegrity": {
    "deviceRecognitionVerdict": ["MEETS_DEVICE_INTEGRITY"]
  },
  "appIntegrity": {
    "appRecognitionVerdict": "PLAY_RECOGNIZED",
    "packageName": "com.example.app",
    "certificateSha256Digest": ["..."]
  },
  "accountDetails": {
    "appLicensingVerdict": "LICENSED"
  }
}
```

## 二、TEE Key Attestation（5 级证书链）

```
Google Hardware Attestation Root CA
    └── Google Hardware Attestation Intermediate CA
            └── Device-specific CA (manufacturer 注入)
                    └── TEE App CA (Trusty 内部签发)
                            └── Attestation Key (用户应用持有)
```

### 关键扩展字段

证书 X.509 扩展 `1.3.6.1.4.1.11129.2.1.17` 包含：
- `attestationVersion`
- `attestationSecurityLevel`：SOFTWARE / TRUSTED_ENVIRONMENT / STRONG_BOX
- `keymasterVersion`
- `attestationChallenge`：服务器给的 nonce
- `uniqueId`
- `softwareEnforced` / `teeEnforced` 各种 KeyDescription：
  - `purpose`、`algorithm`、`keySize`、`digest`、`padding`
  - `creationDateTime`、`origin`、`rollbackResistant`
  - `applicationId`：包名 + 签名 SHA256
- `attestationApplicationId`：含包名+签名 SHA256（防 hijack）
- `RootOfTrust`：
  - `verifiedBootKey`（公钥 hash）
  - `deviceLocked` (bool)
  - `verifiedBootState`：GREEN / YELLOW / ORANGE / RED
  - `verifiedBootHash`

### 绕过现状

| 安全级别 | 绕过难度 | 说明 |
|---|---|---|
| SOFTWARE | 容易 | 改 ROT 字段 + 伪造签名 |
| TRUSTED_ENVIRONMENT | 极难 | 根证书私钥在芯片 TEE，无法 sign 新证书 → 实际只能"复用真机 attest 数据" |
| STRONG_BOX | 几乎不可能 | StrongBox Keymaster 是独立硬件 |

### 工具
- [`vvb2060/KeyAttestation`](https://github.com/vvb2060/KeyAttestation) — 自检测 attestation 工具，能 dump+verify+parse。

## 三、Verified Boot / AVB 2.0

### vbmeta 结构
```
vbmeta_header
+ partition descriptors (boot/system/vendor/...)
+ chain partition descriptors  (链式委托)
+ certificate (公钥)
+ signature (RSA/ECDSA on header+descriptors)
```

### 启动颜色
| 颜色 | 含义 |
|---|---|
| GREEN | OEM 锁定+原厂 key+验签通过 |
| YELLOW | 用户 key+验签通过（解锁但用自己 key 重签） |
| ORANGE | 解锁 bootloader |
| RED | 验签失败（拒绝启动） |

### 风控读取 ROT
- `getprop ro.boot.flash.locked`：1=锁定。
- `getprop ro.boot.veritymode`：enforcing/logging/disabled。
- Key Attestation 内的 `RootOfTrust.deviceLocked` 字段。

### 绕过 vbmeta 验证
```
fastboot --disable-verity --disable-verification flash vbmeta vbmeta_a.img
fastboot --disable-verity --disable-verification flash vbmeta_a vbmeta_a.img
fastboot --disable-verity --disable-verification flash vbmeta_b vbmeta_b.img
```
但会触发 ORANGE 状态，被风控读出。

### Magisk patch boot.img
- Magisk 24+ 处理 vbmeta 时不可避免触发解锁状态。
- 想通过 STRONG_INTEGRITY 必须保留 lock + 用合法证书链。

## 四、ARM PAC / BTI / MTE

### PAC (Pointer Authentication, ARMv8.3+)
- 函数指针上半段是 PAC tag（HMAC of pointer + context + key）。
- 检测点：iPhone XS+ (A12+) 全面启用，Pixel 8+/Snapdragon 8 Gen 3+ 部分启用。
- 对 inline hook 影响：改了指针就要重签 PAC，否则 `autia`/`autda` 等 auth 指令会触发异常。
- 工具：Frida ARM64e 上 `Stalker` 比 inline `Interceptor` 更安全。
- 公开论文：[Project Zero: Examining Pointer Authentication on iPhone XS](https://googleprojectzero.blogspot.com/2019/02/examining-pointer-authentication-on.html)

### BTI (Branch Target Identification, ARMv8.5+)
- 防止任意跳转：跳转目标必须有 `BTI c/j/jc` 指令。
- 类比 x86 的 IBT。

### MTE (Memory Tagging Extension, ARMv9)
- 内存分配带 4-bit tag。
- 主要对抗 use-after-free 和 buffer overflow。
- 风控用得不多（除非检测内存破坏漏洞）。

## 五、iOS 对应（见 [ios/ios-jailbreak-attestation-notes.md](../ios/ios-jailbreak-attestation-notes.md)）

- DeviceCheck / App Attest 是 iOS 等价物。
- 都基于 SEP（Secure Enclave Processor）。
- Hardware Attestation / WebAuthn on iOS。

## raw-hits 来源

- Play Integrity：[hw-system-batch1.md Q1](../raw-hits/hw-system-batch1.md)
- TEE Key Attestation：[hw-system-batch1.md Q2](../raw-hits/hw-system-batch1.md)
- Verified Boot/AVB：[hw-system-batch1.md Q3](../raw-hits/hw-system-batch1.md)

## 关键 URL

Play Integrity：
- [Play Integrity 官方文档](https://developer.android.com/google/play/integrity)
- [tryigit/PlayIntegrityFix (GitHub)](https://github.com/tryigit/PlayIntegrityFix)
- [Play Integrity Fork (KernelSU Modules)](https://modules.kernelsu.org/module/playintegrityfix/)
- [Pass Play Integrity on KernelSU 2026 (gizdev)](https://www.gizdev.com/pass-play-integrity-on-kernelsu/)
- [Android Play Integrity 之殇 (cloudflush 2025-11)](https://blog.cloudflush.win/article/000019/.html)
- [ROOT & Play Integrity 解決方案 (PTT 2024)](https://www.ptt.cc/bbs/Android/M.1725672033.A.187.html)

TEE Key Attestation：
- [Android 官方 Key Attestation](https://source.android.com/docs/security/features/keystore/attestation)
- [[原创] Key Attestation 原理理解 (看雪 2024)](https://bbs.kanxue.com/thread-283191.htm)
- [vvb2060/KeyAttestation (GitHub)](https://github.com/vvb2060/KeyAttestation)
- [Key Attestation 流程和绕过 (知乎 2024-01)](https://zhuanlan.zhihu.com/p/675905006)
- [Strongbox 和 Weaver keymint (CSDN 2023)](https://blog.csdn.net/baidu_25966105/article/details/130775176)

Verified Boot / AVB：
- [AVB vbmeta 结构 (CSDN 2025-08)](https://blog.csdn.net/anjiyufei/article/details/150499666)
- [AVB 2.0 (魅族内核团队 2023)](https://kernel.meizu.com/2023/07/04/Android-R-AVB2-0/)
- [AVB 2.0 详解 (博客园)](https://www.cnblogs.com/schips/p/what_is_android_verified_boot.html)
- [Magisk 关闭 avb2.0 校验 (看雪)](https://bbs.kanxue.com/thread-265792.htm)
- [Android AVB 与启动校验 (初然 2026-04)](https://blog.crneko.top/posts/android-avb/)

## 工作流建议

1. **App 闪退**：优先看是 Play Integrity 还是 SafetyNet（旧）还是 Key Attestation 失败。
2. **Logcat 抓 Verdict**：grep `MEETS_DEVICE_INTEGRITY` / `playintegrity`。
3. **当前组合**：KernelSU + Susfs + ZygiskNext + PlayIntegrityFix → 可过 DEVICE/BASIC INTEGRITY。
4. **STRONG INTEGRITY**：建议放弃软件绕过，转向"自有真机+合法启动+研究签名结构"路线。
5. **TEE Attest**：自有设备做合法采样，研究字段含义和后端校验逻辑（防御研究）。
