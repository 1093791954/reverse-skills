# iOS - 摸底 raw-hits 批次 1

## Q1: `ios frida detection jailbreak 反检测 ellekit palera1n` (Bing, 2026-05)

- **[原创] iOS 越狱检测 app 及 frida 过检测 (看雪 2023-06)** — https://bbs.kanxue.com/thread-277509.htm
  - hook getenv + JailBreakCheek 类
- **iOS 越狱检测 app 及 frida 过检测 (知乎)** — https://zhuanlan.zhihu.com/p/690226623
  - _dyld_get_image_name 遍历链接库
- **iOS 逆向 反调试与绕过 (zskkk 2024-01)** — https://www.zskkk.cn/posts/51299/
- **app 加固之 frida 检测 (博客园 GKLBB 2025-08)** — https://www.cnblogs.com/GKLBB/p/19055030
- **iOS Jailbreak Detection Bypass Palera1n (frida codeshare)** — https://codeshare.frida.re/@DevTraleski/ios-jailbreak-detection-bypass-palera1n/
- **iOS 安全开发中的 Frida 检测 (FreeBuf 2025-12)** — https://www.freebuf.com/articles/mobile/464550.html
- **tealbathingsuit/ellekit (GitHub)** — https://github.com/tealbathingsuit/ellekit
  - 异常处理改线程状态做 hook
- **iOS APP 反越狱检测技术 (CN-SEC 2024-01)** — https://cn-sec.com/archives/2429944.html
  - 拦截 stat / 修改路径检测
- **iOS 逆向反越狱检测实战 (CSDN 2023-08)** — https://blog.csdn.net/m0_72605044/article/details/132113551
  - ApiResolver 批量 hook jail 开头函数
- **iOS 逆向 frida 检测绕过 (小呆博客 2024-07)** — https://mezdosec.github.io/post/ios-ni-xiang-zhi-frida-jian-ce-rao-guo/

## Q2: `ios app attest devicecheck 逆向 sep key secure enclave` (Bing, 2026-05)

- **Establishing your app's integrity (Apple Developer)** — https://developer.apple.com/documentation/devicecheck/establishing-your-app-s-integrity
- **某 DD/某音 iOS DeviceCheck Token 正向研发与逆向 (iosre 2024-06)** — https://iosre.com/t/转载某dd某音-ios-devicecheck-token-正向研发与逆向分析之路思考/24569
- **rustymagnet3000/ios_devicecheck_app_attest (GitHub)** — https://github.com/rustymagnet3000/ios_devicecheck_app_attest
- **iOS 防 dump 可行性 + DeviceCheck/App Attest (掘金)** — https://juejin.cn/post/7251501966592917563
- **如何规避 Apple DeviceCheck 和 AppAttest (approov)** — https://approov.io/zh-cn/knowledge/how-to-defeat-apple-devicecheck-and-appattest
- **iOS Security Features Secure Enclave (CSDN 2025-01)** — https://blog.csdn.net/qq_45797625/article/details/144944805
- **Implementing Apple's Device Check App Attest (dev.to)** — https://dev.to/mnelsonwhite/implementing-apples-device-check-app-attest-protocol-4p2g
- **iOS 14 App Attest 防护功能 (51CTO 2020)** — https://www.51cto.com/article/624795.html
- **iOS 钥匙串 Secure Enclave 加密存储原理 (知乎)** — https://zhuanlan.zhihu.com/p/162717846
- **内核开发系列 2: SEP (看雪)** — https://bbs.kanxue.com/thread-271416.htm

## Q3: `frida-ios-dump bagbak 砸壳 rootless 越狱 ios17` (Bing, 2026-05)

- **Frida-iOS-dump 脱壳记录 (CSDN 2021-03)** — https://blog.csdn.net/qq_35231971/article/details/114580377
- **使用 frida-ios-dump 砸壳 (FreeBuf 2023-03)** — https://www.freebuf.com/articles/mobile/359419.html
- **ChiChou/bagbak (GitHub - deprecated)** — https://github.com/ChiChou/bagbak
- **Frida 脱壳实测 (简书 2024-09)** — https://www.jianshu.com/p/ee25e62ce012
- **iOS 逆向安防 砸壳与 Frida (知乎)** — https://zhuanlan.zhihu.com/p/376727930
  - Clutch / dumpdecrypted / frida 三种工具
- **windows 上 iOS App 一键砸壳教程 (看雪)** — https://bbs.kanxue.com/thread-252384.htm
- **frida-ios-dump 实例 (crifan iOS 砸壳书 2023)** — https://book.crifan.org/books/ios_re_crack_shell_ipa/website/crack_example/frida_ios_dump/
- **iOS 12.2 脱壳/砸壳 frida-ios-dump (腾讯云)** — https://cloud.tencent.com/developer/article/1897106
- **使用 Frida 脱壳与重签名 (阿里云开发者 2023-09)** — https://developer.aliyun.com/article/1321939

## Q4: `mach-o 加固 ios ipa 逆向 ollvm hikari pluto` (Bing, 2026-05)

- **iOS 静态逆向 IPA 结构 Mach-O 分析 (技术栈)** — https://jishuzhan.net/article/2051106564833083394
- **iOS 静态逆向 Mach-O 分析 (CSDN)** — https://blog.csdn.net/liuyinghui523/article/details/160747598
- **iOS 静态逆向 Mach-O 分析 (e-com-net mirror)** — https://www.e-com-net.com/article/2051214595955154944.htm
- **iOS 逆向实战 016 MachO (极客文档)** — https://geekdaxue.co/read/u12101430@fopz92/dg914h
- **iOS 逆向 MachO 文件 (知乎)** — https://zhuanlan.zhihu.com/p/271912854
- **iOS 逆向之 Mach-O 文件 (腾讯云 2022)** — https://cloud.tencent.com/developer/article/1798320
- **iOS 逆向 06 Mach-O (简书)** — https://www.jianshu.com/p/94f917f8a667
- **iOS 逆向 Mach-O (掘金)** — https://juejin.cn/post/7242163788039372855
- **iOS 小白逆向教程 Mach-O (51CTO 2025-01)** — https://blog.51cto.com/u_16099225/13054162
- **iOS 逆向编程 Mach-O 入门 (阿里云开发者)** — https://developer.aliyun.com/article/1291203

## Q5: `ios ssl pinning bypass frida ssl-kill-switch ellekit` (Bing, 2026-05)

- **Bypassing SSL Pinning on iOS (redfoxsec 2025-08)** — https://www.redfoxsec.com/blog/bypassing-ssl-pinning-on-ios-applications
- **iOS 逆向某 app 证书 SSL pinning 绕过 (Zgao blog)** — https://zgao.top/ios逆向四-某app证书ssl-pinning绕过/
- **objection+Frida 解决 iOS SSL Pinning (阿里云开发者)** — https://developer.aliyun.com/article/1160273
- **pritessh/iOS-SSL-Pinning-Bypass iOS17 (GitHub 2026-03)** — https://github.com/pritessh/iOS-SSL-Pinning-Bypass
  - Security.framework / BoringSSL / Network.framework / Alamofire
- **iOS 安装 SSL Kill Switch 2 (知乎)** — https://zhuanlan.zhihu.com/p/409394356
- **Frida 绕过 SSL Pinning iOS (技术栈 2025-07)** — https://jishuzhan.net/article/1945294912152449026
- **Frida 绕过 SSL Pinning iOS (CSDN 2025-07)** — https://blog.csdn.net/woai_zhongguo/article/details/149291087
- **iOS SSL Bypass (frida codeshare lichao890427)** — https://codeshare.frida.re/@lichao890427/ios-ssl-bypass/
- **Bypassing SSL Pinning on iOS (Medium 2024-12)** — https://medium.com/@sachin.hack/bypassing-ssl-pinning-on-ios-devices-a-comprehensive-guide-2fb6cef461aa
- **iOS 突破 SSL Pinning 抓包 (极客文档)** — https://geekdaxue.co/read/sunj3t@uaxxwi/tu-po-ssl-pinning-jin-xing-zhua-bao
