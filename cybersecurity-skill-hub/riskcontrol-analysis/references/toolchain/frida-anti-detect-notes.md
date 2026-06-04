# Toolchain：Frida 反检测 + 魔改 - notes

## 一、Frida 检测点全览（六大类）

### 1. 进程/线程名
- `gum-js-loop`、`gmain`、`gdbus`：Frida 注入后启动的线程，名字硬编码。
- `frida-server`：默认进程名。
- 检测代码：
```c
// 遍历 /proc/self/task/*/comm
// 与 "gum-js-loop" / "gmain" 等字符串比对
```

### 2. 端口
- 27042：默认 Frida server 监听端口。
- `cat /proc/net/tcp` 找 27042（hex `69A2`）。

### 3. 文件
- `/data/local/tmp/frida-server`、`/data/local/tmp/re.frida.server`。
- `libfrida-agent.so`、`libfrida-gadget.so` 在 `/proc/self/maps` 出现。

### 4. 内存特征
- 关键函数前 4 字节是否被 patch 成 inline hook（`B`/`BLR` 跳转），原值应是 `STP X29, X30, [SP, #-16]!`（`FD 7B BF A9`）。
- libfrida-agent 内的特征字节序列扫描。

### 5. JNI / Java 反射
- `Class.forName("frida.something")` 探针。
- 已知 hook 框架的回调类（如 `XvFWWExBridge$HookerCallback`）。

### 6. 系统调用层
- `linker64` 符号扫，找 frida 相关符号。
- `getprop sys.frida.server` 等 prop 探针。

## 二、绕过工具链

### strongR-frida-android (hzzheyang)
- 跟随 frida upstream 自动 patch 反检测特征。
- 改字符串：`gmain` → `fmain`、`gum-js-loop` → 自定义、`frida_agent_main` → `main`。
- 改端口：可在编译时换。
- 改进程名：自定义。

### hluda-server / hluda
- 老牌魔改 frida-server。
- 多平台支持（Android/iOS）。
- 但维护已不如 strongR 活跃。

### 自己魔改
- clone frida-core → grep `gum-js-loop`/`gmain`/`gdbus` → 替换成无意义字符。
- frida-agent.so 改名 → 修改 ELF SONAME/STRING table。
- 编译时改 `FRIDA_AGENT_FILENAME`。

## 三、Magisk / Zygisk / DenyList / Shamiko

### Magisk DenyList（默认）
- 在 Settings → Configure DenyList 勾选要隐藏 root 的 App。
- 但 DenyList 本身只能"卸载 Magisk 痕迹"，不能完全隐藏 root。

### Shamiko (LSPosed 出品)
- Zygisk 模块，比 DenyList 更彻底地隐藏 zygote 注入。
- 配置：建议勾选所有应用 + 开 "whitelist" 模式（白名单内不隐藏）。

### KernelSU / APatch
- 内核态 root，对用户态检测有天然优势。
- 但仍需配合 Susfs 等模块隐藏 mount 点。

## 四、ART Hook 检测

LSPlant（LSPosed 底层）会改 ArtMethod：
- `accessFlags`：被 hook 后会标 native。
- `entryPoint`：从 quick_code 改为 hook stub。
- 比对类是否在 framework boot.oat 内。

防御 App 检查这些字段，hook 框架要保持 ArtMethod 一致性才能逃过检测。

## raw-hits 来源

- 见 [toolchain-batch1.md Q1, Q2](../raw-hits/toolchain-batch1.md)。

## 关键 URL

入门：
- [[原创] Frida 常见检测与绕过 (看雪 2025-12)](https://bbs.kanxue.com/thread-289358.htm)
- [app 加固之 frida 检测六大类 (博客园 GKLBB 2025-08)](https://www.cnblogs.com/GKLBB/p/19055030)
- [Frida 特征检测及绕过 (酸心果子 2025-10)](https://ihandmine.github.io/2025/10/15/article18_frida_detection_bypass/)

进阶：
- [hzzheyang/strongR-frida-android (GitHub)](https://github.com/hzzheyang/strongR-frida-android)
- [Frida 魔改反检测初探 (idocdown 2026-03)](https://idocdown.com/app/articles/blogs/detail/18100)
- [反 Frida 检测与禁止 SSLPinning (bzi-han 2022)](https://blog.bzi-han.top/2022/09/13/编程-反Frida检测与禁止SSLPinning的一些思路和方法/)
- [hluda 安卓 Root 检测绕过 (crifan 2025-01)](https://book.crifan.org/books/android_re_root_env_detect_bypass/website/detect_bypass/frida/bypass/hluda/)

Magisk/Zygisk/Shamiko：
- [Zygisk 版面具过银行 App (知乎)](https://zhuanlan.zhihu.com/p/470468650)
- [Shamiko 模块原理 (酸心果子 2025-09)](https://ihandmine.github.io/2025/09/13/article10_shamiko_analysis/)
- [Magisk 中文网 配置 DenyList](https://magiskcn.com/magisk-configure-denylist.html)
- [LSPosed/LSPosed Wiki](https://github.com/LSPosed/LSPosed/wiki)
- [tiann/KernelSU](https://github.com/tiann/KernelSU)
- [bmax121/APatch](https://github.com/bmax121/APatch)

## 工作流建议

1. App 闪退时先用 strongR-frida 试一遍。
2. 仍闪退：开 Frida 的 `--no-pause` + `Process.enumerateThreads()` 看是不是线程名被检测。
3. 关键函数前 4 字节校验：用 `Memory.protect` + `Memory.writeByteArray` 先写回原字节再 hook（或用 `Stalker` 替代 inline hook）。
4. 长期对抗：自己魔改 frida-agent.so，改字符串+SONAME+入口符号。
5. KernelSU+Shamiko+strongR-frida 是当前 2026 年最稳的组合。
