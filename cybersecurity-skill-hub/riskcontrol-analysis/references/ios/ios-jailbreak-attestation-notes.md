# iOS 风控通用 - notes

## 一、iOS 越狱生态（2026 视角）

| 工具 | 适用 | 状态 |
|---|---|---|
| `palera1n` | A11- (iPhone X 以下) iOS 15-17 | 当前主流（基于 checkm8+KPF） |
| `Dopamine` | A12+ (iPhone XS+) iOS 15-16 rootless | 当前 A12+ 主流 |
| `roothide/Bootstrap` | A12+ iOS 15+ rootless 兼容 Substrate | rootless 折中方案 |
| `checkra1n` | A11- iOS 12-14 | legacy（不再维护） |
| `unc0ver` | iOS 11-14 | legacy |
| `Taurine` | iOS 14 | legacy |
| `TrollStore` | iOS 14-16.x，免越狱永久签名 | CoreTrust bug 链未修复期间最神奇 |

### Hook 框架
- **ElleKit** (`evelyneee/ellekit` / `tealbathingsuit/ellekit`)：palera1n+Dopamine 默认；Substrate 已不维护；用异常处理改线程状态实现 hook。
- **Substitute** (`coolstar/Substitute`)：rootless 之前的过渡。
- **Theos+Logos**：`%hook` `%orig` 工具链入门必备。
- **Orion** (`theos/orion`)：Swift-friendly hook DSL。
- **fishhook** (`facebook/fishhook`)：C 函数级 hook（rebind dyld lazy/non-lazy symbols）。

## 二、反越狱探针（典型 5 件套）

### 1. ptrace
```c
ptrace(PT_DENY_ATTACH, 0, 0, 0);
// 或 svc 0x80 #26 直接调内核
```

### 2. sysctl
```c
struct kinfo_proc info;
size_t size = sizeof(info);
int mib[] = {CTL_KERN, KERN_PROC, KERN_PROC_PID, getpid()};
sysctl(mib, 4, &info, &size, NULL, 0);
return (info.kp_proc.p_flag & P_TRACED) != 0;
```

### 3. 文件路径黑名单
- `/Applications/Cydia.app`
- `/var/lib/apt`
- `/usr/bin/ssh`
- `/private/var/lib/cydia`
- `/usr/sbin/sshd`
- `/usr/libexec/cydia/firmware.sh`
- `/Library/MobileSubstrate/MobileSubstrate.dylib`

### 4. URL scheme
- `cydia://`、`sileo://`、`zbra://`、`undecimus://`、`xina://`、`installer5://`

### 5. dyld_image_count + 黑名单
- 遍历 `_dyld_get_image_name(i)` 找：
  - `libsubstrate.dylib`
  - `libsubstitute.dylib`
  - `TweakInject`、`SBInject`
  - `MobileSubstrate.dylib`、`SubstrateLoader.dylib`

### 6. Frida 检测
- 端口 27042（默认）。
- 线程名 `gum-js-loop`/`gmain`/`gdbus`。
- 进程名 `frida-server`。

### 绕过方案
- `A-Bypass`、`Liberty Lite`、`Shadow`、`HookKiller`、`KernBypass`、`Choicy`。
- 自写 Frida 脚本：hook `getenv`/`stat`/`fopen`/`access`/`strstr`/`_dyld_get_image_name`/`canOpenURL:`/`sysctl`/`ptrace`。

## 三、Mach-O & 砸壳

### Mach-O 结构
```
[Header]
[Load Commands]
  - LC_SEGMENT_64 __TEXT (cryptid=1 表示 FairPlay 加密)
  - LC_SEGMENT_64 __DATA
  - LC_ENCRYPTION_INFO_64 (FairPlay)
  - LC_DYLD_INFO_ONLY (旧) / LC_DYLD_CHAINED_FIXUPS (新, iOS15+)
  - LC_CODE_SIGNATURE
  - LC_MAIN / LC_THREAD
[Data]
```

### 砸壳工具
- **frida-ios-dump** (`AloneMonkey/frida-ios-dump`)：rootless 兼容；通过 Frida 把内存里已解密的 __TEXT 段 dump 回磁盘。
- **bagbak** (`ChiChou/bagbak`)：rootless 友好（ElleKit）。
- **CrackerXI+**：图形化越狱设备本地砸壳。
- **Iridium**：现代砸壳工具。
- **Clutch**：legacy（已停更，不支持现代设备）。

### TrollStore 时代
- 装现成解密版 ipa（基于 CoreTrust bug，免越狱永久签名）。
- iOS 14-16.x 黄金期；iOS 16.x+ Apple 修复后无效。

## 四、苹果原生反作弊

### DeviceCheck (iOS 11+)
- 服务器端给设备打 2-bit 标记，重置需要重置整机。
- 限制：每个 App 一个 device_token，且只能本 App 服务器查询。
- 现状：被国内 App 大量用作"封号位"。

### App Attest (iOS 14+)
- 基于 SEP key 的硬件 attestation。
- attest API → SEP 生成 keypair → 服务器验 X.509 链 → assertion API 后续签名。
- 验证流程：
```
1. attestKey = generateKey()  // SEP 内部
2. attestation = attest(attestKey, challenge)
3. server: validate cert chain root = Apple App Attestation Root CA
4. server: verify nonce + clientDataHash
5. assertion = generateAssertion(attestKey, message)
6. server: validate assertion with attestation
```
- 绕过现状：除非提取 SEP key（接近不可破），只能在多设备间复制 attestation 数据时被 nonce 反制。

### Private Access Tokens (iOS 16+)
- 基于 IETF Privacy Pass 标准。
- iOS 16+/Safari 17+ 设备访问支持 PAT 的网站时，无需出现 captcha。
- Cloudflare/Fastly 已支持。

### iCloud Private Relay
- 让 IP 检测失效（双 hop）。
- iCloud+ 订阅用户开启后，IP 会被屏蔽。

### SEP / Secure Enclave
- 协处理器，独立 RAM+存储。
- Touch/Face ID 数据、AppAttest key、Apple Pay 都在里面。
- 不可读出（除非 OS 命令明确允许）。

## 五、加密参数（与 Android 对应）

| 参数 | App | 说明 |
|---|---|---|
| `X-Argus`/`X-Gorgon`/`X-Ladon` | 抖音/TikTok iOS | 与 Android 共用 ttencrypt，但壳和探针不同 |
| `mmtls` | 微信 | TLS 1.3 草案变体，封装在 Mars 网络库 |
| `x-sign`/`x-mini-wua` | 淘宝 iOS | mtop 协议，securitysdk + ub_aes |
| `h5st`/`x-api-eid-token` | 京东 iOS | 5.0+ iOS/web 共 jsvmp |
| `APDID`/`umid`/`rds` | 支付宝 iOS | mPaaS 体系 |
| `params`/`encSecKey` | 网易云 iOS | 与 web 同源 |
| `w_rid`/`wts` | bilibili iOS | wbi，iOS/web 同算法 |
| `x-mini-mua/s1/sig`/`shield` | 小红书 iOS | 与 libtiny.so 关联 |

## 六、网络 / TLS 指纹

- NSURLSession vs CFNetwork vs WKWebView 的 ClientHello 顺序不同。
- iOS 15+ 走 NWConnection（基于 Network.framework）。
- ATS（App Transport Security）强制 TLS 1.2+；要抓包必须先 disable ATS。
- WKWebView 内部 JSContext 反 hook：检测 method swizzling。

## 七、运行时反 Method Swizzling 检测

App 启动时可遍历类的 method list 算 hash → 后续比对。Frida hook 会改 method IMP → hash 变 → 检测命中。

工具：[`securing/IOSSecuritySuite`](https://github.com/securing/IOSSecuritySuite) 是工业级开源探针清单（含越狱+swizzle+jb 检测）。

## raw-hits 来源

- 越狱+Frida 检测：[ios-batch1.md Q1](../raw-hits/ios-batch1.md)。
- AppAttest+SEP：[ios-batch1.md Q2](../raw-hits/ios-batch1.md)。
- 砸壳：[ios-batch1.md Q3](../raw-hits/ios-batch1.md)。
- Mach-O：[ios-batch1.md Q4](../raw-hits/ios-batch1.md)。
- SSL Pinning：[ios-batch1.md Q5](../raw-hits/ios-batch1.md)，并见 [toolchain/ssl-pinning-bypass-notes.md](../toolchain/ssl-pinning-bypass-notes.md)。

## 关键工具 URL

- [palera1n/palera1n](https://github.com/palera1n/palera1n)
- [opa334/Dopamine](https://github.com/opa334/Dopamine)
- [opa334/TrollStore](https://github.com/opa334/TrollStore)
- [roothide/Bootstrap](https://github.com/roothide/Bootstrap)
- [evelyneee/ellekit](https://github.com/evelyneee/ellekit)
- [theos/theos](https://github.com/theos/theos)
- [AloneMonkey/frida-ios-dump](https://github.com/AloneMonkey/frida-ios-dump)
- [ChiChou/bagbak](https://github.com/ChiChou/bagbak)
- [securing/IOSSecuritySuite](https://github.com/securing/IOSSecuritySuite)
- [Lessica/KernBypass-Public](https://github.com/Lessica/KernBypass-Public)

## 工作流建议

1. **越狱选型**：先看设备 SoC（A11- vs A12+）+iOS 版本 → 选对应越狱。
2. **砸壳**：rootless 用 bagbak，传统用 frida-ios-dump。
3. **绕反越狱**：A-Bypass + 自写 Frida hook（`stat`/`access`/`canOpenURL:`/`_dyld_get_image_name`）。
4. **抓包**：SSL Kill Switch 2（越狱）+ mitmproxy + 安装根证书。
5. **AppAttest 类**：放弃伪造，改"记录-验证"研究。
