# References Index — app-riskcontrol-analysis

本目录收录每个被分析平台 / SDK 的逐字技术笔记。`SKILL.md` 仅提供**通用工作流**，平台特定细节都放在这里，按需加载。

## 案例索引

| App / 平台 | SO / SDK | 关键参数 | 加密栈摘要 | 反检测亮点 | 参考文件 |
|---|---|---|---|---|---|
| 小红书 Xiaohongshu (`com.xingin.xhs` 9.24.0) | `libtiny.so` | `x-mini-mua`, `x-mini-s1`, `x-mini-sig`, `shield` | X25519 ECDH（basepoint=9）+ 修改版 AES-128-CBC（自定义 MixColumns/ShiftPerm，固定 11 条轮密钥）+ 修改版 HMAC-MD5（改 K/shift/IV + NEON 字节反转）+ RC4(`"std::abort();"` 13B 硬编码 key) + base64url 信封；sig 用 SHA256 + `transform_16` 128×128 GF(2) 仿射 | `code-patch-check` 9 段内存周期性 64-bit 双哈希；函数序言 `FD 7B BF A9` 探针；`/proc/self/maps` 与 `/data/data/.../user/0/...` 路径走查；TEE Key Attestation 5 级证书链；GPU `Mali-G78` vs Swiftshader 模拟器探针；`x144` 同指纹连读 5 次冗余校验；Java `XvFWWExBridge$HookerCallback` 反射探针 | [xhs-libtiny-notes.md](xhs-libtiny-notes.md) |

> 后续条目按上面这一行的列结构追加。

## 如何新增条目

收到新平台的风控分析资料后：

1. 在本目录新增一份 `<short-app-name>-notes.md`，文件首部放一张 5 行摘要表（**包名 / SO / 参数名 / 加密栈 / 反检测亮点**），随后是逐字技术内容（按"BR 反混淆 / 字符串解密 / JSON ABI / 加密栈 / xN 字段 / 自校验 / 上传 schema / 心跳 / 姊妹接口"分节）。
2. 在上面这张表里追加一行，注明该文件位置。
3. 如果该平台引入了**全新的工作流环节**（例如 V8 字节码风控、JNI 跨进程通信、iOS LLVM bitcode 加固、WASM 风控），再到 `../SKILL.md` 里**只补对应一节** Path，不要重写已有路径。
4. 通用规律写进 `SKILL.md`，样本特定细节写进 `references/<平台>-notes.md` —— 这是技能能持续扩张而不臃肿的关键。

## 文件命名约定

- `xhs-` 小红书 / Xiaohongshu
- `douyin-` 抖音 / TikTok
- `wechat-` 微信
- `meituan-` 美团
- `bili-` 哔哩哔哩
- `taobao-` 淘宝
- `pdd-` 拼多多
- `kuaishou-` 快手

后接 SO 名或 SDK 名，例：`xhs-libtiny-notes.md`、`douyin-libcms-notes.md`、`meituan-mtguard-notes.md`。
