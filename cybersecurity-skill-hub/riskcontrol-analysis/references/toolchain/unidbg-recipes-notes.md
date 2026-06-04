# Toolchain：unidbg 黑盒模拟 + qiling - notes

## 一、unidbg 简介

[zhkl0228/unidbg](https://github.com/zhkl0228/unidbg) 是国内事实标准的"在 PC 上黑盒调用 Android/iOS SO 函数"的工具，基于 unicorn 引擎+Java JNI 桥+完整的 Android/iOS Runtime mock。

**核心价值**：风控 SO 加密参数还原时，**无需真机+无需 root+无需 Frida**，离线在 IDE 跑出加密结果。

## 二、典型用法

```java
// 1. 加载 APK 与 SO
AndroidEmulator emulator = AndroidEmulatorBuilder.for64Bit().build();
Memory memory = emulator.getMemory();
memory.setLibraryResolver(new AndroidResolver(23));
VM vm = emulator.createDalvikVM(new File("app.apk"));
DalvikModule dm = vm.loadLibrary(new File("libtarget.so"), false);
dm.callJNI_OnLoad(emulator);

// 2. 调用目标 Java 方法（会触发到 Native）
DvmObject<?> obj = ProxyDvmObject.createObject(vm, target);
DvmObject<?> result = obj.callJniMethodObject(emulator,
    "encrypt(Ljava/lang/String;)Ljava/lang/String;",
    "input_data");
System.out.println(result);
```

## 三、常见坑点

### JNI mock 不完整
- `unidbg` 默认只 mock 一些 Android API；如 SO 调了 `getprop` / `readlink` / `pthread_create` / `mmap MAP_SHARED` 等 → 必须自己写 stub。
- 错误兆：返回 0/null 或 UnsupportedOperationException。
- 解法：实现 `Hookable.callObjectMethod` / `IOResolver` 等接口。

### syscall 未实现
- 如 fstat 对目录返回全零、SECCOMP 等冷门 syscall → 触发 `[exit] panic` 或返回错。
- 解法：用 `syscallHandler` 注册，参考 `安卓逆向这档事第 26 课 Unidbg 补完环境` (看雪 2025-10)。

### 业务依赖运行时数据
- 若 SO 依赖 `/data/data/<pkg>/files/some.dat`、APK 内的 assets、`/proc/self/...` → 必须填入对应数据。
- 解法：vm.setupApkSign() / mock 文件系统。

### code-patch-check 自校验
- 风控 SO 会校验自身 .text 段哈希，unidbg 启动时 patch 了的 SO 哈希会变 → SO 拒绝运行。
- 解法：用 unidbg-boot-server 时配合 `vm.setVerbose(false)` + 关闭 unidbg 自身的 patch；或者在算 sig 前重写 .text 段为原值。

## 四、unidbg-boot-server

[anjia0532/unidbg-boot-server](https://github.com/anjia0532/unidbg-boot-server) 把 unidbg 包成 Spring Boot 服务，提供 HTTP 接口。

- 适合工业化批量调用：抖音/快手/京东/拼多多公开案例都用过。
- 单机 QPS 几十到几百（取决于 SO 计算量）。
- 注意池化与并发：每个请求启一个 emulator 实例较慢；建议预热 N 个实例池化复用。

## 五、qiling 与 AndroidNativeEmu

### qiling
[qilingframework/qiling](https://github.com/qilingframework/qiling) 全系统跨架构模拟，可跑 Linux ELF / Windows PE / macOS Mach-O / iOS / Android。

- 适合：跨架构（不仅 ARM64，还有 MIPS/PowerPC）、跨 OS。
- 不适合：纯 Android JNI 风控（unidbg 更专精）。

### AndroidNativeEmu
[AeonLucid/AndroidNativeEmu](https://github.com/AeonLucid/AndroidNativeEmu) 是 Python+unicorn 的 unidbg 等价物。

- 优点：Python 生态，方便集成。
- 缺点：JNI mock 完成度不如 unidbg；维护活跃度也不如。

## raw-hits 来源

- 见 [toolchain-batch1.md Q3](../raw-hits/toolchain-batch1.md)。

## 关键 URL

入门：
- [Android 逆向 Unidbg 实战调试 (CSDN 2026-03)](https://blog.csdn.net/weixin_29214559/article/details/158987898)
- [Unidbg 入门介绍 (gla2xy 2024-12)](https://gal2xy.github.io/2024/12/05/Unidbg模拟执行/Unidbg学习与实践/)
- [Unidbg 调用 so 层函数 (OSCHINA)](https://my.oschina.net/xiaominmin/blog/10097065)

进阶：
- [[原创] 安卓逆向这档事第 26 课 Unidbg 补完环境 (看雪 2025-10)](https://bbs.kanxue.com/thread-288711.htm)
- [应用安全 Unidbg (51CTO GKLBB)](https://blog.51cto.com/gklbb/14175652)
- [第二十三课 黑盒魔法之 Unidbg (GitHub ZJ595)](https://github.com/ZJ595/AndroidReverse/blob/main/Article/25%E7%AC%AC%E4%BA%8C%E5%8D%81%E4%B8%89%E8%AF%BE%E3%80%81%E9%BB%91%E7%9B%92%E9%AD%94%E6%B3%95%E4%B9%8BUnidbg.md)

实战案例：
- [unidbg 主动调用 tiktok so 生成签名 (逆想技术)](https://nixiang.tech/forum.php?mod=viewthread&tid=401)
- [wmm1996528/unidbg_douyin11 (GitHub)](https://github.com/wmm1996528/unidbg_douyin11)

工业化：
- [anjia0532/unidbg-boot-server (GitHub)](https://github.com/anjia0532/unidbg-boot-server)

## 工作流建议

1. **新 SO 第一刀**：拿到 SO → unidbg 加载 → 调用 JNI_OnLoad → 看是否报错。
2. **报 unimplemented syscall**：补 `syscallHandler`，看雪 26 课文章列了常见的。
3. **报 io 问题**：补 `IOResolver` 给虚拟文件。
4. **拿到结果**：与真机抓包结果对比 → byte-by-byte 一致才算通。
5. **批量化**：包成 unidbg-boot-server，对外提供 HTTP。
6. **稳定性**：注意 emulator 实例并发隔离，每个线程独立实例。
