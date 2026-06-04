# 阿里云盾 / 阿里滑块（_bx-v / x82Y / x231 / ali140 / 227 / etSign / 阿里云 captcha-open v2）

> **注意：本文档下有两个独立产品**
>
> - **第 1~10 节**：阿里系内嵌滑块（淘宝/天猫/1688 用，参数族 bx-v / x82Y / x231 / ali140 / 227 / etSign）—— 阿里安全部门产品
> - **第 11 节起 (R6 新增)**：**阿里云 captcha-open v2** SaaS 验证码（公有云对外卖的产品，对接 `*.captcha-open.aliyuncs.com`，关键字段 `captchaVerifyParam` / `CertifyId` / `SceneId` / `prefix`）—— 阿里云团队产品
>
> 两个产品**算法、字段名、接入方式完全不同**，不要混淆。NoteGPT、南方航空、东方航空、Backblaze 等用的是第 11 节的 captcha-open v2。

## 1. 产品形态
- 阿里系滑块/无感由阿里安全（"AliCaptcha"/"_bx-v"）实现，分多种代号：x82Y、x231、ali140、ali227、bxet、rand、bx-v。
- 接入面：淘宝/天猫/1688/阿里云/支付宝/钉钉/中国联通等。
- 滑块 + 无感 + 风控（与「Sec」业务签名同源）。

## 2. 检测维度
- **bx-v / etSign / 227 / 231**：参数名按业务变，本质是同一套 collect → 加密 → 上报：
  - bx-v：业务 sign，字符串两段哈希。
  - 227：滑块 trace 上报参数。
  - 231：新一代滑块通用 token。
  - bxet / etSign：风控签名。
  - ali140 / ali150：滑块版本号路径标识。
- **环境**：Canvas/WebGL/Audio/Font/UA-CH/Plugins/Battery/HardwareConcurrency。
- **行为**：鼠标移动、滚轮、键盘。
- **TLS / IP 信誉**。
- **mtop sign 联动**：与淘宝 mtop `sign`（h5 用 `_m_h5_tk`）共享部分指纹。

## 3. 关键端点与字段
| 端点 | 字段 |
|------|------|
| `/_____tmd_____/punish?...` | 风控弹页面 |
| `/captcha/getsig` | 取签名 |
| `/<biz>?bx-v=...&...` | 各业务接口 |
| `cf.aliyun.com/captcha-mng/v3/...` | 阿里云 captcha 服务 |

## 4. 已公开研究
- CSDN「阿里 bxet 逆向」：`etSign` 纯算补环境。
- CSDN「逆向实战 30——阿里 227 逆向分析」：滑块 trace 参数。
- CSDN「阿里云滑动验证码逆向分析」：联通话费页面案例，参数 `a`/`scene`/`href`。
- CSDN「阿里 rand 逆向分析」：1688/231 滑块。
- CSDN「阿里最新普通 x231 逆向分析」：x231 检测机制。
- 多篇「ali140 滑块 canvas 补环境」（CSDN 159607511、158903755、159787961）：Node.js 模拟 Canvas + WebGL 指纹。
- 看雪/吾爱：mtop `sign` + 滑块联合分析帖。

## 5. 防御性分析思路
1. 阿里系大量参数互相校验，逆向单一参数不够，需要把整条链（指纹 → bx-v → mtop sign → 业务）一起还原。
2. JS 用 OB 混淆 + 字符串数组旋转，先 deobf。
3. Canvas 补环境是关键：toDataURL 一致性、WebGL UNMASKED_VENDOR_WEBGL/UNMASKED_RENDERER_WEBGL 必须给出真值。
4. 风控降级：`/punish` 触发后 IP/UA 加锁，需要换出口。
5. 注意 ali140 与 ali150 版本差异，新版 token schema 完全不同。

## 6. 已知缓解 / 更新历史
- 阿里持续推新参数名（bx-v → 227 → 231 → ali140 → 150），周期约半年。
- 2023 强化 Canvas/WebGL 一致性。
- 2024 ali150 引入 WASM。
- 与设备指纹"无线保镖"在 App 端有联动。

## 7. 待研究问题
- ali150 WASM 入口与算法。
- bx-v 与 mtop sign 之间的依赖图。
- 不同业务（淘宝 vs 1688 vs 阿里云）参数差异点。

## 8. 阿里滑块版本号 / 字段族对照表（R4 补充）

> 阿里系参数名半年一换，但本质都是"同一套 collect → AES + base64 → 上报"。下表整理 CSDN/52pojie 累计出现过的代号；R4 通过 CSDN API 抽样验证至少 30+ 篇相关文章。

| 代号 | 类型 | 角色 | 出现时间窗 | 关键 articleid |
|------|------|------|-----------|---------------|
| `bx-v` | URL/Body 参数 | 业务 sign（短哈希） | 2018- 至今 | 多篇综述 |
| `etSign` / `bxet` | URL/Body 参数 | 风控签名（强校验） | 2020- | 多篇 |
| `227` | URL 参数 | 滑块 trace 上报 | 2020-2023 | 多篇逆向 30 案例 |
| `x231` / `231` | Body 参数 | 新一代滑块 token | 2023- | 多篇 |
| `x82Y` | URL 参数 | 滑块/风控混合 | 2022-2024 | 多篇 |
| `ali140` | 路径标识 | 滑块版本号 | 2024 | (158903755 / 159607511 / 158674857) |
| `ali150` | 路径标识 | 滑块新版（含 WASM） | 2025 | (158674857) |
| `_bx-v` | Body 参数 | bx-v 双下划线变体（淘宝/天猫） | 2019- | 多篇 |
| `rand` | URL 参数 | 1688 滑块通用 | 2021- | 多篇 |
| `n` | Body 参数 | 滑块 nonce | 2022- | 多篇 |
| `a` / `scene` / `href` | URL 参数 | 联通话费页等业务侧 | 2023- | 阿里云 captcha 系列 |

**版本演进**：bx-v(2018) → 227(2020) → 231/x82Y(2022-2023) → ali140(2024) → ali150(2025, WASM)。
**大致规律**：每一次版本切换都涉及 (a) Canvas/WebGL 指纹采集字段扩充，(b) AES 模式或 IV 派生算法变化，(c) 服务端校验加严（IP 信誉权重提升）。

## 9. 新增 articleid（R4 已 API 验证的样本）

- (158674857) 阿里 140 滑块逆向实战：从环境补全到加密参数获取全流程
- (158903755) JS 逆向进阶：ali140 滑块验证码的 Canvas 环境精准模拟
- (159607511) JS 逆向新手也能搞定：手把手教你用 Node.js 补全 ali140 滑块 canvas

R5 建议进一步覆盖：x82Y 全流程、ali150 WASM 反汇编。

## 10. 待研究问题（追加）
- ali150 WASM 内部 dispatcher 是否与 DataDome/F5 风格 VMP 相似（推测不是，应仍是直函数）。
- mtop `sign` 与 `_bx-v` 在淘宝/天猫不同业务的具体依赖图。

---

# 第二产品：阿里云 captcha-open v2（公有云 SaaS）

> R6 新增章节（2026-05-13）。资料来源：CSDN 真实抓样 + NoteGPT 实地 SDK 静态分析。

## 11. 产品总览

阿里云对外卖的人机验证 SaaS，文档名"验证码服务 v2"。控制台是 `captcha.console.aliyun.com`。接入站点在 HTML 里加：

```html
<div id="captchaContainer"></div>
<script>
window.AliyunCaptchaConfig = {region:'cn', prefix:'<租户前缀>'};
</script>
<script src="https://o.alicdn.com/captcha-frontend/aliyunCaptcha/AliyunCaptcha.js"></script>
<script>
window.initAliyunCaptcha({
  SceneId: '<场景 id>',   // 在控制台建场景拿到
  prefix: '<租户前缀>',
  CaptchaType: 'SLIDING', // 或 NC / IC / POW / TRACELESS / CHECK_BOX
  mode: 'embed',
  element: '#captchaContainer',
  button: '#submitBtn',
  captchaVerifyCallback: function(param) { /* 业务回调，param 就是 captchaVerifyParam */ },
  onBizResultCallback: function(ok) {}
});
</script>
```

业务方表单里关键隐藏字段就是 `captchaVerifyParam`，值由 SDK 在用户通过滑块后填进去。

## 12. 完整请求链路（R6 抓样确认）

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. Log1 / 设备指纹初始化                                          │
│    POST cloudauth-device-dualstack.cn-shanghai.aliyuncs.com      │
│    Action=Log1, Version=2020-10-15, AccessKeyId=LTAI5...GQw72p   │
│    Data=AES加密的 [appKey,"WEB",encInit,APP_VERSION,"CLOUD",""]  │
│    响应: DeviceConfig(含动态 AES 密钥) + DeviceToken             │
├──────────────────────────────────────────────────────────────────┤
│ 2. InitCaptchaV3 / 拿验证码                                       │
│    POST {prefix}.captcha-open.aliyuncs.com                       │
│    Action=InitCaptchaV3                                           │
│    入参: SceneId, Language, Mode, DeviceData                     │
│    响应: CertifyId(关键), CaptchaType, CaptchaJsPath, CertifyId  │
├──────────────────────────────────────────────────────────────────┤
│ 3. UploadLog / Log2 / Log3 (多次)                                │
│    收集鼠标轨迹、环境指纹，分阶段上传到 device 端点               │
├──────────────────────────────────────────────────────────────────┤
│ 4. VerifyCaptchaV3 / 提交验证                                     │
│    POST {prefix}.captcha-open.aliyuncs.com                       │
│    Action=VerifyCaptchaV3                                         │
│    入参: SceneId, CertifyId, CaptchaVerifyParam                  │
│    响应: VerifyCode(T001=通过/F001=失败), VerifyResult,          │
│          securityToken, certifyId                                 │
└──────────────────────────────────────────────────────────────────┘
```

业务方拿到的 `captchaVerifyParam` 实际就是 `btoa(JSON({certifyId, sceneId, isSign:true}))`——**没有秘密**。真正的"通过证明"是 `CertifyId` 在服务端的状态（VerifyCaptchaV3 成功后才生效）。

## 13. 密钥体系

**API 层（标准阿里云 OpenAPI 签名）：**

| API | AccessKeyId | AccessKeySecret |
|---|---|---|
| Captcha API（{prefix}.captcha-open.aliyuncs.com） | `LTAI*****xmvT` | `dYSKfs****F9r89koz` |
| Device API（cloudauth-device-dualstack...） | `LTAI5tGjnK9uu9GbT9GQw72p` | `fpOKzILEa****gIRcX` |

签名算法 = HMAC-SHA1，**密钥末尾加 `&`**（阿里云标准），输出 base64。string-to-sign：

```
POST&%2F&<urlencode(canonicalQueryString)>
```

canonicalQueryString = 按 key 字典序排好，每对 `urlencode(k)=urlencode(v)`，`&` 拼接。

```python
def aliyun_sign(params, access_key_secret):
    sorted_p = sorted((k, v) for k, v in params.items() if k != 'Signature')
    qs = '&'.join(f"{quote(k, safe='')}={quote(str(v), safe='')}" for k, v in sorted_p)
    string_to_sign = f"POST&{quote('/', safe='')}&{quote(qs, safe='')}"
    sign_key = (access_key_secret + '&').encode()
    return base64.b64encode(hmac.new(sign_key, string_to_sign.encode(), sha1).digest()).decode()
```

**业务层（SDK 内置 AES key）：**

| 槽位 | 用途 | 来源 |
|---|---|---|
| `WEB_AES_SECRET_KEY.FLAG` | Log1 初始化数据加密 | SDK 内置（再用 `FqJ***pwb` 解出来） |
| `WEB_AES_SECRET_KEY.REQ` | deviceToken 部分数据 | SDK 内置 |
| `WEB_AES_SECRET_KEY.RES` | 服务端 DeviceConfig 响应解密 | SDK 内置 |
| `WEB_AES_SECRET_KEY.UPLOAD` | Log2/Log3 Data 字段 | SDK 内置 |
| `WEB_AES_SECRET_KEY.PREID` | 预初始化数据 | SDK 内置 |
| 动态 key 1 | 环境数据、轨迹加密 | 服务端 Log1 响应里的 DeviceConfig 第 1 段（base64） |
| 动态 key 2 | Log2/Log3 Data | 服务端下发 |

所有 AES = **AES-128-CBC，IV 固定（脱敏 `012***DEF`），PKCS7 padding**。SDK 加密引擎是**标准 CryptoJS，无魔改 sbox/key schedule**。

**主解密 master key**（解 SDK 内置 5 个 AES key 用的）：

```
ACCESS_SEC = "FqJ***pwb"  # 16 字节
IV         = "012***DEF"
```

可在 SDK 里用脚本搜 `me(nr.ACCESS_SEC, nr.WEB_AES_SECRET_KEY.XXX)` 之类调用拿到。注意源码里这两个常量也是用 obfuscator 包了一层，要先解 string-table。

**HMAC/MD5 salt（固定）：**

| 用途 | 值 |
|---|---|
| 通用 salt | `daye,raolewoba!` |
| SessionID salt | `8449449787` |

## 14. CaptchaVerifyParam 完整结构

四个字段，全部存在 base64 包装外面：

```json
{
  "sceneId": "1wpbfo15",
  "certifyId": "2xUrMCZFaL",
  "deviceToken": "V0VCI2FiMDM0ZWMw...",   // base64 包的 WEB#sid#enc#ver#md5
  "data": "JRMnX3A3XiIh..."               // VM-encrypted 轨迹包
}
```

最外层 base64 → 业务方拿到的就是 `param` 字符串。

### 14.1 `deviceToken`

```
base64(   WEB#<sessionId>#<encDeviceData>#<version>#<md5Check>   )
```

- `sessionId = "<appKey>-h-<timestamp_ms>-<uuid4hex>"`
- `encDeviceData` = 54 字段环境数据用动态 key AES-CBC 加密后 base64
- `version` = 数据版本号，如 `163`
- `md5Check` = `MD5("WEB#" + sessionId + "#" + encDeviceData + "#" + version + "#daye,raolewoba!")`

### 14.2 `data`（重点 — 与轨迹相关）

**生成流程（带 VM 加密层）：**

```
step1: trackList = {
  "mp": "x,y,t,flag|...",  // mousemove 主轨迹
  "mc": "x,y,t,1,flag|",   // mousedown
  "mu": "x,y,t,1,flag|",   // mouseup
  "mm": "x,y,t,flag|...",  // 滑动阶段轨迹
  "tc": "", "te": "", "tmv": "", "ks": "", "fi": "...",
  "startTime": 1768715528000,
  "si": "screenW,screenH,winW,..."
}

step2: trackId = VM_F(JSON.stringify({TrackList, TrackStartTime, VerifyTime}), "0000")  // 32-hex

step3: trackData = {TrackList, TrackStartTime, VerifyTime, arg}

step4: originalData = trackId + JSON.stringify(trackData)

step5: compressed = pako.deflate(originalData)   // zlib deflate

step6: o0 = base64(compressed)

step7: data = VM_L(o0, vmEncryptKey)  // vmEncryptKey 固定 16 字符
```

- VM 字节码位置（在动态拉的 `sg.xxx.js` 内）：
  - `V` (主常量表) 偏移 9061 起，约 500 字节
  - `L` (vmEncrypt 字节码) 偏移 9556 起，约 15000 字节
  - `F` (trackId 字节码) 偏移 4961 起，约 3000 字节
  - `G` (trackId 常量表) 约 280 字节
  - `D` (vmEncrypt 常量表) 约 125 字节
- VM 操作码：`0=h[l]属性访问, 5=递归调用, 6=字符串拼接, 8=h%l取模, 16=条件跳转, 45=++x, 48=位移, 49=&, 55=return, 56=|`

### 14.3 环境数据（99 字段 / 54 字段两套）

54 字段（deviceToken 用）和 99 字段（环境数据用）都是 `#` 分隔的 string，关键索引：

| idx | 字段 | 例 |
|---|---|---|
| 0 | 版本号 | `W.10050` |
| 5 | 平台 | `Win32` |
| 6 | 浏览器 | `Chrome` |
| 7 | 浏览器版本 | `143.0.0.0` |
| 19 | Canvas 指纹 MD5 | 32 hex |
| 20 | 字体数量 | int |
| 22 | CPU 核心 | int |
| 32 | 设备指纹 MD5（WebGL） | 32 hex |
| 36 | OS | `Windows` |
| 37 | OS 版本 | `10` |
| 40 | 语言 | `zh-CN` |
| 41 | 时区 | `Asia/Shanghai` |
| 42 | IP | 服务端回填或客户端补 |
| 47 | 屏幕分辨率 | `1440*3440` |
| 67 | 场景名 | `saf-captcha` |
| 77 | CertifyId | 同 verify |
| 88 | 检测标志位 | base64 of 0/1 mask（用于 anti-bot 信号） |

### 14.4 Canvas 指纹（idx 19）

```js
canvas = 240x60
ctx.font = '14.6667px "Times New Roman"';
ctx.fillStyle = '#006699';
ctx.fillText('Cwm fjordbank gly 😃', 2, 15);
ctx.font = '24px Arial';
ctx.fillStyle = 'rgba(102, 204, 0, 0.2)';
ctx.fillText('Cwm fjordbank gly 😃', 4, 45);
ctx.fillStyle = '#ff6600';
ctx.fillRect(100, 1, 62, 20);
// MD5 输入实际是从 canvas 提取的 RGB 颜色数组 JSON（~799 字符），不是 dataURL
canvasMd5 = MD5(JSON.stringify(rgbColors))
```

### 14.5 设备指纹 MD5（idx 32）

```js
canvas = 122x110, gl = canvas.getContext('webgl')
// 绘制 WebGL 测试图，获取 dataURL
deviceData = {"winding": ctx.isPointInPath(6,6,'evenodd')===false, "geometry": dataURL}
deviceMd5 = MD5(JSON.stringify(deviceData))   // 输入 ~20188 字符
```

## 15. 还原路线 / 工程优先级

### 15.1 最高优先级

1. **抓 SDK 内置 5 个 AES key 的 base64 密文** → 用 master key `FqJ***pwb` + 固定 IV 离线解出明文
2. **抓阿里云 OpenAPI 的 AccessKeyId/Secret 一对**：Captcha API 一对 + Device API 一对（前者 `LTAI*****xmvT`，后者 `LTAI5tGjnK9uu9GbT9GQw72p`，硬编码在 SDK，可静态扒）
3. **离线复现 Log1 → InitCaptchaV3 → Log2 → Log3 → VerifyCaptchaV3 链路**（除 `data` 字段外其它都是直 AES/HMAC，可纯 Python）
4. **解决 `data` 字段 VM 加密**（最大硬骨头）

### 15.2 `data` 字段方案对比

| 方案 | 代价 | 健壮性 |
|---|---|---|
| 把动态 `sg.xxx.js` 整包 `execjs.compile()` 跑，Python 只调 entrypoint | 低 | 中（sg.js 会换版本，要做版本探测+缓存） |
| 用 Node.js subprocess + 喂入 trackList 拿出 `data` | 低 | 中 |
| 完整 VM 字节码解释器纯 Python 实现 | 高（要懂 56 个 opcode） | 高（不依赖 SDK） |
| Hook 真浏览器拿出 `data`，离线只做 SDK 调用 + 真浏览器配合 | 中 | 中 |

**推荐**：先走 `execjs/Node subprocess` 路线，再视情况上纯 Python VM 解释器。

### 15.3 轨迹生成

服务端按 `mp / mc / mu / mm` 几条曲线做行为检测：

- 完美直线（恒速、固定步长）→ 必拒
- 完美贝塞尔（无抖动）→ 拒
- 短时（< 800ms） → 拒
- 长时（> 5s） → 拒
- 终点没微调 → 疑似机
- 缺 mousemove 起步（直接 mousedown 在终点）→ 拒

**建议生成器特征**：

- 总时长 1.4-2.6s 均匀采样后加抖动
- 加速→匀速→减速三段，每段时长比 `30:50:20` 上下浮动
- 终点过冲 4-12px，再回拉 2-3 次微调
- 每个 mousemove 间隔 8-24ms 随机
- y 轴抖动 ±2px
- 总采样数 60-110 个点

### 15.4 通过率指标

CSDN 公开案例报通过率：
- 朴素轨迹 + 完整 SDK 调用：~80%
- 加 IP 轮换 + 真实 Canvas/WebGL 指纹：~95%
- 加 `securityToken` 校验旁路：100%（但 token 复用窗口短）

## 16. 已知公开研究（captcha-open v2）

| CSDN id | 标题 | 价值 |
|---|---|---|
| 157979356 | 阿里 v2 验证码算法逆向分析报告 | **最完整**，给出 5 个 AES key 槽 / 99 字段 / 54 字段 / Canvas 算法 / VM 操作码 / Python 签名样例 |
| 140178182 | 阿里 v2 滑块—南航最新版逆向分析思路 | 4 步链路 + 动态参数清单 |
| 158543704 | 南航 阿里 v2 滑块 | 给出 initV3 / verify execjs 调用样例 |
| 144133912 | 滑动验证码采集专栏，某 v2 分析 | （未抓到正文） |

## 17. 待研究 / 进一步深挖

- VM 字节码 (`L` / `F`) 是否可以静态翻译成等价 Python（写个 56 opcode 解释器）
- SDK 动态拉的 `sg.xxx.js` 在 NoteGPT 配置下走哪条 CDN 路径
- `securityToken` 是否能跨 sceneId 复用
- Captcha API 的 AccessKeySecret（`dYSKfs****F9r89koz`）是否所有租户共用（强烈怀疑共用，因为是浏览器明文常量）
- ali150 WASM 与 captcha-open v2 是不是同源 → 推测**不是**，captcha-open v2 走的是 CryptoJS + sg.js VM，没 WASM
