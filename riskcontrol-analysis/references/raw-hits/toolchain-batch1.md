# Toolchain - 摸底 raw-hits 批次 1（Frida/Xposed/Magisk/unidbg/反混淆）

## Q1: `frida 反检测 anti-frida detection strongR-frida gum-js-loop` (Bing, 2026-05)

- **hzzheyang/strongR-frida-android (GitHub)** — https://github.com/hzzheyang/strongR-frida-android
- **[原创] Frida 常见检测与绕过 (看雪 2025-12)** — https://bbs.kanxue.com/thread-289358.htm
  - gmain/gdbus/gum-js-loop 字符串硬编码；HLuda 改字符串
- **app 加固之 frida 检测六大类 (博客园 GKLBB 2025-08)** — https://www.cnblogs.com/GKLBB/p/19055030
- **Frida 特征检测及绕过 (酸心果子 2025-10)** — https://ihandmine.github.io/2025/10/15/article18_frida_detection_bypass/
  - 进程/文件/端口/内存/动态库
- **安卓逆向：Frida 检测绕过与反制 (CSDN 2026-04)** — https://blog.csdn.net/weixin_30687051/article/details/159701396
- **Frida 魔改反检测初探 (idocdown 2026-03)** — https://idocdown.com/app/articles/blogs/detail/18100
  - frida_agent_main → main 改入口点符号
- **绕过 frida 特征检测 (SegmentFault 2022)** — https://segmentfault.com/a/1190000042082961
- **反 Frida 检测与禁止 SSLPinning (bzi-han 2022)** — https://blog.bzi-han.top/2022/09/13/编程-反Frida检测与禁止SSLPinning的一些思路和方法/
- **hluda 安卓逆向 Root 检测绕过 (crifan 2025-01)** — https://book.crifan.org/books/android_re_root_env_detect_bypass/website/detect_bypass/frida/bypass/hluda/
- **frida-server 去特征+编译 (sechub.in)** — https://sechub.in/view/2512467

## Q2: `magisk denylist zygisk shamiko 隐藏 root 检测` (Bing, 2026-05)

- **Zygisk 版面具 Magisk 过银行 App 等 Root 检测 (知乎)** — https://zhuanlan.zhihu.com/p/470468650
- **Magisk Zygisk 与 Shamiko 模块配置全攻略 (CSDN)** — https://blog.csdn.net/weixin_42526015/article/details/160811736
- **Magisk Zygisk 隐藏安卓 Root 状态实战 (hey99 mirror 2026)** — https://www.hey99.cn/shot/CSDN_158293220
- **Shamiko 模块原理解析 (酸心果子 2025-09)** — https://ihandmine.github.io/2025/09/13/article10_shamiko_analysis/
- **Zygisk 模块 Shamiko 隐藏 (阿里云开发者)** — https://developer.aliyun.com/article/1230670
- **Zygisk 版 Magisk 过银行 App Root 检测 (简书)** — https://www.jianshu.com/p/a450f27fe3e7
- **个人自用隐藏 root 方法/工具/模块 (博客园 enderdavidcode 2026)** — https://www.cnblogs.com/enderdavidcode/p/19686942
- **Android Root/VPN 隐藏方案 (felix021 gist)** — https://gist.github.com/felix021/2a5148e5e7aae3835712748e77b109ed
- **Magisk Zygisk 隐藏 (B 站)** — https://www.bilibili.com/video/BV1Su411Q7a5/
- **配置排除列表 Configure Denylist (Magisk 中文网)** — https://magiskcn.com/magisk-configure-denylist.html

## Q3: `unidbg 逆向 黑盒 模拟 so 主动调用` (Bing, 2026-05)

- **Android 逆向 Unidbg 实战调试与 Hook (CSDN 2026-03)** — https://blog.csdn.net/weixin_29214559/article/details/158987898
- **应用安全 模拟独立运行 so 的方法 Unidbg (51CTO GKLBB)** — https://blog.51cto.com/gklbb/14175652
- **第二十三课 黑盒魔法之 Unidbg (GitHub ZJ595/AndroidReverse)** — https://github.com/ZJ595/AndroidReverse/blob/main/Article/25%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E8%AF%BE%E3%80%81%E9%BB%91%E7%9B%92%E9%AD%94%E6%B3%95%E4%B9%8BUnidbg.md
- **Unidbg 入门介绍 (gla2xy)** — https://gal2xy.github.io/2024/12/05/Unidbg%E6%A8%A1%E6%8B%9F%E6%89%A7%E8%A1%8C/Unidbg%E5%AD%A6%E4%B9%A0%E4%B8%8E%E5%AE%9E%E8%B7%B5/
- **android 逆向 unidbg 调用 so 层函数 (OSCHINA)** — https://my.oschina.net/xiaominmin/blog/10097065
- **进入 Unidbg 的世界 (夏洛魂博客 2024-06)** — https://xialuohun.top/posts/android/unidbg/01%E8%BF%9B%E5%85%A5unidbg%E7%9A%84%E4%B8%96%E7%95%8C/
- **安卓逆向前戏 黑盒调用 frida-rpc + Unidbg (B 站)** — https://www.bilibili.com/video/BV1rKW6eeELG/
- **[原创] 安卓逆向这档事第 26 课 Unidbg 补完环境 (看雪 2025-10)** — https://bbs.kanxue.com/thread-288711.htm
- **Unidbg 调试 so (知乎)** — https://zhuanlan.zhihu.com/p/403037464

## Q4: `ollvm 去混淆 control flow flatten unflatten d-810` (Bing, 2026-05)

- **cdong1012/ollvm-unflattener: Miasm 还原 (GitHub)** — https://github.com/cdong1012/ollvm-unflattener
- **[原创] Ollvm 混淆还原学习 (看雪 2025-11)** — https://bbs.kanxue.com/thread-289179.htm
  - BCF + FLA/CFF 双核心
- **去除控制流平坦化 (linkpwn 2025-09)** — https://linkpwn.github.io/2025/09/09/去除控制流平坦化/
- **去 ollvm 平坦化 (viol1t 2024-07)** — https://viol1t.com/2024/07/24/去ollvm平坦化/
- **反 OLLVM 控制流扁平化工具 (知乎 Miasm)** — https://zhuanlan.zhihu.com/p/1890330591536338937
- **0 基础学习 ollvm 反混淆 控制流平坦化 (iosre 2024-09)** — https://iosre.com/t/0基础学习ollvm反混淆之-0x02-控制流平坦化-fla/24880
  - D810 直接完美还原 + clang-15 -mllvm -enable-cffobf
- **Ollvm 混淆还原学习 (信息安全知识库 gm7)** — https://www.gm7.org/archives/19545
- **OLLVM 混淆原理深度解析 BCF/FLA (yunpan 2025-12)** — https://yunpan.plus/t/4559-1-1
- **D810 安装和使用 (吾爱破解 2023-12)** — https://www.52pojie.cn/thread-1872852-1-1.html
  - https://gitlab.com/eshard/d810

## Q5: `ssl pinning bypass frida universal okhttp conscrypt` (Bing, 2026-05)

- **CYRUS-STUDIO/frida-ssl-pinning-bypass Java+Native (GitHub 2025-07)** — https://github.com/CYRUS-STUDIO/frida-ssl-pinning-bypass
- **Bypass SSL Pinning (frida codeshare Q0120S)** — https://codeshare.frida.re/@Q0120S/bypass-ssl-pinning/
- **Android 证书绑定绕过研究 (二) (CSDN)** — https://blog.csdn.net/qq_30135181/article/details/119677157
- **Frida Android 实战 7 SSL Pinning (技术栈 2025-11)** — https://jishuzhan.net/article/1991704466169593858
- **通用使用 Frida 绕过 Android SSL (51CTO 2022)** — https://blog.51cto.com/lilongsy/5456472
- **FridaBypassKit SSL Pinning (DeepWiki 2026-02)** — https://deepwiki.com/okankurtuluss/FridaBypassKit/4.2-ssl-pinning-bypass
- **Frida 绕过 Android SSL Pinning (腾讯云)** — https://cloud.tencent.com/developer/article/2201981
- **Android15 Frida 绕过 SSL (CN-SEC 2025-04)** — https://cn-sec.com/archives/3916232.html
- **使用 frida 绕过安卓 ssl pinning (掘金)** — https://juejin.cn/post/7095682271457312776
- **Frida Android 实战 4 SSL Pinning (博客园 2025-12)** — https://www.cnblogs.com/jzssuanfa/p/19333298

## Q6: `lsposed xposed 模块 教程 hook java` (Bing, 2026-05)

- **LSposed hook 学习分享 (博客园 ClownLMe 2025-04)** — https://www.cnblogs.com/ClownLMe/p/18814473
- **LSPosed 模块开发完整指南 (CSDN 2025-12)** — https://blog.csdn.net/gitblog_00402/article/details/155691338
- **LSPosed-Java 层 Hook (夏洛魂 2022)** — https://xialuohun.top/posts/android/android-hook/lsposed/lsposed-java层hook/
- **Android Hook + 简单 xposed 模块 (Kinoko 2025-01)** — https://blog.kinoko.fun/2025/01/11/2025/androidhook-xposed-module/
- **LSPosed 模块开发入门 + 踩坑 (技术栈)** — https://jishuzhan.net/article/1830806770482679809
- **编译 Lsposed 默认 hook 所有 app (拓森)** — https://www.uzilol.cn/article/139bf20f-1d11-80d4-aa26-c1ddeaf40df6
- **LSPosed+Xposed 模块 Hook (binmt 2023-12)** — https://bbs.binmt.cc/thread-125074-1-1.html
- **Xposed 模块开发保姆级 (狐言狐语 2022)** — https://blog.ketal.icu/cn/Xposed模块开发入门保姆级教程/
- **Xposed Hook 学习 (Ma5k 2025-09)** — https://alenirving.github.io/2025/09/01/Xposed-Hook学习/
- **lsposed 开发教程专题 (B 站)** — https://www.bilibili.com/video/BV1Jo9oYzEmA/

## Q7: `frida-il2cpp-bridge unity 逆向 加密` (Bing, 2026-05)

- **Frida-il2cpp-bridge 终极指南 Unity (CSDN 2025-12)** — https://blog.csdn.net/gitblog_00372/article/details/155336214
- **frida-il2cpp-bridge 对 Unity hook (24k 2026-02)** — https://24kblog.top/posts/2611483955/
- **[原创] Unity il2cpp lua 手游逆向 (看雪 2025-08)** — https://bbs.kanxue.com/thread-287964.htm
- **frida-il2cpp-bridge Unity 教程 (hey99 2026-01)** — https://www.hey99.cn/shot/CSDN_155767786
- **掌握 frida-il2cpp-bridge (AtomGit GitCode)** — https://blog.gitcode.com/129182d088439170ebde833924b38bfe.html
- **Il2cpp 逆向 global-metadata 解密 (腾讯云 2023-02)** — https://cloud.tencent.com/developer/article/2216959
- **vfsfitvnm/frida-il2cpp-bridge (GitHub)** — https://github.com/vfsfitvnm/frida-il2cpp-bridge
- **Frida Il2Cpp Bridge 实例 Hook (吾爱破解 2024-02)** — https://www.52pojie.cn/thread-1891741-1-1.html
- **破解 Unity 单机金币 (博客园 apiter)** — https://www.cnblogs.com/apiter/articles/17888765.html
- **Unity3D+Frida+Hook (Jche143 2022-03)** — https://jche143.github.io/2022/03/04/Unity3D-Frida-Hook/
