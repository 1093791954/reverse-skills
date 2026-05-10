# Frida 17 + Android Java Hook 工作流（不绑定具体 APP）

> **更新**: 2026-05-10
> **适用**: frida 17.x（17.0.0 起 Java/Objc/Swift bridge 已从内置 runtime 拆出）+ Android root 设备
> **典型场景**: hook APP 的 Java/Kotlin 方法绕过校验、伪造回调、dump 参数

## 0. frida 17 的 breaking change（务必先读）

| 变化 | 影响 |
|---|---|
| Java/Objc/Swift bridge 从 GumJS runtime 拆出 | `device.attach()` 后 `typeof Java === 'undefined'` |
| `frida` CLI 仍内置 bridge（用 `Script.evaluate` 加载） | CLI 可直接用 `Java.perform`，但 Python API 不行 |
| `--no-pause` 选项移除 | `frida -f <pkg>` 默认就是不暂停 |

## 1. Java bridge 加载方式（最稳）

frida-tools 自带 `frida_tools/bridges/java.js`，是已 bundle 好的 IIFE。前置到自己的脚本里即可：

```python
from pathlib import Path
import frida

JAVA_BRIDGE = Path(frida.__file__).parent.parent / 'frida_tools' / 'bridges' / 'java.js'
bridge_src = JAVA_BRIDGE.read_text(encoding='utf-8')

# bridge 是个 IIFE 末尾返回 bridge 对象，需要把它暴露到 globalThis
combined = bridge_src + "\nglobalThis.Java = bridge;\n" + your_hook_code
session.create_script(combined)
```

**不要用** `frida.Compiler()` 或 `import Java from 'frida-java-bridge'` —— 单文件 hook 不需要 ESM 解析，前置 IIFE 更稳。

## 2. 标准启动顺序（铁律）

```python
pid = device.spawn([PKG])              # 1. spawn 但不启动
session = device.attach(pid)           # 2. attach
script = session.create_script(code)   # 3. 创建 script
script.on('message', on_message)
script.load()                          # 4. ⚠️ load 必须在 resume 前
device.resume(pid)                     # 5. 最后 resume
```

**关键**：`load()` 必须在 `resume()` 前完成——否则 Java VM 起来后 hook 还没装好，错过类加载时机。

## 3. attach 已运行 APP（备选）

如果 spawn 模式触发反检测崩溃（如字节系），改用 attach：

```python
# 让用户手动启动 APP，我们 attach
for p in device.enumerate_processes():
    if PKG in p.name or '汽水' in p.name:
        pid = p.pid; break
session = device.attach(pid)
# 后续步骤一样
```

⚠️ attach 模式 hook 对 **APP 已经创建过的对象** 仍生效，但**已执行的方法** hook 不到（错过了）。

## 4. 长驻运行（不要让 Python 退出）

**别用** `sys.stdin.read()`（SSH/nohup/Windows 后台都会立即 EOF）。

```python
import threading
stop = threading.Event()
try:
    while not stop.is_set():
        time.sleep(1)
except KeyboardInterrupt:
    stop.set()
```

## 5. 自动重连（APP 崩溃/被杀后）

```python
relaunch = threading.Event()
def on_detach(reason, *a):
    print(f'[!] detached: {reason}')
    if reason in ('process-terminated', 'process-replaced'):
        relaunch.set()  # 触发重新 spawn

session.on('detached', on_detach)

while not stop.is_set():
    relaunch.clear()
    sess, scr = spawn_and_attach(device)
    while not relaunch.is_set() and not stop.is_set():
        time.sleep(0.5)
    try: sess.detach()
    except: pass
```

## 6. message handler 完整模板

```python
def on_message(msg, data):
    t = msg.get('type')
    if t == 'send':
        print('[send]', msg.get('payload'), flush=True)
    elif t == 'log':
        # frida 17 console.log 通过 type=log 上报
        print(f"[{msg.get('level','info')}]", msg.get('payload'), flush=True)
    elif t == 'error':
        print('[ERROR]', msg.get('description'), flush=True)
        if msg.get('stack'): print(msg['stack'], flush=True)
```

## 7. Java hook 脚本套路

```javascript
// 头部不需要 Java.perform 包，但内部要包
Java.perform(function () {
    // 步骤 1: 找到目标类
    var Target = Java.use('com.example.Target');

    // 步骤 2: 看可用重载
    Target.method.overloads.forEach(function (ov, i) {
        send({tag: 'overload', i: i, types: ov.argumentTypes.map(function(t){return t.className})});
    });

    // 步骤 3: hook 所有重载
    Target.method.overloads.forEach(function (ov) {
        ov.implementation = function () {
            send({tag: 'hit', argc: arguments.length});
            // 修改参数 / 返回值 / 不调用原函数
            var ret = ov.apply(this, arguments);
            send({tag: 'ret', value: ret + ''});
            return ret;
        };
    });
});
```

### 7.1 找类时机问题

某些类（特别是 Kotlin、动态加载类）启动时还没载入。两条解：

```javascript
// 方案 A: 用 performNow（spawn 注入时早期生效）
Java.performNow(function() { /* hook */ });

// 方案 B: 周期性重试
function tryHook() {
    try { var T = Java.use('com.foo.Bar'); /* hook */ }
    catch (e) { setTimeout(tryHook, 500); }
}
tryHook();

// 方案 C: 监听类加载
Java.enumerateClassLoaders({
    onMatch: function (loader) {
        Java.classFactory.loader = loader;
        try { var T = Java.use('com.foo.Bar'); /* hook */ } catch (e) {}
    },
    onComplete: function () {}
});
```

### 7.2 找实现接口的类

```javascript
function findImpls(interfaceName) {
    var impls = [];
    Java.enumerateLoadedClassesSync().forEach(function (cn) {
        try {
            var cls = Java.use(cn);
            cls.class.getInterfaces().forEach(function (iface) {
                if (iface.getName() === interfaceName) impls.push(cn);
            });
        } catch (e) {}
    });
    return impls;
}
```

### 7.3 NativeCallback 防 GC

frida QuickJS 没有 `global`，要用 `globalThis`：

```javascript
if (!globalThis._cbs) globalThis._cbs = [];
var cb = new NativeCallback(function(){return 0}, 'int', ['pointer']);
globalThis._cbs.push(cb);  // 不保留引用 cb 会被 GC，导致后续调用 SIGSEGV
```

## 8. 调试 hook 失败的套路

| 症状 | 检查 |
|---|---|
| `Java is not defined` | bridge 没加载好，前置 java.js 是否正确 |
| `ClassNotFoundException` | 类还没被加载，用 7.1 的方案 B/C |
| hook 没触发 | 类加载了但你 hook 错了重载，先 dump 全部 overloads 签名 |
| 一 hook 就 SIGSEGV/SIGTRAP | NativeCallback 被 GC（7.3）；或字节系反检测拦截 |
| `Failed to spawn: need Gadget` | frida-server 没启动或权限不对 |
| `invalid PID` on resume | spawn 顺序错了，必须 spawn → attach → load → resume |

## 9. frida-server 部署清单（Android root）

```bash
# 版本号必须严格匹配 PC 端 frida 版本（pip show frida）
VER=17.8.0
ARCH=arm64           # arm / arm64 / x86 / x86_64
URL="https://github.com/frida/frida/releases/download/${VER}/frida-server-${VER}-android-${ARCH}.xz"

# 下载
curl -L -x http://127.0.0.1:7897 -o frida-server.xz "$URL"
python -c "import lzma; open('frida-server','wb').write(lzma.open('frida-server.xz').read())"

# 推送（注意 push 到 /data/local/tmp 直接会 fchown 失败，要中转）
adb push frida-server /sdcard/
adb shell "su -c '
  cp /sdcard/frida-server /data/local/tmp/frida-server
  chmod 755 /data/local/tmp/frida-server
  chown root:root /data/local/tmp/frida-server
  rm /sdcard/frida-server
'"

# 启动
adb shell "su -c 'pgrep -f frida-server || nohup /data/local/tmp/frida-server -D >/dev/null 2>&1 &'"

# 验证
frida-ps -U | head
```

## 10. 完整可复用模板：runner.py

见 `frida-android-hook-runner-template.py`（同目录）。

## 11. 反检测注意事项

| 来源 | 应对 |
|---|---|
| 字节系 APP 检测 frida-server 端口 (27042/27043) | 启动时改端口：`frida-server -l 0.0.0.0:27999`；PC 端 `frida -H 127.0.0.1:27999`（配合 adb forward） |
| 检测 `/proc/self/maps` 里的 `frida-agent.so` | 用 `frida-server -t patched` 或 magisk 模块隐藏 |
| 检测 zygote 注入痕迹 | spawn 模式更易被检测；改用 attach 已启动 APP |
| native 反 hook（如字节 libsscronet） | 不要 hook 它的 SSL 函数，改 hook 业务 Java 层 |

## 12. 关键参考

- frida 17 changelog: https://frida.re/news/
- frida-java-bridge: https://github.com/frida/frida-java-bridge
- 字节系签名总览: [bytedance-x-gorgon-x-argus-notes.md](./bytedance-x-gorgon-x-argus-notes.md)
- Android APK 通用工作流: [android-apk-reversing-on-rooted-device-workflow.md](./android-apk-reversing-on-rooted-device-workflow.md)
