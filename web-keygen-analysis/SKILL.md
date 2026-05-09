---
name: web-keygen-analysis
description: 用于在合法授权前提下分析网页站点的注册机、加密参数还原、登录注册风控、设备指纹与人机验证等 JS 逆向工作流。涵盖 sign/token/x-bogus/x-s/x-t/x-common/x-gorgon/h5st/_abck/sensor_data/akamai/瑞数/极验/网易易盾/数美/防水墙/Vaptcha 等参数还原；webpack 解包、AST 解混淆、Babel pass、控制流平坦化、jsvmp 还原、多态 VM、补环境（缺啥补啥）、纯算还原、RC4/SHA256/MD5 魔改识别；浏览器指纹（Canvas/WebGL/AudioContext/Font/UserAgent/TLS）、轨迹风控、滑块 OCR/模板匹配、PoW 暴力搜索、JSONP 回调；以及邮箱注册、Apple 账号注册、批量注册、接码平台等场景的防御性研究。当任务涉及 JS 逆向、加密参数还原、签名算法、x-bogus/x-s/x-t/x-common/x-gorgon/h5st/sensor_data/_abck、akamai/瑞数/极验/防水墙/网易易盾/数美/Vaptcha、设备指纹、Canvas 指纹、TLS 指纹、滑块验证码、jsvmp、TENCENT_CHAOS_VM、AST 还原、Babel pass、补环境、纯算实现、抖音/TikTok/小红书/京东/拼多多/美团/网易云/boss直聘 等站点的 web 接口逆向、邮箱/Apple/手机号注册流程，或一般性"授权 web 站点的注册机/加密参数还原"时使用。
---

# Web 站点注册机与加密参数还原（web-keygen-analysis）

把已收集的（看雪 + 后续会补充的其他来源）web 端 JS 逆向资料，整理为一套可复用的分析工作流。目标是在合法授权前提下，把"网页风控黑盒"拆成可解释的几层：抓包侦察 → AST 解混淆 → 参数定位 → 算法识别 → 补环境/纯算 → 验证回放。

## 边界（Boundary）

- 仅用于自有站点、受邀渗透、漏洞研究、安全合规审计、红蓝对抗、个人学习等**已授权**场景。
- 不为绕过商业风控产品（Akamai bmp/瑞数/极验/网易易盾/防水墙等）以批量爬取、批量注册、薅羊毛、套利、撞库提供成品脚本。
- 当请求是"过 xxx 验证 / 还原 xxx 参数"，先在内部翻译为：①样本归属与授权确认 → ②抓包侦察 → ③AST 解混淆 → ④参数追源 → ⑤算法识别 → ⑥补环境/纯算实现 → ⑦回放验证 → ⑧撰写分析备忘。
- 若用户没有给出授权来源，仅停留在"机制解释 + 工作流"层面，不给具体目标的可运行脚本。

## 总体工作流（Workflow）

按下列 12 步推进；每一步都有对应的 Path 段落详细展开。本技能共 13 条 Path：1~10 对应 Workflow 主线，11~13 是横切支撑（工具链 / TLS 指纹 / 版本跟进），任何阶段都可能用到。

1. **样本归类与授权确认**：站点域名、目标接口、风控产品（Akamai/瑞数/极验/防水墙/自研 jsvmp/Webpack 普通混淆）、关键参数名（sign/x-bogus/x-s/x-t/h5st/sensor_data/_abck/...）。
2. **抓包侦察**：列出所有需要逆向的请求字段（典型形如 `a/c/d/e/g/k/p/s/u/v` 或 `aid/ua/lang/entry_url/sess/...`），定位 Initiator → 找到生成入口的 JS 文件。
3. **JS 文件清单与混淆分级**：按文件大小排序（KB），结合"webpack 模块化 / 单字母变量 / 控制流平坦化 / jsvmp / 多态 VM"5 类标签初判。
4. **AST 解混淆**：用 Babel 跑 9 个 Pass（字符串解密 → 字符串数组 → 常量折叠 → 逗号表达式 → 变量重命名 → 对象字典展开 → 死代码清理）。
5. **参数追源**：从条件断点 + 日志断点逆向找出"赋值处 → 拼装函数 → 字节码入口"。
6. **算法识别**：判断是 base64 变体 / 魔改 SHA256 / 魔改 MD5 / RC4 / 自定义 jsvmp / 多态 VM。
7. **路径选择（三选一）**：
   - **a) 纯算还原**：算法稳定，按字符表 + 位运算公式重写（见 Path 5）
   - **b) 补环境**：算法形态频繁变 / 依赖浏览器 API（见 Path 5）
   - **c) 黑盒 + MITM 异步**：极复杂风控，让真浏览器跑、MITM 截参数（见 Path 7）
8. **风控字段处理**：识别 envData / fingerprint / 轨迹这类"采集字段"——很多**不参与签名验证**，可以固定写死。
9. **滑块/PoW/验证码**：OpenCV 模板匹配 + 三段式轨迹 + PoW 暴力搜 md5。
10. **回放验证**：用恢复的密钥/字符表/常量在脱机环境复现密文；和真实抓包对比。
11. **JSVMP / 多态 VM 兜底**：还原成本太高时走"AI 辅助 + 补环境"绕过路线（见 Path 8）。
12. **横向校验姊妹接口**：register / login / cfg / profile 通常共用密钥和签名格式；找一个最简单的接口先打通，再迁移到复杂接口。

---

## Path 1: 抓包与 JS 文件清单（Recon Path）

适用：拿到一个 web 站点 + 目标接口，第一件事先列清单。

1. **F12 + Network**：定位需要逆向的请求；记录 method、URL、headers、body、cookies。
2. **逆向字段清单**：把待解参数列成表格。常见 6 类：
   - **签名类**：sign / x-sign / x-s / x-bogus / x-gorgon / signature / nsign / h5st / X-MMe-Nas-Qualify（Apple）
   - **会话类**：msToken / token / sess / sid / nonce / callback（JSONP，常见单调递增）
   - **指纹类**：fingerprint / device_id / canvas_fp / webgl_fp / audio_fp / ja3 / akamai_bm-sz
   - **轨迹类**：collect / sensor_data / mst / kev / mev / tev / ffs / inf
   - **凭据类**：cookie 中的 `_abck` / `__zp_stoken__` / `__NS_xxx` / `__TS01__`（F5）
   - **加密载荷类**：data / encrypt / payload / ciphertext（多为 AES/RC4 + base64 包装）
3. **Initiator 跟栈**：右键请求 → Initiator → 跳进调用栈，找到生成参数的最近一行。
4. **JS 文件清单**：按大小列；常见模式：
   - 大文件（200KB+）= 主业务 + 算法
   - 中文件（70-100KB）= 设备指纹采集
   - 小文件（<10KB）= 加载器
5. **混淆分级标签**：
   - **L1 普通混淆**：字符串数组 + 单字母变量（OB/sojson 风）
   - **L2 控制流平坦化**：长 switch + dispatcher + while(true)
   - **L3 webpack 模块化**：函数调用链跨模块
   - **L4 单 VM**：自定义字节码 + 解释器，case → 固定语义
   - **L5 多态 VM**：30+ 个 dispatcher，同一 opcode 在不同 VM 中含义不同
   - **L6 浏览器指纹绑定**：算法依赖 Canvas/WebGL/AudioContext 的真实硬件输出
6. **风控产品识别**：搜文件中的特征字符串
   - Akamai → `_abck`、`bmak`、`sensor_data`
   - 瑞数 → 重写 `XMLHttpRequest.prototype.send`、URL 后缀动态参数
   - 极验 → `geetest`、`gt_captcha`、`challenge`
   - 防水墙 → `__TENCENT_CHAOS_STACK`、`tdc.js`、`TDC.setData`
   - 网易易盾 → `dun.163.com`
   - 数美 → `shumei`、`fp_id`
   - F5 Shape → `__TS01__`
   - Vaptcha → `vaptcha`

---

## Path 2: AST 解混淆（Babel Pass Path）

适用：拿到一份混淆 JS 后，先跑标准 9 个 Pass 还原可读形态。

工具栈：`@babel/core` + `@babel/parser` + `@babel/generator` + `@babel/traverse` + `@babel/types`。

### 9 个 Pass（按顺序）

| Pass | 功能 | 关键 visitor 节点 |
|---|---|---|
| 1 | 字符串解密函数还原 | `CallExpression`：识别解密器并求值 |
| 2 | 字符串数组还原 | `MemberExpression`：`_arr[42] → "appid"` |
| 3 | 常量折叠 | `BinaryExpression / UnaryExpression`：`0x1a + 0x3c → 数值` |
| 4 | 逗号表达式展开 | `SequenceExpression → BlockStatement` |
| 5 | 变量语义重命名 | `Identifier`：`_2n8l4 → Bytecode` |
| 6 | 对象字典展开 | `_$wR.add(x,y) → x + y` |
| 7 | 死代码移除 | `IfStatement`：永真/永假分支裁剪 |
| 8 | 未使用变量删除 | `scope.bindings` + 引用计数 |
| 9 | 控制流平坦化反平坦 | switch dispatcher 识别 + 按 case 顺序拉平 |

### 调试技巧

- **分 Pass 执行**：每个 Pass 单独写 `pass1.js`、`pass2.js` ... 单测。
- **错误反馈给 AI**：报错信息直接发给 AI 修复（语法不识别 / 节点类型错）。
- **在线调试**：`https://astexplorer.net/`。
- **traverse 的 enter/exit**：默认 enter；写 `{ NumericLiteral: { enter, exit }}` 控制时机。
- **多类型联用**：`"NumericLiteral|StringLiteral"(path) {...}` 一个 visitor 处理多种节点。
- **path 常用属性**：`toString()` / `node` / `parent` / `parentPath` / `type` / `replaceWith` / `remove` / `insertAfter`。

### 输出工件

- **解混淆后的 JS**：方便人类阅读
- **字节码数组**：从 jsvmp 提取
- **字符串表**：所有解密后的常量字符串
- **VM dispatcher 结构**：每个 case 的语义映射表

---

## Path 3: 参数追源（Parameter Tracing Path）

适用：抓包知道字段名，但不知道生成位置。

1. **条件断点**：`_func.apply(_this, _args).length == 28`（以 X-Bogus 28 字节为例）
2. **逆栈往上跳**：从 send/fetch 入口往上找最近一次 `setHeader / setRequestHeader / push fields`。
3. **日志断点**（不要 alert，否则卡死）：

   ```js
   "1", "j>>>", j, "A>>>>", A, "O>>>>>", JSON.stringify(O,
     function(k, v) { if (v == window) return undefined; return v; })
   ```

   注意 **window 引用要去掉**，否则循环引用爆栈。

4. **多次保存日志比对**：相同输入跑多次，看哪些字段是
   - 每次完全相同（**固定值，可写死**）
   - 每次随机（**真实随机数**）
   - 每次按时间递增（**时间戳**）
   - 周期变化（每周/每天，**算法版本标记**）
5. **Initiator 链路图**：把"参数 → 拼装函数 → 字节码 → VM 入口"画成调用链。
6. **`setFuncKeyMap` 类 hook**：把所有 `key → fn` 映射提前打印缓存，避免每次跟踪函数。

---

## Path 4: 算法识别（Algorithm Pattern Path）

### 4 种主流模式 + 识别特征

| 模式 | 识别特征 | 还原难度 |
|---|---|---|
| **base64 变体** | 64 字符表 + `(v >> shift) & 63` 形态 | 低 |
| **魔改 SHA256** | 输入预处理 / 内部 `_append` 多写 / IV 改 / 输出字节交换 | 中 |
| **魔改 MD5** | 4 round 的 K 常量改 / shift 数组改 / 初始 IV 改 | 中 |
| **RC4** | `S[256]` + `(d + S[i] + key) % 256` 经典 KSA + PRGA | 低 |
| **HMAC 魔改** | NEON 字节反转、轮 shift 改 | 中 |
| **自定义 jsvmp** | 巨型 switch + 字节码数组 + dispatcher | 高 |
| **多态 VM** | 30+ 个互不通用的 dispatcher | 极高（建议补环境） |

### 魔改 SHA256/MD5 必查 4 点

1. **输入预处理**：`_seData1(input)` 是否追加动态后缀（按字符码累加 + 自定义字符表映射）
2. **`_append` 是否被替换**：标准实现是 `buffer += data`；魔改版会调 `_eData(data)` 追加固定后缀
3. **IV 是否被改**：标准 IV `0x6a09e667/...`，对照源码看
4. **输出后处理**：字节交换（如 `byte[0] ↔ byte[2]`）/ 重排

### base64 变体公式

```js
const tab = "<64 字符替换表，可能 + 替换为 -，/ 替换为 _ 等>";
let out = "";
for (let i = 0; i < src.length; i += 3) {
    const c1 = src.charCodeAt(i), c2 = src.charCodeAt(i+1), c3 = src.charCodeAt(i+2);
    const v = c3 | (c2 << 8) | (c1 << 16);
    out += tab[(v & 0xFC0000) >> 18] +
           tab[(v & 0x3F000) >> 12] +
           tab[(v & 0xFC0) >> 6] +
           tab[v & 0x3F];
}
```

抖音 X-Bogus 的固定字符表：`Dkdpgh4ZKsQB80/Mfvw36XI1R25-WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe=`（多年未换）。

---

## Path 5: 补环境（Environment Faking Path）

适用：算法在 jsvmp 内、依赖浏览器 API、纯算还原成本高时。

### 缺啥补啥模板（最小集）

```js
window = global;
document = {};
document.addEventListener = function () {};
navigator = {
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0'
};
```

### 进阶补：事件监听器 + 鼠标轨迹

```js
document._eventListeners = {};
document.addEventListener = function(type, fn) {
    (document._eventListeners[type] = document._eventListeners[type] || []).push(fn);
};

function simulateMouseTrack(track) {
    for (const p of track) {
        const evt = { type: 'mousemove', clientX: p.x, clientY: p.y, timeStamp: p.t };
        (document._eventListeners['mousemove'] || []).forEach(fn => fn(evt));
    }
}
```

### 常见检测项与对应补法

| 检测点 | 真实浏览器 | Node 默认 | 补法 |
|---|---|---|---|
| `process / require / module` | undefined | 存在 | `delete global.process; delete global.require;` |
| `window` | 真对象 | undefined | `window = global` |
| `navigator.userAgent` | 浏览器 UA | undefined | 设置完整 UA |
| `navigator.webdriver` | undefined / false | - | 设为 `false` |
| `document.createElement` | 返回 element | undefined | mock 对象，至少支持 `.style` 和 `.appendChild` |
| `performance.now()` | 高精度时间 | 部分支持 | `performance = require('perf_hooks').performance` |
| `Canvas / WebGL / AudioContext` | 硬件输出 | 无 | mock 返回固定值 |
| `screen / window.innerWidth` | 真实尺寸 | 无 | `screen = { availHeight: 1040, availWidth: 1920, width: 1920, height: 1080 }` |
| `crypto.subtle` | 浏览器 API | Node 18+ 自带 | 直接用即可 |

### 补环境 vs 纯算 决策树

- 算法稳定（结构和 case 多次抓不变）→ **纯算**（可移植到任意语言、性能高）
- 算法形态频繁变（每周更新 jsvmp 字节码）→ **补环境**（一次性投入低，跟版本快）
- 多态 VM / 算法依赖硬件指纹 → **补环境是唯一可行**
- 上面两条都不划算（算法极端复杂、变得快、且 QPS 不高）→ 走 **Path 7（黑盒 + MITM 异步）**

---

## Path 6: 滑块 / PoW / 验证码（Captcha Path）

### 滑块 7 步流程（防水墙、极验、数美、网易易盾通用）

```
Step 1 prehandle 接口 → 拿 sess、sprite_url、bg_url、challenge
Step 2 下载 sprite 图 + 背景图
Step 3 OpenCV Canny + 模板匹配定位缺口位置
Step 4 三段式轨迹（加速 70% + 减速 30% + 微调抖动）
Step 5 PoW 暴力搜：md5(prefix + counter) == target
Step 6 设备指纹采集：TDC.setData({ft}) → getData → collect / eks
Step 7 verify 接口提交 → 拿 ticket
```

### 三段式轨迹模板

时间分配：加速 40% → 减速 50% → 微调 10%（总和 100%）。距离分配：加速段走 70%，减速段走 30%，微调段在终点附近抖动。

```python
import random

def build_trace(distance, total_ms=1500):
    """
    返回 [(x, y, t_ms), ...] 形式的轨迹。
    x 是相对滑块起点的水平偏移；y 是垂直噪声；t_ms 是相对开始的时间戳。
    """
    steps = []
    accel_dist = distance * 0.7
    decel_dist = distance * 0.3
    accel_t    = total_ms * 0.4    # 0~600 ms
    decel_t    = total_ms * 0.5    # 600~1350 ms
    fine_t     = total_ms * 0.1    # 1350~1500 ms

    # 加速阶段：x = accel_dist * t^2
    n1 = max(1, int(accel_t / 16))
    for i in range(1, n1 + 1):
        t = i / n1
        x = accel_dist * t * t
        steps.append((round(x), round(random.gauss(0, 1)), int(t * accel_t)))

    # 减速阶段：x = accel_dist + decel_dist * (1 - (1-t)^2)
    n2 = max(1, int(decel_t / 16))
    for i in range(1, n2 + 1):
        t = i / n2
        x = accel_dist + decel_dist * (1 - (1 - t) ** 2)
        steps.append((round(x), round(random.gauss(0, 1)), int(accel_t + t * decel_t)))

    # 微调阶段：在终点附近抖一下
    n3 = max(1, int(fine_t / 30))
    for i in range(1, n3 + 1):
        t = i / n3
        jitter = random.randint(-2, 2) if i < n3 else 0
        steps.append((distance + jitter, 0, int(accel_t + decel_t + t * fine_t)))

    return steps
```

### 浏览器特征 50 项 ft 字符串

`features = [matches, msMatchesSelector, webkitMatchesSelector, matchMedia, CSS.supports, createRange, CustomEvent, scrollIntoView, getUserMedia, IntersectionObserver, ontouchstart, performance, ...]`

每项布尔值串接 → 形成站点指纹。

---

## Path 7: 黑盒 + MITM 异步方案（瑞数风格）

适用：算法极复杂（瑞数四代/五代）、无法/不值得纯算还原。

```
浏览器（真实环境）─→ 触发 fetch(目标URL?probe=1)
                         │
                         ▼
                   瑞数 JS 重写 fetch / XHR
                         │ 在请求出门前补齐 Cookie + URL 后缀
                         ▼
                  MITM (mitmproxy/Burp/Fiddler)
                         │ 拦截、提取动态参数和 Cookie
                         ▼
            ┌────────────┴────────────┐
            │                         │
       本地文件 / DB             本地 API 服务
            │                         │
            ▼                         ▼
     主程序（Python requests）轮询读取或 GET API
```

**注意**：是**异步**架构，无法做 RPC 同步等待响应。需要共享存储或本地通信。

**优点**：完全不用还原算法。
**缺点**：吞吐受限（每个请求要走真实浏览器），适合**低 QPS 高价值**场景。

---

## Path 8: jsvmp / 多态 VM（VM Reverse Path）

适用：腾讯防水墙 `__TENCENT_CHAOS_STACK` / 京东 h5st / 抖音 jsvmp / 小红书 mns / Akamai bmp 等。

### 单 VM（普通）

- 一个 dispatcher（长 switch 或 while-true + lookup）
- opcode 与语义一一对应（`case 2 → PUSH`、`case 5 → POP`）
- 还原方法：抽出 case → opcode → handler 映射表 → 静态翻译字节码 → 转 IR

### 多态 VM（京东 h5st 风）

- **30+ 个独立 dispatcher**
- **同一 opcode 在不同 VM 中含义完全不同**：`VM_A: case 2 → PUSH`、`VM_B: case 2 → STORE`、`VM_C: case 2 → CALL`
- 静态分析极难，**必须 AI 辅助 + 人工浏览器验证**

### AI + 人工协作模式（京东 h5st 案例验证可行）

```
┌─────────┐  分析代码、定位关键点 ┌─────────┐
│   AI    │ ─────────────────→ │   人工   │
│         │ ←───────────────── │         │
└─────────┘  执行结果、变量值   └─────────┘
```

具体节奏：
1. AI 读 AST 解混淆产物，识别 dispatcher
2. AI 给出"在 X 函数入口设断点"指令
3. 人工浏览器执行 → 反馈传入参数 / `this.buffer` 内容 / 返回值
4. AI 据此调整分析方向 → 找出第二层魔改
5. 反复迭代直到调用链全部明确

### VM 调用链梳理示例（京东 h5st）

```
signSync()
  ↓
┌───────────────────────────────────────────────────┐
│ l34 (签名入口)                                     │
│   ↓                                               │
│ l31 (h5st 组装) ────────────────────────────┐      │
│   ├→ l24 (密钥) → l25                       │      │
│   ├→ l28 (签名计算) → jd_sha256              │      │
│   ├→ l30 (签名数据)                          │      │
│   ├→ wm_encode (自定义 base64)               │      │
│   └→ l27 (最终组装) ←────────────────────────┘      │
└───────────────────────────────────────────────────┘
```

---

## Path 9: 风控字段固定化（envData Pin Path）

适用：算法已还原，但缺指纹环境跑不通时。

**核心观察**：很多"风控字段"（envData / fingerprint / TLS / Canvas）只是**反爬探针**，**不参与签名验证**。

**做法**：
1. 用真实浏览器抓一份完整的 envData
2. 在还原代码里直接固定这一份
3. 跑通签名验证后再考虑是否要做风控规避（多账号轮换 / vPhone / 浏览器指纹差异化）

**京东 h5st 案例**：第 8 个字段 envData 收集了 UA / Canvas / WebGL / 屏幕尺寸 / 时区 / 性能时序，但**固定 envData 后签名验证不影响**。

---

## Path 10: 回放与验证（Validation Path）

成功标准：用还原后的脚本（Python / Node）能离线产出与抓包一致的密文。

### 清单

1. 把所有硬编码常量（字符表、IV、轮密钥、固定后缀、字节交换索引）抠出独立 `consts.py`/`consts.js`。
2. 写 `sign(method, path, query, body, jwt) → str` 等单函数。
3. 用同一组输入跑两次 → 输出**逐字节一致**。
4. 横跨 register / login / cfg / profile 多接口复用同一密钥再验。
5. 用真实浏览器抓包对比；不一致时回到 Path 3 用日志断点定位差异点。

### 常见漂移点

- 字段顺序：JSON `Object.keys` 在不同引擎顺序不同 → 强制按抓包顺序拼装
- 时间戳格式：秒 / 毫秒 / 13 位整数 / `+new Date` / `Date.now()`
- URL 编码：`encodeURIComponent` vs `encodeURI` vs 自定义白名单
- Hash 大小写：hex 通常小写，但有些站点用大写
- 拼接换行：`\n` vs `\r\n`
- BOM / 首字节零宽字符：偶尔在拼装的 plaintext 头部插入 `​/﻿`
- 大端小端：构造 `Uint8Array` 时字节序错乱

---

## Path 11: 工具链（Toolchain Path）

各阶段推荐工具，按"调研→分析→联调→交付"顺序：

### 抓包 / 流量

| 工具 | 适用 | 备注 |
|---|---|---|
| **mitmproxy** | 命令行 + Python 插件 | Path 7 异步方案首选；脚本化拦截 |
| **Burp Suite** | 拦截 / 改包 / 重放 | 适合渗透；Repeater + Intruder |
| **Fiddler / Fiddler Everywhere** | Windows 桌面 | 抓 HTTPS、AutoResponder 替换 JS 文件 |
| **Charles** | macOS 桌面 | 同 Fiddler |
| **Yakit** | 国产渗透平台 | 内置 MITM、爬虫、Webfuzzer |
| **Wireshark** | 底层抓包 | 排查 TLS / TCP 异常时用 |

### 浏览器调试

| 工具 | 适用 |
|---|---|
| **Chrome DevTools** | 主力，断点 / 日志断点 / Initiator / Sources Override |
| **Sources Override**（DevTools 内置） | 替换线上 JS 文件为本地修改版，免重发布 |
| **Chrome DevTools MCP** | AI 驱动浏览器（让 Claude 抓包、断点） |
| **chii** | 远程 DevTools 调试嵌入 webview |
| **userscript（Tampermonkey）** | 注入 hook 脚本，例如打印每次 fetch 参数 |

### AST 解混淆

| 工具 | 适用 |
|---|---|
| **Babel**（`@babel/parser/generator/traverse/types`） | 主力 9 Pass 工作流 |
| **astexplorer.net** | 在线浏览 AST 节点结构 |
| **deobfuscator.io** | 一键去常见混淆（OB/sojson 风） |
| **Restringer** | Open-source 自动反 OB |
| **wakaru** | webpack 还原成模块文件 |
| **shift-refactor / esprima** | 备选解析器 |

### 自动化执行 / 补环境

| 工具 | 适用 |
|---|---|
| **Playwright** | 跨浏览器自动化，反检测能力强；Path 7 黑盒方案首选 |
| **Puppeteer / puppeteer-extra-plugin-stealth** | Chrome 专用，stealth 自带 |
| **Selenium / undetected-chromedriver** | 老牌，UDC 抗检测 |
| **rod** | Go 语言版 Puppeteer |
| **Node.js + jsdom** | 轻量补环境，但 jsdom 缺很多 BOM |
| **vm2 / isolated-vm** | 沙盒执行不受信 JS |

### RPC / 调用桥（让浏览器跑算法、Python 调）

| 工具 | 适用 |
|---|---|
| **Sekiro** | RPC 桥架，浏览器 hook 函数 → 注册 → Python 调 |
| **JsRPC** | 类似 Sekiro，更轻量 |
| **rpc.py** + frida | 移动端类似方案 |

### 滑块图像识别

| 工具 | 适用 |
|---|---|
| **OpenCV (cv2.matchTemplate)** | 模板匹配缺口，最常用 |
| **ddddocr** | OCR + 滑块缺口检测，开箱即用 |
| **YOLO v8** | 训练自己的滑块/点选模型 |
| **PaddleOCR** | 文字点选验证码 |

### 代码搜索 / 反查

| 工具 | 适用 |
|---|---|
| **ripgrep / `code --search`** | 在解混淆后的几 MB 代码里 grep |
| **JADX**（Android）/ **Hopper**（iOS） | 跨端时用 |

---

## Path 12: TLS / JA3 指纹（TLS Fingerprint Path）

适用：参数对了但请求仍被风控（Akamai bmp、Cloudflare、阿里 226 常见）。

**核心观察**：很多风控**先看 TLS 握手指纹**（ja3 / ja3s / ja4 / akamai_bm-sz），再看参数。Python `requests` 的握手 ciphersuite 与 Chrome 不一样 → 一抓一个准。

**对策**：

1. **`curl_cffi`**：Python 库，模拟 Chrome/Firefox/Safari/Edge 的 TLS 指纹
   ```python
   from curl_cffi import requests
   r = requests.get(url, impersonate="chrome120", headers=headers)
   ```
2. **`tls-client`（Python/Go）**：精准 ja3 / HTTP/2 帧级模拟
3. **`undetected-chromedriver`**：浏览器层走真 TLS
4. **JA3/JA4 在线检测**：`https://tls.peet.ws/api/all`、`https://tls.browserleaks.com/json`，对比"目标浏览器 vs 你的脚本"

**JA3 字段**：`SSLVersion,Cipher,SSLExtension,EllipticCurve,EllipticCurvePointFormat`。`SHA1` 一下就是 ja3 hash。

**JA4** 是新版（2023+），结构更分层，区分 TLS 1.2 / 1.3 / QUIC。

**akamai_bm-sz cookie**：Akamai 风控会把首次握手的 ja3 + UA + IP 打包成 `bm_sz` cookie；后续请求 cookie 没带、或者新会话 ja3 不一致就直接 403。

---

## Path 13: 版本指纹与升级跟进（Version Fingerprint Path）

风控算法每过几周就会升级一次。同一个站点，今天抓到的算法和上周不一样很常见。**版本指纹**让你一眼看出当前是哪一版，避免拿错版本的还原代码套新流量。

### 版本指纹的几种形态

1. **数据结构长度**：小红书 x-s 的中间数组长度
   - 4.2.6 → 124 位
   - 4.2.9 → 135 位
   - 4.3.1 → 144 位（= 124 + 20）
   每升一版加几个字段。
2. **JS 文件的某段魔数**：抖音 jsvmp 字节码数组长度、京东 h5st VM 数量
3. **响应头/响应体的 version 字段**：Akamai 的 `ver` 由 `OCH = CP()["E"].apply(...)` 算出，每周变
4. **关键函数名的 mangled 后缀**：`_0xfca8c3` 这类编号，混淆后会变，但同一份 JS 里稳定
5. **SDK 版本号**：URL 里的 `?v=4.3.1`、`/static/4_3_1/...`
6. **Cookie key 名变化**：`__zp_stoken__` 升级到 `__zp_stoken_v2__`

### 跟版策略

1. **抓"版本嗅探脚本"**：每天/每小时拉一次目标站点首页，提取上面 6 个指纹，对比上次。
2. **保存历史 JS 文件**：每个版本的 JS 完整存档（带 hash 命名），方便对比 diff。
3. **diff 关键函数**：用 AST 解混淆后再 diff，避免变量名漂移污染。
4. **算法变动 vs 字段变动**：90% 的"升级"是加几个采集字段（envData 多收一项），算法核心不变；只在字段层面跟。
5. **建立 issue 看板**：每个版本一行——版本号 / 抓包日期 / 改动点 / 还原代码 commit。

---

## Troubleshooting

- **算法重写后密文对不上**：先怀疑魔改的 4 点（输入预处理 / `_append` / IV / 输出后处理），不要先怀疑算法本身。
- **补环境跑不通且报错"window is not defined"**：用 `window = global` 而不是 `window = {}`；同时 `globalThis = global`。
- **补环境跑通了但密文不对**：很可能补多了不该补的（比如 `process` 没删干净），先 `delete global.process` 再试。
- **多态 VM 某个 opcode 行为奇怪**：检查是不是同一个数字在另一个 VM 中已经被你定义了不同含义。
- **滑块通过了但马上被风控**：env / 指纹被打了风险标记；做账号轮换或换浏览器指纹。
- **PoW 跑得慢**：搜索空间一般是几万到几十万，单线程 md5 即可；瓶颈是单次 hash 速度。
- **JSONP 回调拿不到**：注意 `callback=_aq_191730` 这种递增 ID，部分站点会校验 ID 单调递增。
- **参数对了但仍 403 / 521 / 412**：先查 TLS 指纹（Path 12），换 `curl_cffi` 或 `tls-client`；再查 cookie 完整性（`_abck` / `bm_sz` 是否带齐）。
- **同一份代码昨天能跑、今天不行**：风控升级了，按 Path 13 的"版本指纹"流程嗅探当前版本；不要修代码，先确认是不是算法变了。
- **解混淆后还是看不懂**：可能是 Pass 顺序错了（变量重命名要在字符串还原之后；死代码移除要在常量折叠之后）。
- **AST `replaceWith` 报错"Cannot insert ... while traversing"**：用 `path.replaceWithMultiple([...])` 或在 exit 阶段做。
- **接口偶现成功偶现失败**：先排查时间戳精度、随机数种子、cookie 状态机；不一致的成因 90% 是状态依赖。

---

## 参考资料

- 案例索引：[references/README.md](references/README.md)。
- 看雪搜索日志（24 个关键词、~70 高价值帖子分级）：[references/kanxue-search-log.md](references/kanxue-search-log.md)。
- 看雪精读笔记（6 篇高密度技术贴的工作流提炼）：[references/kanxue-notes.md](references/kanxue-notes.md)。

仅在任务确实涉及对应平台/产品时再 Read 对应 references 文件，避免不必要地把整个语料拉进上下文。

---

## 如何扩充本技能（How to extend）

当后续收到新平台/新风控产品的资料时，按下面流程并入：

1. 在 `references/` 下新增 `<平台短名>-notes.md`（例：`xhs-xs-notes.md`、`douyin-xbogus-notes.md`、`jd-h5st-notes.md`、`akamai-bmp-notes.md`）。文件首部放一张 5 行摘要表（站点 / 风控产品 / 参数 / 算法栈 / 反检测亮点），随后是逐字技术内容。
2. 在 `references/README.md` 索引表里追加一行。
3. 如果新平台引入了**全新的工作流环节**（例如 WebAssembly 风控、Service Worker 拦截、WebRTC 指纹），再到 `SKILL.md` 里**只补对应一节** Path（不要重写已有路径）。
4. 通用规律写进 `SKILL.md`，样本特定细节写进 `references/<平台>-notes.md`。
