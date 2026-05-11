# 阿里盾滑块（Aliyun Captcha SLIDING）— SDK 反向利用法

> **2026-05-11 实战发现，来源：NoteGPT 注册流程逆向**。
>
> 旧思路：模拟人类轨迹拖动滑块（mousedown→连续 mousemove→mouseup），
> 配合 ease-out 曲线 + jitter + overshoot。**实测无效**——playwright
> CDP-driven `page.mouse.down/move/up` 在 NoteGPT 这个阿里盾配置下
> 完全不被识别（slidedWidth 始终 0、captchaVerifyParam 始终空）。
> 推断阿里盾 3.25.x 版本内部依赖某些**只有真实 OS 鼠标流**才有的
> 信号（带宽时间戳、压感、加速度归一化数据）。
>
> 新思路：**直接利用 SDK 暴露的内部对象 + 全局 API**，跳过 UI 交互层。

## 阿里盾的指纹（DOM/JS 全局变量）

DOM 类名/ID：
- `.aliyun-captcha` （wrapper）
- `#aliyunCaptcha-sliding-wrapper`
- `#aliyunCaptcha-sliding-body`
- `#aliyunCaptcha-sliding-slider`
- `#aliyunCaptcha-sliding-left`（已滑动条）
- `#aliyunCaptcha-sliding-text`（提示文字）
- `#aliyunCaptcha-sliding-failTip`（失败提示）
- `#aliyunCaptcha-sliding-errorCode`

全局 window 变量：

| 变量 | 含义 |
|---|---|
| `window.captchaInstance` | **核心** SDK 实例 — 一切操作的入口 |
| `window.AliyunCaptcha` | 工厂函数 |
| `window.AliyunCaptchaConfig` | 初始配置 `{region, prefix}` |
| `window.__ALIYUN_CAPTCHA_UTILS` | 工具 |
| `window.__ALIYUN_CRYPT` | 加密层 |
| `window.__ALIYUN_CAPTCHA_TEXTS` | 文案资源 |
| `window._aliyun_device_ifr` | 设备指纹（iframe）|
| `window._aliyun_device_cvs` | 设备指纹（canvas）|
| `window.AliyunCaptcha_clientX` | 客户端坐标流缓存 |
| `window.initAliyunCaptcha` | 初始化入口 |
| `window.__CloseAliyunCaptcha` | 关闭入口 |
| `window.CAPTCHA_LANG` | 语言 |

**5 秒识别法**：`Object.keys(window).filter(k => /aliyun|captcha/i.test(k))` 命中 ≥ 5 个 → 就是阿里盾。

## captchaInstance 的方法清单

```
captchaVerifyCallback   - 业务侧 verify 回调（成功时被调用，参数是 certifyId）
onBizResultCallback     - 业务结果回调
CaptchaConstructor      - 内部构造器
startPOWCalculation     - 启动 Proof-of-Work 计算
init                    - 初始化
bindEvents              - 绑定事件
show / hide             - 显示/隐藏
loading                 - 加载状态
onBizSuccess            - 业务成功 hook（**关键**，token 在这里组装）
onBizFail               - 业务失败 hook
initPopup/initEmbed/initFloat  - 3 种模式初始化
destroyCaptcha          - 销毁
refresh                 - 刷新
onCloseClick            - 关闭按钮点击
startTracelessVerification  - "无痕验证"模式 — 不需 UI 交互
```

## onBizSuccess 内部逻辑（反编译）

```js
function(t) {
  if (t) {
    var n;
    n = "1.0" === this.config.verifyType
      ? t
      : window.btoa(JSON.stringify({
          certifyId: t,
          sceneId: this.config.SceneId,
          isSign: !0,
          securityToken: this.config.securityToken
        }));
    this.success && this.success(n);
  } else {
    this.onBizResultCallback && this.onBizResultCallback(!0);
  }
}
```

**结论**：成功的 `captchaVerifyParam` token 是：
- verifyType 1.0：直接 `certifyId`
- verifyType **2.0**（NoteGPT 当前）：`base64(JSON.stringify({certifyId, sceneId, isSign:true, securityToken}))`

`certifyId` 是阿里盾后端发的；`sceneId` / `securityToken` 在 `inst.config` 里能直接读。

## 反向利用策略（按优先级）

### 策略 A — 拦截 success callback（**首选**）

不破滑块本身，**hook captchaInstance.success**：让真实用户在浏览器手动过一次滑块后，把得到的 token 持久化。后续注册请求都用同一个 token？❌ 行不通：`certifyId` 是 one-shot，过期 60–120 秒。

### 策略 B — 调用内部 API 触发 verify

```js
// 在已经初始化的 captchaInstance 上
inst.startTracelessVerification()   // 试探"无痕" — 实测 NoteGPT 返回 {} 但没触发 callback
inst.captcha.refresh()              // 刷新滑块状态
```

`startTracelessVerification` 在某些 SceneId 上能工作（阿里盾"无痕认证"模式），NoteGPT 实测不工作（SceneId weh6qjag 仍要交互）。

### 策略 C — 模拟人类拖动（**playwright CDP 实测失败**）

旧思路。在某些更老版本阿里盾上可能 work，在 NoteGPT 部署的 3.25.1 版本失败。**不推荐**作为唯一手段。

### 策略 D — 真实浏览器（Selenium + undetected-chromedriver / camoufox）

不用 playwright（CDP 可被检测到），用 **undetected-chromedriver** 或 **camoufox**：它们提供更接近真实 OS 的鼠标事件流，配合滑动轨迹算法（轨迹来自录制的真人样本）能过。

### 策略 E — 反向 SDK，**直接对接阿里盾后端 API**

阿里盾后端 URL：`https://<prefix>.captcha-open.aliyuncs.com/`。SDK 调用顺序：
1. POST `/init` 拿 `CertifyId` / 滑块图片（如果是图片型）
2. 用户滑动 → SDK 收集轨迹 → SHA + RSA 加密 → POST `/verify`
3. 服务端通过 → 返回签名 → 客户端 base64(JSON{...}) → 业务侧 token

**完整逆向**：把 `__ALIYUN_CRYPT.encrypt` 和 SDK 的 dynamic JS（`/captcha-frontend/dynamicJS/3.25.1/sg.016.*.js`）做静态分析，复现加密 + 直接 POST `/verify`。**最稳但工作量大**（1-2 周）。

## 业务侧绑定关系

NoteGPT 的 form 字段：
```html
<input type="hidden" name="captchaVerifyParam" value="">
<button id="beforeSubmit" class="ibtn">Submit</button>
```

`captchaInstance.$button == #beforeSubmit`：

```js
// initEmbed 里看到：
this.$button.onclick = K(n.bind(this), 1e3);
// n 是 verify 流程，K 是 debounce 1000ms
```

**关键**：点 Submit 按钮才触发 verify。不是拖完滑块自动 verify。所以注册流程其实是：

1. 滑块拖到位 → SDK 把 verify 缓存进内部 state（但 verify input 还是空）
2. 点 `#beforeSubmit` → SDK 触发 verify → 成功后填 `captchaVerifyParam` 隐藏字段 → 同时通过 onclick 走 form.submit()

实际尝试时如果**SDK 拖动模拟失败**，点 Submit 也只会显示 "Please slide to verify"，不会发请求。

## 5 项硬性验证 step 1 的优化（应加进 `5-minute-triage.md`）

当探测到阿里盾时（DOM 含 `.aliyun-captcha` 或 window 含 `captchaInstance`）：

```javascript
{
  // ...原有 captcha 检测...
  aliyunSliding: !!window.captchaInstance && window.captchaInstance.config?.CaptchaType === 'SLIDING',
  aliyunVerifyType: window.captchaInstance?.config?.verifyType,  // "1.0" / "2.0"
  aliyunSceneId: window.captchaInstance?.config?.SceneId,
  aliyunPrefix: window.captchaInstance?.config?.prefix,
}
```

- verifyType 1.0 → token 短，策略 A 可能 work
- verifyType 2.0 → token base64 包了 sceneId/securityToken，必须新鲜的 certifyId
- 任何 verifyType → 策略 D（undetected-chromedriver）通常能过；playwright 默认不行
- 看 `_aliyun_device_*` 检测设备指纹是否被采集到，采集到说明该浏览器没被它信任 → 即使滑过去也可能被风控判失败

## 实测对照表

| 操作 | NoteGPT 上的结果 |
|---|---|
| DOM dispatchEvent 合成 mousedown/move/up | ❌ slidedWidth=0，未识别 |
| playwright `page.mouse.down/move/up` 带 ease-out + jitter | ❌ slidedWidth=0，未识别 |
| playwright `dragTo` (HTML5 drag) | ❌ 不是 mouse 事件 |
| `inst.startTracelessVerification()` | 返回 `{}` 但 callback 没被调用 |
| `inst.show()` / `inst.refresh()` | 改 UI 状态，不产生 token |
| 直接修改 `<input name="captchaVerifyParam">` 的 value | ❌ 后端会校验签名 |

**结论：NoteGPT 当前部署的阿里盾 3.25.1 + SceneId weh6qjag + verifyType 2.0，是 playwright 单纯模拟拖动很难过的版本**。需要走策略 D 或 E。

## 取舍建议

对单个站点（如 NoteGPT 反代）：
1. **试一次 undetected-chromedriver** + 真实轨迹库 — 1-2 小时 setup
2. ~~不过就接 **2captcha / capsolver / yescaptcha** 这类付费打码服务（阿里盾基础滑块 $1-2 / 1000 次） — 30 分钟接入~~
   - **2026-05-11 实测更正：CapSolver 不支持阿里盾**。其 createTask 接受的 type 列表只有 reCAPTCHA v2/v3、GeeTest、MTCaptcha、DataDome、AWS WAF、Cloudflare Turnstile / Challenge、ImageToText 共 8 类。试过 `AliyunCaptchaTaskProxyLess` / `AliyunSlidingTaskProxyLess` / `AliyunSliderCaptchaTask` 等多种命名全返回 `ERROR_TYPE_NOT_SUPPORTED`。
   - 据用户社区报告，**支持阿里盾的服务**：2captcha（要确认）、yescaptcha、nocaptcha.io（**国产**，对阿里盾支持最好）。
3. 如果项目预算允许，付费打码 ROI 远高于自破 — **但要先确认所选服务支持该 captcha 类型**

对多个站点：
- 写一个统一的 `captcha_solver_aliyun_sliding(page) -> str` 接口，内部用付费服务作 backend，再叠加 undetected-chromedriver 兜底
- 接入费可分摊到所有需要破阿里盾的站点

## CapSolver API 支持类型清单（2026-05-11 实测）

| Type | 支持 |
|---|---|
| reCAPTCHA v2 / v3 | ✅ |
| Cloudflare Turnstile | ✅ |
| Cloudflare Challenge | ✅ |
| AWS WAF | ✅ |
| DataDome | ✅ |
| GeeTest | ✅ |
| MTCaptcha | ✅ |
| ImageToText (OCR) | ✅ |
| **Aliyun Sliding** | ❌ **不支持** |
| hCaptcha | ✅（旧版有支持） |
| FunCaptcha | ✅（旧版有支持） |

> 选服务前先用免费 `getBalance` 调用看 key 有效；然后用 `createTask` 试一次目标类型名，看返回 `ERROR_TYPE_NOT_SUPPORTED` 还是真正排队 — 错误请求 capsolver 不扣费，是免费试探。
