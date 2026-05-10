# 汽水助手 浮窗 APP - 当前进度与下次继续指南

> **更新**: 2026-05-11 凌晨
> **APK 位置**: `D:\tmp\hacker\Android\QishuiHelper\app\build\outputs\apk\debug\app-debug.apk`
> **包名**: `com.qishuihelper`
> **手机已装**: ✅

## 1. 已经完成

### 1.1 项目结构（D:\tmp\hacker\Android\QishuiHelper\）
- `settings.gradle.kts` + `build.gradle.kts` (root + app)
- `gradle.properties` 配置了代理 `127.0.0.1:7897`
- `app/src/main/`
  - `AndroidManifest.xml` - 声明 SYSTEM_ALERT_WINDOW、FOREGROUND_SERVICE、AccessibilityService
  - `java/com/qishuihelper/`
    - `MainActivity.kt` - 引导用户授权
    - `FloatingService.kt` - 前台 Service + 悬浮窗（▶/⏸/×）
    - `QishuiAccessibilityService.kt` - 状态机 + 自动点击
  - `res/` - layout/drawable/values

### 1.2 核心机制
- **悬浮窗**: WindowManager + TYPE_APPLICATION_OVERLAY，可拖动
- **无障碍**: 监听 com.luna.music 的 typeWindowStateChanged|typeWindowContentChanged
- **手势点击**: 用 GestureDescription 派发，含 3 秒防抖
- **状态机**: 11 种状态识别（fuli_clean、ad_playing、ad_finished、svip_promo、live_ad...）
- **跨进程通信**: FloatingService → AccessibilityService 用 broadcast

### 1.3 编译/装机命令
```bash
cd D:/tmp/hacker/Android/QishuiHelper
gradle assembleDebug --no-daemon

adb push app/build/outputs/apk/debug/app-debug.apk /sdcard/q.apk
adb shell "su -c 'cp /sdcard/q.apk /data/local/tmp/q.apk && pm install -r /data/local/tmp/q.apk'"

# 自动授权（需 root）
adb shell "su -c 'appops set com.qishuihelper SYSTEM_ALERT_WINDOW allow'"
adb shell "su -c 'settings put secure enabled_accessibility_services com.qishuihelper/com.qishuihelper.QishuiAccessibilityService'"
adb shell "su -c 'settings put secure accessibility_enabled 1'"

# 但是 MIUI 还会要求用户在系统设置里手动 *再点开关* 一次（因 MIUI 安全限制）
# 然后会弹"危险"提示，点确定授权

# 启浮窗
adb shell "su -c 'am start-service -n com.qishuihelper/.FloatingService'"

# 触发 START（模拟点击 ▶）
adb shell "su -c 'am broadcast --user 0 -a com.qishuihelper.ACTION_FROM_FLOAT_START -p com.qishuihelper'"
```

## 2. 没完成的核心问题

### 2.1 luna Compose UI 不暴露文字
luna 福利页的「领时长」「免费听时长」等关键按钮**没暴露 text/contentDescription** 给 AccessibilityService。控件树里只有底栏 5 个 tab 是 TextView，主内容区都是没有 text 的 ViewGroup（仅部分有 desc）。

**已尝试**:
- `findAccessibilityNodeInfosByText(kw)` - 找不到
- 自己 walk 全树搜 text+desc - 也找不到「领时长」
- 兜底 GestureDescription 点固定坐标 (923, 886) - 100% 失败（不知为何）

**下次思路**:
- 验证 GestureDescription 能否真的点中 luna 的 Compose 按钮 — 用更长 duration（200ms+）
- 或者扩大手势"按下-松开"，用 ACTION_DOWN/UP 模拟更真实的 Touch
- **替代方案**：直接发 InputEvent，但需要 INJECT_EVENTS 权限
- **最稳的替代方案**：在 APP 里跑 root shell 调 `input tap` —— 但这违背了"用户级 APP"的初衷

### 2.2 状态识别不准
在 `ExcitingVideoActivity` 里：
- `root.packageName == "com.luna.music"` ✓
- 但 `windows().firstOrNull{it.isActive}.title` 仍是「汽水音乐」
- root 控件树几乎为空（广告页主要是 SurfaceView 渲染）

**下次思路**:
- 用 AccessibilityWindowInfo 的 `getRoot()` 看每个 window 的真实内容
- 监听 TYPE_WINDOW_STATE_CHANGED 时获取 `event.className` —— 可能是 ExcitingVideoActivity 的全名
- 或者用 `event.getSource()` 拿真实窗口

### 2.3 已验证有效的部分
✅ 有一次手动测试：触发 START → luna 在福利页（自然识别为 fuli_clean）→ ExcitingVideoActivity 启动了广告 → 30 秒后顶部出现「领取成功 ×」→ VIP 进度从 3 推进到 2 次。

但**广告完成后的"自动关闭 + 回福利 + 循环"** 没跑通。

## 3. 下次启动 checklist

```bash
# 1. 检查环境
adb devices                                        # c256d8fa
adb shell "su -c id"                              # uid=0
adb shell "settings get secure enabled_accessibility_services"  # 应有 qishuihelper

# 2. 项目位置
cd D:/tmp/hacker/Android/QishuiHelper
gradle --version                                   # 8.14.3
echo $ANDROID_HOME                                 # C:\Users\GOD\AppData\Local\Android\Sdk

# 3. 一键编译装机
gradle assembleDebug --no-daemon && \
adb push app/build/outputs/apk/debug/app-debug.apk /sdcard/q.apk && \
adb shell "su -c 'cp /sdcard/q.apk /data/local/tmp/q.apk && pm install -r /data/local/tmp/q.apk && rm /data/local/tmp/q.apk /sdcard/q.apk'"

# 4. 看 logcat 调试
adb shell "logcat -c"
# ... 触发操作 ...
adb shell "logcat -d -t 500 | grep QSAuto"
```

## 4. 关键代码位置

需要修改的文件（按优先级）：
1. `app/src/main/java/com/qishuihelper/QishuiAccessibilityService.kt`
   - `detectState()` - 状态识别逻辑
   - `clickStartAd()` - 点击启动广告
   - `gestureClick()` - 手势点击实现
   - `triggerCheck()` - 主调度

## 5. 备选方案（如果浮窗 APP 不工作）

回到 PC 端 Python 脚本：`D:/tmp/hacker/Android/auto_qishui_ad.py`
- 用 OCR 识别每一步
- adb shell + root + input tap
- 已验证至少有 1 轮成功

## 6. 用户需求（不要忘）

> 看广告获取时长。能够一直循环看广告。

最终方案不必拘泥于浮窗 APP，**能稳定循环 = 成功**。
