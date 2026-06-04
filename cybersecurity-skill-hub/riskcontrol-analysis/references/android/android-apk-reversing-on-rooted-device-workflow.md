# Android APK 逆向通用工作流（KernelSU/SukiSU root 设备）

> **更新**: 2026-05-10
> **适用**: 任何 Android APK 逆向，已 root（KernelSU/Magisk 系）的真机 + Windows PC
> **典型目标**: 抓包还原 API、签名算法还原、广告/会员等业务功能逆向、frida hook 跳过验证

本文档是 **可复用的工作流**，不绑定具体 APP。最后附一个汽水音乐 (`com.luna.music`) 的实战案例。

---

## 0. 一次性环境准备清单

### 0.1 PC 端
```
adb (platform-tools)
Python 3.11+ + pip
  pip install frida frida-tools mitmproxy objection requests httpx pycryptodome cryptography
Node 22 (写 frida hook 脚本可选)
JDK 17+ (跑 jadx/apktool)
jadx-gui     # APK 反编译看 Java
apktool      # APK 拆包/重打包
aapt         # 看 APK 元信息（Android SDK 自带）
代理（如本机 7897）  # GitHub 资源走它
```

### 0.2 设备端（一次性配置）
```bash
# 1. frida-server 版本必须严格匹配 PC 端 frida 版本，架构匹配 ABI
# 下载：https://github.com/frida/frida/releases/download/<VER>/frida-server-<VER>-android-<ABI>.xz
adb push frida-server /sdcard/
adb shell "su -c 'cp /sdcard/frida-server /data/local/tmp/ && chmod 755 /data/local/tmp/frida-server && rm /sdcard/frida-server'"

# 2. 在 root 管理器（SukiSU/Magisk）里给 Shell（com.android.shell）授予 root
#    完成后 adb shell "su -c id" 应返回 uid=0(root)
```

### 0.3 抓包链路（每次会话）
```bash
# 1. 启动 frida-server（守护模式）
adb shell "su -c 'pgrep -f frida-server || nohup /data/local/tmp/frida-server -D &'"

# 2. 启动 mitmweb
mitmweb --listen-host 127.0.0.1 --listen-port 8080 \
        --web-host 127.0.0.1 --web-port 8081 \
        --set confdir=<workdir>/.mitmproxy

# 3. adb reverse 反向代理（手机的 127.0.0.1:8080 直通电脑，无需同 WiFi）
adb reverse tcp:8080 tcp:8080

# 4. 装 mitmproxy CA 为系统证书
HASH=$(openssl x509 -inform PEM -subject_hash_old -in mitmproxy-ca-cert.pem | head -1)
cp mitmproxy-ca-cert.pem ${HASH}.0
adb push ${HASH}.0 /sdcard/
adb shell "su -c '
  mkdir -p /data/local/tmp/cacerts
  cp /system/etc/security/cacerts/* /data/local/tmp/cacerts/
  cp /sdcard/${HASH}.0 /data/local/tmp/cacerts/
  chmod 644 /data/local/tmp/cacerts/${HASH}.0
  mount --bind /data/local/tmp/cacerts /system/etc/security/cacerts
'"
# ⚠️ Tricky Store 等模块若已 bind-mount 该目录，需先 umount

# 5. 设置代理（MIUI 等定制 ROM 必须用 root）
adb shell "su -c 'settings put global http_proxy 127.0.0.1:8080'"

# 取消代理：adb shell "su -c 'settings put global http_proxy :0'"
```

---

## 1. 拿到 APK

| 来源 | 方法 |
|---|---|
| 官网 | curl 下页面找下载短链；常见是 `ugapk.com/<id>` 跳到 `lf*.ugapk.cn/.../.apk` |
| 已安装的 APP | `adb shell pm path <pkg>` 拿路径 → `adb pull` |
| 第三方 APK 站 | apkpure.com / apkmirror.com / 酷安 |
| Google Play | gplaydl / Aurora Store |

### 用 aapt 看元信息
```bash
"<sdk>/build-tools/35.0.0/aapt.exe" dump badging app.apk | head -30
# 拿到 package='xxx' versionName='x.x.x' targetSdkVersion='xx'
# 看 uses-permission 找广告 SDK / 风控 SDK 痕迹（如 TT_PANGOLIN = 穿山甲）
```

### 看 APK 结构（直接 zipinfo）
```python
import zipfile
with zipfile.ZipFile('app.apk') as z:
    names = z.namelist()
    print('dex 数量:', sum(1 for n in names if n.startswith('classes') and n.endswith('.dex')))
    print('架构:', sorted(set(n.split('/')[1] for n in names if n.startswith('lib/'))))
    sigs = [n for n in names if n.startswith('META-INF/') and n.endswith('.RSA')]
    print('签名文件:', sigs)  # 字节系是 META-INF/BYTESIGN.RSA
```

## 2. 安装 APK 到手机

### 直接 install 通常会被 MIUI/HyperOS 拦
```bash
adb install -r app.apk
# Failure [INSTALL_FAILED_USER_RESTRICTED: Install canceled by user]
```

### Root 强制安装（最稳）
```bash
adb push app.apk /sdcard/
adb shell "su -c '
  cp /sdcard/app.apk /data/local/tmp/
  chmod 644 /data/local/tmp/app.apk
  pm install -r -i com.android.vending /data/local/tmp/app.apk
  rm /data/local/tmp/app.apk /sdcard/app.apk
'"
```

`-i com.android.vending` 把"安装来源"伪造成 Google Play，可绕过部分 APP 的"非官方安装"检测。

## 3. 列出 APP 加载的 native 库（找 SSL pinning 入口）

```bash
PID=$(adb shell "su -c 'pgrep -f <package>'" | head -1 | tr -d '\r')
adb shell "su -c 'cat /proc/$PID/maps | grep -oE \"/data/.*\\.so\\$|/system/.*\\.so\\$\" | sort -u'" \
  | grep -iE "ssl|crypt|cronet|net|tt|byte"
```

**字节系常见 native 库**：
- `libttboringssl.so` ← BoringSSL，pinning 在这里
- `libsscronet.so` ← Cronet，pinning 也可能在这里
- `libttcrypto.so`, `libEncryptor.so` ← 加密签名
- `libbytehook.so` ← inline hook 框架

**拉出库做静态分析**：
```bash
adb shell "su -c 'cp /data/app/.../lib/arm64/libxxx.so /sdcard/'"
adb pull /sdcard/libxxx.so .
strings libxxx.so | grep -iE "^SSL_|^X509_"  # 看导出符号
```

## 4. SSL Pinning 绕过（按强度递增）

### 4.1 Java 层（OkHttp + TrustManager + WebView）
直接用 [HTTP Toolkit 的 unpinning script](https://github.com/httptoolkit/frida-interception-and-unpinning):
```bash
# 三件套
curl -O .../config.js
curl -O .../android-certificate-unpinning.js
curl -O .../android-certificate-unpinning-fallback.js
```

config.js 里填 mitmproxy 的 CA 证书 PEM 和代理地址，启动：
```bash
frida -U -f <pkg> -l config.js -l android-certificate-unpinning.js -l android-certificate-unpinning-fallback.js
```

**对大多数 APP 这步就够了**。但字节系/抖音系 APP 还需要下面的 native hook。

### 4.2 Native 层（BoringSSL/Cronet）

字节系 APP 用自家 `libttboringssl.so`，pinning 在 **`SSL_CTX_set_custom_verify`** 设置的 callback 里。这个 callback 会去校验证书指纹是不是字节官方的。

**bypass 思路**：拦截 `SSL_CTX_set_custom_verify(ctx, mode, callback)`，把 `callback` 替换成永远返回 `0` (`ssl_verify_ok`) 的假函数。

frida 17 关键 API：
```js
// 不要再用废弃的 Module.findExportByName(libName, sym)！
// 用：
Process.findModuleByName('libttboringssl.so').findExportByName('SSL_CTX_set_custom_verify')
// 全局符号用：
Module.findGlobalExportByName('dlopen')
```

完整脚本参见 `<workdir>/hooks/native-ssl-bypass.js`。要点：
- 关注库列表: `libttboringssl.so` / `libsscronet.so` / `libssl.so` / `libboringssl.so`
- 这些库通常 APP 启动后 dlopen，要 hook `dlopen`/`android_dlopen_ext` 拦截加载事件
- 也要周期性 retry（因为 dlopen 调用顺序未知）
- **NativeCallback 实例必须保存到 global 防 GC**

BoringSSL 关键 API:
```c
void SSL_CTX_set_custom_verify(SSL_CTX *ctx, int mode,
    enum ssl_verify_result_t (*callback)(SSL *ssl, uint8_t *out_alert));
// 返回值: ssl_verify_ok=0, ssl_verify_invalid=1, ssl_verify_retry=2

long SSL_get_verify_result(const SSL *ssl);  // 返回 0=X509_V_OK 表示成功

int X509_verify_cert(X509_STORE_CTX *ctx);   // 返回 1=成功
```

### 4.3 排查：bypass 是否成功
```bash
# 看 mitmweb 日志的 "Client TLS handshake failed" 是否针对目标域名
grep "TLS handshake failed" <mitmweb.log> | grep <target-domain>

# 看 logcat 的 SSL 错误
adb shell "su -c 'logcat -d -t 500'" | grep -iE "ssl|trust|cert|<package-keyword>"

# 关键错误信号:
#   "Trust anchor for certification path not found"  → Java 层未绕过
#   "ssl/tls alert certificate unknown"               → APP 拒绝代理证书 = native pin 未绕过
```

## 5. 抓包分析

### 5.1 列举所有抓到的流量
```python
import requests
d = requests.get('http://127.0.0.1:8081/flows').json()
for f in d:
    if f.get('response'):
        r, rs = f['request'], f['response']
        print(rs.get('status_code'), r['method'], r['pretty_host'], r['path'][:80])
```

### 5.2 过滤业务相关请求
```python
keys = ['<your-target-domain>']  # 如 'qishui.com', 'douyin.com'
matched = [f for f in d if any(k in f['request']['pretty_host'] for k in keys)]
```

### 5.3 导出 .har 文件给浏览器看
mitmweb 已提供 `/flows.dump`、单个 flow 的 `/flows/<id>.json`，也可在 mitmweb UI 里右键导出。

## 6. 反编译看签名算法

### jadx-gui
```
File → Open APK → 选 .apk
全文搜索 (Ctrl+Shift+F):
  目标域名（如 'api5.qishui.com'）
  签名 header 名（如 'X-Argus', 'X-Gorgon', 'X-Khronos'）
  关键字符串（如 'sign=', 'Signature'）
```

### 字节系常见签名机制
- `X-Khronos`: 时间戳秒
- `X-Gorgon`: 校验值（V0~V5），一般 0408/0404 前缀
- `X-Argus`: 设备指纹+签名（protobuf 后加密）
- `X-Ladon`: URL/Body 派生签名
- 详见 [bytedance-x-gorgon-x-argus-notes.md](./bytedance-x-gorgon-x-argus-notes.md)

## 7. Hook 业务逻辑（绕过广告/校验）

### 通用模式：找"看完广告 → 领奖"的回调
```js
Java.perform(function() {
    // 1. 列出可疑类
    Java.enumerateClassLoaders({
        onMatch: function(loader) {
            Java.classFactory.loader = loader;
            Java.enumerateLoadedClasses({
                onMatch: function(name) {
                    if (name.toLowerCase().match(/reward|ad.*callback|videoad.*listener/)) {
                        console.log('Candidate:', name);
                    }
                },
                onComplete: function() {}
            });
        },
        onComplete: function() {}
    });
});
```

### 字节系常见类名
- `com.bytedance.sdk.openadsdk.TTRewardVideoAd` → 穿山甲激励视频
- `com.bytedance.sdk.openadsdk.TTAdNative$RewardVideoAdListener`
- 关键回调: `onRewardVerify(boolean success, int rewardAmount, ...)`

### Hook 强制 reward
```js
var Listener = Java.use('com.xxx.RewardVideoAdListener');
Listener.onRewardVerify.implementation = function(success) {
    return this.onRewardVerify.call(this, true, 1, 'coin', 0, '');
};
```

## 8. 已知坑（Android 13 + MIUI）

| 问题 | 现象 | 解决 |
|---|---|---|
| `adb root` 失败 | `cannot run as root in production builds` | 用 `su -c` 代替；root 管理器里给 Shell 授权 |
| `settings put` 拦截 | `WRITE_SECURE_SETTINGS` 拒绝 | `adb shell "su -c 'settings put ...'"` |
| `input tap` 拦截 | `INJECT_EVENTS` 拒绝（普通 adb shell） | **`adb shell "su -c 'input tap X Y'"` 可绕过！** |
| `adb push /data/local/tmp` fchown 失败 | 报错但实际拷贝成功 | 先 push 到 `/sdcard/` 再 `su cp` |
| `adb install` 失败 | `INSTALL_FAILED_USER_RESTRICTED` | 改用 `pm install -r -i com.android.vending` |
| frida 17 找不到导出 | `Module.findExportByName not a function` | API 变了：`Process.findModuleByName(...).findExportByName(...)` |
| frida 17 报 `--no-pause` 不识别 | 启动失败 | 直接 `-f <pkg>`，默认就是不暂停 |
| frida CLI 后台运行立即退出 | `Process terminated` | stdin EOF 触发 REPL 退；用 `( while true; do sleep 60; echo ""; done ) \| frida ...` 喂 stdin |
| frida Python `console.log` 不显示 | message handler 不接 | 改 `on_message` 加 `elif t == 'log': print(msg.get('payload'))` |
| `/system/etc/security/cacerts` 不可写 | 已被 Tricky Store 等 bind-mount | 先 `umount` 再 mount 自己的，或合并 |
| HTTP Toolkit fallback 不报新类 | 字节系走纯 native | 必须自己 hook `libttboringssl.so` |
| **字节 SIGTRAP 反 hook** | hook libsscronet/libttboringssl 的 SSL 函数后 ChromiumNet0 线程 SIGTRAP | **不要硬刚 native pinning**，改走 Java 层业务 hook |
| frida QuickJS 没有 `global` | `'global' is not defined` | 用 `globalThis._cbs` 防 NativeCallback GC |

## 9. 快速命令速查

```bash
# 看哪个 Activity 在前台
adb shell "dumpsys window displays | grep mCurrentFocus"

# UI dump（看可见文本）
adb shell "uiautomator dump /sdcard/ui.xml"
adb pull /sdcard/ui.xml .
grep -oE 'text="[^"]+"' ui.xml | sort -u

# 截图（pull 出来用图像查看器看）
adb shell "screencap -p /sdcard/s.png"
adb pull /sdcard/s.png .

# 一键启动 APP
adb shell "monkey -p <pkg> -c android.intent.category.LAUNCHER 1"

# 强杀 APP
adb shell "am force-stop <pkg>"

# 列出所有三方 APP
adb shell "pm list packages -3"

# 看某个 APP 的 PID
adb shell "su -c 'pgrep -f <pkg>'"

# 看 APP 加载的库
adb shell "su -c 'cat /proc/<PID>/maps' " | grep "\.so$" | sort -u

# 看实时 SSL 错误
adb shell "su -c 'logcat | grep -iE ssl\|trust\|cert'"

# frida 列进程
frida-ps -U
frida-ps -Ua  # 仅 APP（带名字）

# objection 一键 explore（交互式）
objection -g <pkg> explore
```

## 10. 实战案例：汽水音乐 com.luna.music v19.1.0

### 10.1 挑战点
- 字节系 native pinning（`libttboringssl.so` 380KB，`libsscronet.so` 6.1MB）
- Java 层 SSL pinning bypass 后 `is.snssdk.com` 通了，但 `api5.qishui.com` / `vod-luna.douyin.com` 仍 fail
- 32 个 dex，全 ProGuard 混淆
- 含 `mssdk.volces.com` = X-Argus 签名上报，必走字节四神签名

### 10.2 关键域名
- `api5.qishui.com` ← 主 API（**native pin**）
- `vod-luna.douyin.com` ← 音视频流
- `is.snssdk.com` ← 字节通用 SDK API（OkHttp pin，已绕过）
- `mssdk.volces.com` ← 火山 SDK / X-Argus
- `pangolin-sdk-toutiao.com` / `gromore.pangolin-sdk-toutiao.com` ← 穿山甲

### 10.3 实施进度
- ✅ 抓包链路打通（adb reverse + 系统证书 + frida）
- ✅ Java 层 pinning 已绕过（HTTP Toolkit 脚本，验证：is.snssdk.com 200 OK）
- ❌ **`libsscronet.so` native pinning 无法绕过 → APP SIGTRAP 崩溃**
  - 已尝试 hook `SSL_CTX_set_custom_verify` / `SSL_set_custom_verify` 替换 callback
  - 即便只 hook `libttboringssl.so`，因两库共享代码地址（如 `SSL_get_verify_result`、`X509_verify_cert` 同址），libsscronet 调用时也会触发，并在 `libsscronet+0x3d24cc` 处主动 `SIGTRAP TRAP_BRKPT`
  - 推测字节有**反 hook 检测**：检查 `SSL_CTX_set_custom_verify` callback 是否是预期的硬编码地址
- ✅ **改走 Java 层 hook 业务回调路线** — 已成功
  - hook 目标: `com.ss.android.excitingvideo.ExcitingVideoAd.startExcitingVideo(config, adEvent, listener)`
  - 第三个参数 listener 是 `RewardAdSdkService$showRewardVideoAd$1` (内部 C40131)
  - 不调原方法，直接调 `listener.onShow + onRewardComplete + onRewardReceived + onClose`
  - 客户端层完全成功（无任何错误）
- ❌ **服务端校验依赖穿山甲 server-to-server callback** — 客户端 hook 无效
  - APP 的"VIP 天数"是从服务器查的，服务器只信任穿山甲后端的 reward callback
  - 即使客户端伪造了所有回调，服务器侧账户的 VIP 天数不会增加
  - 这是穿山甲激励视频的标准架构：客户端 SDK 只是 UI，真实奖励由 server-to-server 同步

### 10.4 关键经验
- **不要硬刚字节 native pinning** —— 它会主动 anti-hook 让你崩
- **改走业务层 hook**：找业务流程关键调用而非 SDK 底层
- **MIUI 的 `input tap` 拦截 root 可破**：`adb shell "su -c 'input tap X Y'"` 工作正常，普通 `adb shell input tap` 失败
- **穿山甲激励视频 server-to-server**：客户端 hook 无法绕过，必须真实播放或自动化点击
- **小米 13 + MIUI 13 视频解码 bug**: 汽水 v19.1.0 启动 ExcitingVideoActivity 必崩 (libstagefright SIGSEGV)，这是 ROM 兼容性问题不是反检测

### 10.5 最终方案
由于服务端校验，唯一可行的路径是**自动化播放完整广告**：
1. uiautomator/adb shell tap 模拟点击「领时长」
2. 真实播放广告（让 APP 走正常路径，但因为 ROM bug 会崩）
3. 改用云手机 / 别的 Android 设备避开此 ROM bug
4. 或**改用旧版 APK** (找 v18.x 看是否兼容)

### 10.4 用户需求
> 看一次 15-30 秒视频广告 = 1 天会员，希望脚本化跳过手动点击

可行路径排序:
1. **frida hook** 穿山甲 `RewardVideoAdListener.onRewardVerify` 强制 success
2. 抓包还原 `/getVip` 等请求 + 用 unidbg 还原 X-Argus（高强度）
3. **uiautomator 自动化**点击（不是逆向，但兜底 100% 可用）

---

## 11. 工作目录推荐布局

```
<project>/
├── *.apk                         ← 目标 APK
├── *.so                          ← 拉出的 native 库
├── start-reverse-env.bat         ← 一键启动抓包+frida 环境
├── stop-reverse-env.bat          ← 一键关闭并清理代理
├── .mitmproxy/                   ← mitmproxy 工作目录
│   ├── mitmproxy-ca-cert.pem
│   └── <hash>.0                  ← 系统级证书安装格式
├── hooks/
│   ├── config.js                 ← HTTP Toolkit 配置（CERT_PEM + 代理）
│   ├── httptoolkit-unpin.js      ← Java 层 pinning bypass
│   ├── httptoolkit-fallback.js   ← 兜底 patcher
│   └── native-ssl-bypass.js      ← native 层 pinning bypass（自写）
└── tools/
    └── frida-server-*.xz
```

## 12. 关键参考

- HTTP Toolkit unpinning: <https://github.com/httptoolkit/frida-interception-and-unpinning>
- BoringSSL API doc: <https://commondatastorage.googleapis.com/chromium-boringssl-docs/ssl.h.html>
- frida 17 changelog（API 变更）: <https://frida.re/news/>
- 字节系签名总览: [bytedance-x-gorgon-x-argus-notes.md](./bytedance-x-gorgon-x-argus-notes.md)
- 风控总览 SKILL: [../../SKILL.md](../../SKILL.md)
