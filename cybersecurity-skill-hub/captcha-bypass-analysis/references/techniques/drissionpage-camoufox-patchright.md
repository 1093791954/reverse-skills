# DrissionPage / camoufox / patchright 三大反检测自动化工具

> R5 深化：把这三个在 R3/R4 中反复被引用、但**未单独成笔记**的工具集中归档。
> 三者都解决"playwright/selenium 反检测不够"的问题，但走的路线截然不同。

## 1. 总览对比

| 维度 | DrissionPage | camoufox | patchright |
|------|-------------|---------|-----------|
| 语言 | Python | Python（包装 Firefox 二进制） | Python / Node.js |
| 底层 | requests + DevTools 双模 | 修改版 Firefox | 修改版 Playwright |
| 主要绕的 | webdriver / navigator.webdriver | Canvas/WebGL/字体/AudioContext 全套 | CDP 暴露面（Runtime.enable / executionContextCreated） |
| 是否需要专属浏览器 | ❌（用本地 Chrome） | ✅（自带 firefox 二进制） | ❌（patch 标准 chromium） |
| CSDN 命中量 | 1817 篇 | 8 篇（中文圈较少） | 51 篇 |
| 适用场景 | 中文网站抓取/小型反爬 | 高强度指纹检测（CreepJS / FpJS Pro） | Cloudflare/DataDome 这类 CDP 检测站 |

## 2. DrissionPage（中文圈最热）

### 2.1 设计思想
- 在同一个会话里，**同时维护一个 requests 会话和一个 CDP 浏览器**，根据需要切换：
  - 需要执行 JS / 看 DOM → 走 ChromiumPage
  - 只取数据 / 不需要渲染 → 退化为 SessionPage（直接 requests）
- 这种"切换"使得"先用浏览器拿到 cookie/token，再用 requests 高速跑接口"成为一行代码即可。

### 2.2 关键反检测特性
- 默认启动参数已包含 `--disable-blink-features=AutomationControlled`
- 自动注入"删除 webdriver"的脚本（页面级 stealth）
- 支持复用本机已登录的 Chrome 用户数据目录（绕过登录验证码）

### 2.3 与本技能的联动
- 适合先用 DrissionPage 启动一个"已经过滑块/极验"的浏览器，把 cookie 拷给 curl_cffi（参考 `techniques/replay-token.md`）
- 缺点：CDP 暴露面没有处理，遇到 Cloudflare Turnstile / DataDome WASM 检测仍会失败

### 2.4 已存档 CSDN articleid
- 159536265（DrissionPage + 字符滑块破 163 邮箱）
- 158218118（请求头实战、不可见动态验证）
- 148453143（绕过请求头 + 风控）
- 145017849（实战商品爬）
- 157818810（结合 Python 模拟点击 + 高级反爬）
- 145662563（爬某搜索）
- 140689739（Linux 服务器自动化）
- 98576760（动态请求 + 反爬）

## 3. camoufox（Firefox 反检测分支）

### 3.1 设计思想
- 不依赖 JS 注入，而是**修改 Firefox 二进制**：在 `nsCanvasRenderingContext2D.cpp` 之类的源码层注入指纹噪声 + 用户可控的"假指纹模板"
- 完全绕过 navigator.* 检测（因为整个底层 API 都被改过）
- 启动参数走 `LaunchOptions(humanize=True)` 自动给鼠标轨迹加噪声

### 3.2 关键反检测特性
- Canvas / WebGL / Font / AudioContext 全部走"模板 + 持久种子"模式（per-profile 一致性）
- WebRTC IP leak 防护：可绑定到指定 SOCKS5 出口，内核级伪装 ICE 候选
- BrowserForge 指纹库自动同步（每月数千个真实指纹模板）

### 3.3 与本技能的联动
- **首选**：CreepJS / BrowserGap / FpJS Pro 等"测得出 Chromium 修改痕迹"的高强度场景
- 与 `techniques/fingerprint-bypass.md`（Chromium Canvas 噪声化）形成"双保险"：用户可以选 Chrome 系（patchright + 噪声）或 Firefox 系（camoufox）
- 与 `vendors/datadome.md` / `vendors/akamai-bmp.md` 配合好：这些厂商对 Firefox UA 的检测分支较弱

### 3.4 已存档 CSDN articleid
- 160842016（基于 Firefox 和 Selenium 的 Camoufox 反检测）
- 156664555（Camoufox 收集服务安全指南）
- 154632815（Camoufox 项目构思）
- 160343844（Scrapling 框架使用 — 与 camoufox 同生态）

## 4. patchright（Playwright 修改版）

### 4.1 设计思想
- 不动浏览器二进制，但**修改 Playwright 客户端代码**：
  - 移除 `Runtime.enable` 的全局开启（CDP 检测点 #1）
  - 移除 `Page.addScriptToEvaluateOnNewDocument` 的特征字符串
  - 重写 `executionContextCreated` 事件处理，不让网页发现"新执行上下文"
- 仍然用标准 chromium，**对网络层无侵入** → JA3 / TLS 与原生一致

### 4.2 关键反检测特性
- 修复了 puppeteer-extra-stealth 已被检测的所有特征（如 navigator.plugins 长度、permissions.query 模式）
- 自动同步 Playwright 上游版本（patch 是脚本化的，不会过时）
- Node.js 和 Python 双语言版本

### 4.3 与本技能的联动
- 首选 Cloudflare Turnstile / DataDome（这两家重度依赖 CDP 检测）
- 与 `techniques/browser-stealth.md` 直接互补：那里讲 puppeteer-extra-stealth 已被检测，这里给替代
- 不解决 Canvas/WebGL 噪声 → 需要叠加 fingerprint-bypass 笔记里的 Chromium 改 SkiaCanvas 方案

### 4.4 已存档 CSDN articleid
- 147006976（patchright 使用教程）
- 147006873（项目使用教程）
- 147007106（项目安装与发行指南）
- 147472718（开源项目实践教程 Node.js）
- 147472720（patchright-nodejs 安装与教程）
- 142010584（自动化 patchright 安全指南）
- 151497592（与 Browser-Use 集成）
- 147521158（基于 Browser-Use + patchright 加速）

## 5. 三选一决策树

```
站点重检 Canvas/WebGL/AudioContext 指纹一致性？
├─ 是 → camoufox（不可替代）
└─ 否
   ├─ 站点重检 CDP 暴露面（Runtime.enable, executionContextCreated）？
   │  ├─ 是 → patchright
   │  └─ 否 → DrissionPage（中文资料最丰富，开发最快）
   └─ 需要"先浏览器后 requests"双模高速？
      └─ DrissionPage（其它两家无此能力）
```

## 6. 与本技能其他笔记的链接

- `techniques/browser-stealth.md`：补充 puppeteer/selenium-stealth 通用方案
- `techniques/fingerprint-bypass.md`：camoufox 走的"内核改 Canvas"思路在那里有 Chromium 版本的对应实现
- `vendors/cloudflare-turnstile.md`：patchright 推荐绑定
- `vendors/datadome.md`：patchright + camoufox 二选一推荐
