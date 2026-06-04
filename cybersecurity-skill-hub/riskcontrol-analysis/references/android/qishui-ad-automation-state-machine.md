# 汽水音乐 看广告领时长 自动化 - 完整状态机文档

> **更新**: 2026-05-10
> **APP 版本**: com.luna.music v19.1.0 (versionCode 100191030)
> **设备**: 小米 13 (1080×2400)
> **目标**: 自动化点击「看广告领免费听时长」

## 1. 业务规则

- 看 **2 个广告 = 升级 1 天免费听时长**（计数器从 3 减到 0 触发升级）
- 升级一次后计数器重置为 3
- 每天每个用户有上限（具体多少待测，估计 7 天）
- 广告播放约 30 秒，**前 ~25 秒不可关闭**（"X 秒后可领取奖励"），最后 ~5 秒后顶部 × 出现可关闭

## 2. 核心坐标参考

| 位置 | 坐标 | 说明 |
|---|---|---|
| 底栏「福利」 | (756, 2160) | 主页底栏第三个 tab |
| 福利页「领时长」 | (923, 886) | 主按钮 |
| 「免费听时长 X天」 | (886, 460) | 当前 VIP 天数显示 |
| 「再看 X 次」 | (336, 760) | 距离升级还差几次 |
| 广告页关闭 × | (~1000, 130) | 广告播完后顶部右侧 |
| 「领取奖励」按钮 | (540, 1316) | 中间弹窗 |
| 「再看 3 个提前领」 | (754, 1816) | 恭喜页右侧 |
| LunaRewardActivity 关闭 × | (919, 142) | 推销页右上 |
| 弹窗外的"恭喜获得第 X 天"覆盖 | (540, 1461) | 不可点（已领取标记）|

## 3. 状态机

```
[S0: APP 关闭]
    │ 启动 APP (monkey -p com.luna.music)
    ▼
[S1: MainActivity 主页（音乐播放）]
    特征：底栏 "发现/听抖音/音乐/福利/我的"
    │ tap 福利 (756, 2160)
    ▼
[S2: 福利中心页]
    特征：顶部 "市集/福利中心/音乐节"，"领时长" (923, 886)
    │ tap 领时长 (923, 886)
    ▼
[S3: ExcitingVideoActivity 广告播放中]
    特征：顶部 "广告 | 反馈 [Ns 倒计时]"
    │ 等待 N 秒
    ▼
[S4: 广告可关闭]
    特征：顶部右侧出现 "领取成功 ×" 或 "× 关闭"
    │ tap × (右上角约 1000, 130)
    ▼
   分支：
   ├─ [S5a: LunaRewardActivity 推销 SVIP 页]
   │       特征：「SVIP包月」「￥0.01 立即购买」
   │       │ keyevent BACK
   │       ▼
   ├─ [S5b: 中间「领取奖励」弹窗]
   │       特征：「领取奖励」按钮 (540, 1316)
   │       │ tap (540, 1316)
   │       ▼
   ▼
[S6: 福利页 + 「恭喜获得第 X 天」浮层]
    特征：「恭喜获得第 X 天免费时长畅听」+ 「已领取/再看3个提前领」
    │ keyevent BACK
    ▼
[S2 干净的福利页]
    可继续下一轮
```

## 4. 各状态 OCR 检测特征

### S1 主页（MainActivity）
关键词命中（任一即可）:
- 底栏: "发现"、"听抖音"、"福利"、"我的"
- 中间内容: 歌曲名、"标准/极高/音效"

### S2 福利中心
关键词:
- "福利中心" (310, 140)
- "免费听时长" (920, 388)
- "X天" 在 (886, 460)
- "已解锁X天再看Y次提前解锁下一天" (336, 760)
- "领时长" (923, 886) ⭐ 核心按钮

### S3 广告播放中
关键词:
- "广告" (~150, 130)
- "反馈" (~625, 130)
- "[N秒]" 倒计时 (~570, 130)
- "[N秒后可领取奖励]" (~830, 130)

### S4 广告可关闭
关键词:
- "领取成功" (在顶部 y < 200)
- "×" (y < 200)

### S5a LunaRewardActivity 推销页
关键词:
- "SVIP包月"
- "立即购买"
- "0.01" "￥0.01"
- "汽水音乐SVIP7天试用"

### S5b 中间「领取奖励」弹窗
关键词:
- "领取奖励"
- "再看 X 个视频提前得"
- "坚持退出"

### S6 恭喜浮层
关键词:
- "恭喜获得第 X 天"
- "已领取"
- "再看3个提前领"

## 5. 异常处理

| 异常 | 检测 | 应对 |
|---|---|---|
| APP 崩溃 | 焦点不在 com.luna.music | 重新启动 APP |
| 网络异常 | OCR 出现 "网络异常" "请检查网络" | 等几秒重试 |
| 广告播完没出 × | 90 秒还没出现可关闭 | 强制返回，重新开始 |
| 误点到游戏下载页 | 焦点切到非 luna 包 | 强制返回 |
| 已达每日上限 | 「领时长」按钮变成「明日再来」之类 | 退出 |
| 推销页死循环 | LunaRewardActivity 持续 5 次以上 | 强制 force-stop + 重启 |

## 6. 操作时序常量

```python
WAIT = {
    'app_main': 30,          # 启动到主页
    'fuli_page': 15,         # 进福利页
    'ad_started': 25,        # 广告启动
    'ad_finished': 90,       # 广告播完（最长）
    'congrats_appear': 15,   # 恭喜页出现
    'screen_change': 3,      # 切页面后渲染稳定时间
}

POLL = 1.5  # OCR 轮询间隔
```

## 7. ADB 操作命令

```bash
# tap （MIUI 下需要 root）
adb shell "su -c 'input tap X Y'"

# back 键（root 也行）
adb shell "su -c 'input keyevent KEYCODE_BACK'"

# 启动 APP（不杀已有进程）
adb shell "monkey -p com.luna.music -c android.intent.category.LAUNCHER 1"

# 强杀 APP
adb shell "am force-stop com.luna.music"

# 截图
adb shell "screencap -p /sdcard/s.png"
adb pull /sdcard/s.png

# 当前焦点
adb shell "dumpsys window displays | grep mCurrentFocus"
```

## 9. PC 端实验关键发现（用于浮窗 APP 设计）

### 9.1 业务规则细节
- 看 **2 个广告 = 升级 1 天免费听时长**（但实测有时是 1 个广告，不稳定）
- 升级一次后「再看 X 次」从 0 重置为 3
- 中途如果点了「领取奖励」也可能算"看完一次"

### 9.2 重要状态
| 状态 | 焦点 Activity | 触发方式 | 处理 |
|---|---|---|---|
| 福利干净页 | MainActivity | tap 底栏「福利」 | 主操作页 |
| 福利+恭喜浮层 | MainActivity | 看完一个广告后 | 按 BACK 退到干净页 |
| 广告播放中 | ExcitingVideoActivity | 点「立即解锁第N天畅听」 | 等顶部 × 出现 |
| 广告 reward_dialog | ExcitingVideoActivity | 用户尝试关闭广告 | 点「坚持退出」回到广告 |
| 广告完成 | ExcitingVideoActivity | 倒计时结束 | 点顶部 × 退出 |
| SVIP 推销 | LunaRewardActivity | 广告完成后 | 按 BACK 退出 |
| 直播间广告 | LunaDefaultLivePlayerActivity | 部分广告是直播 | 等够时长后退出 |

### 9.3 「领时长」按钮说法变化
随着 VIP 进度变化，主按钮文字会变：
- 「领时长」（早期）
- 「立即解锁第 N 天畅听」（已领多次后）  ← 实测这个按钮才能稳定启动广告
- 「再看 N 个提前领」（恭喜页右侧）

⚠️ **绝不能依赖固定坐标**——按钮位置会随版本/状态变化。**必须用控件树+文本匹配**。

### 9.4 推荐控件识别策略（浮窗 APP 用）
用 AccessibilityService 拿到 AccessibilityNodeInfo 树：
```kotlin
fun findClickableByText(root: AccessibilityNodeInfo, keyword: String): AccessibilityNodeInfo? {
    if (root.text?.contains(keyword) == true && root.isClickable) return root
    if (root.contentDescription?.contains(keyword) == true && root.isClickable) return root
    for (i in 0 until root.childCount) {
        val r = findClickableByText(root.getChild(i) ?: continue, keyword)
        if (r != null) return r
    }
    return null
}
```

但 luna 是 Compose 渲染，AccessibilityNode 可能没文字。回退到 OCR：
```kotlin
// 用 MediaProjection 截屏 → ML Kit / PaddleOCR-Android 识别 → 找按钮
fun findButtonByOcr(screenshot: Bitmap, keyword: String): Rect? { ... }
```

### 9.5 关键控件搜索关键词列表（重要！按优先级匹配）

#### 启动广告
| 优先级 | 文本 | 备选 desc | 出现位置 |
|---|---|---|---|
| 1 | "立即解锁" | (无) | 福利页底部 |
| 2 | "领时长" | (无) | 福利页右侧 |
| 3 | "再看 N 个提前领" | (无) | 恭喜浮层右侧 |

#### 关闭广告页（任何形式）
| 优先级 | 描述 | 文本 | 出现页面 |
|---|---|---|---|
| 1 | desc="关闭" | "×" | 直播广告右上 |
| 2 | (无) | "退出不看了" | 直播二次确认 |
| 3 | (无) | "坚持退出" | 视频广告中途确认（注意：选这个 = 不领奖！）|
| 4 | (无) | "领取成功" + "×" | 视频广告完成时顶部 |

#### 关闭推销页 / 恭喜浮层
- 直接按 BACK 键

#### 中途处理
- 出现 "领取奖励" + "坚持退出" 弹窗 → **不要点!** 这是用户中途想退的提示，会导致广告中断
- 应该等待广告自然完成

### 9.6 控件树检测代码模板（Kotlin / AccessibilityService）

```kotlin
class QishuiAccessibilityService : AccessibilityService() {

    override fun onAccessibilityEvent(event: AccessibilityEvent?) {
        // 监听 com.luna.music 的窗口变化
        if (event?.packageName != "com.luna.music") return
        val root = rootInActiveWindow ?: return

        // 状态识别
        val state = detectState(root)
        Log.d("QSAuto", "state=$state")

        when (state) {
            "fuli_clean" -> findAndClickStartAd(root)
            "ad_finished" -> findAndClickClose(root)
            "live_ad" -> findAndClickLiveClose(root)
            "live_confirm" -> findAndClickLiveExit(root)
            "svip_promo" -> performGlobalAction(GLOBAL_ACTION_BACK)
            "fuli_with_congrats" -> performGlobalAction(GLOBAL_ACTION_BACK)
            else -> {}
        }
    }

    private fun detectState(root: AccessibilityNodeInfo): String {
        // 优先按文本特征
        if (hasText(root, "退出不看了")) return "live_confirm"
        if (hasText(root, "立即购买") && hasText(root, "SVIP")) return "svip_promo"
        if (hasText(root, "领取奖励") && hasText(root, "坚持退出")) return "ad_reward_dialog"
        if (hasText(root, "领取成功")) return "ad_finished"
        if (hasText(root, "秒后可领取")) return "ad_playing"
        if (hasText(root, "恭喜获得")) return "fuli_with_congrats"
        if (hasText(root, "立即解锁") || hasText(root, "领时长")) return "fuli_clean"
        if (hasDesc(root, "关闭") && hasText(root, "本场点赞")) return "live_ad"
        return "unknown"
    }

    private fun findAndClickStartAd(root: AccessibilityNodeInfo) {
        for (kw in listOf("立即解锁", "领时长", "再看")) {
            val nodes = root.findAccessibilityNodeInfosByText(kw)
            for (n in nodes) {
                if (n.isClickable) {
                    n.performAction(AccessibilityNodeInfo.ACTION_CLICK)
                    return
                }
                // 找父节点 clickable
                var p = n.parent
                while (p != null) {
                    if (p.isClickable) {
                        p.performAction(AccessibilityNodeInfo.ACTION_CLICK)
                        return
                    }
                    p = p.parent
                }
            }
        }
    }

    private fun findAndClickClose(root: AccessibilityNodeInfo) {
        // 按 desc "关闭" 找
        // ...
    }

    private fun hasText(root: AccessibilityNodeInfo, text: String): Boolean {
        return root.findAccessibilityNodeInfosByText(text).isNotEmpty()
    }

    private fun hasDesc(root: AccessibilityNodeInfo, desc: String): Boolean {
        return walkTree(root) { it.contentDescription?.contains(desc) == true }
    }

    private fun walkTree(node: AccessibilityNodeInfo, pred: (AccessibilityNodeInfo) -> Boolean): Boolean {
        if (pred(node)) return true
        for (i in 0 until node.childCount) {
            val c = node.getChild(i) ?: continue
            if (walkTree(c, pred)) return true
        }
        return false
    }
}
```

### 9.7 浮窗 + 服务架构

```
┌── MainActivity (启动 + 引导授权)
│   └── 1. 引导用户去"无障碍"开启服务
│       2. 引导用户开启"显示在其它应用上层"权限
│       3. 启动浮窗 Service
│
├── FloatingService (前台 Service)
│   └── 用 WindowManager.addView 显示浮窗按钮
│       浮窗内容：[运行 / 停止 / 关闭]
│       状态显示：当前轮次、已领天数
│
├── QishuiAccessibilityService (无障碍服务)
│   └── 监听 com.luna.music 的事件
│       状态机执行
│       从浮窗 Service 接收 启动/停止 命令
│
└── AndroidManifest.xml 必须声明
    - android.permission.SYSTEM_ALERT_WINDOW
    - android.permission.FOREGROUND_SERVICE
    - <service> with BIND_ACCESSIBILITY_SERVICE permission
```
