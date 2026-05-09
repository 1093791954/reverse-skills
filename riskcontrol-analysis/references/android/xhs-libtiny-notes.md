# 小红书 libtiny.so 风控参数全量分析笔记

> 本文是一份对小红书 App 风控参数（`x-mini-mua`、`x-mini-s1`、`x-mini-sig`、`shield`）的逐字技术笔记，原始资料：`某红薯App风控参数分析.html`。仅用于授权范围内的安全研究、机制理解与防御性分析。

## 摘要表

| 项 | 值 |
|---|---|
| 包名 | `com.xingin.xhs` |
| 版本 | `9.24.0`（versionCode `9240811` = `0x8D00EB`） |
| 目标 SO | `libtiny.so` |
| 风控参数 | `x-mini-mua`、`x-mini-s1`、`x-mini-sig`、`shield` |
| 主上传接口 | `/api/v1/profile/android` |
| 姊妹接口 | `/api/v1/register/android`、`/api/v1/cfg/android`（共用密钥栈） |
| 旁路接口 | `apm-native.xiaohongshu.com/api/collect`、`t2.xiaohongshu.com/api/collect`、`edith.xiaohongshu.com/api/...` |
| 密钥协商 | X25519 ECDH，basepoint=9，硬编码 server pubkey，`shared[0:16]`=AES key、`[16:32]`=IV |
| 体加密 | AES-128-CBC（标准 / 修改版混用） |
| HMAC | 修改版 HMAC-MD5（改 Round 1~4 shift/K、改 IV、NEON 字节反转） |
| 外层 | RC4 with `"std::abort();"` 13B 硬编码 key + `"XY" + Base64(header + ct)` |
| 签名 | SHA256 + `transform_16` 128×128 GF(2) 仿射 |
| 设备指纹字段数 | 短包 ~90，全包 ~200 |
| 字符串解密器数 | 10 个，魔数 `0xBD69BD22`，`switch (i % 5)` |

---

## 1. ARM64 BR 花指令去除（`libtiny.so`）

作者把 `BR Xt` 间接跳花指令分为 8 类，逐类给出 patch 策略。这一步是**所有静态分析的前置**——没去花的 SO 在 IDA 里几乎没法读。

策略总纲：
- 写一个从基本块入口出发的 ARM64 局部模拟器，状态走到 `BR Xt`。
- 若 `BR` 寄存器最终落到一个确定的 `.text` 内地址，且去常态化后不是垃圾 → 把 `BR Xt` 重写成 `B target`。
- `CSEL/CSET/CSINV/CSINC/CSNEG` 处用多状态分裂模拟（true / false 两路并行）。
- 表读 (`LDR`) 用 ELF/relocation 解析表基址 + 计算偏移。
- 索引型 `LDR Xt,[base,index,LSL#3] ; ... ; BR Xt` 在严苛条件下用 angr 兜底。

### Type 1 — 常量地址构造 + BR

```asm
ADRP X8, #target@PAGE
ADD  X8, X8, #target@PAGEOFF
BR   X8
```

或：

```asm
MOV  X9, #imm
MOVK X9, #imm, LSL #16
ADD  X8, X8, X9
BR   X8
```

策略：从局部块入口模拟到 `BR`；若 `BR` 寄存器是确定的 `.text` 地址且去常态化后不是垃圾，重写 `BR Xt → B final_target`。

### Type 2 — 静态表读 + BR

```asm
ADRP X13, #off_xxx@PAGE
ADD  X13, X13, #off_xxx@PAGEOFF
LDR  X9, [X13,#off]
ADD  X9, X9, W10,SXTW
BR   X9
```

策略：①解析 `ADRP+ADD` 得表基址 ②从 ELF/relocation 读条目 ③模拟偏移加 ④重写 `BR → B`。如果索引来自 `CSEL/CSET`，下沉到 Type 3。

### Type 3 — CSEL/CSET 条件分派

```asm
CMP  W8, #0
CSEL W10, W11, W10, NE
SUB  W10, W10, W8
ADD  X9, X9, W10,SXTW
BR   X9
```

策略：在 `CMP/TST/CMN` 处记录标志；遇到 `CSEL/CSET/CSINV/CSINC/CSNEG` 分裂为 true/false 两条状态，并行模拟到 `BR`，两端目标都能静态求出时重写为：

```asm
B.cond target_true
B      target_false
```

### Type 4 — BR 之前夹真副作用

```asm
ADD  X8, X9, W8,SXTW
STR  X15, [X19,#0x468]   ; 真业务副作用
MOV  X12, X15            ; 真业务副作用
BR   X8
```

策略：识别可安全前移的尾部副作用，上提到补丁区开头，再写 `B.cond + B`，原位置 NOP。

改写示例：

```asm
0x3AC8E0 STR X15, [X19,#0x468]
0x3AC8E4 MOV X12, X15
0x3AC8E8 B.NE 0x404E14
0x3AC8EC B    0x367A3C
0x3AC8F0 NOP
0x3AC8F4 NOP
```

### Type 5 — 纯载体垃圾块

仅做"对载体寄存器加减常量再跳"。两种形态：

形态 A：

```asm
MOV  X8, #neg_const
ADD  X8, X9, X8
BR   X8
```

或：

```asm
LDR X9, [X19,#field]
MOV X8, #neg_const
ADD X8, X9, X8
BR  X8
```

形态 B：

```asm
ADRP X8, #off_xxx@PAGE
LDR  X8, [X8,#off_xxx@PAGEOFF]
MOV  X10, #const_a
MOV  X9,  #const_b
MOVK X10, #...
MOVK X9,  #...
ADD  X8,  X8,  X10
ADD  X12, X12, X9
BR   X12
```

策略：状态传播过载体块，**只重写"上游业务分支"**到最终目标；**不要**重写载体自身的 `BR`（否则会产生伪静态 xref）。如果上游是 CSEL/CSET 单状态求值得 UNKNOWN，必须把上游升级为多状态再重写**它**的分支。

`libtiny.so` 中应当**保留为 BR**（载体白名单）的地址：

```
0x19FDBC BR X8
0x37C7D4 BR X8
0x3FF9AC BR X8
```

工作样例（地址 `0x4AAD3C`）：

```asm
0x4AAD34 CMP  W10, #0
0x4AAD38 CSEL X8, X8, X9, NE
0x4AAD3C B    0x4AAE00          ; 进入载体
0x4AAE00 LDR  X9, [X28,#0xB50]
0x4AAE14 ADD  X9, X9, X11
0x4AAE18 ADD  X8, X8, X10
0x4AAE1C BR   X9
```

锚点 `X28 = 0x772000`，`[0x772000+0xB50]+const` 解出载体目标。把 `0x4AAD38` 这一对改写为：

```asm
0x4AAD38 B.NE 0x4AA6A8
0x4AAD3C B    0x4AA62C
```

### Type 6 — 保存域链

```asm
STR X10, [X19,#field]
B   mid_block

mid_block:
LDR X9, [X19,#field]
ADD X8, X9, #offset
BR  X8
```

策略：自定义模拟器把 `[reg+offset]` 表达成符号化 memory key；写入是确定地址时，未来同 key 的读取就能恢复目标。允许多层 `B → mid → carrier → BR` 链。**仅对已验证过的 saved-field key 启用**，否则会误改。

### Type 7 — 真调用尾的分派

```asm
BL  some_func
...
ADD X9, X9, W10,SXTW
BR  X9
```

策略：默认载体 `BR` 不重写；但当分派紧跟在 `BL/BLR` 之后，属于真业务路径，可以重写（例：`0x185F40 → B 0x19E0E4`）。

### Type 8 — 小型索引开关 + angr 兜底

```asm
ADRP X10, #table@PAGE
ADD  X10, X10, #table@PAGEOFF
LDR  X8, [X10,X8,LSL#3]
MOV  X10, #const
MOVK X10, #const, LSL#16
SUB  X1, X9, #1          ; 真副作用，必须保留
ADD  X8, X8, X10
BR   X8
```

严格条件：
- 索引 `LDR Xt,[base,index,scale]` 的 `Xt` 终结于 `BR Xt`。
- 表基址静态可解。
- 枚举条目 → `.text` 内地址 2~3 个。
- 目标必须是前向短距（`<0x100` 字节）。
- 补丁区容得下"副作用 + CMP/B.EQ + B"。
- 幸存副作用可安全前移、不依赖目标计算用的临时寄存器。
- 用 angr 从索引 `LDR` 步进到 `BR` 验证每个 index 的目标。
- 用 angr 的 `SYMBOL_FILL_UNCONSTRAINED_*`，**不要** zero-fill（避免把未知误判为 0）。

样例（`0x1A5788`）：

```asm
0x1A5774 LDR X8, [X10,X8,LSL#3]
0x1A5778 MOV X10, #...
0x1A577C MOVK X10, #...
0x1A5780 SUB X1, X9, #1
0x1A5784 ADD X8, X8, X10
0x1A5788 BR X8
```

静态枚举 + angr 验证：

```
index 0 -> 0x1A578C
index 1 -> 0x1A5798
index 2 -> 0x1A57A4
```

改写为：

```asm
0x1A5774 SUB X1, X9, #1
0x1A5778 CMP X8, #0
0x1A577C B.EQ 0x1A578C
0x1A5780 CMP X8, #1
0x1A5784 B.EQ 0x1A5798
0x1A5788 B    0x1A57A4
```

### 完成判据

> 所有业务节点不再跳进载体垃圾区；保留下来的 `BR` 都是已确认的纯载体块，不再需要被静态求值。

---

## 2. 字符串解密

### 6 特征签名（IDA 反编译命中）

| # | 特征 | 反编译可见 |
|---|---|---|
| 1 | 2 个参数 | `result, a2` |
| 2 | 神奇右移 | `0xBD69BD22 >> (8 * (x & 3))` |
| 3 | `i % 5` 分支 | `switch (i % 5)` |
| 4 | 5 种操作 | `eor`、`mvn`、`sub`、`lsl(+shift)`、`lsr(+shift)` |
| 5 | do-while | 末尾 `cbz/cbnz` 比较计数 |
| 6 | 原地写回 | `*ptr = *ptr ⊕ key` 写回原字节 |

### 标准伪代码

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

`libtiny.so` 中匹配到 **10 个**字符串解密器函数。批量解密后产出的字典是后续工作的核心资产（露出 `getprop` 键、JSON 路径键、API 端点、错误日志、服务名）。

---

## 3. JSON 树 / SSO 内存布局

`libtiny.so` 用 SSO（Small String Optimization）维护字符串，槽宽 24 字节（`0x18`）。

### SSO 字符串槽

```
小串（hdr 偶数）：
  [hdr (1B)] [data (23B)]
  len = hdr >> 1
  data 起始 = ptr + 1

大串（hdr & 1 != 0）：
  [hdr (1B)] [pad (7B)] [len (8B QWORD)] [data_ptr (8B)]
  len 在 ptr+8
  data 指针在 ptr+16
```

### Frida JS 读取器（直接可用）

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
        if (len > 0x100000) return "";   // 防垃圾
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

### 值类型 tag

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

---

## 4. 算法概括（`x-mini` 系列 + `shield`）

### 4.1 `x-mini-mua`（基础参数；其他参数都依赖它）

- **X25519 ECDH**：客户端生成 32 字节私钥 → `X25519(priv, basepoint=9)` = `client_pub` → `X25519(priv, hardcoded server_pub)` = `shared`。
- **派生密钥**：`shared[0:16]` = AES key，`shared[16:32]` = CBC IV。
- **设备指纹**：200+ 字段 JSON → **zlib** 压缩。
- **AES-128-CBC**（标准）加密压缩后的 JSON。
- **输出**：`base64url(header_json) "." base64url(ciphertext) "."`。

### 4.2 `x-mini-s1`

- **修改版 AES-128-CBC**——表驱动（行/列混淆矩阵）、**非标准 `mix_columns`**、自定义 `shift_perm`；轮密钥与 prewhiten key 都是**固定常量**。
- **明文**：`METHOD\nPATH\nQUERY\nSHA256(BODY).hex()\nMUA_JWT`
- **`hash32` 混淆**：`SHA256` → 行排列 → 字节变换（`0xD0 / 0xF4 / 0x8B / 0x4E` XOR + 半字节交换）。
- **`raw44` 打包**：`4B timestamp + 2B encoded + 2B encoded + hash32 + CRC32 尾`。
- **随机扰乱**：libc `rand()` 产生 shuffle 索引重排一张固定 `pair_table`。
- **输出**：`Base64(packet) = [counter][ciphertext][crc_a][crc_b]`。

### 4.3 `x-mini-sig`

- **明文**：与 `x-mini-s1` 同 5 行格式。
- **算法**：`sig = transform_16(SHA256(plain)[0:16]) || SHA256(plain)[16:32]`
- `transform_16` 是 GF(2) 上的 **128×128 仿射变换**：128 个输出位 = 128 个输入位 XOR 组合 + 16 字节常量偏移。等价于把 **5288 条 ARM64 NEON 向量指令** 压缩成一个 128×128 二进制矩阵。
- **输出**：64 字符 hex。

### 4.4 `shield`

- **HMAC key 解密**：调 `aes_decrypt_main_hmac` → 64 字节 HMAC key（与设备绑定）。
- **修改版 HMAC-MD5**：Round 1~4 的 shift 与 K 常量都被改过（不同于 RFC1321 MD5），初始 IV 也被改；pipeline 中夹一次 NEON 128-bit 字节反转。
- **RC4 加密**：用 13 字节硬编码 key `"std::abort();"`，加密一个 83 字节结构：`version + app_id + type + build + deviceId + hmac_digest`。
- **输出**：`"XY" + Base64(16 字节 header + RC4 密文)`。

#### `aes_decrypt_main_hmac` 内部（修改版 AES-128-CBC）

- KeySchedule = `DeviceId[:16] + 自定义 XOR 常量 + 改造 Rcon + 非标准 WordRotate/SubWord`。
- **11 条轮密钥**全部从 ARM64 trace 抠出**硬编码**。
- 仅由 `shield.py` 调用，用于解密 `main_hmac` 字符串 → 得到 64 字节 HMAC key。

---

## 5. 设备指纹上传（`d` 字段）

### 端点

- `/api/v1/register/android`
- `/api/v1/cfg/android`
- `/api/v1/profile/android`  ← **主目标**

### 上传体形态

```jsonc
{
  "a": "ECFAAF01",                              // App ID（固定）
  "c": 82,                                      // 请求计数器
  "d": "<x-mini-mua 风格密文, base64url(header).base64url(zlib+AES(JSON)).>",
  "e": {
    "dd": 1778219998657,                        // 采集时间
    "device_id": "c2a88145-b110-31f7-b034-d8b42786844a",
    "kk": "CE65F4E2D70C2B48E869BF712E1574C4",   // 完整性校验 (=x302)
    "now": 1778220001118,                       // 请求时刻
    "rr": "0",
    "sid": "session.1778149057347685101536",
    "tt": "MEYC...",                            // ECDSA P-256 DER (=x303)
    "uid": "68529ca9000000001d0099d1",
    "vv": 1
  },
  "g": "<APK SHA384, =x146>",
  "k": "<X25519 32B client_pub hex>",
  "p": "a",                                     // 平台: a=Android, i=iOS
  "s": "<x-mini-sig 64 hex>",
  "u": "<UID>",
  "v": "2.9.63"                                 // SDK 版本
}
```

`d` 密文用与 `x-mini-mua` **同一套 AES key/IV**，载荷是设备指纹 JSON。

### 5.1 短包（`x-mini-mua` 内嵌指纹，~90 字段）逐项注解

**App 身份**

| 字段 | 含义 |
|---|---|
| `x0` | 包名 = `com.xingin.xhs` |
| `x1` | versionName = `9.24.0` |
| `x2` | versionCode = `9240811` |
| `x3` | 首次安装时间戳 |
| `x4` | 最后更新时间戳 |
| `x92` | targetSdkVersion = `35` |

**厂商伪造 vs 真实设备**

| 字段 | 含义 |
|---|---|
| `x5` | `"Vivo"`（**硬编码伪造**：`create_string("Vivo")`） |
| `x20` | BRAND = `google` |
| `x23` | MANUFACTURER = `Google` |
| `x24` | MODEL = `Pixel 6` |

> `x5=Vivo` 与 `x7=gs101` / `x24=Pixel 6` 之间矛盾，证明 SO 在主动伪造厂商字段。日志显示 SDK 先尝试 Mi/Coolpad OAID 服务，失败后回退到硬编码 `"Vivo"`。

**Build / 系统属性**（来自 `getprop` / `android.os.Build.*`）

| 字段 | 来源 / 含义 |
|---|---|
| `x6` | `ro.build.date.utc` |
| `x7` | `ro.board.platform`（Tensor） |
| `x8` | `ro.build.date.utc * 1000` |
| `x9` | `ro.build.display.id` |
| `x10` | `ro.build.fingerprint` |
| `x11` | `ro.build.host` |
| `x12` | `ro.build.id` |
| `x13` | `ro.build.tags` |
| `x14` | `ro.build.type` |
| `x15` | `ro.build.version.incremental` |
| `x16` | `ro.build.version.release` |
| `x17` | `ro.build.version.sdk` |
| `x18` | `ro.build.version.security_patch` |
| `x19` | `ro.product.device` |
| `x21` | `SUPPORTED_ABIS` |
| `x22` | `ro.product.name` |
| `x25` | `ro.hardware` |
| `x26` | `ro.product.cpu.abi` |
| `x27` | `uname -r` |
| `x28` | `uname -v` |
| `x29` | baseband 版本 |

**显示 / 电池**

| 字段 | 含义 |
|---|---|
| `x30` | `1080,2400,420`（宽,高,DPI） |
| `x31` | MEDIA_PERFORMANCE_CLASS |
| `x32` | charging |
| `x33` | battery status |
| `x34`/`x35` | battery%（冗余两份，交叉校验） |
| `x36` | USB charging |
| `x37` | unknown |
| `x38` | health |

**网络**

| 字段 | 含义 |
|---|---|
| `x40` | type |
| `x41` | carrier |
| `x42` | MCC+MNC |
| `x43` | connection（wifi） |
| `x44` | connect timestamp |
| `x45` | duration ms |

**进程**

| 字段 | 含义 |
|---|---|
| `x78` | UID |
| `x79` | TID |
| `x80` | thread count |

**存储**

| 字段 | 含义 |
|---|---|
| `x231`/`x232` | total（冗余两份） |
| `x235` | used |
| `x236`/`x237` | free（冗余两份） |

**CPU 采样**（`/proc/stat` deltas）

| 字段 | 含义 |
|---|---|
| `x247` | `{0..5: percent}`（每核 CPU 占用） |

**时间戳**

| 字段 | 含义 |
|---|---|
| `x8` | ROM build |
| `x70` | report 间隔 (s) |
| `x72` | 冷启动 |
| `x73` | 最近一次操作 |
| `x87` | 采集入口 |
| `x93` | 采集序号 |
| `x234` | `{1,2,3:...}` SDK 初始化三阶段 |
| `x243` | 事件基准 |
| `x258` | 全局请求计数器（跨 session） |
| `x259` | 非首次运行标志 |
| `x260` | 采集结束 |
| `x269` | epoch 偏移 (`1230768000000` = 2009-01-01) |
| `x289` | HTTP 发送 |
| `x293` | 采集耗时 (ms) |

**安全 / 环境探针**（**关键逆向目标**）

| 字段 | 含义 |
|---|---|
| `x97` | `{s1..s11, d1..d13}` JSON——系统服务可用性签名 |
| `x98` | 模拟器检测（`"0"` = 真机） |
| `x100` | Root 检测 |
| `x102` | 注入检测 |
| `x120` | 多开 / 虚拟环境 |
| `x122` | hook 框架触发 |
| `x131` | **Frida 检测** |
| `x136` | AccessibilityService 检测 |
| `x186`/`x187` | ADB / 开发者选项 |
| `x194` | SDK 已初始化 |
| `x202`/`x203` | 安全标志 |
| `x206` | 签名一致（重打包检测） |
| `x207` | 签名校验（冗余） |
| `x213` | 屏幕锁 |
| `x214` | Verified Boot color (`green`) |
| `x215` | SELinux (`enforcing`) |
| `x226` | SELinux netlink reject text |
| `x239` | Treble 支持 |
| `x256` | 完整 `uname -a` |
| `x261` | 正常启动 |
| `x263` | ART 正常 |
| `x264` | runtime 正常 |
| `x267` | 进程存活 |
| `x272` | 无热修篡改 |
| `x290` | 官方 ROM (`release-keys`) |
| `x301` | SDK 状态 (`LOADED`) |
| `x304` | TEE key 有效 |
| `x305` | 错误码 (`-3` = OK) |

**身份与密钥**

| 字段 | 含义 |
|---|---|
| `x146` | APK 签名 SHA384（GID） |
| `x185` | 16 字符 session token（`IiGgSsKkCVvEePp` 大小写 Base64 风格） |
| `x302` | MD5 fingerprint key id（KK） |
| `x303` | 72 字节 DER ECDSA-P256 签名 |

**杂项**

| 字段 | 含义 |
|---|---|
| `x99` | 蓝牙状态 CRC32 |
| `x238` | SIM 国家 |
| `x242` | 外设 |

### 5.2 全包（`/api/v1/profile/android` 完整上传，~200 字段）增量

**RIL / 哈希**

| 字段 | 含义 |
|---|---|
| `x103` / `x143` | RIL 字符串 + 其 MD5（`Samsung S.LSI Vendor RIL V2.3 Build ...`） |
| `x104` / `x67` | SHA256 设备 ID |
| `x85` | SHA256 |
| `x86` | SHA1 |

**系统/SDK 细节**

| 字段 | 含义 |
|---|---|
| `x105` | 铃声 |
| `x110` | OAID |
| `x180` | 设备 UUID |
| `x112` | DNS 服务器 |
| `x113` | HTTP 代理启用标志 |
| `x114` | 信号% |
| `x115` | SDK 版本 |
| `x118` | RIL daemon (`running`) |
| `x123` | WebView UA |
| `x125` | 随机 ID |

**运行时已加载 dex/jar**

| 字段 | 含义 |
|---|---|
| `x126` | 80+ 条运行时加载的 dex/jar 路径，包括系统 APEX、`base.apk!classes2..22.dex`、`Anonymous-DexFile@xxx.jar`（来自 Robust 热修复）、`app_petal/` 插件、系统 framework jars、无物理路径的 `Anonymous-DexFile@...` |
| `x127` | `.`（表示所有完整性已校验） |

**Configuration / 完整性 MD5**

| 字段 | 含义 |
|---|---|
| `x128` | 完整 `Configuration.toString()` |
| `x129` / `x226` | netlink 拒绝文本 |
| `x135` | 系统分区 MD5 |
| `x137` | `build.prop` MD5 |
| `x138` | `default.prop` MD5 |
| `x143` | x103 的 MD5 |
| `x205` | `{x3: SHA1}` 关键路径 SHA1 |

**冗余 / 防篡改**

| 字段 | 含义 |
|---|---|
| `x144` | 同一指纹**连读 5 次**（防内存改写交叉校验） |
| `x145` | `{package: signature}` 映射 |
| `x146` | GID（APK 签名 SHA384） |

**文件 inode / 路径完整性**

| 字段 | 含义 |
|---|---|
| `x165` | 9 个文件的 inode/timestamp 元组（`timestamp-inode-devid-mode-offset`） |
| `x189` | inode 引用 |
| `x193` | IMS 状态 |
| `x198` | Activity 启动来源 |
| `x199` | 触摸序列（正常 = `[]`） |

**环境与安全**

| 字段 | 含义 |
|---|---|
| `x202` / `x203` | 安全标志 |
| `x206` | 签名一致 |
| `x207` | 签名校验冗余 |
| `x208` | statfs `{c, d, f, s, t, tt}` |
| `x209` | `Build.SERIAL`（Android 10+ = `unknown`） |
| `x210` | `Build.DISPLAY` 副本 |
| `x213` | 锁屏 |
| `x214` | Verified Boot |
| `x215` | SELinux |

**TLS / MITM 检测**

| 字段 | 含义 |
|---|---|
| `x227` | TLS 证书链：DigiCert → DNSPod → `*.xiaohongshu.com` |
| `x228` | MITM 检测列表 |

**输入设备**

| 字段 | 含义 |
|---|---|
| `x230` | 来自 `/proc/bus/input/devices`：bus、key flags、name |

**网络**

| 字段 | 含义 |
|---|---|
| `x240` | `wlan0` IP / MAC 映射 |

**关键文件 MD5**

| 字段 | 含义 |
|---|---|
| `x241` | 12 个关键文件的 MD5 映射 |

**杂项小标志**

| 字段 | 含义 |
|---|---|
| `x244` / `x251` / `x252` 等 | 杂项小标志（多为 0/1 状态） |

**CPU 与 Build 静态字段**

| 字段 | 含义 |
|---|---|
| `x247` | 每核 CPU 占用 |
| `x248` | 完整 Build 静态字段 JSON：BOARD、SOC_MANUFACTURER=Google、SOC_MODEL=Tensor、BOOTLOADER、SKU、IS_EMULATOR=false 等 |

**进程内存比**

| 字段 | 含义 |
|---|---|
| `x265` | `78:32` RSS/VSIZE 比（约 41% 常驻） |

**启动时间戳与 Key Attestation**

| 字段 | 含义 |
|---|---|
| `x266` | 上次启动时间戳 |
| `x274` | **5 级 Key Attestation 证书链**（Key Attestation CA → Droid CA2 → Droid CA3 → TEE app cert → Android Keystore Key），元数据 `{f:1, h:1, v:0, z:1}` 表示成功/硬件支持/TrustedEnvironment/通过；level-5 证书 extension 嵌入 `com.xingin.xhs, google, oriole, oriole, Google, Pixel 6` |

**cgroup**

| 字段 | 含义 |
|---|---|
| `x276` | cgroup 4 层：`3:cpuset:/top-app\n2:cpu:/system\n1:blkio:/\n0::/uid_10396/pid_28625` |

**CPU 细节**

| 字段 | 含义 |
|---|---|
| `x277-x288` | CPU 详情：`x278=0xd44`（features）、`x279=0x41`（ARM implementer）、`x280=0x412fd050`（`sched_getaffinity`）、`x281=0x0`（idle affinity）、`x283=16`（`availableProcessors()`）、`x284=21`（频率档）、`x287=[5,6,9,11,13,14]`（在线核）、`x288=[0..7]`（全 8 核） |
| `x282` | 三阶段耗时 |

**SDK 阶段**

| 字段 | 含义 |
|---|---|
| `x294-x308` | 额外预留/标签字段 |
| `x295` | ~5.5 KB Base64 加密指纹校验载荷 |
| `x301` | SDK status `LOADED` |
| `x304` | TEE key 有效 |
| `x305` | 错误码 |
| `x306` | GPU/OpenGL ES：`vendor=ARM`、`renderer=Mali-G78`、`version="OpenGL ES 3.2 v1.r38p1-..."`、`totalMemory=8081297408`、`vendorID=5045`、`eglImplementation=mali`、`shadingLanguageVersion="OpenGL ES GLSL ES 3.20"`。**GPU 指纹是核心反模拟器探针**（真机 = Mali-G78/ARM-5045，模拟器 = Swiftshader/ANGLE/VirGL） |
| `x307` | `3` = 请求类型 = 指纹上报 |
| `x308` | `{"3":"...","s":0}` 环境总结 |

**传感器**

| 字段 | 含义 |
|---|---|
| `x58` | 30+ 传感器与厂商：LSM6DSR (STMicro)、MMC56X3X (MEMSIC)、TMD3719 (AMS)、ICP10101 (InvenSense)、VD6282 (STMicro)、Camera V-Sync (Google) 等，外加虚拟复合传感器与 wake-up 传感器 |

---

## 6. 代码完整性自检（Frida 检测机制）

Frida log dump 显示 SDK 内部生成的 JSON：

```jsonc
{
  "global": {
    "code-patch-check": [
      "detect tiny code patch!",
      "hash[0] = 4374629818410490178 hash[1] = 4645753627478656280",
      "hash[0] = 5413470446597402419 hash[1] = 8056311877987315933",
      "hash[0] = 10375212707557656182 hash[1] = 8208716317797788442",
      "hash[0] = 14789127626113654434 hash[1] = 6362402964521876721",
      "hash[0] = 17540343258695014053 hash[1] = 9019156388800152406",
      "hash[0] = 2332245349839540828 hash[1] = 15792192795412816771",
      "hash[0] = 4421864420400602596 hash[1] = 6671147805527458612",
      "hash[0] = 1230701200501964179 hash[1] = 2093930530577762092",
      "hash[0] = 1785509536373080354 hash[1] = 10386807068207794068"
    ],
    "code-patch-prepare": [
      "",
      "sections[0] = 0x0000007677557e80 - 0x0000007677558a00",
      "sections[1] = 0x0000007676f1c300 - 0x0000007676f2e540",
      "sections[2] = 0x0000007676f5cbb0 - 0x0000007677557e80",
      "sections[3] = 0x0000007676f2e540 - 0x0000007676f37154",
      "sections[4] = 0x0000007676f37158 - 0x0000007676f5cbac",
      "sections[5] = 0x0000007676e1b288 - 0x0000007676e1c710",
      "sections[6] = 0x0000007676e1d028 - 0x0000007676e1d9b8",
      "sections[7] = 0x0000007676e1d9b8 - 0x0000007676f1b1d0",
      "sections[8] = 0x0000007676f1b1d0 - 0x0000007676f1c2e0"
    ]
  },
  "s1": {}, "s11": {},
  "s6": { "9": ["", "FD 7B BF A9"] },
  "s7": { "4": ["", "package name: com.xingin.xhs"] },
  "t":  {
    "26": ["", "/data/data/com.xingin.xhs",
              "/data/data/./../user/0/com.xingin.xhs",
              "/proc/self/maps"],
    "29": ["zkqsExVMbegb.ZpIkGBRG.XvFWWExBridge$HookerCallback"]
  }
}
```

机制：

- `code-patch-prepare` 枚举 9 段内存范围。
- `code-patch-check` 对每段计算一对 64-bit 哈希（疑似 SipHash 类带种子；每段 16B）→ 任一对与基线不符 → emit `"detect tiny code patch!"`。
- 同时**直读关键函数序言字节**：`FD 7B BF A9` = `STP X29, X30, [SP, #-16]!`——若被 Frida trampoline 替换则立刻识别。
- 读取 `/data/data/com.xingin.xhs`、`/data/data/./../user/0/com.xingin.xhs`、`/proc/self/maps`——遍历进程映射，寻找 trampoline / 未授权 .so。
- Java 端反射检测已知 hooker 类名（此处 = `XvFWWExBridge$HookerCallback`）。

---

## 7. 心跳 `t` 字段两阶段能力位

**初始化阶段**（c=1..99）：

```json
"t": {"c":0, "d":0, "f":0, "s":4098, "t":0, "tt":[]}
```

**激活阶段**（c≥100）：

```json
"t": {"c":45, "d":4, "f":0, "s":4098, "t":68577897, "tt":[1]}
```

字段含义：

- `c` = 已完成的风控检测周期。
- `d` = 检测到的状态变化次数。
- `s = 4098` 常量。
- `t`（如 `0x4166A69`）= 单调累加的事件计数 / 计时器。
- `tt = [1]` = 触发的检测类型位。

---

## 8. 其他被发现的 API 端点

| URL | 用途 | 备注 |
|---|---|---|
| `https://apm-native.xiaohongshu.com/api/collect` | APM 性能上报 | gzip，UA `okhttp/3.14.9.033` |
| `https://t2.xiaohongshu.com/api/collect` | 数据采集 | gzip，~879 字节 |
| `https://edith.xiaohongshu.com/api/...` | 主业务 API | `OkHttp CacheInterceptor` |

---

## 9. 工具 / 方法学（推断）

- **IDA Pro**——反编译 + 6 特征模式匹配字符串解密器。
- **angr**（用 `SYMBOL_FILL_UNCONSTRAINED_*`，**避开** zero-fill）——对 BR 反混淆中 Type 8 的索引开关做兜底。
- **自定义 ARM64 模拟器**——多状态 CSEL 分裂、saved-field 符号化 memory key。
- **ELF / relocation 解析**——给 `ADRP+ADD` 表基址定位。
- **Frida (JS)**——运行时 SSO 字符串读取、JSON 树 dump、hook 日志化指纹采集流水线；SSO 读取器函数已在第 3 节给出。
- **Python (`shield.py`)**——驱动每设备的 `main_hmac` 解密，使用抠出的硬编码轮密钥。
- **抓包对比**——用真实 JSON 请求体对照加密的 `d`，比较 `mini-mua`(~90 字段) 与全量上传(~200 字段) 的差集，是分析的关键支点。

---

## 10. 给后续平台分析的可复用规律（提炼）

把对小红书的发现升级为通用观测：

- **Native SO 通常都有 BR 类花指令**——任何算法推理之前先做模式归一化。本文 8 类对 OLLVM 系（及其衍生）ARM64 obfuscator 普遍可复用。
- **字符串解密器是分析的基石**——每个 native 风控 SDK 都有一个识别度极高的 5 / 6 特征解密器（魔数 + 小模数 switch + 4~8 op + do-while + 原地写回）。找到它，dump 出整个字典，设计意图 80% 暴露。
- **JSON 节点 ABI 不会是标准的**——很多 App 用 SSO + RB-tree。一次还原节点布局，就能用 Frida 任意 dump 现场数据。
- **`xN` 数字键是混淆战术**——把它们当不透明槽，靠"哪个 `getprop` / Java 反射 / 系统调用 写它"反查含义。`xN ↔ source` 对应关系是罗塞塔石碑。
- **厂商伪造字段经常出现**——比对 `MANUFACTURER` / `BRAND` / `MODEL` / `platform` / `hardware`。一旦看到硬编码 `"Vivo"` 与 `Pixel`/`Samsung` MODEL 共存，就知道 SDK 在做厂商伪造，且有"Mi/Coolpad/HW OAID 服务 → 硬编码"的回退链。
- **加密栈是分层的，且常被改过**——永远先假设：AES 是表改过的（自定义 MixColumns/ShiftPerm/Rcon/SubWord），MD5/HMAC 是常量改过的（轮 shift、K、初始 IV），密钥派生涉及设备绑定材料 + 硬编码 XOR 常量。标准库的"匹配"只是表面。
- **5 行明文模板**（`METHOD\nPATH\nQUERY\nSHA256(BODY).hex()\nJWT`）在国内多家 App 风控 SDK 通用。
- **"修改版对称体 + 外层 RC4 with 伪装代码字符串"** 是国内常见的二次封装；外层 RC4 key 经常假装成无害源码字面量（`"std::abort();"`、`"AbCd1234"` 之流）。
- **反调试 / 反 Frida 是分层的**：
  - 文件系统探针（`/proc/self/maps`、`/data/data/<pkg>` 与其 `..` 路径别名）。
  - 函数序言字节快照（`FD 7B BF A9` = `STP X29, X30, [SP, #-16]!`）。
  - 周期性对固定大小内存区做 64-bit 哈希（`code-patch-check` 机制）。
  - DEX 完整性（Robust/Anonymous-DexFile 出现 + MD5）。
  - Java 反射查已知 hooker 类名。
  - TEE Key Attestation（5 级 X.509 链证明硬件 backed key）——绕得最难的一项。
  - SELinux / Verified Boot / 官方 `release-keys` / cgroup 路径 / `availableProcessors` 不一致。
  - GPU 是**头号**模拟器特征（Mali/Adreno/PowerVR/Apple vs Swiftshader/ANGLE/VirGL）。
- **心跳字段位图**通常编码 SDK 状态机。忠实复现需要先跑完 `c<100` 周期再进入 active。
- **API 端点清单**：APM (`apm-native.*`)、数据采集 (`t2.*`)、业务 (`edith.*`) —— 三者请求格式一致性是稳定的回放校验。
- **冗余字段**（`x144` 同指纹 5 次、`x231/x232` 与 `x236/x237` 冗余存储、`x34/x35` 冗余电池%）专门用来抓懒人 spoofer——回放工具必须保持一致。
- **不要硬填没把握的字段**——保持不确定性比强行编造一个值更安全。`x244, x251, x294, x296` 这一类要标注为不透明槽。

---

## 附 A：硬编码常量速查（碎片化但都验证过）

| 名称 | 值 |
|---|---|
| 字符串解密魔数 | `0xBD69BD22` |
| 字符串解密器函数数 | 10 |
| `x-mini-s1` hash32 字节变换 | `0xD0`, `0xF4`, `0x8B`, `0x4E` |
| `shield` RC4 key | `"std::abort();"`（13 字节） |
| `shield` 输出前缀 | `"XY"` |
| `aes_decrypt_main_hmac` 轮密钥 | 11 条，硬编码（从 trace 抠出） |
| `transform_16` 矩阵规模 | 128 × 128 GF(2) + 16B 偏移 |
| `transform_16` 等价指令数 | 5288 条 ARM64 NEON |
| 心跳常量 `s` | `4098` |
| 函数序言指纹 | `FD 7B BF A9`（`STP X29,X30,[SP,#-16]!`） |
| epoch 偏移 | `1230768000000`（2009-01-01） |
| App ID `a` | `ECFAAF01` |
| 平台标识 `p` | `a` = Android、`i` = iOS |
| X25519 basepoint | `9` |
| 设备指纹采样冗余次数 | `x144` 连读 5 次 |
| Key Attestation 证书链层数 | 5 |
| `code-patch-check` 内存段数 | 9 |
| 每段双哈希长度 | 64-bit × 2 |

## 附 B：保留为 BR 的载体白名单（小红书 libtiny.so）

```
0x19FDBC BR X8
0x37C7D4 BR X8
0x3FF9AC BR X8
```

## 附 C：BR 改写工作样例索引

| 起始地址 | 类型 | 备注 |
|---|---|---|
| `0x3AC8E0` ~ `0x3AC8F4` | Type 4 | 副作用上提 + `B.cond + B + NOP` |
| `0x4AAD3C` | Type 5（含上游 CSEL） | 锚点 `X28=0x772000`，`[X28+0xB50]+const` 解载体 |
| `0x1A5788` | Type 8 | angr 验证 3 路 index → CMP/B.EQ + B |
| `0x185F40 → 0x19E0E4` | Type 7 | 真调用尾分派 |
