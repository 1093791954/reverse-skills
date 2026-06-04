---
name: riskcontrol-analysis
description: 用于在合法授权前提下分析移动 App / iOS / Web / H5 / 小程序 / PC 浏览器风控、反爬、设备指纹、加密参数还原与人机验证对抗的通用工作流。覆盖 Android 大站参数（x-gorgon, x-argus, x-ladon, x-khronos, mtgsig, h5st, anti_content, x-bogus, x-s, x-zse-96, w_rid, encSecKey, acsToken, __NS_sig3 等）、iOS 反越狱与 App Attest / DeviceCheck / SEP、Web 反爬厂商（Akamai sensor_data / _abck、Cloudflare Turnstile / cf_clearance、PerimeterX、DataDome、Kasada、Imperva reese84、F5 Shape、reCAPTCHA、hCaptcha、Arkose、GeeTest 极验、网易盾 NECaptcha、数美、顶象、Vaptcha、阿里盾 _bx-v）、浏览器/TLS 指纹（JA3/JA4/JA4+、JARM、HTTP/2 frame、UA-CH、Canvas/WebGL/AudioContext）、jsvmp/AST 解混淆/补环境/纯算还原、ARM64 BR 花指令去除、字符串解密器识别、四层加密栈（5 行明文 → SHA256 → 修改版 AES → RC4/HMAC）、X25519 ECDH、修改版 MD5/HMAC/AES、Frida/Xposed/LSPosed/Magisk/Zygisk/KernelSU 反检测、Play Integrity / TEE Key Attestation / Verified Boot、unidbg/qiling 黑盒模拟、SSL Pinning bypass、JA3 / JA4 mimic、wxapkg 解包、滑块/点选 OCR、reCAPTCHA v3 score warming、IP 信誉与设备指纹复制等。当任务涉及风控参数还原、加密签名分析、Web/App 反爬、设备指纹、滑块验证码、TLS 指纹、jsvmp 还原、补环境、root 检测对抗、anti-frida、anti-debug、x25519、修改版 AES/MD5/HMAC、5 行明文签名、上传 schema (a/c/d/e/g/k/p/s/u/v)、APK 砸壳/iOS 砸壳、Mach-O 加固、wxapkg、抖音/TikTok/小红书/京东/拼多多/淘宝/美团/B 站/网易云/快手/微博/知乎/boss直聘/12306/Apple ID/Gmail 注册等场景的合法授权研究时使用。
---

# 风控分析（riskcontrol-analysis）

把已收集的（小红书 / 后续会补充的其他平台）风控逆向资料，整理为一套可复用的分析工作流。目标是在合法授权前提下，把"风控 SDK 黑盒"拆成可解释的几层：原生 SO 反混淆 → 字符串/JSON 还原 → 设备指纹字段映射 → 加密栈分层 → 反检测清单 → 上传 schema → 离线回放校验。

## 边界（Boundary）

- 仅用于自有 App、受邀渗透、漏洞研究、安全合规审计、红蓝对抗、个人研究等**已授权**场景。
- 不为绕过商业风控、规避反爬封禁、批量伪造设备指纹、对抗付款/版权/防作弊等场景提供"现成可用"的成品代码或攻破方案。
- 当请求是 "过 xxx 风控 / 还原 xxx 加密参数"，先在内部翻译为：①样本归属与授权确认 → ②静态去混淆 → ③字符串/JSON ABI 还原 → ④加密栈分层 → ⑤反检测清单 → ⑥离线回放验证 → ⑦撰写分析备忘。
- 若用户没有给出授权来源，仅停留在"机制解释 + 工作流"层面，不给具体设备指纹伪造模板。

## 总体工作流（Workflow）

按下列 12 步推进；每一步都有对应的 Path 段落详细展开。

1. **样本归类与授权确认**：包名、版本号（versionName / versionCode 双重）、目标 SO、关键参数名（mua / sig / shield / token / X-Sign / X-Gorgon …）。
2. **Native 反混淆（前置）**：识别并修复 ARM64 BR 花指令（8 类），保证后续静态分析可读。详见 *Native Obfuscation Path*。
3. **定位字符串解密器**：用 6 特征签名搜索，批量解密整个 SO 中的常量串，露出 `getprop` key、JSON key、API endpoint。详见 *String Decryptor Discovery Path*。
4. **还原 JSON 节点 ABI**：识别 SSO（Small String Optimization）+ 红黑树/容器节点布局，写一个 Frida 读取器，运行时直接 dump 任意 JSON。详见 *Fingerprint JSON Reverse Path*。
5. **整理 xN 参数清单**：把每一个数字化键（`x0..x308`）追溯到来源（getprop / Java 反射 / Linux syscall / 自检函数），分组归档。
6. **检测项 vs 数据项分类**：把 xN 字段拆成"被动采集（passive）"与"反检测探针（probe）"两类。详见 *Anti-Detection Triage Path*。
7. **识别四层加密栈**（5 行明文 → 哈希 → 修改版 AES → RC4/HMAC 外层）。详见 *Crypto Stack Path*。
8. **识别密钥协商层**：典型为 X25519 + 硬编码 server pubkey，`shared_secret[0:16]` = AES key、`[16:32]` = IV，client_pub 走 `k` 字段上报。
9. **识别签名层（sig 类）**：通常是对同一份 5 行明文的 SHA256 + 一个 128×128 GF(2) 仿射变换（`transform_16` 模式）。
10. **整理上传 schema**：通用信封形如 `{a, c, d, e:{dd,device_id,kk,now,rr,sid,tt,uid,vv}, g, k, p, s, u, v}`。详见 *Endpoint & Schema Path*。
11. **离线回放验证**：用恢复的密钥/IV/常量轮密钥写 `xxx.py`，在脱机环境复现密文；用同 device_id 多次采样比对。详见 *Replay Validation Path*。
12. **横向校验姊妹接口与心跳**：`register / cfg / profile` 通常共用密钥；心跳 `t` 字段编码两阶段（init / active）能力位，复制时要走完 `c<100` 才会进入 active。

---

## Native Obfuscation Path（ARM64 BR 花指令去除）

适用：拿到一份 SO，IDA 反编译大量函数被打断成"伪基本块 + `BR Xt`"碎片，无法静态阅读。

总体策略：写一个 ARM64 局部模拟器，从基本块入口模拟到 `BR Xt`。若 `BR` 寄存器是确定的 `.text` 内地址 → 重写 `BR Xt` 为 `B target`；不能确定 → 保留原 `BR`。CSEL/CSET 用多状态分裂模拟。表读用 ELF/relocation 解析。索引型 `LDR ... LSL #3 ; ... ; BR` 在条件严苛时用 angr 接管。

8 类 BR 花指令模式（按从简到难）：

1. **常量构造型**：`ADRP+ADD` 或 `MOV+MOVK+ADD` 直接构造目标地址 → `BR Xt`。模拟到 `BR` 即可静态解出 → 重写为 `B target`。
2. **静态表读型**：`ADRP X13,table; ADD X13,...; LDR X9,[X13,#off]; ADD X9,X9,W10,SXTW; BR X9`。先解出表基址，再从 ELF/relocation 读条目。如果索引由 `CSEL/CSET` 提供 → 走第 3 类。
3. **CSEL/CSET 条件分派型**：`CMP/TST/CMN` 设置标志后 `CSEL/CSET/CSINV/CSINC/CSNEG` 选两个状态再 `BR`。模拟器要分裂成两条并行状态走到 `BR`，两端目标都能静态解出时重写为 `B.cond target_true ; B target_false`。
4. **真实副作用型**：`BR` 之前夹带 `STR/MOV` 等真业务副作用，不能丢。把可安全前移的副作用上提到补丁区开头，再写 `B.cond + B`，原位置 NOP。例：

   ```asm
   0x3AC8E0  STR X15, [X19,#0x468]
   0x3AC8E4  MOV X12, X15
   0x3AC8E8  B.NE 0x404E14
   0x3AC8EC  B    0x367A3C
   0x3AC8F0  NOP
   0x3AC8F4  NOP
   ```

5. **纯载体垃圾块**：仅做 "对载体寄存器 ± 常量" 然后 `BR`。两种形态：
   - 形态 A：`MOV X8,#neg_const ; ADD X8,X9,X8 ; BR X8` 或先 `LDR X9,[X19,#field]` 再加常量。
   - 形态 B：`ADRP X8,off ; LDR X8,[X8,#off] ; MOV X10,#a ; MOV X9,#b ; MOVK X10,...; MOVK X9,...; ADD X8,X8,X10 ; ADD X12,X12,X9 ; BR X12`。

   策略：把状态传播过载体块，**只重写"上游业务分支"** 到最终目标；**不要**重写载体自身的 `BR`（否则会制造伪静态 xref）。如果上游就是 CSEL/CSET 单状态求值得 UNKNOWN，必须把上游升级为多状态模拟，再重写**它**的分支。

   小红书 libtiny.so 中应保留为 `BR` 的载体地址（白名单示例）：`0x19FDBC`、`0x37C7D4`、`0x3FF9AC`。

   工作样例（`0x4AAD3C`）：

   ```asm
   0x4AAD34 CMP  W10, #0
   0x4AAD38 CSEL X8, X8, X9, NE
   0x4AAD3C B    0x4AAE00          ; 进入载体
   0x4AAE00 LDR  X9, [X28,#0xB50]
   0x4AAE14 ADD  X9, X9, X11
   0x4AAE18 ADD  X8, X8, X10
   0x4AAE1C BR   X9
   ```

   `X28 = 0x772000` 为锚点，`[0x772000+0xB50]+const` 解出载体目标 → 把 `0x4AAD38` 改写为：

   ```asm
   0x4AAD38 B.NE 0x4AA6A8
   0x4AAD3C B    0x4AA62C
   ```

6. **保存域链型**：`STR X10,[X19,#field] ; B mid ; mid: LDR X9,[X19,#field] ; ADD X8,X9,#off ; BR X8`。模拟器要把 `[reg+off]` 表达成符号化 memory key，写入是确定地址时，未来同 key 的读取就能恢复。允许多层 `B → mid → carrier → BR`。仅对**已验证过的** saved-field key 启用，否则误重写。
7. **真调用尾分派型**：`BL some_func` 之后紧跟 `ADD X9,X9,W10,SXTW ; BR X9`。默认载体 `BR` 不重写；但当分派紧跟 `BL/BLR`，属于真业务路径，可以重写（例：`0x185F40 → B 0x19E0E4`）。
8. **小型索引开关 + angr 兜底**：`ADRP X10,table ; ADD X10,... ; LDR X8,[X10,X8,LSL#3] ; MOV X10,#... ; MOVK X10,#... ; SUB X1,X9,#1 ; ADD X8,X8,X10 ; BR X8`。

   严格条件：①索引 `LDR Xt,[base,index,scale]` 的 `Xt` 终结于 `BR Xt` ②表基址静态可解 ③枚举条目仅 2~3 项 ④目标必须是前向短距 (`<0x100`) ⑤补丁区容得下"副作用 + CMP/B.EQ + B" ⑥幸存副作用可安全前移、不依赖目标计算用的临时寄存器 ⑦用 angr 从索引 `LDR` 步进到 `BR` 验证每个 index 目标 ⑧用 `SYMBOL_FILL_UNCONSTRAINED_*`，**不要**用 zero-fill（避免把未知误判为 0）。

   样例（`0x1A5788`）：

   ```asm
   0x1A5774 LDR X8, [X10,X8,LSL#3]
   0x1A5778 MOV X10, #...
   0x1A577C MOVK X10, #...
   0x1A5780 SUB X1, X9, #1
   0x1A5784 ADD X8, X8, X10
   0x1A5788 BR X8
   ```

   静态枚举 + angr 确认：index 0 → `0x1A578C`、index 1 → `0x1A5798`、index 2 → `0x1A57A4`。重写：

   ```asm
   0x1A5774 SUB X1, X9, #1
   0x1A5778 CMP X8, #0
   0x1A577C B.EQ 0x1A578C
   0x1A5780 CMP X8, #1
   0x1A5784 B.EQ 0x1A5798
   0x1A5788 B    0x1A57A4
   ```

**完成标准**：没有任何业务节点跳进载体垃圾区；保留下来的 `BR` 都是已确认的纯载体块，不再需要被静态求值。

---

## String Decryptor Discovery Path（字符串解密器发现）

风控 SO 的字符串解密器有非常稳定的 6 特征签名，IDA 反编译后特征如下：

| # | 特征 | 反编译可见 |
|---|---|---|
| 1 | 2 个参数 | `result, a2` |
| 2 | 神奇右移 | `0xMAGIC >> (8 * (x & 3))`（小红书 MAGIC = `0xBD69BD22`） |
| 3 | 小模数 switch | `switch (i % 5)` 或 `% 4 / % 6 / % 8` |
| 4 | 5 种操作 | `eor / mvn / sub / lsl(+shift) / lsr(+shift)`（XOR、按位非、减法、循环左移、循环右移） |
| 5 | do-while | 末尾 `cbz/cbnz` 比较计数 |
| 6 | 原地写回 | `*ptr = *ptr ⊕ key` 写回原字节 |

伪代码模板（小红书形态）：

```c
do {
    v8 = *v_counter;
    v9 = 8 * (v8 & 3);
    v10 = MAGIC >> v9;             // MAGIC = 0xBD69BD22
    v11 = v10 - 7 * ...;
    v12 = v11 + 1;
    switch (v8 % 5) {
        case 0: *out = *in ^ v10;        break;
        case 1: *out = *in ^ ~v10;       break;
        case 2: *out = *in - v10;        break;
        case 3: *out = ROTL(*in, v12);   break;
        case 4: *out = ROTR(*in, v12);   break;
    }
    *in = *out;
} while (++i < len);
```

小红书 `libtiny.so` 中匹配到 **10 个** 解密器函数。批量解密后能露出 `getprop` 键名、JSON 路径键、API 路径、错误日志、服务名 → 这是后续工作的"字典"。

通用做法：
- 用 IDA Python 写一个签名扫描器，对每个函数检查这 6 个特征。
- 命中后，把所有调用点 (`xref`) 的"解密器 + 密文常量"配对 dump，离线模拟解密。
- 如果魔数 / 模数 / op 数变了，更新签名后重扫；模板基本不变。

---

## Fingerprint JSON Reverse Path（设备指纹 JSON 节点还原）

`libtiny.so` 类风控 SDK 通常用 SSO（Small String Optimization）+ 红黑树 / 自定义 map 来维护设备指纹，节点 ABI 一般如下（小红书的具体值）：

### SSO 字符串槽（24 字节，`0x18`）

```
小串（hdr 偶数）：
  [hdr (1B)] [data (23B)]
  len = hdr >> 1
  data 起始地址 = ptr + 1

大串（hdr & 1 != 0）：
  [hdr (1B)] [pad (7B)] [len (8B QWORD)] [data_ptr (8B)]
  len 在 ptr+8
  data_ptr 在 ptr+16
```

Frida JS 读取器（直接可用）：

```js
function readSmallStr(ptr) {
    if (ptr.isNull()) return "";
    try {
        var hdr = ptr.readU8();
        var len, buf;
        if ((hdr & 1) !== 0) {
            len = ptr.add(8).readU64().toNumber();
            buf = ptr.add(16).readPointer();
        } else {
            len = (hdr >>> 1);
            buf = ptr.add(1);
        }
        if (len === 0) return "";
        if (len > 0x100000) return "";  // 防垃圾
        return buf.readUtf8String(len);
    } catch (e) {
        return "";
    }
}
```

### JSON 节点（72 字节 / `0x48`）

```
+0x00  8   left  child
+0x08  8   right child
+0x10  8   parent
+0x18  8   color/metadata（红黑树）
+0x20 24   key（SSO 字符串）
+0x38  1   value type tag
+0x40  8   value data
```

值类型 tag：

| tag | 含义 | data 内容 |
|---|---|---|
| 0 | null | – |
| 1 | object | 子树容器指针 |
| 2 | array | vector 指针 |
| 3 | string | SSO 字符串指针 |
| 4 | bool | 非空表示 true |
| 5 | int64 | 直接 i64 |
| 6 | uint64 | 直接 u64 |
| 7 | double | 直接 double |

拿到这两套布局之后，写一个递归 `dumpNode(ptr)` 即可在运行时把任意指纹 JSON 整树打印出来 → 此后所有 `xN` 字段一目了然。

---

## Crypto Stack Path（四层加密栈）

国内大多数风控参数遵循一个**四层 + 一层密钥协商**的可复用模板：

### Tier 0 — 密钥协商（X25519 ECDH）

```
priv = random(32B)
client_pub = X25519(priv, basepoint=9)
shared    = X25519(priv, server_pub_hardcoded)
aes_key = shared[0:16]
aes_iv  = shared[16:32]
```

`client_pub` 通过外层信封的 `k` 字段上报；`shared` 永远在客户端内存里，不外传。

### Tier 1 — 5 行明文组装

```
METHOD\n
PATH\n
QUERY\n
SHA256(BODY).hex()\n
JWT_OR_MUA
```

这是大多数 `sig / s1 / mua` 的"待签明文"。换行符、是否大写 hex、QUERY 是否排序，都可能是变体点。

### Tier 2 — 哈希摘要

- 朴素形式：`SHA256(plain)`。
- 加固形式（小红书 `x-mini-sig`）：`transform_16(SHA256(plain)[0:16]) || SHA256(plain)[16:32]`。`transform_16` 是 GF(2) 上的 128×128 仿射变换 + 16 字节常量偏移，对应 5288 条 ARM64 NEON 向量指令压缩成一个二进制矩阵。
- 输出常见形式：64 字符 hex / Base64 / Base64URL。

### Tier 3 — 对称体加密（往往是修改版 AES）

- 标准 AES-128-CBC（小红书 `x-mini-mua`：标准 AES + zlib 压 JSON）。
- 修改版 AES-128-CBC（小红书 `x-mini-s1` 与 `aes_decrypt_main_hmac`）：
  - 表驱动的 `mix_columns`（行列混淆矩阵非标准）。
  - 自定义 `shift_perm`。
  - 固定 round keys + prewhiten key（与 KeyExpansion 无关）。
  - 或反过来：以 `DeviceId[:16]` 做种子，经过自定义 XOR 常量、改造的 Rcon、改造的 `WordRotate/SubWord` 生成 11 条轮密钥。

### Tier 4 — 外层封装（RC4 / Base64 / HMAC）

- 路线 A（mua 风格）：`base64url(header_json) "." base64url(ciphertext) "."`。
- 路线 B（shield 风格）：`"XY" + Base64(16B header + RC4_ct)`，RC4 用一段**伪装成代码字符串的硬编码短 key**，例如 `"std::abort();"`（13 字节）。
- HMAC 路线：HMAC-MD5 with **修改的 Round 1~4 shift / K 常量 / 初始 IV**，pipeline 中夹一次 NEON 128-bit 字节反转。

### Tier 5 — `raw44` / 包打包 + libc rand 扰乱（s1 风格变体）

`x-mini-s1` 风格的"包"打法：`raw44 = [4B timestamp][2B encoded][2B encoded][hash32][CRC32]`，再用 libc `rand()` 产生 shuffle 索引重排一张固定 `pair_table`，最后 Base64：`[counter][ciphertext][crc_a][crc_b]`。

> 经验法则：**永远先假设 AES 是被改过的、MD5/HMAC 是被改过的、Rcon/IV 是被改过的**。和标准库对比能匹配只是表面；实际密钥/常量必须从 trace 里抠出来。

---

## Anti-Detection Triage Path（反检测项清单）

把 SDK 上报的字段拆成两类：被动数据 vs 主动探针。常见探针清单（参考小红书 200+ 字段中的探针子集）：

- **文件系统探针**：`/proc/self/maps`（找 trampoline / 未知 .so）、`/data/data/<pkg>` 与其 `..` 路径别名（路径混淆校验）、`/proc/bus/input/devices`（输入设备真实性）。
- **函数序言指纹**：直接读取关键函数前 4 字节，期望 `FD 7B BF A9` = `STP X29, X30, [SP, #-16]!`。被 Frida inline hook 替换成跳板会立刻暴露。
- **代码段周期性自校验**（`code-patch-check`）：枚举 9 段固定内存范围，对每段算一对 64-bit 哈希（疑似 SipHash 类带种子）。任何与基线不符即"detect tiny code patch!"。
- **DEX 完整性**：枚举 ClassLoader 加载链上的 dex/jar 路径，特别盯 `Anonymous-DexFile@xxx.jar`（Robust 类热修复）和 `base.apk!classes2..22.dex` 的 MD5。
- **Java 反射探针**：枚举 Java 端是否有已知 hook 框架的回调类，例如 `XvFWWExBridge$HookerCallback`。
- **TEE Key Attestation**：5 级 X.509 证书链（Key Attestation CA → Droid CA2 → Droid CA3 → TEE app cert → Android Keystore Key），扩展里嵌入包名与设备型号。这是**软件层最难绕过**的一项。
- **系统态探针**：SELinux `enforcing`、Verified Boot color = `green`、`release-keys`（官方签名）、cgroup 路径 (`3:cpuset:/top-app` 等)、`availableProcessors()`、`Build.IS_EMULATOR`。
- **GPU 模拟器特征**：真机 `vendor=ARM, renderer=Mali-G78`（或 Adreno、PowerVR、Apple GPU）；模拟器 = `Swiftshader / ANGLE / VirGL / llvmpipe`，几乎没法假。
- **冗余交叉校验**：同一指纹连读 5 次（小红书 `x144`），冗余电池百分比（`x34/x35`），冗余存储字段（`x231/x232`、`x236/x237`）。replay 时这些必须保持一致。
- **设备唯一性**：APK signature SHA384 (`x146`)、ECDSA-P256 DER 签名（`x303` 72B）、MD5 fingerprint key id（`x302` `kk`）。

---

## Endpoint & Schema Path（接口与上传 schema）

### 通用上传信封

```jsonc
{
  "a": "<App ID, 固定常量>",
  "c": <序列号 / 计数>,
  "d": "<core 加密载荷, 见 Tier 1~4>",
  "e": {
    "dd": <采集时间戳 ms>,
    "device_id": "<UUID 形式>",
    "kk": "<完整性校验, MD5 fingerprint key id>",
    "now": <请求时刻 ms>,
    "rr": "0",
    "sid": "<session id>",
    "tt": "<ECDSA P-256 DER, base64>",
    "uid": "<用户 ID 或匿名占位>",
    "vv": 1
  },
  "g": "<APK 签名 SHA384>",
  "k": "<X25519 client_pub, 32B hex>",
  "p": "a",            // a=Android, i=iOS
  "s": "<sig 64 hex>",
  "u": "<UID>",
  "v": "<SDK 版本>"
}
```

### 三个姊妹接口（共用密钥）

| 接口 | 用途 |
|---|---|
| `/api/v1/register/android` | 设备注册 / 首次握手 |
| `/api/v1/cfg/android` | 拉取下发配置 |
| `/api/v1/profile/android` | 完整设备指纹上报（`d` 最大） |

### 旁路接口（可作交叉验证锚点）

- `https://apm-native.xiaohongshu.com/api/collect` — APM 性能上报（gzip，UA `okhttp/3.14.9.033`）。
- `https://t2.xiaohongshu.com/api/collect` — 数据采集（gzip，~879B）。
- `https://edith.xiaohongshu.com/api/...` — 业务主接口，命中 `OkHttp CacheInterceptor`。

### 心跳 t 字段两阶段

```
init     (c=1..99) :  t = {c:0,  d:0, f:0, s:4098, t:0,        tt:[]}
active   (c≥100)   :  t = {c:45, d:4, f:0, s:4098, t:68577897, tt:[1]}
```

- `c` = 已完成的风控检测周期。
- `d` = 检测到的状态变化次数。
- `s = 4098` 常量。
- `t` = 单调累加的事件计数（例 `0x4166A69`）。
- `tt = [1]` = 触发的检测类型位。

回放时必须真实跑完 `c<100` 才能进入 active，否则后端能从心跳节奏识别异常。

---

## Replay Validation Path（离线回放验证）

成功标准：用 trace 中抠出的常量 + 当前 device_id + 当前 5 行明文，能在脱机 Python/Node 里独立产出与抓包一致的 `d / s / shield`。

清单：
1. 把所有硬编码常量（`MAGIC`、RC4 key、修改版 AES 11 条轮密钥、HMAC IV、`pair_table`、`shift_perm`、modified MixColumns 矩阵）从 trace dump 出独立 `consts.py`。
2. 写 `derive_hmac_key(device_id) -> 64B`：复刻 `aes_decrypt_main_hmac`。
3. 写 `mua(json) -> str`、`s1(method, path, query, body, jwt) -> str`、`sig(method, path, query, body, jwt) -> str`、`shield(struct83) -> str`。
4. 用同一台设备跑两次：抓包 1 与抓包 2 比对，验证 `mua/s1/sig/shield` 输出与抓包**逐字节一致**。
5. 横跨三接口（`register / cfg / profile`）复用同一密钥再验。
6. 离线工具命名建议：`shield.py` / `mini_mua.py` / `mini_s1.py` / `mini_sig.py`。

---

## Web Path（网页端风控通用工作流）

**适用**：浏览器端的 Cookie / Header / Body 加密参数（`sensor_data` / `_abck` / `cf_clearance` / `__cf_bm` / `_px3` / `datadome` / `reese84` / `x-kpsdk-ct` / `x-bogus` / `x-s` / `h5st` / `mtgsig` / `acs-token` / `__zp_stoken__` / `encSecKey` / `w_rid` / `x-zse-96` / `RAIL_DEVICEID` / `anti_content` 等）。

**通用模型**（先按这个顺序套，再判断卡在哪一层）：

1. **Cookie / Header / Body 三栏分类**：把抓包看到的所有可疑参数按生成方式分类。Cookie 类（如 `_abck`、`cf_clearance`、`__zp_stoken__`、`reese84`、`acw_sc` 等）通常由前置 challenge JS 在 `document.cookie =` 设置；Header 类（如 `x-bogus`、`x-s`、`acs-token`、`mtgsig`、`x-kpsdk-ct`、`x-zse-96`）多由 fetch/xhr 拦截器在请求发出前注入；Body 类（如 `params`/`encSecKey`、`anti_content`、`h5st` 的部分字段）由业务代码同步算出。
2. **加载链回溯**：先抓 HTML → 找返回 202/429 拦截页 → 拿到 `<script src=...>` 或 `eval(atob(...))` 的 challenge JS。Akamai 是 `_bm-challenge.js` / `bm-verify`、Cloudflare 是 `cdn-cgi/challenge-platform/h/.../orchestrate/managed/v1`、PerimeterX 是 `*.PXxxxx.js` + `init.js`、DataDome 是 `tags.js` + `captcha-delivery.com`、Kasada 是 `ips.js`、Imperva 是 `_utmvc` + `reese84`。
3. **混淆识别**：识别 obfuscator.io（数组+字符串解密器+控制流平坦化）、jsvmp（自定义字节码 + dispatcher loop）、TENCENT_CHAOS_VM（多 opcode 表）、WASM 插值（pdd `anti_content`、Kasada 部分）。jsvmp 的特征是一段巨大的字节数组 + `switch(opcode){...}` 模式 + 寄存器风格的虚拟栈。
4. **三选一还原方法**：
   - **RPC 远程调用**：把混淆 JS 跑在 jsdom/browser 里，主程序 RPC 调用。最快但需要常驻。
   - **补环境（缺啥补啥）**：`document/navigator/window/location/setTimeout/HTMLImageElement/TextEncoder/Intl/Performance...`，依赖 `pysunday/sdenv`、`vm2`/`isolated-vm`、`jsdom`。常见的反检测点：`__filename` / `Buffer` / `process` 在 nodejs 是 truthy，在浏览器是 undefined，会被 `Object.keys(window)` 长度差异、`Function.toString().length` 等校验出来。
   - **纯算还原**：把 jsvmp 字节码 + dispatcher 用 Python/Go 重写。耗时最长但最稳。`pysunday/rs-reverse`（瑞数）、`B1gM8c/X-Bogus`、`Cloxl/xhshow`（小红书）等是可参考实现。
5. **TLS / HTTP/2 指纹层**：`requests`/`httpx`/`okhttp` 在 ClientHello、ALPN、cipher suites、HTTP/2 SETTINGS 帧、PRIORITY/WINDOW_UPDATE 顺序上都和 Chrome/Firefox 不同；许多厂商（CF、Akamai、PX）会用 JA3/JA4 + HTTP/2 fingerprint 作为前置过滤。解决方案：`curl-impersonate`、`bogdanfinn/tls-client`、`refraction-networking/utls`、`zhkl0228/impersonator`、`curl_cffi`。详见 *Fingerprint Path*。
6. **轨迹 / 行为风控层**：滑块 / 点选 / 无感都需要"鼠标轨迹"，曲线靠贝塞尔 + 加速度抖动 + 真人录制拟合；详见 *Captcha Path*。
7. **离线回放校验**：固定 `device_id` + 固定 `timestamp` 跑两次，hash 必须 byte-by-byte 一致；如果不一致，回到第 4 步看哪一项是动态熵源（常见：随机 IV、`Date.now()` 近似匹配、`Math.random()`、加密未关 padding）。

**典型变体识别表**：

| 厂商/参数 | 形态 | 关键词 |
|---|---|---|
| Akamai sensor_data | Cookie `_abck`+POST `sensor_data`，jsvmp v1→v3 | `bm_sz`/`bm-verify`/`cKH 类`/`cKH.bx-pp`/8 段拼接 |
| Cloudflare Turnstile | Cookie `cf_clearance`+`__cf_bm`，managed challenge JS+Turnstile widget | `cdn-cgi/challenge-platform/h/.../orchestrate`/`window._cf_chl_ctx` |
| PerimeterX (HUMAN) | Cookie `_px2`/`_px3`/`_pxhd`/`_pxvid`，主 JS `main.min.js` | `cssCheck`/`bake_appId`/3 bundle+1g 请求 |
| DataDome | Cookie `datadome`+`tags.js`+`captcha-delivery.com` | `dd_t`/`dd_s`/`x-dd-b`/POST `js-data` |
| Kasada | Header `x-kpsdk-ct`/`x-kpsdk-cd`/`x-kpsdk-im`+`ips.js` vmp | `/tl`/`/ips.js`/payload 由 vmp 跑出 |
| Imperva | Cookie `incap_ses`/`visid_incap`/`reese84`+`_utmvc` | `___utmvc`/`/_Incapsula_Resource` |
| reCAPTCHA v2/v3 | iframe anchor+bframe，token `recaptcha-token` | `grecaptcha.execute`/`reload?k=`/audio challenge |
| GeeTest 极验 4 | `gt`/`challenge`/`w`，POST `/load`+`/verify` | `lot_number`/`payload`/`pow_msg`/`pow_sign` |
| 网易盾 NECaptcha | `id`/`token`/`fp`/`actoken`/`data`/`validate`/`NECaptchaValidate` | 滑块取轨迹前 50 位加密；`cb` 与 `data` |
| 数美 Blackbox | `tokenId`/`profile.json`+`fp` | 3DES + RSA |
| 顶象 const-id | `constId`/`bx-pp`/`bx-et`/`slidedata` | dx 滑块 + canvas 切割 |
| 阿里 x5sec | Cookie `x5secdata`+POST `/_____tmd_____/punish` | `bx-pp`/`bx-et`/`slidedata`/`sg.js` |
| 抖音 Web | Header `X-Bogus`/`_signature`/`x-tt-params`/`msToken` | jsvmp + webmssdk.js + ttencrypt |
| 小红书 Web | Header `x-s`/`x-t`/`x-s-common`/`x-mns` | webpack + signSvn 版本号 + VMP |
| 京东 h5st | Header `h5st`+Cookie `_jdb_`+`x-api-eid-token` | 8 段结构 + jsvmp + AES + fp 一致性 |
| 拼多多 anti_content | POST `anti_content`（base64 嵌套+多层 zlib+WASM） | `0CN0H...` 起始/CSP-Report-Only |
| 美团 mtgsig | Header `mtgsig`+`_token`+`x-mt-bx-v` | h5guard.js + WASM v3.0/4.x |
| Boss 直聘 | Cookie `__zp_stoken__`+`zp_token` | 控制流平坦化 + 动态代码 |
| 12306 | Cookie `RAIL_DEVICEID`+`RAIL_EXPIRATION` | logdevice + hashAlg dict |
| 网易云音乐 | POST `params`+`encSecKey` | AES-CBC（i 参数） + RSA |
| 知乎 x-zse-96 | Header `x-zse-96`+`x-zst-81`+`d_c0` | jsvmp + SM4 + 自定义编码 + 版本号拼接 MD5 |
| 百度 acs-token | Header `Acs-Token`+`ab_sr` | AES + 环境检测 + "玉门关"自注释 |
| bilibili wbi | Query `w_rid`+`wts` | imgKey+subKey 混合 mixinKey |
| 快手 web | `__NS_sig3`+`__NStokensig`+`kpf`/`kpn` | sub_3FDA4 + sha256 魔改 + base64x2 |

**Tips**：
- **不要在抓 HTML 之前就开搜参数关键字**：很多 challenge JS 是在 HTML 里 `eval(atob(...))` 注入到 window 的，而 DevTools 的 Sources 面板看到的"压缩后的 JS"和实际跑的"动态注入 JS"不是同一份。
- **`debugger` 关键字陷阱**：CF/瑞数/PX/Akamai 都会有反调试形如 `(function(){var a=...; if(...) { while(true){} } })()`，先用 `Override` 把这段 NOP 掉再调试。
- **请求顺序也是指纹**：先取 HTML→静态 JS→jsvmp→`/init`→业务，少一步都会被识别。
- **TLS 指纹与 JS 计算无关**：即使你 JS 算对了，但 `requests` 的 ClientHello 与 Chrome 不一样，仍可能 403。先 `tls.peet.ws` 验证你的 client 指纹。

详见 [references/web/](references/web/)、[references/captcha/](references/captcha/)、[references/fingerprint/](references/fingerprint/)。

---

## Captcha Path（人机验证 / 滑块 / 点选 / 无感）

**适用**：极验 v3/v4、网易盾 NECaptcha、数美、顶象、Vaptcha、同盾、阿里 NoCaptcha/x5sec、Cloudflare Turnstile、reCAPTCHA v2/v3/Enterprise、hCaptcha、Arkose Labs FunCAPTCHA、DataDome 滑块。

**通用四件套**：
1. **指纹采集**：Canvas / WebGL / Audio / Font / `navigator.*` / `screen.*` / `window.chrome` / `Notification.permission`、`Permissions.query()`、`MediaDevices.enumerateDevices()` 等。绝大多数 captcha 厂商都先生成一个 `device_id` / `fp` 并和后端绑定。
2. **轨迹生成**：滑块需要 `(t, x, y, action)` 序列，最大值范围 600-1500ms，曲线遵循贝塞尔；时间间隔 ~16ms（60fps）但要带 ±2-5ms 抖动；起始几个点必须有"思考停顿"。`x82y`、`GeetestReverseEngineering`、`DingxiangCaptchaBreak` 都给了示例轨迹模型。
3. **PoW / 密钥协商**：极验 4 有 `pow_msg`/`pow_sign`（CPU 暴力搜索）；reCAPTCHA v3 给"分数"（warming session+稳定 cookie+真人鼠标轨迹能拉到 0.7+）；Arkose 的 BDA 是浏览器指纹+key 协商；Kasada 用 `ips.js` 跑一段类 vmp PoW。
4. **图像识别**：滑块缺口 `cv2.matchTemplate` 或 `ddddocr.slide_match()`；点选用 `ddddocr.det+ocr` 或 `YOLOv8 + CLIP`；旋转字 `imagenet pretrained CNN`；语音验证用 Whisper / Vosk。

**典型识别签名**（看到这类 cookie/参数立刻判定厂商）：

| 厂商 | 关键签名 |
|---|---|
| 极验 v3 | `gt`/`challenge`/`w` 三件套；URL 含 `/static/js/slide` |
| 极验 v4 | `lot_number`+`payload`+`process_token`+`pow_msg`+`pow_sign` |
| 网易盾 | `NECaptchaValidate`+`actoken`+`fp`+`/api/v2/{init,get,check}` |
| 数美 | `tokenId`+`profile.json`+`organization`+RC4+3DES+RSA |
| 顶象 | `constId`+`bx-pp`/`bx-et`+`x82y` |
| 阿里 NoCaptcha | `x5secdata` cookie+`/_____tmd_____/punish`+`bx-v` |
| reCAPTCHA | `grecaptcha`+`anchor.html`+`bframe.html`+`reload?k=` |
| hCaptcha | `hcaptcha.com/captcha/v1/api.js`+`siteKey`+`token` 64 字符 |
| Arkose | `funcaptcha.com`+`bda`+`token` 形如 `xxxxxxx.timestamp\|...`+`/fc/gt2/public_key/` |
| Cloudflare Turnstile | `challenges.cloudflare.com/turnstile`+`cdata`+`flow` |
| DataDome | `captcha-delivery.com`+`/captcha/?initialCid=...`+滑块或 puzzle |
| Kasada | `x-kpsdk-ct`/`-cd`/`-im`+`/ips.js`+`/tl` |

**OCR 工具**：`sml2h3/ddddocr`（一站式：图片 OCR、滑块 slide_match、点选 det+ocr）；`yolov8 + Roboflow` 训练点选样本；`opencv` 模板匹配是滑块兜底方案。

详见 [references/captcha/](references/captcha/)。

---

## Fingerprint Path（浏览器指纹 / TLS 指纹 / 设备指纹）

**三大指纹层**（自上而下都能被检测）：

### 1. JavaScript 端浏览器指纹

- **Canvas**：`canvas.toDataURL()` / `getImageData()` 渲染同一段图形，硬件 GPU+驱动差异让结果有微差。`fingerprintjs2` 用一段固定文字+emoji，结果熵 ≈ 8-10 bit。
- **WebGL**：`getParameter(GL_VENDOR/GL_RENDERER)`、`UNMASKED_VENDOR_WEBGL/UNMASKED_RENDERER_WEBGL`、`getSupportedExtensions()`、shader compile log。能看到 GPU 型号（"Apple M2"、"NVIDIA GeForce RTX 4090"、"Mali-G78"）。
- **AudioContext**：`OfflineAudioContext` 跑一段 oscillator → `getChannelData()` → 哈希。差异来自浮点 + DSP 实现。
- **Font / FontFaceSet**：`measureText` 量字宽，或 `FontFaceSet.check()` 直接试探安装字体。
- **CDP / WebDriver 反检测**：`navigator.webdriver`、`window.chrome.runtime` (无头无)、`Permissions.query({name:'notifications'})` 与 `Notification.permission` 矛盾、`languages` 长度 0、`plugins` 空数组、UA-CH `Sec-CH-UA-Full-Version-List` 缺失、`window.outerHeight==0`、headless `User-Agent` 含 "HeadlessChrome"。
- **隐藏库**：`puppeteer-extra-plugin-stealth`（18 种规避）、`playwright-stealth`、`undetected-chromedriver`、`stealth.min.js`。最难规避的是 `CDP Runtime.evaluate` 级别的 hook + `Object.getOwnPropertyDescriptor(navigator, 'webdriver')` 检测。

### 2. 网络层 TLS / HTTP/2 指纹

- **JA3 / JA3S**：MD5(`SSLVersion,Cipher,Extensions,EllipticCurves,EllipticCurvePointFormats`)。`requests` ≈ 标准 Python 指纹；Chrome/Firefox/Safari 各有特征。
- **JA4 / JA4+**：拓展化、模块化、可读化（不再 MD5）。包含 ALPN、SNI、cipher、extension order、ALPS。
- **JARM**：服务器端 TLS 指纹，用于识别 CDN 后真实源站。
- **HTTP/2 SETTINGS / PRIORITY / WINDOW_UPDATE**：Akamai 用这个判 client；Chrome 的 `INITIAL_WINDOW_SIZE=6291456`、`HEADER_TABLE_SIZE=65536`、`MAX_HEADER_LIST_SIZE=262144`、PRIORITY 树形结构都有特征。
- **HTTP/3 QUIC**：TLS 1.3 帧顺序、`quic-transport-parameters`。
- **绕过工具**：`curl-impersonate`（魔改 curl，模拟 Chrome/FF/Safari/Edge）、`bogdanfinn/tls-client`（Go）、`refraction-networking/utls`（Go）、`curl_cffi`（Python wrapper of curl-impersonate）、`zhkl0228/impersonator`（Java）。
- **指纹自检站**：`tls.peet.ws`、`browserleaks.com/tls`、`tls.browserleaks.com`、`scrapfly.io/web-scraping-tools`。

### 3. App 端设备指纹（移动）

- **Android**：`Build.MODEL`/`SERIAL`/`FINGERPRINT`、`Settings.Secure.ANDROID_ID`、IMEI（API 29+ 受限）、GSF ID、Widevine `getPropertyByteArray("deviceUniqueId")`、Mali GPU 字符串（vs Swiftshader）、cgroup `/proc/self/cgroup`、`SystemProperties.get("ro.boot.flash.locked")` (Verified Boot)、`Build.IS_EMULATOR`、`/proc/net/tcp` 找 27042（Frida 端口）等。
- **iOS**：IDFA / IDFV / `UIDevice.identifierForVendor`、AppAttest assertion、DeviceCheck 2-bit、SEP key 派生。
- **典型 SDK**：阿里 wua/x5sec、字节 x-helios、美团 mtguard、京东 eid、快手 sigsdk、网易盾 yidun、数美 ishumei smid、顶象 constid、同盾 blackbox、瑞数 RASP、蚂蚁 mPaaS APDID。

### 检测/防御态势

- **防御侧**：`fingerprint.com`（前 fingerprintjs Pro）、`Castle.io`、`HUMAN`、`Spur.us`（住宅代理识别）、`IPQualityScore`、`MaxMind GeoIP2 Anonymous IP`。
- **检测自检**：`bot.sannysoft.com`、`creepjs.abrahamjuliot.io`、`browserleaks.com`、`amiunique.org`、`tls.peet.ws`。

详见 [references/fingerprint/](references/fingerprint/)。

---

## Toolchain Path（工具链 / Hook / 模拟 / 抓包）

**移动端 Hook 与模拟**：
- **Frida**：`frida-server` (Android/iOS)、`Stalker`（trace 任意指令）、`Interceptor.attach` (可读寄存器+回调)、`replace`（整体替换函数）。**反 Frida**：扫 27042 端口、扫 `gum-js-loop`/`gmain`/`gdbus` 线程名、`/proc/self/maps` 找 `libfrida-agent.so`、关键函数前 4 字节 STP 校验、`linker64` 符号扫。**绕过**：`hzzheyang/strongR-frida-android`、`hluda-server`，改 frida 字符串 + 入口符号。
- **Xposed/LSPosed**：`LSPosed/LSPosed`（Zygisk/Riru 双形态）、`LSPlant`（底层 ART hook）。Java 层 hook 经典；反检测可通过 `LSPosed/Shamiko` 隐藏。
- **Magisk / Zygisk / DenyList**：`topjohnwu/Magisk`、`Shamiko` 模块、`LSPosed-Riru`。Magisk 24+ Zygisk 取代 Riru，DenyList 是当前主流隐藏机制。
- **KernelSU / APatch / SukiSU**：内核态 root，对用户态 root 检测有天然优势；`tiann/KernelSU`、`bmax121/APatch`、`SukiSU-Ultra`。
- **Inline Hook**：`jmpews/Dobby`（跨平台）、`bytedance/android-inline-hook` (ShadowHook)、`SandHook`、`YAHFA`、`Whale`、`Riru`。
- **模拟执行**：`zhkl0228/unidbg`（事实标准，Java 黑盒模拟 SO）、`unidbg-boot-server`（包成 Spring Boot）、`AeonLucid/AndroidNativeEmu`（Python+unicorn）、`qilingframework/qiling`（跨架构跨 OS）、`mandiant/speakeasy`（Win 用户态/内核）。
- **DEX 加固脱壳**：`hluwa/FRIDA-DEXDump`、`CodingGay/BlackDex`、`reflutter`、`ARTDump`。主流加固：360 加固（libjiagu）、爱加密（libsecexe）、梆梆安全、腾讯乐固（libshellx）、阿里聚安全（libmobisec）、几维安全、娜迦。脱壳核心：DEX 在 ART 执行时一定会进内存，抓住时机 dump。
- **iOS 砸壳**：`AloneMonkey/frida-ios-dump`、`ChiChou/bagbak`（rootless 友好）、`Iridium`、`appdecrypt`。`Clutch` 已停更。
- **iOS 越狱**：`palera1n/palera1n`（A11- iOS 15-17）、`opa334/Dopamine`（A12+ rootless）、`checkra1n`、`unc0ver`、`Taurine`、`opa334/TrollStore`（永久签名 iOS 14-16.x）、`roothide/Bootstrap`。
- **iOS Hook**：`ElleKit`（palera1n/Dopamine 默认）、`Substitute`、`Theos`/`Logos`/`Orion`、`fishhook`。

**反编译 / 反混淆**：
- **平台**：IDA Pro 9.x、Ghidra、Binary Ninja、radare2/Cutter/Rizin、jadx、apktool、APKEditor。
- **OLLVM 反混淆**：`obfuscator-llvm/obfuscator`（原版）、`Hikari`（已死）、`bluesadi/Pluto-Obfuscator`（iOS LLVM 主流 fork）。
- **反 OLLVM**：`d-810`（IDA microcode 级）、`cdong1012/ollvm-unflattener`（Miasm）、`Triton` 符号执行、`angr` 兜底。三大 pass：BCF（虚假控制流）、FLA/CFF（控制流平坦化）、SUB（指令替换）。
- **IDA 插件**：`mandiant/capa`（能力识别）、`CheckPointSW/Karta`（库识别）、`google/bindiff`、`joxeankoret/diaphora`、`findcrypt`。
- **Unity / IL2CPP**：`vfsfitvnm/frida-il2cpp-bridge`、`Il2CppDumper`、`zygisk-il2cppdumper`（无需 metadata）。

**抓包 / SSL Pinning**：
- **平台**：`mitmproxy`、`HTTP Toolkit`、`Reqable`、`Charles`、`Fiddler`。
- **Android Pinning Bypass**：`objection`（Frida-based 通用）、`apk-mitm`（自动 patch APK）、`MagiskTrustUserCerts`（系统证书移植）、`CYRUS-STUDIO/frida-ssl-pinning-bypass`（Java+Native）、`Q0120S/bypass-ssl-pinning`（frida codeshare）。OkHttp/Conscrypt/Volley/Retrofit 各有不同 hook 点。
- **iOS Pinning Bypass**：`SSL Kill Switch 2`（越狱设备）、`pritessh/iOS-SSL-Pinning-Bypass`（iOS 17）、`objection`、`lichao890427/ios-ssl-bypass`（codeshare）。

**反检测系统层**：
- **TracerPid / proc 过滤**：`darvincisec/DetectTracer`。
- **/proc/self/maps 注入隐藏**：`strongR-frida` 的 maps 隐藏 + 模块改名。
- **inotify 反 inotify**：`Project Zero` 博客有详细说明。
- **selinux / cgroup / qemu_pipe**：`framgia/android-emulator-detector` 列出全部检测点。
- **GPU 字符串**：真机 = `Mali-G78`/`Adreno-750`/`Apple A17 GPU`；模拟器 = `Swiftshader`/`ANGLE`/`VirGL`/`llvmpipe`。

详见 [references/toolchain/](references/toolchain/)。

---

## iOS Path（iOS 风控通用工作流）

**1. 二进制结构**：Mach-O（Header + Load Commands + Data 段），LC_ENCRYPTION_INFO_64 是 FairPlay 加密段（cryptid=1 表示加密）。砸壳本质是把内存里已解密的 `__TEXT` 段 dump 回磁盘并修复 `cryptid=0`。
- **dyld shared cache**：iOS 15+ 系统库进 dsc，逆向需用 `blacktop/ipsw` 或 `dsc_extractor` 抽取。
- **ChainedFixups**：iOS 15+ 取代 LC_DYLD_INFO_ONLY，rebase/bind 走 chained pointer。
- **ARM64e PAC**：A12+，function pointer 上半段是 PAC tag。`pacxx`/`autia`/`autda` 系列指令验证。

**2. 砸壳**（必须越狱设备）：
- 主流：`AloneMonkey/frida-ios-dump`（rootless 兼容）、`ChiChou/bagbak`、`Iridium`。
- TrollStore 时代：`opa334/TrollStore` 永久签名（iOS 14-16.x，CoreTrust bug 链），可装解密版 ipa。

**3. 越狱生态**：
- **palera1n** (checkm8 + KPF, A11- iOS 15-17 rootless)、**Dopamine** (A12+ iOS 15-16 rootless)、**checkra1n** (legacy)、**roothide/Bootstrap**（rootless 二级方案）。
- **Hook 框架**：`ElleKit`（默认）、`Substitute`、`Theos+Logos+Orion`、`fishhook`（C 函数 hook）、`MobileSubstrate`（已弃）。

**4. 反越狱探针**（典型 5 件套）：
- `ptrace(PT_DENY_ATTACH)` / 直接 `svc 0x80 #26`。
- `sysctl(KERN_PROC, KERN_PROC_PID, getpid())` 检 P_TRACED 位（更隐蔽）。
- `fork()` / `getppid()`：越狱环境下行为异常。
- 文件路径黑名单：`/Applications/Cydia.app`、`/var/lib/apt`、`/private/var/lib/apt`、`/usr/bin/ssh`。
- URL scheme：`cydia://`、`sileo://`、`zbra://`、`undecimus://`、`xina://`。
- `dyld_image_count` + 黑名单：libsubstrate.dylib / libsubstitute.dylib / TweakInject / SBInject。
- `_dyld_register_func_for_add_image` 监控注入。
- Frida 检测：端口 27042 / 线程名 `gum-js-loop`/`gmain` / `frida:rpc` / `frida-server` 进程名。

**绕过方案**：`A-Bypass`/`Liberty Lite`/`Shadow`/`HookKiller`/`KernBypass`/`Choicy`，加上自写 frida 脚本（hook getenv/stat/fopen/access/strstr/`_dyld_get_image_name`）。

**5. SSL Pinning Bypass**：`SSL Kill Switch 2`（系统级，越狱设备最方便）、`pritessh/iOS-SSL-Pinning-Bypass` (iOS 17 + Security.framework + BoringSSL + Network.framework + Alamofire)、`objection`、`lichao890427/ios-ssl-bypass`（frida codeshare）。

**6. 苹果原生反作弊**：
- **DeviceCheck**（2-bit）：服务器端给设备打 2-bit 标记，重置需要重置整机。
- **App Attest**（iOS 14+）：基于 SEP key 的硬件 attestation，attest API 生成 keypair → 服务器验证 X.509 链 → assertion API 后续签名。**绕过**：除非提取 SEP key（接近不可破），只能在多设备间复制 attestation 数据时被 nonce 反制。
- **Private Access Tokens (PAT)**（iOS 16+）：替代 captcha 的隐私令牌（基于 Privacy Pass）。
- **iCloud Private Relay**：会让 IP 检测失效。
- **SEP / Secure Enclave**：协处理器，独立内存+存储，Touch/Face ID 数据、AppAttest key 都在里面，不可读出。

**7. 加密参数（与 Android 对应）**：抖音/TikTok iOS x-argus / x-gorgon / x-ladon（与 Android 共用 ttencrypt 但壳和探针不同）；微信 mmtls（基于 TLS 1.3 草案，封装在 Mars 网络库里）；淘宝 iOS sign（mtop x-sign，securitysdk + ub_aes）；京东 iOS h5st / x-api-eid-token（h5st 5.0+ iOS/web 共 jsvmp）；支付宝 iOS APDID/umid/rds（mPaaS 体系）；网易云 iOS eapi/linuxapi（与 web 同源）；bilibili wbi/w_rid（iOS/web 同算法）。

**8. 网络 / TLS 指纹**：NSURLSession vs CFNetwork vs WKWebView 的 ClientHello 顺序不同；iOS 15+ 走 NWConnection；ATS（App Transport Security）强制 TLS 1.2+ 是抓包前置。

详见 [references/ios/](references/ios/)。

---

## HW-System Path（硬件 / 系统 / 凭证完整性）

**Play Integrity API**（取代 SafetyNet Attestation，2024+ 国内 App 主线）：
- **判定矩阵**：MEETS_DEVICE_INTEGRITY（标准 Android 设备）/ MEETS_BASIC_INTEGRITY（更宽松）/ MEETS_STRONG_INTEGRITY（A13+ 硬件 backed）/ MEETS_VIRTUAL_INTEGRITY（云手机）。
- **请求模式**：Standard request（在线，最严格）vs Classic request（离线签名 token）。
- **绕过现状**：`tryigit/PlayIntegrityFix` + `Susfs` + `ZygiskNext`，Magisk/KernelSU/APatch 路径都有方案；STRONG_INTEGRITY 需要 spoof locked bootloader+合法证书链，难度极高。

**TEE Key Attestation 5 级证书链**（StrongBox/Trusty）：
1. Google Hardware Attestation Root CA（公开根）
2. Google Hardware Attestation Intermediate CA
3. Device-specific CA (manufacturer 注入)
4. TEE App CA (Trusty 内部签发)
5. Attestation Key (用户应用持有)

**关键扩展字段**：`AttestationApplicationId` 含包名+签名 SHA256，`AttestationSecurityLevel`（SOFTWARE/TRUSTED_ENVIRONMENT/STRONG_BOX）、`KeymasterVersion`、`RootOfTrust.deviceLocked`/`verifiedBootState`(GREEN/YELLOW/ORANGE/RED)/`verifiedBootKey`。

**绕过现状**：
- 软件层（SOFTWARE）：可改 ROT 字段、伪造证书链。
- TRUSTED_ENVIRONMENT：根证书私钥保存在芯片 TEE，无法 sign 新证书 → 实际只能"复用真机 attest 数据"，被 nonce 反制。
- STRONG_BOX：StrongBox Keymaster 独立硬件，更难。

**Verified Boot / AVB 2.0**：
- **vbmeta**：分区描述符 + 证书链 + 签名。
- **启动颜色**：GREEN（OEM 锁定+验签通过）、YELLOW（用户 key+验签通过）、ORANGE（解锁 bootloader）、RED（验签失败）。
- **风控读取**：通过 `getprop ro.boot.flash.locked`、`getprop ro.boot.veritymode`、Key Attestation 的 `RootOfTrust.deviceLocked` 字段。
- **绕过 vbmeta**：`fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img`，但会触发 ORANGE 状态。

**ARM PAC / BTI / MTE**（v8.3+/v8.5+/v9）：
- PAC 让函数指针带签名标签，inline hook 时改了指针就要重签；Frida/Dobby 在 ARM64e 上需要特殊处理。
- BTI（Branch Target Identification）阻止任意跳转。
- MTE（Memory Tagging Extension）做内存标签校验，主要对抗内存破坏漏洞。

**iOS 对应**：
- **DeviceCheck / App Attest**：见 *iOS Path*。
- **Hardware Attestation / WebAuthn on iOS**：基于 SEP，与 Apple 服务器双向校验。
- **Private Access Tokens**：替代 captcha。

**Verdict**：硬件层凭证（TEE Key Attestation、StrongBox、SEP）短期内无法软件绕过，从风控对抗角度建议改成"记录-验证"而非"伪造"——对自有设备做合法采样，研究签名结构、字段含义和后端校验逻辑，作为防御研究。

详见 [references/hw-system/](references/hw-system/)。

---

## Troubleshooting

- **BR 重写后控制流断裂**：检查是否误把"纯载体块的 BR"重写了；恢复白名单 `BR` 即可。
- **CSEL 双状态都解出 UNKNOWN**：上游某个寄存器仍是符号；扩大模拟范围到上一个基本块，或再多分裂一层状态。
- **AES 看似匹配但密文不对**：先怀疑 MixColumns 矩阵被改、ShiftPerm 被改、Rcon 被改、SubWord 被改；用 `vec(plain) → vec(ct)` 反求 KeyExpansion。
- **修改版 MD5 摘要不匹配**：对比每一轮 `K[i]` 与 shift table；NEON 字节反转极易漏。
- **GPU / SELinux 字段把伪环境暴露**：`Mali-G78` vs `Swiftshader`、`enforcing` vs `permissive`、cgroup 路径里出现 `kvm` / `qemu` 都会触发后端封禁。
- **心跳停在 init**：你没真跑完 `c<100`，或 `t` 单调计数被你 reset 了。
- **TEE Key Attestation 5 级证书链验证失败**：除非有真机硬件 backed key，几乎没法绕；考虑改成"记录-验证"而不是"伪造"。
- **同一指纹冗余字段不一致**（`x144`、`x231/x232`）：replay 时必须把所有冗余镜像同步生成，不能各填各的。

---

## 参考资料（references/）

- 案例索引：[references/README.md](references/README.md)。
- 小红书 `libtiny.so` 全量逐字技术笔记：[references/android/xhs-libtiny-notes.md](references/android/xhs-libtiny-notes.md)。包含 8 类 BR 花指令的 ASM 示例与改写、字符串解密器伪码、SSO/JSON ABI、四个加密参数（`x-mini-mua / x-mini-s1 / x-mini-sig / shield`）的完整算法、`/api/v1/profile/android` 上传 schema、~200 个 `xN` 字段逐项注解、`code-patch-check` 自校验 9 段哈希原文、心跳两阶段位图、姊妹接口与 APM 旁路。

仅在任务确实涉及对应平台时再 Read 对应 references 文件，避免不必要地把整个语料拉进上下文。

---

## 如何扩充本技能（How to extend）

当后续收到新平台风控分析资料时，按下面流程把它并入本技能：

1. 在 `references/` 下新增一份 `<平台短名>-notes.md`（例：`douyin-libcms-notes.md`、`meituan-mtguard-notes.md`、`bili-bilictrl-notes.md`）。文件首部放一张 5 行摘要表（包名 / SO / 参数名 / 加密栈 / 反检测亮点），随后是逐字技术笔记。
2. 在 `references/README.md` 的索引表里新增一行，列出：App、SO/SDK、参数名、加密栈摘要、反检测亮点、reference 文件名。
3. 如果新平台引入了**全新的工作流环节**（例如 V8 字节码风控、iOS LLVM bitcode 风控、JNI 反向通信通道），再在本 `SKILL.md` 里**只补对应一节**的 Path（不要重写已有路径）。
4. 把通用规律写进 `SKILL.md`、把样本特定细节写进对应 `references/<平台>-notes.md` —— 这是这个技能能持续扩张而不臃肿的关键。
