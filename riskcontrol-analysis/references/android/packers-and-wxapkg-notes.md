# Android 加固壳 + 小程序 wxapkg - notes

## 一、主流加固壳速查

| 加固厂 | 主 SO | 特征 | 脱壳工具 |
|---|---|---|---|
| **360 加固** | `libjiagu*.so`, `libjgdtc*.so` | classes.dex 为壳 dex；运行时解 + 加载真实 dex | `frida-dexdump`, `BlackDex` |
| **爱加密** | `libsecexe.so`, `libsecmain.so`, `libsecshell.so` | 反调试强 + 多 dex | `frida-dexdump` + 反调试 hook |
| **梆梆安全 (Bangcle)** | `libsecexe.so`（同名但不同实现）+ 多 dex 链 | 多重 dex 嵌套 + native 校验 | `BlackDex` + IDA 手脱 |
| **腾讯乐固** | `libshellx*.so`, `libtencentloc*.so` | DEX 直接内存解密 + AOT 化 | `frida-dexdump` |
| **阿里聚安全** | `libmobisec*.so`, `libsgmain*.so` | 与阿里 mtop 共生；deep VMP | unidbg+frida hook |
| **几维安全** | KiwiVM | VMP 字节码解释器 | 难，几乎只能动态分析 |
| **娜迦** | NagaPT VMP | 同 KiwiVM | 难 |
| **百度** | `libbaiduprotect*.so` | 中等强度 | `frida-dexdump` |

## 二、通用脱壳原理

不论加固方式：**ART 虚拟机执行时，真实 DEX 一定会在内存中完整存在**——脱壳就是在那一刻把内存里的 DEX 抓回磁盘。

### 主流脱壳工具

- **FRIDA-DEXDump** ([hluwa/FRIDA-DEXDump](https://github.com/hluwa/FRIDA-DEXDump))：基于 Frida，扫所有 mmap 内存找 DEX 头（`dex\n035\0` 等），dump 出来。
- **BlackDex** ([CodingGay/BlackDex](https://github.com/CodingGay/BlackDex))：免越狱免 Frida，注入到目标进程做 dump。
- **reflutter**：针对 Flutter 应用。
- **ARTDump**：从 ART 内部 hook 入口拿 dex。

### 反调试常见检测点

- TracerPid (`/proc/self/status`)
- ptrace 自占位
- 反 inotify (`inotify_init` 监控被改)
- 关键函数前 4 字节校验
- VbMeta 启动状态检查

绕过方案：用 [`darvincisec/DetectTracer`](https://github.com/darvincisec/DetectTracer) 列出的清单逐个 hook。

## 三、典型工作流

### 360 加固脱壳
1. `ApkCheckPack` 查壳确认（其他在线工具：`apkidentifier`, `pkid` 等）。
2. `frida-server` push 到设备。
3. 启动 App。
4. `frida -U -f <pkg> -l frida-dexdump.js`，等几秒。
5. dump 出来一堆 dex 文件。
6. 重组 + jadx 反编译。

### 爱加密企业版
1. 反调试很强，需要先 hook 一系列检测函数（pthread_create / dlopen / mprotect / 篡改时间）。
2. FreeBuf 那篇（参考 raw-hits）给了完整 Frida 脚本。
3. 配合 frida-dexdump。
4. 重打包后用 NP 管理器+fancy 去签 + 修复签名校验。

### 阿里聚安全 / 腾讯乐固
- 难度更大，建议用 unidbg 黑盒模拟+frida 双管齐下。

## 四、微信小程序 wxapkg 解包

### 文件结构
- `__APP__.wxapkg`：主包。
- `subpackages/<name>.wxapkg`：分包。
- 头部含魔数 + 文件索引表。

### 加密
- PC 端微信里的 wxapkg 是加密的（双层 AES + xor），需要先解密。
- 解密 key 在 PC 内存，可通过 wxapkg 关联的 wxid+小程序 appid 派生。
- 工具：[BlackTrace/pc_wxapkg_decrypt](https://github.com/BlackTrace/pc_wxapkg_decrypt)。
- 真机抓的 wxapkg 通常直接解包（不加密）。

### 解包工具
- [wux1an/wxapkg](https://github.com/wux1an/wxapkg)（Go，现在最活跃）。
- [qwerty472123/wxappUnpacker](https://github.com/qwerty472123/wxappUnpacker)（老牌）。
- 在线：[See Wxapkg](https://seewxapkg.keepbuild.cn/)。

### 解包后
- 得到 `app.json`、`pages/*.html`、`*.wxss`、`*.js` 等。
- 部分小程序内置 jsvmp（如京东、美团小程序），需要二次还原。

### URL
- [微信小程序+反编译+AES 加解密 (CSDN 2025-12)](https://blog.csdn.net/huagangwang/article/details/135013405)
- [微信小程序逆向解密实战 (博客园 2026-01)](https://www.cnblogs.com/jzssuanfa/p/19455255)
- [手把手教你 微信小程序解密+反编译 (掘金)](https://juejin.cn/post/7312678013559636006)
- [2025 反编译微信小程序教程 (SegmentFault)](https://segmentfault.com/a/1190000046438288)
- [分包小程序解包反编译 (知乎)](https://zhuanlan.zhihu.com/p/719729034)
- [小程序反编译+最新存储位置 (FreeBuf 2025-08)](https://www.freebuf.com/articles/sectool/443248.html)
- [unwxapkg 工具 (GitCode)](https://blog.gitcode.com/ec16be06c7e4ea114ba23769830c875b.html)
- [[原创] 微信小程序反编译/解包 (看雪)](https://bbs.kanxue.com/thread-281804.htm)

## raw-hits 来源

- 加固壳：[android-batch3.md Q1, Q2](../raw-hits/android-batch3.md)。
- wxapkg 小程序：[web-batch1.md Q6](../raw-hits/web-batch1.md)。
