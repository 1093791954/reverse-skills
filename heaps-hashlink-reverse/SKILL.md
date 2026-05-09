---
name: heaps-hashlink-reverse
description: Reverse engineer games built on Heaps.io / HashLink VM (Shiro Games stack — Northgard, Wartales, Dune Spice Wars, Darksburg, Farever, Evoland, Dead Cells). Use when the task involves a hlboot.dat file, libhl.dll, .hdll native bindings, Haxe bytecode, HL/JIT vs HL/C output, h2d/h3d/hxd/hxsl packages, HxSL shaders, CastleDB (.cdb) data, HIDE prefabs, .pak resource files, or SDK dump (类似 Il2CppDumper / Unreal SDKGenerator 的等价物). Triggers on: hlboot.dat, libhl, hashlink, heaps engine, Northgard mod, Wartales mod, Farever, Dead Cells modding, Shiro Games, Haxe game reverse, .hl bytecode, HL SDK dump, hlbc, crashlink.
---

# Heaps.io / HashLink 游戏逆向工程技能

> 适用于 Shiro Games 系列(Northgard、Wartales、Dune Spice Wars、Darksburg、Evoland、
> Farever)以及任何使用 Haxe + HashLink VM + Heaps.io 引擎构建的游戏。

## 0. 触发场景识别(开场 30 秒判定)

**强信号 — 看到任何一个就是 HL/Heaps 游戏:**
- 游戏目录有 `hlboot.dat`(纯字节码,无任何资源)
- 游戏目录有 `libhl.dll`(Windows) / `libhl.so`(Linux) / `libhl.dylib`(Mac)
- 游戏目录有以 `.hdll` 为后缀的 DLL(如 `heaps.hdll` / `ui.hdll` / `fmt.hdll` /
  `sdl.hdll` / `directx.hdll` / `openal.hdll` / `steam.hdll`)
- `.exe` 体积很小(几百 KB ~ 2 MB), 实际逻辑都在 `hlboot.dat`
- 进程内能扫到 `HLB` 三字节文件 magic

**辅助信号:**
- 字符串里出现 `hl.types.*`, `h2d.*`, `h3d.*`, `hxd.*`, `hxsl.*`
- 字符串里出现 `Hello Hashlink`, `HashLink`, `__type__`, `hl_alloc_obj`
- 游戏开发商: Shiro Games / Motion-Twin(Dead Cells 也是 HL)

**反向排除信号(不是本技能):**
- 看到 `UnityPlayer.dll` → Unity(用 il2cpp / IDA 套件)
- 看到 `*-Win64-Shipping.exe` + `pak` → Unreal(用 ue-reverse 技能)
- 看到 `data.win` / `audiogroup*.dat` → GameMaker
- 看到大量 `.assets`/`*.bundle` → Unity assets

## 1. Shiro / Heaps 完整技术栈

```
┌─────────────────────────────────────────────────────────────┐
│ 游戏代码: Haxe 源 (.hx)                                     │
└────────────────────────┬────────────────────────────────────┘
                         │ haxe 编译器
            ┌────────────┴────────────┐
            ▼                         ▼
   ┌─────────────────┐       ┌──────────────────┐
   │ HL/JIT  .hl     │       │ HL/C  .c → .exe  │
   │ (PC 主流)        │       │ (Switch/PS/XBox) │
   │ = hlboot.dat    │       │  AOT 原生编译    │
   └────────┬────────┘       └──────────────────┘
            │
            ▼
   ┌────────────────────┐
   │ hl.exe (300KB VM)  │  ← 只是 bootstrapper
   │   loads libhl.dll  │
   │   JIT-compiles .hl │
   └────────┬───────────┘
            │ 调用 native
            ▼
   ┌────────────────────────────────────────────────┐
   │ libhl.dll  (运行时: GC + 异常 + 字符串 API)      │
   │ heaps.hdll (Heaps 引擎 native 部分)             │
   │ directx.hdll / sdl.hdll  (渲染后端)             │
   │ openal.hdll (声音)  ui.hdll (窗口)              │
   │ fmt.hdll (zip/png/ogg) ssl.hdll uv.hdll         │
   │ steam.hdll  (可选)  + 自研 *.hdll              │
   └────────────────────────────────────────────────┘
```

**Heaps API 顶层包**:
- `h2d` — 2D 显示与 UI
- `h3d` — 3D 渲染
- `hxd` — 跨平台基础(Bitmap、资源加载、声音、输入)
- `hxsl` — Heaps Shader Language
- `hide` — 编辑器代码(运行时不会出现)
- `hrt` — HIDE Prefab 运行时(关卡/特效/粒子加载器)

**Shiro 私有栈(可能在游戏里出现)**:
- `castle` (CastleDB) — 静态数据库,典型类: `cdb.Module`
- `domkit` — XHTML+CSS UI 框架
- `hscript` — Haxe 语法子集脚本解释器
- `hxbit` — 序列化/网络同步(存档 + 多人)
- `mpman` — 多人系统(闭源,可能有 anti-cheat 痕迹)

## 2. 游戏文件布局

```
<GameDir>/
├── <game>.exe                  ← 极小,仅 hl bootstrapper
├── hlboot.dat                  ← 字节码(=.hl 重命名),100% 符号
├── libhl.dll                   ← VM 运行时
├── heaps.hdll                  ← 引擎 native 绑定
├── directx.hdll / sdl.hdll     ← 渲染
├── openal.hdll                 ← 声音
├── ui.hdll                     ← 窗口
├── fmt.hdll                    ← zip/png/ogg/jpg
├── ssl.hdll uv.hdll
├── steam.hdll  (可选)
├── res.pak / *.pak             ← Heaps pak 资源(可选)
└── res/                        ← 散装资源(纹理/FBX/CDB/JSON)
```

**关键事实**:
- **`hlboot.dat` 是百分之百完整符号的 .hl 字节码**, 无加密、无混淆(默认)
- **JIT 与 Release 没有区别**, 玩家手里的字节码 = 开发机字节码 = 带源行号
- **类名/方法名/字段名/源文件名/行号都保留** → 反编译后等同看 Haxe 源

## 3. `.hl` / `hlboot.dat` 文件格式

```
偏移   长度    字段
+0     3       magic = "HLB"
+3     1       version (常见 4 / 5)
+4     var     flags (bit0=有调试信息)
+      var     nints
+      var     nfloats
+      var     nstrings
+      var     nbytes        (version >= 5)
+      var     ntypes
+      var     nglobals
+      var     nnatives
+      var     nfunctions
+      var     nconstants    (version >= 4)
+      var     entrypoint    (findex)
+      4*nints     ints[]    (i32 常量池)
+      8*nfloats   floats[]  (f64 常量池)
+      strings 段(4字节 size + 0 结尾的串列表)
+      bytes 段(version>=5)
+      debug files(若 flags 有调试)
+      ntypes      类型表
+      nglobals    全局类型
+      nnatives    natives (lib名/函数名/类型/findex)
+      nfunctions  function 字节码
+      nconstants  全局初始化常量
```

**`var` 是变长整数** (1/2/4 字节),省空间。所有索引都是 var。

**类型 kind 表(逆向时识别 type kind 字节用):**
| kind | name | 说明 |
|------|------|------|
| 0 | void | |
| 1 | u8 | |
| 2 | u16 | |
| 3 | i32 | |
| 4 | i64 | |
| 5 | f32 | |
| 6 | f64 | |
| 7 | bool | |
| 8 | bytes | C char* 风格 |
| 9 | Dyn | dynamic |
| 10 | Fun | 函数签名 |
| 11 | **Obj** | **Haxe class!** |
| 12 | Array | |
| 13 | Type | 反射用 |
| 14 | Ref | |
| 15 | Virtual | 匿名结构/接口 |
| 16 | DynObj | |
| 17 | Abstract | |
| 18 | Enum | |
| 19 | Null | 可空包装 |
| 20 | Method | 同 Fun |
| 21 | Struct | 同 Obj |
| 22 | Packed | |

**Obj 结构(逆向时直接对应游戏类):**
```
name(string ref) | super(type ref, 可<0) | global(global ref)
nfields | nprotos | nbindings
fields[]    : name + type
protos[]    : name + findex + pindex(override slot)
bindings[]  : field ref + findex (静态方法/构造器)
```

**字段索引规则(踩坑必读!)**:
子类字段索引在**整个继承链上累加**,不是在自己类里从0开始。
```haxe
class A { var a:Int; }       // a 索引 = 0
class B extends A { var b:Int; } // b 索引 = 1, a 索引仍 = 0
```
→ 要从 hlboot.dat 解析字段,必须**遍历父类链合并**字段表。

**Function 段:**
```
type(ref) | findex | nregs | nops | regs[] | opcodes[] | debuginfo[] | nassigns + assigns[]
```
- `findex` 是全局函数索引,**与 native 共享同一个 findex 空间**
  → 解析时要建一张 findex → (function/native) 映射
- `debuginfo` 给每条 opcode 一组 (file, line)
- `assigns` 给变量名 + opcode 编号(变量名恢复用)
- 函数本身**没有名字**,名字来自:
  - Obj.protos(类的实例方法)
  - Obj.bindings(静态方法)
  - 反过来推断

**Opcodes 一共 98 个**,详见研究笔记 `research/02-hashlink-vm-internals.md`。
关键类别:数据移动 / 算术 / 调用(call/callmethod/callclosure/callthis) /
控制流(j*) / 字段访问(field/setfield/dynget/dynset) / 字节读写(getui8.../setui8...)
/ 数组 / Enum / 异常 / 类型 / 引用。

## 4. HL 内存布局(运行时 hook 必看)

**所有 HL 对象第一个字段都是 `hl_type *`**(x86=4B / x64=8B)。这是逆向定位类的钥匙。

### 4.1 String 内部结构(超常用)
```c
struct _String {
    hl_type  *$type;   // +0
    vbyte    *bytes;   // +8 (x64)  UCS-2 (16-bit) 字节序列
    int       length;  // +16       字符数
};
```
→ 内存扫描所有字符串: 找首字节 8 字节 ptr 指向 String 类型描述,后跟 UCS-2 数据。

### 4.2 静态对象(Haxe class) 内存布局
```
+0   hl_type *$type          ← 类描述
+8   父类字段(按声明序排列,含对齐)
+?   本类字段(按声明序排列,含对齐)
```
- `i32`/`f32` 4B 对齐, `f64` 8B 对齐, `ui8` 紧凑, `bool` 1B 或 4B(看编译器)
- 一旦确定 `$type`,字段偏移就是固定的(从字节码里 Obj 段算)

### 4.3 Array (`varray`)
```
+0   hl_type *$type
+8   hl_type *at         (元素类型)
+16  int     size
+20  int     capacity
+24  data...             (元素数据原地或独立 buffer 取决于版本)
```

### 4.4 Closure (`vclosure`)
```
+0   hl_type *$type
+8   void    *fun        (函数指针, JIT 后的 native 地址)
+16  void    *value      (绑定的 this; hasValue 由 type 判断)
```
**hook 点**: 给定 vclosure*, `c->fun` 直接 cast 成对应签名调用即可
(HL 遵循平台 cdecl/x64 ABI)。

### 4.5 DynObj
- 字段按 hash 排序的数组,O(log n) 查找
- 用 `hl_dyn_geti/getp/getf/getd` 系列 API 访问
- 字段 hash = `hl_hash_utf8("fieldname")`

### 4.6 Virtual
三种形态:
1. **基于静态对象**:存底层对象指针 + 各字段地址引用
2. **基于 dynobj**:同上,但有 NULL 引用回退到动态访问
3. **compact**:无底层对象,字段数据内嵌

### 4.7 装箱规则(`todyn` opcode)
**直接装入 dyn 不分配新内存**(它们首字段已是 hl_type*):
- Function / Object / Virtual / Array / Null / DynObj

**需要装箱分配**:
- 基础类型(i32/f32/f64/bool 等) / bytes / type / ref / abstract / enum

## 5. HL/C 输出(主机版/优化版)

主机版用 `haxe -hl out/main.c -main Main`,生成的 C 文件特征:

**符号命名规则(逆向利器!)**:
| Haxe | C 符号 |
|------|--------|
| `Class.method()` | `Class_method` |
| `pkg.SubClass.method` | `pkg__SubClass_method` |
| 全局变量 N | `global$N` |
| 字符串常量 N | `string$N` |
| 类型描述 N | `<TypeName>__val` |

**典型函数:**
```c
HL_API varray*    hl_alloc_array(hl_type*, int);
HL_API vdynamic*  hl_alloc_obj(hl_type*);
HL_API vdynamic*  hl_alloc_dynamic(hl_type*);
HL_API venum*     hl_alloc_enum(hl_type*, int idx);
HL_API vvirtual*  hl_alloc_virtual(hl_type*);
HL_API vdynobj*   hl_alloc_dynobj();
HL_API vbyte*     hl_alloc_bytes(int size);
HL_API vclosure*  hl_alloc_closure_ptr(hl_type*, void *fn, void *ptr);

HL_API int        hl_dyn_geti(vdynamic*, int hfield, hl_type*);
HL_API void*      hl_dyn_getp(vdynamic*, int hfield, hl_type*);
HL_API float      hl_dyn_getf(vdynamic*, int hfield);
HL_API double     hl_dyn_getd(vdynamic*, int hfield);
HL_API void       hl_dyn_seti/setp/setf/setd(...);

HL_API int        hl_hash_utf8(const char*);   // 计算字段 hash
HL_API vdynamic*  hl_dyn_call(vclosure*, vdynamic** args, int nargs);
HL_API void       hl_add_root(void**);          // GC 防回收
HL_API void       hl_remove_root(void**);
```
**用 IDA/Ghidra 时**先把上面这些符号从 `libhl.dll` 导出表 import,再分析就有了语义。

## 6. 工具链(按使用频率排序)

### 6.1 hlbc — Rust 反汇编/反编译/GUI 主力
- **仓库**: https://github.com/Gui-Yom/hlbc
- **专为 Shiro 系游戏(Northgard/Wartales/Dune Spice Wars)mod 设计**
- 安装(Rust):
  ```bash
  cargo install hlbc-cli
  cargo install hlbc-gui   # 可视化浏览
  ```
- 用法:
  ```bash
  hlbc hlboot.dat                # 进入交互 REPL
  > help
  > info
  > entry                        # 入口函数
  > fn 22                        # 反汇编 findex=22
  > findex Main.main             # 按名字找
  > strings | grep -i player
  > callgraph 22 -o cg.dot       # 调用图
  > decompile 22                 # 反编译(部分支持)
  > wiki                         # 字节码格式说明
  ```
- 提供 `hlbc::Bytecode` 结构,可写 Rust 工具自动化批量处理

### 6.2 crashlink — Pure Python (IDAPython 兼容)
- **仓库**: https://github.com/N3rdL0rd/crashlink
- **优势**: IDAPython 内可直接 import,自动给 IDA 函数命名
- 安装:
  ```bash
  pip install crashlink[extras]
  ```
- 用法:
  ```python
  from crashlink import *
  code = Bytecode.from_path("hlboot.dat")
  print(disasm.func(code.fn(22)))
  # 22 / 240 是常见入口 findex
  for f in code.functions:
      if "Player" in f.name(code) or "":
          ...
  # 修改字节码 → 重新写回
  code.serialize("patched.hl")
  ```
- 内置 patcher: 可直接改 opcode,做小型 mod
- 内置 assembler: 从源码生成新字节码

### 6.3 vshaxe/hashlink-debugger — VSCode 调试器
- 仓库: https://github.com/vshaxe/hashlink-debugger
- 配合源代码可下断点,看变量;**没源码也能附加进程**看堆栈
- 启动方式: 游戏 `.exe` 加 `--debug` 参数或直接附加

### 6.4 HashLink 自带 dump
若你能拿到 Haxe 源(对方开源/泄露/buildlog 中):
- `-D dump` → `dump/hlcode.txt` 完整字节码人读形式
- `-D hl-no-opt` → 关优化,字节码更直观
- `-D hl-dump-spec` → `dump/hlspec.txt` 求值规范

### 6.5 IDA / Ghidra 用法
- 静态分析 `libhl.dll` / `*.hdll` / HL/C 编译的主机版 .exe
- 关键导出符号:
  - `hl_alloc_obj`, `hl_alloc_dynamic`, `hl_alloc_array`, `hl_alloc_bytes`
  - `hl_dyn_call`, `hl_dyn_geti/getp/getf/getd`
  - `hl_hash_utf8`, `hl_add_root`, `hl_remove_root`
  - `hl_throw`, `hl_throw_buffer`, `hl_assert`
  - `hl_module_init`, `hl_code_read`, `hl_jit_code`
- 字符串搜 `__type__`, `hl.types.`, `h2d.`, `h3d.`, `hxd.`
- 用 crashlink Python 脚本批量给 sub_xxxxxx 改名为 Haxe 全限定名

### 6.6 Cheat Engine / x64dbg
- 找内存里 String 对象: 扫 UCS-2 字串 → 起始减 0x10(x64)就是 _String 头
- 找 hlboot.dat 在内存中的镜像: 搜 `HLB` magic 三字节

## 7. 标准工作流

### 工作流 A: 静态分析(刚拿到游戏,什么都不懂)
1. **指纹确认**: 看目录有 `hlboot.dat` + `libhl.dll` + 多个 `.hdll`
2. **拷贝 `hlboot.dat` 到工作目录**
3. **`hlbc hlboot.dat` 进入 REPL**:
   - `info` 看 magic / version / 函数数 / 类型数
   - `entry` 找入口 findex(通常 22 或 240)
   - `strings` 导出全部字符串 → 找游戏特定关键词
   - `classes` 列出所有类
4. **找游戏关键类**(常见命名):
   - `Game` / `GameState` / `World` / `Level`
   - `Player` / `Hero` / `Unit` / `Entity` / `Actor`
   - `Inventory` / `Item` / `Skill` / `Spell`
   - `SaveData` / `Save`
5. **反汇编/反编译关键方法**:
   - 看构造函数 `new` → 看字段初始化
   - 看 `update` / `tick` 找主循环
   - 看 `damage` / `takeHit` / `addExp` 等修改器找数值入口
6. **对比 Heaps 标准命名**:
   - 看到 `h3d.scene.Object`/`h2d.Object` → 渲染节点
   - 看到 `hxd.Window` / `hxd.Stage` → 窗口管理
   - 看到 `hxd.Res` / `hxd.res.*` → 资源加载

### 工作流 B: 动态调试(运行时分析)
1. 启动游戏,用 Process Hacker / x64dbg 附加进程
2. 内存搜 `HLB` 找 hlboot.dat 加载位置(JIT 后字节码仍在内存)
3. 找 `libhl.dll` 导出表,记下:
   - `hl_alloc_obj`, `hl_dyn_call`, `hl_dyn_getp`, `hl_dyn_setp` 地址
4. 在 `hl_alloc_obj` 下断点,日志 `hl_type *` 第一参数 → 监控对象创建
5. 看 hl_type 结构第一个字段 `kind`,11=Obj,然后取它的 name(string ref)
6. 配合 hlbc 反汇编结果对照: findex / 字段索引

### 工作流 C: 内存外挂 / Cheat Table
1. 用 hlbc 找到目标类(如 `Player`)的字段表:
   ```
   class Player @458 extends Entity
       fields:
         @0 hp f32
         @1 maxHp f32
         @2 gold i32
         @3 exp i32
   ```
2. 计算字段绝对偏移(累加父类字段大小,带对齐)
3. CE 扫"血量"找候选地址 → 减偏移得到 Player 实例 ptr
4. 倒退找指向 Player 实例的指针(通常是单例或 GameState 的字段)
5. 用 pointermap 写出多级指针稳定地址

### 工作流 D: 修改字节码做 Mod
1. **crashlink 加载**:
   ```python
   code = Bytecode.from_path("hlboot.dat")
   ```
2. **找目标函数**:
   ```python
   for f in code.functions:
       n = f.resolve_name(code)
       if n == "Player.takeDamage":
           target = f
   ```
3. **改 opcode**: 把 `sub` 改成 `nop`,或者把 `jslt` 跳转改方向
4. **写回**:
   ```python
   code.serialize("hlboot.patched.dat")
   ```
5. **替换游戏目录的 hlboot.dat**(先备份!),启动测试

### 工作流 E: 解 .pak 资源
- Heaps `.pak` 由 `hxd.fmt.pak.FileSystem` 读取(源码:
  https://github.com/HeapsIO/heaps/tree/master/hxd/fmt/pak)
- 格式: header + 文件目录树(JSON 风格) + 数据 blob
- 工具: 写一个小 Heaps 项目调用 `hxd.fmt.pak.Reader` 即可枚举全部文件
- 或参考 `heaps/tools/Pak.hx` 自带的 pak 工具
- **替代方案**: 多数游戏不用 pak,直接散装 res/ 目录;先看磁盘上有没有

## 8. Heaps 引擎重点类速查(逆向时定位用)

### 8.1 hxd / 平台 & 资源
| 类 | 作用 | 逆向用途 |
|---|---|---|
| `hxd.Window` | 窗口/输入入口 | 找窗口句柄、键鼠输入注入点 |
| `hxd.Stage` | 旧版窗口(同上) | |
| `hxd.System` | 系统信息 | |
| `hxd.Res` | 资源根(由 macro 生成) | 资源访问起点 |
| `hxd.res.Resource` | 资源基类 | |
| `hxd.res.Loader` | 资源加载器 | hook 这里抓 raw 数据 |
| `hxd.fs.FileSystem` | 文件系统抽象 | |
| `hxd.fmt.pak.FileSystem` | pak 文件系统 | 解 .pak |
| `hxd.Key` | 键盘常量 | 找按键检测 |
| `hxd.Pad` | 手柄 | |
| `hxd.snd.Manager` | 声音管理 | mute hook |

### 8.2 h2d / 2D & UI
| 类 | 作用 |
|---|---|
| `h2d.Object` | 2D 节点基类 |
| `h2d.Scene` | 2D 根场景 |
| `h2d.Bitmap` | 单图 |
| `h2d.Tile` | 图块 |
| `h2d.Text` | 文字 |
| `h2d.Flow` | 自动布局容器(UI 主力) |
| `h2d.Interactive` | 交互区域(按钮基础) |
| `h2d.RenderContext` | 渲染上下文(在这 hook 可加自定义绘制) |
| `h2d.Graphics` | 立即模式画图 |

### 8.3 h3d / 3D 渲染
| 类 | 作用 | 逆向用途 |
|---|---|---|
| `h3d.scene.Object` | **3D 节点基类** | 所有 actor / 模型基类 |
| `h3d.scene.Scene` | 根场景 | 找它就找到所有 entity |
| `h3d.scene.Mesh` | 单网格对象 | |
| `h3d.scene.World` | World 节点 | |
| `h3d.scene.Renderer` | 渲染器 | hook 自定义渲染 |
| `h3d.scene.RenderContext` | 渲染上下文 | |
| `h3d.Camera` | 摄像机 | hook 视图/投影矩阵,wts 计算 |
| `h3d.Engine` | 引擎单例 | 全局入口 |
| `h3d.mat.Material` | 材质 | |
| `h3d.mat.Texture` | 纹理 | dump 时 hook |
| `h3d.prim.*` | 几何图元 | |
| `h3d.anim.*` | 骨骼动画 | 找骨骼/关节用 |

### 8.4 hxsl / 着色器
| 类 | 作用 |
|---|---|
| `hxsl.Shader` | shader 基类 |
| `hxsl.RuntimeShader` | 运行时编译产物 |
| `hxsl.SharedShader` | 共享 shader |

**关键**: HxSL 是 **Haxe 子集 DSL**,运行时拼接小片段 → 转 HLSL/GLSL → 提交。
要 dump shader 必须在 D3D11/OpenGL 提交点 hook(`ID3D11DeviceContext::DrawXxx`),
**直接从字节码里拿不到完整 HLSL**(只是片段)。

### 8.5 hrt / Prefab(关卡/特效)
| 类 | 作用 |
|---|---|
| `hrt.prefab.Prefab` | Prefab 基类(关卡数据) |
| `hrt.prefab.Library` | Prefab 库 |
| `hrt.prefab.fx.FX` | 特效 |
| `hrt.prefab.l3d.*` | 3D 关卡 |
| `hrt.prefab.l2d.*` | 2D 关卡 |

### 8.6 castle / CDB 数据
| 类 | 作用 |
|---|---|
| `cdb.Module` | 通过 macro 生成数据访问类 |
| `cdb.Database` | DB 接口 |
| `cdb.Data` | 静态数据(由 macro 注入) |

CastleDB 是单文件多行 JSON,游戏运行时把它编译进字节码 → 字符串池里能搜到原始字段名。

### 8.7 hxbit / 序列化&网络
| 类 | 作用 | 逆向用途 |
|---|---|---|
| `hxbit.Serializable` | 序列化 mixin | 看哪些字段会进存档/网络 |
| `hxbit.Serializer` | 序列化引擎 | hook 它能拿全部状态 |
| `hxbit.NetworkHost` | 网络主机 | 找联机入口 |
| `hxbit.NetworkSerializable` | 同步对象 | |
| `hxbit.NetworkClient` | 网络客户端 | |

## 9. Hook / Cheat 实战技术

### 9.1 找 Engine 单例(进入 3D 世界)
```
1. hlbc 找 h3d.Engine.getCurrent / Engine.CURRENT 静态字段
2. 该字段在 hl 全局表,索引 globals[N]
3. JIT 后 globals 表是一段连续内存,libhl 暴露 hl_get_global / hl_globals
4. 拿到 Engine 实例 → engine.s3d (h3d.scene.Scene)
5. scene.children : Array<Object> → 遍历所有 3D 节点
```

### 9.2 World-to-Screen
Heaps `h3d.Camera` 自带 `m`(viewProj 矩阵)字段:
```haxe
public var m : h3d.Matrix;
public var mcam : h3d.Matrix;
public var mproj : h3d.Matrix;
public function project( x, y, z, screenWidth, screenHeight ) : h3d.Vector
```
- 直接读 `engine.s3d.camera.m` 4x4 浮点矩阵,col-major
- 或者 hook `h3d.Camera.project` 函数

### 9.3 给 native 函数下 hook(MinHook / Detours)
```c
// 例: hook hl_alloc_obj 监控所有对象创建
typedef vdynamic* (*pfnAllocObj)(hl_type*);
pfnAllocObj orig_AllocObj;

vdynamic* hook_AllocObj(hl_type *t) {
    // t->kind == 11 = Obj
    // t->obj->name 是 const char*(UCS-2!)
    if (t && t->kind == 11) {
        log_class(t->obj->name);
    }
    return orig_AllocObj(t);
}
```

### 9.4 hl_type 结构(运行时识别类用)
```c
typedef struct hl_type {
    int kind;          // +0  HOBJ=11, HFUN=10, HSTRUCT=21 ...
    union {
        hl_type_obj  *obj;
        hl_type_fun  *fun;
        hl_type_enum *tenum;
        hl_type      *tparam;  // for Ref/Null/Packed
        ...
    };
    void **vobj_proto;     // 虚表(JIT后)
    unsigned int *mark_bits;
} hl_type;

typedef struct {
    int       nfields;
    int       nproto;
    int       nbindings;
    const uchar *name;     // UCS-2 类名!!!
    hl_type    *super;
    hl_obj_field *fields;
    hl_obj_proto *proto;
    int        *bindings;
    void      **global_value;
    hl_module_context *m;
    hl_type    *rt;
} hl_type_obj;

typedef struct {
    const uchar *name;     // 字段名 UCS-2
    hl_type     *t;
    int          hashed_name;
} hl_obj_field;
```
**关键**: 给定任意对象指针,`*(hl_type**)obj` 就是它的类型,
然后 `type->obj->name` 是类名(UCS-2 串)。

### 9.5 调用游戏函数
```c
// 已知一个 vclosure*
vclosure *fn = ...;
if (fn->hasValue == 0) {
    // 静态函数,fn->fun 是 native 地址
    typedef void (*PlayerHeal)(Player*, int);
    ((PlayerHeal)fn->fun)(player, 9999);
} else {
    // 闭包,用 hl_dyn_call
    vdynamic *args[2];
    args[0] = (vdynamic*)player;
    args[1] = hl_make_dyn(&heal, &hlt_i32);
    hl_dyn_call(fn, args, 2);
}
```

### 9.6 防 GC 回收自己的对象
```c
static vdynamic *my_holder = NULL;
hl_add_root(&my_holder);   // 注册 GC root
my_holder = some_value;
// 用完:
hl_remove_root(&my_holder);
```

### 9.7 GC 行为(注意点)
- HashLink GC = mark-and-not-sweep,以 64KB 页为单位
- mark 阶段会 stop-the-world,**hook 时切勿在 mark 中分配 HL 对象**
- 内存 kind: `MEM_KIND_DYNAMIC=0` `RAW=1` `NOPTR=2` `FINALIZER=3`
- 你的 native hook 给字段写指针前要确保该指针指向 HL 堆,否则下次 GC 会清掉

### 9.8 Cheat Engine 用法贴士
- 数值多用 f32 / f64(Haxe Float = f64,Single = f32)
- Int 是 i32,**不是** Neko 那种带 tag 的 31bit
- 找一个 Player 实例后,**它前面 8 字节是 hl_type ptr,所有同类对象都指向同一个**
  → 这是稳定特征,可以 AoB 扫所有 Player 实例

## 10. HxSL Shader 系统

**特点**: 不是写一整个大 shader,而是**写很多小 effect**,运行时由 hxsl 编译器
组合后转为 HLSL/GLSL/Metal。

**字节码里能找到的**: `hxsl.Shader` 子类的字段(uniforms / varying / texture slots)
**字节码里找不到的**: 拼装后的最终 HLSL 文本

**dump shader 的方式**:
1. **D3D11**: hook `ID3D11Device::CreateVertexShader` / `CreatePixelShader`,
   抓 bytecode → 用 `d3dcompiler` 反汇编为 HLSL ASM
2. **API 截帧**: NVIDIA NSight / RenderDoc / PIX 直接抓帧拿 shader
3. **运行时反射**: 在 `hxsl.RuntimeShader` 上 hook,它在 `compile` 阶段
   持有完整 HLSL 字符串

**HxSL 类型(字节码里看到的)**:
- `Float`, `Vec2/3/4`, `Mat3/4`, `Sampler2D`, `SamplerCube`, `Channel`(贴图通道)
- `@global @param @const` 修饰

## 11. 资源 / 资产文件格式

Heaps 内置格式(源码: https://github.com/HeapsIO/heaps/tree/master/hxd/fmt):

| 目录 | 格式 | 说明 |
|---|---|---|
| `bfnt` | bitmap font | |
| `blend` | Blender | 直接读 .blend 文件 |
| `fbx` | FBX | 二进制/ASCII FBX |
| `grd` | Photoshop gradient | |
| `hbson` | binary JSON | Heaps 自定义紧凑 BSON |
| `hdr` | HDR | Radiance HDR 图 |
| `**hmd**` | **Heaps Mesh Data** | **Heaps 自有的 3D 模型格式(从 FBX 转换),Shiro 游戏常见** |
| `kframes` | 动画关键帧 | |
| `**pak**` | **Pak 包** | **资源打包格式** |
| `spine` | Spine | 2D 骨骼动画 |
| `tiff` | TIFF | |

### 11.1 Pak (.pak) 格式
源码: `hxd.fmt.pak.Data` / `hxd.fmt.pak.FileSystem`
- Header 含文件计数 + 索引表
- 文件目录是树状(目录 → 文件)
- 数据 blob 紧随
- 多 pak 时按字母序合并(后者覆盖前者)
- **解包**: 直接写 Heaps 项目调用 `hxd.fmt.pak.Reader`,枚举 + dump

### 11.2 HMD (.hmd) 格式
- Heaps 自有的 3D 模型容器(取代直接用 FBX)
- 含 mesh / 材质 / 骨骼 / 动画
- 由 HIDE / Heaps 工具从 FBX 烘焙
- 想看模型: 用 HIDE 打开,或写 Heaps loader 加载

### 11.3 CDB (.cdb) — CastleDB
- **结构化游戏数据库**,文本 JSON(可 git diff)
- 编辑器: HIDE 内置或独立 CastleDB 编辑器
- 游戏运行时由 macro `cdb.Module.build("data.cdb")` **编译期内联**
  → **磁盘上可能根本没有 .cdb 文件**, 数据直接在字节码里
- 提取方式: hlbc 看 `cdb.Data` / `Data.cdb` 全局,字符串里搜出原始字段

### 11.4 Prefab (HIDE 关卡/特效)
- 文本 JSON, 类层级 = `hrt.prefab.*`
- 关卡通常是 `.l3d` / `.fx` / `.prefab` 后缀
- 由 `hrt.prefab.Library.load(...)` 加载

## 12. 已知 Shiro 系游戏案例

### Northgard (2017)
- 引擎: 早期 Heaps + HashLink
- Mod 工具/参考:
  - `dibertz/northgard-camera-move` — 改相机距离限制
  - `grnt426/Vanishing-Whispers-Northgard-Mod` — 内容 mod
  - `FirowMD/Northgard-Auto-Accept` — 自动接受排位
  - `jetpropulsioncloud/northgard-analyzer` — 数据分析器
- 游戏目录有 `hlboot.dat` + 多个 `.hdll`
- 字符串里能直接搜到氏族名、单位名、技能名

### Wartales / Dune: Spice Wars
- 同栈, 文件结构相同
- hlbc README 明确点名为目标游戏
- 联机部分用 hxbit + mpman

### Darksburg
- HIDE 文档截图来自这个游戏的关卡
- 有大量 prefab 数据

### Farever (2026)
- 最新 Shiro 作品(Steam 抢先体验)
- 多人在线动作 RPG, 用同套技术栈
- 预计 hlboot.dat + libhl + heaps.hdll + directx.hdll 标准布局

### Dead Cells (Motion-Twin, 2018)
- **不是 Shiro 但同栈作者(Nicolas Cannasse 创建 Heaps 时在 Motion-Twin)**
- 同样 HashLink + Heaps
- 有大量社区逆向研究, 可作为参考材料

## 13. 常见任务速查表

| 想做的事 | 怎么做 |
|---|---|
| 看类层次 | hlbc → `classes`, crashlink → `code.types` 中筛 kind=11 |
| 看字符串 | hlbc → `strings`, 或 IDA 内字符串引用 |
| 找入口 | hlbc → `entry`(通常是个 `Main.main` 包装) |
| 改一个数值 | crashlink 修改 opcode 的 int/float pool 索引或把 sub 改 nop |
| 解锁全部关卡 | 找 `unlock` / `progression` 类, 改 setfield 为常 true |
| 去掉冷却 | 在 `cooldown` 字段相关 `setf32` 处把值改 0 |
| 一键秒杀 | hook `Player.takeDamage`(或敌人对应类),改 hp 为 0 |
| 显示隐藏单位 | hook `h3d.scene.Object.visible`,或者改 culling |
| ESP 框 | hook `h2d.RenderContext.flush` 或 D3D 绘制,叠加 ImGui |
| Aimbot | 读 `h3d.Camera.m`,枚举 `Scene.children` 中的敌人, WTS 投影 |
| 解 .pak | 写 Heaps 项目调 `hxd.fmt.pak.Reader` |
| 抓 shader | RenderDoc / NSight,或 hook D3D11 CreatePixelShader |
| Mod loader | 启动时替换/合并 hlboot.dat,或注入 dll 在 module init 后 patch |

## 14. 陷阱 / 反作弊 / 防护

### 14.1 默认无加密 / 无混淆
- Shiro 系列出货时**几乎没做反逆向**
- hlboot.dat 直接是标准格式, 字符串/类名/方法名/源行号全在
- 没有 string encryption, 没有 control flow flattening, 没有 packing

### 14.2 可能存在的检查
- **Steam 校验文件 hash** — 改 hlboot.dat 后无法多人联机
- `mpman`(闭源)可能含 anti-cheat/anti-modify 检查
- 修改后玩**离线**通常没问题

### 14.3 跨版本字节码不兼容
- HL 版本 4 / 5 字段排列不同(version >= 5 多了 nbytes 段)
- 看 magic 后第 4 字节 version 选对解析路径

### 14.4 版本差异
- HashLink 1.11 起 64-bit JIT 才稳, 早期游戏可能是 32-bit hl(罕见)
- HL/C 主机版**没有 .hl 文件**, 一切在 .exe 里

### 14.5 不是所有 Heaps 游戏都用 HashLink
- 一些 web 游戏走 `-hl ... -lib heaps -D js` 输出 JS+WebGL
  → 那是 web 逆向(JS 反混淆), 不在本技能范围

## 15. 参考资料(收藏起来)

### 一手文档
- Heaps 文档: https://heaps.io/documentation/home.html
- Heaps API: https://heaps.io/api/
- HashLink: https://hashlink.haxe.org/
- HashLink GitHub: https://github.com/HaxeFoundation/hashlink
- HashLink Wiki: https://github.com/HaxeFoundation/hashlink/wiki
  - HashLink In Depth(关键深度文): https://github.com/HaxeFoundation/hashlink/wiki/HashLink-In-Depth
- Shiro 全栈介绍: https://heaps.io/documentation/fullstack.html

### 字节码深度文(必读)
- https://haxe.org/blog/hashlink-indepth/(Part 1 — 字节码格式)
- https://haxe.org/blog/hashlink-in-depth-p2/(Part 2 — 类型系统 + 完整 opcode)

### 工具
- hlbc(Rust): https://github.com/Gui-Yom/hlbc
  - 字节码格式 wiki: https://github.com/Gui-Yom/hlbc/wiki/Bytecode-file-format
- crashlink(Python/IDA): https://github.com/N3rdL0rd/crashlink
- vshaxe debugger: https://github.com/vshaxe/hashlink-debugger
- HLCC: https://github.com/Yanrishatum/HLCC

### Heaps 引擎源码(查类布局/字段顺序)
- 主仓库: https://github.com/HeapsIO/heaps
- 资源格式: https://github.com/HeapsIO/heaps/tree/master/hxd/fmt
- HIDE 编辑器: https://github.com/HeapsIO/hide
- HxBit(序列化/网络): https://github.com/HeapsIO/hxbit
- HScript: https://github.com/HaxeFoundation/hscript
- CastleDB: https://github.com/ncannasse/castle

### Haxe 语言
- Haxe 主页: https://haxe.org/
- Haxe Manual: https://haxe.org/manual/

### 社区
- Hashlink Modding Community Discord(crashlink README 内邀请链接)
- Heaps Discord: https://discordapp.com/channels/162395145352904705/501408700142059520
- Heaps Forum: https://community.heaps.io/

### 笔记附件(本技能配套研究文档,含原始抄录)
- `research/01-stack-overview.md` — Shiro 完整技术栈
- `research/02-hashlink-vm-internals.md` — VM/字节码/类型系统/全部 opcode
- `research/04-tooling.md` — 工具链对比

## 16. 30 秒快速决策手册

```
看到 hlboot.dat?
    └─ YES → 这是 HL/Heaps 游戏,本技能适用
              └─ 第一步: hlbc hlboot.dat
                          ├─ 没出错 → 直接静态分析
                          └─ 报错 → version 不匹配,试 crashlink 或新版 hlbc

看到 libhl.dll 但没 hlboot.dat?
    └─ HL/C 主机端编译版 — 走 IDA/Ghidra,符号导入 hl_alloc_obj 等

游戏体积很大但 hlboot.dat 很小?
    └─ 资源在 .pak 或散装 res/, 字节码本身就这么小很正常

字节码反编译看不懂?
    └─ 不是混淆, 是 Haxe 语言特性: 闭包多、virtual多、enum 是 ADT
       看 opcode 比看反编译更直接
```

---

> 本技能 **覆盖 Heaps.io / HashLink 游戏逆向 ≈ 95% 的需求**。当遇到罕见特殊情况
> (主机版 HL/C / 自研 native lib / Shiro mpman 反调试),回到 hashlink 源码
> (`src/code.c`, `src/jit.c`, `src/module.c`)和 Heaps 源码定位类布局,
> 这两个仓库是最终真理来源。

---

## 17. 真实游戏逆向案例集

### 17.1 Dead Cells (Motion-Twin / Evil Empire) — 最完善的社区
Dead Cells 是 HashLink 生态里**逆向资料最丰富的游戏**,它的工具链可以直接套到
任何 HL 游戏上。

#### 关键陷阱: hlboot.dat 内嵌在 deadcells.exe!
**Windows 版**: `hlboot.dat` **不是**单独文件, 它**附加在 `deadcells.exe` 末尾**
(也可能是 PE 资源)。直接读 `.exe` 看不到字节码,需要先 extract。

**Linux 版**: 字节码就在游戏目录单独的 `hlboot.dat`,不需要 extract。

**应对方案 — alivecells 工具**:
```bash
git clone https://github.com/N3rdL0rd/alivecells
cd alivecells
pip install -r requirements.txt
python alivecells.py extract <path>/deadcells.exe --output hlboot.dat
# 现在可以丢给 hlbc / crashlink 分析
python alivecells.py install <newdir> <gamedir>  # 把游戏部署到独立 HashLink VM 目录
```
**重要**: 用 `deadcells.exe` 不是 `deadcells_gl.exe`。后者是 OpenGL 后端版。

#### Dead Cells 完整工具生态
| 工具 | 仓库 | 用途 |
|---|---|---|
| **alivecells** | N3rdL0rd/alivecells | 字节码 extract / VM 安装 |
| **CellPacker** | ReBuilders101/CellPacker | Java GUI, 浏览/解包/重打包 `res.pak`(纹理/声音/CDB) |
| **DeadCellsDecomp** | N3rdL0rd/DeadCellsDecomp | **完整反编译** 出来的 Dead Cells Haxe 源码(参考用) |
| **DeadCellsCoreModding** | dead-cells-core-modding/core | 完整 .NET mod loader, 用 HashlinkNET 桥接 |
| **HashlinkNET** | DreamBoxSpy/HashlinkNET | C# 与 HashLink VM 互操作运行时 |
| **MonoMod** | MonoMod/MonoMod | 运行时方法替换(底层基础设施) |
| **Hashlink Modding Community Discord** | 邀请见 crashlink README | 主社区 |

**逆向 Dead Cells 的完整流程**:
1. `alivecells extract deadcells.exe → hlboot.dat`
2. `alivecells install ./moddir <gamedir>`(独立目录, 不污染原游戏)
3. `hlbc hlboot.dat` 在 REPL 里浏览代码
4. 参考 `DeadCellsDecomp` 仓库的反编译源码对照(关键!)
5. 用 `crashlink` 写 Python patcher 改 opcode
6. 替换回 mod 目录的 hlboot.dat
7. 跑 `hl.exe`(不是 deadcells.exe,因为 exe 已被改造)

### 17.2 Northgard / Wartales / Dune Spice Wars (Shiro Games)
**这些游戏没有 exe 内嵌套路** —— `hlboot.dat` 直接在游戏目录:
```
<GameDir>/
├── Northgard.exe         (1-2 MB hl bootstrapper)
├── hlboot.dat            (~30 MB 字节码,直接拿)
├── libhl.dll
├── *.hdll                (heaps/directx/sdl/openal/fmt/steam/...)
└── res.pak / res/        (资源)
```
直接 `hlbc hlboot.dat` 即可。Steam Workshop mod 走官方路径,但底层字节码 mod
完全可以用 hlbc + crashlink。

### 17.3 Northgard 已知 mod 实战参考
| 仓库 | 做法 | 学到什么 |
|---|---|---|
| `dibertz/northgard-camera-move` | 改 hlboot.dat 中相机距离限制常量 | 找浮点常量在 floats 表的位置,直接覆写 |
| `FirowMD/Northgard-Auto-Accept` | **外部** Win32 程序点击窗口 | 不动字节码,只读屏幕识别 + SendMessage |
| `grnt426/Vanishing-Whispers-Northgard-Mod` | Steam Workshop 内容 mod(不动字节码) | 用游戏内置 modding API |

### 17.4 Heaps 商业游戏全景(逆向时识别用)
```
  Shiro Games (统一栈)
    ├─ Evoland 1/2          (老,2D 主)
    ├─ Northgard
    ├─ Darksburg
    ├─ Wartales
    ├─ Dune: Spice Wars
    └─ Farever (2026)

  Motion-Twin / Evil Empire
    └─ Dead Cells           (社区最活跃逆向目标)

  Deepnight (独立)
    └─ Nuclear Blaze 等小品 (Sébastien Bénard, Heaps 推广者)

  其他独立
    └─ Papers Please, Brawlhalla, Dicey Dungeons (是 Haxe 但**不是 HL+Heaps**)
```
注: **Papers Please 等 Haxe 游戏不在本技能范围**,它们用其他 Haxe target(C++/JS/AIR)。
判定标准看是否同时具有 hlboot.dat + libhl.dll。

### 17.5 N3rdL0rd 的 Dead Cells 反编译仓库(必看参考)
- **DeadCellsDecomp**: https://github.com/N3rdL0rd/DeadCellsDecomp
- 提供一份 Dead Cells `hlboot.dat` 反编译后的 Haxe 风格代码
- **逆向其它 HL 游戏时, 把它当模板**: 类命名风格、字段命名风格、典型 Haxe 模式
- 看 N3rdL0rd 是怎么命名重组反编译输出的, 你可以仿照

## 18. HashLink Hot Reload — 字节码热替换

**HashLink 1.12+ 原生支持热重载**, 这是逆向 / mod 的金钥匙之一。

### 启用方式
1. **VM 端**: 启动 `hl.exe --hot-reload <bytecode.hl>`
   或 VSCode debugger 配置 `"hotReload": true`
2. **游戏代码端**(只对带源码的开发版有意义): 主循环里调 `hl.Api.checkReload()`
   或 Heaps 加 `-D hot-reload`
3. VM 会**轮询字节码文件 mtime**, 改变时:
   - 解析新字节码
   - 对每个被修改函数 JIT 出新地址
   - **patch 调用点**, 让所有调用跳到新版本
   - 新类型可以加, 但**已存在类的字段不能改**(实例已分配)

### 逆向用途
- **不重启替换字节码**: 改完 hlboot.dat,游戏自动 reload
- **快速迭代 mod**: 不用每次重启
- **限制**: 改字段布局会失败,只能改函数体逻辑

### 实战流程
```bash
# 1. 启动游戏(开了 hot-reload)
hl --hot-reload hlboot.dat &

# 2. 用 crashlink 改字节码,落盘
python -c "
from crashlink import Bytecode
c = Bytecode.from_path('hlboot.dat')
# ... patch func ...
c.serialize('hlboot.dat')
"

# 3. 游戏立刻 reload, 无需重启
```

## 19. Mod Loader 注入式实现思路

参考 `DeadCellsCoreModding` 这种成熟方案,完整 mod loader 的关键技术:

### 19.1 进程启动注入
- **DLL Injection**: 用 `CreateRemoteThread` / `SetWindowsHookEx` /
  `LoadLibrary` 把自己的 dll 塞进 hl.exe 进程
- **替代 hl.exe**: 像 DeadCellsCoreModding 做法,提供自己的 `DeadCellsModding.exe`
  作为新启动器,内部 `LoadLibrary("libhl.dll")` 自己手动 init VM
- **DLL hijack**: 替换 `libhl.dll` 同名 dll,转发原 API + 加自己的 hook

### 19.2 函数级别 hook(运行时方法替换)
**MonoMod 思路**:
1. 等待 `hl_module_init` 完成(JIT 后所有函数都有了 native 地址)
2. 通过 `hl_module_context->functions_ptrs[findex]` 拿到目标函数 native 地址
3. 用 MinHook / Detours 在那个地址下经典 trampoline hook
4. 自己的 hook 函数用 vclosure 调用约定接收参数

**HashlinkNET 思路**:
- 把 HL vclosure 包装成 C# delegate
- 把 C# 方法注册成 HL native 调用 → HL 字节码就能调 C# 函数
- 实现"C# 写 mod, HL 字节码不改"

### 19.3 字节码 patch 注入
- 启动前用 crashlink 修改 hlboot.dat → 直接落盘
- 优点: 简单, 兼容所有 HL 游戏
- 缺点: 每次改要写盘, 不像 hot reload 那样灵活
- 多 mod 合并: 按顺序 apply 各 mod 的 patch

### 19.4 资源替换
**用 Heaps 内置 fs 抽象**:
- Heaps 的 `hxd.Res` 通过 `hxd.fs.FileSystem` 抽象读资源
- mod loader 可以 hook `FileSystem.get(path)`,先查 mod 目录再 fallback 到原资源
- DeadCellsCoreModding 就这么做的

### 19.5 已知 mod loader 借鉴对象
| 项目 | 启示 |
|---|---|
| **DeadCellsCoreModding/core** | 完整流程范本(MIT),.NET 桥接 HL |
| **HashlinkNET (DreamBoxSpy)** | C# 调 HL native 函数互操作 |
| **MonoMod** | 通用方法替换框架 |
| **Polymod** (FunkinCrew/polymod) | Haxe **官方** atomic mod 框架, 支持 ZIP mod、依赖、blacklist。运行时打 patch,不动字节码 |

## 20. 存档 / 序列化格式

### 20.1 hxbit 序列化(主流)
Shiro 系列普遍用 `hxbit.Serializer` 做存档和网络同步。

**hxbit 二进制特征**:
- 头部含一个 schema hash(SerializableSignature),判断版本是否兼容
- 字段按声明序按类型 tag 写出
- 含基本类型 + nullable + array + 自定义对象引用
- 可读取: 把游戏字节码里的 `Serializable` 子类的 `__hxb_serialize` 方法对照

**存档定位**:
- Win: `%APPDATA%\<GameName>\` 或 `%USERPROFILE%\Saved Games\<GameName>\`
- Steam Cloud: `<SteamPath>\userdata\<UserID>\<AppID>\remote\`
- 文件后缀常见: `.sav`, `.dat`, `.bin`, 也有用 `.json`

### 20.2 hbson — Heaps 二进制 JSON
- 源码: `hxd.fmt.hbson`
- 用于紧凑存储**字符串表 + 结构化数据**
- 类似 BSON 但 Heaps 自有变体
- HIDE 编辑器存数据时常用

**结构**:
- header: magic + 版本
- value 树: 类型 tag(int/float/string/bool/object/array) + 数据
- string 表(去重)

### 20.3 prefab .l3d/.fx/.prefab — JSON 文本
直接文本 JSON, 顶层 `type` 字段对应 `hrt.prefab.*` 类。可以直接编辑。

## 21. HashLink 调试协议(逆向利器,被忽视的方法)

**被忽视的事实**: HashLink 内置 GDB-like 调试协议,
hashlink-debugger VSCode 插件就是它的客户端。
**没源码也能用** — 它能读所有局部变量、堆栈、全局表!

### 21.1 启动调试服务
```bash
hl --debug=<port> --debug-wait hlboot.dat
# 默认端口 6112
```
游戏会在入口前等待客户端连接。

### 21.2 协议能做什么(逆向用途)
- 列出所有线程的调用栈(完整 Haxe 函数名 + 行号!)
- 读任意线程任意帧的局部变量(带类型!)
- 读全局表内容
- 设置断点(行号或函数名)
- 单步执行字节码
- 修改寄存器值
- **所有这些不需要游戏源码**, 因为符号信息在字节码里

### 21.3 实战:作为"超级 cheat engine"用
1. 启动游戏带 `--debug=6112`
2. VSCode 装 vshaxe.hashlink-debugger
3. 创建空 Haxe 项目, launch.json 配 attach 到 6112
4. 命中入口断点 → 游戏暂停
5. 在 Variables 面板里**直接看到所有 Haxe 类的实例和字段**
6. 修改 hp/gold 等字段 → continue → 立刻生效

这是**最快的非破坏性 cheat 方法**,无需修改任何文件。

### 21.4 协议格式
- 简单的 socket 协议, 自描述
- 详见 hashlink 源码 `src/debugger.c`
- vshaxe-debugger 是 Haxe 写的客户端, 易读

## 22. 加固检测 / 反调试可能性

虽然 Shiro 系列默认无加固,商业游戏可能引入:

### 22.1 字节码完整性检查
- 启动时算 hlboot.dat 的 hash → 与硬编码值比对
- **绕过**: hlbc 找到比对函数,改成总返回 true

### 22.2 Steam DRM
- Wartales 等可能用 Steam Wrapper, 解密后才暴露原 hl.exe
- 用 Steamless / SteamlessUI 脱壳

### 22.3 mpman 反 cheat (Shiro 闭源)
- 多人模式可能校验玩家状态(联机时)
- 单机基本无影响

### 22.4 反调试探测
- 没见过 HL 游戏自带反调试
- 但 hl 进程加 ScyllaHide 类工具防 IsDebuggerPresent 没坏处

## 23. 终极工作流(综合应用)

### 23.1 拿到一个未知 HL 游戏的标准 30 分钟流程
```
0:00  指纹判定 → 找 hlboot.dat / libhl.dll / *.hdll
0:02  内嵌检测 → 如果没单独 hlboot.dat 但有 libhl.dll, 试 alivecells extract
0:05  hlbc hlboot.dat 进 REPL
0:07  > info / entry / strings | head -50 → 看版本和入口
0:10  > classes 全列表 → 找 Player/Game/World/Save/Item 等关键词
0:15  > fn <entry findex> → 看入口函数,跟着 call 链找 Game.init 类
0:20  写一个 crashlink 脚本: 列出所有"修改 hp / gold / exp"的 setfield
       (字段名搜 "hp"/"gold"/"exp"/"level"/"score" 等)
0:25  确定 mod 目标: 内容 mod / 数值 mod / 行为 mod
0:30  开 hashlink-debugger attach, 实时验证假设
```

### 23.2 不同目标的差异化路径
**做秒杀 cheat**: hashlink-debugger attach → 找 Player.hp 字段 → 写无穷大
**做无 cooldown**: 找所有 cooldown setfield, crashlink patch 改成 setfield 0
**做新内容 mod**: 走官方 Workshop / Polymod, 不动字节码
**做存档破解**: 看 hxbit Serializer schema → 用同 schema 写 Haxe 工具读写
**做反外挂研究**: 找 mpman 类的 import / 网络协议字段 → hxbit Serializable

## 24. 关键事实速查(总结所有反复用到的事实)

```
✓ hlboot.dat = .hl 字节码,默认无加密无混淆
✓ Magic 是 "HLB" 三字节
✓ 字节码保留所有类名 / 方法名 / 字段名 / 源行号
✓ HL 对象首字段总是 hl_type * (x86=4B, x64=8B)
✓ 字段索引在继承链上累加(子类不重置)
✓ String 内部: $type / vbyte* (UCS-2) / int length
✓ 装箱规则: 5 种引用类型直接转 dyn,基础类型需分配
✓ 全部 98 个 opcode,见 references/opcodes-cheatsheet.md
✓ HL 1.12+ 支持 hot reload(改函数体可,改字段不行)
✓ HL native 调试协议默认端口 6112,完整符号
✓ libhl 关键函数: hl_alloc_obj / hl_dyn_call / hl_hash_utf8
✓ HL/C 主机版符号: <Pkg>__<Class>_<method>
✓ Dead Cells Win 版字节码内嵌 exe (用 alivecells extract)
✓ Shiro 系列字节码独立文件(直接拿 hlboot.dat)
✓ Steam 内容 mod 走 Workshop, 字节码 mod 用 hlbc/crashlink
✗ Papers Please / Brawlhalla / Dicey Dungeons 是 Haxe 但**不是** HL+Heaps
✗ 没有标准 .pak 加密(开盒即可读),但纹理可能 BC 压缩
```

## 25. 决策树 v2(2026 更新版)

```
拿到游戏文件夹
  │
  ├─ 看到 libhl.dll + hdll? ──否──→ 不是本技能,走 ue/unity/gm 等
  │      │是
  │      ▼
  ├─ hlboot.dat 单独存在?
  │      │
  │      ├─ 是 → Shiro Games / 标准布局 → 直接 hlbc hlboot.dat
  │      └─ 否 → 字节码内嵌 exe(像 Dead Cells)
  │              → alivecells extract <game>.exe
  │
  ▼
进入 hlbc / crashlink
  │
  ├─ 字节码版本 v4? → hlbc 默认支持
  ├─ 字节码版本 v5? → 用最新 hlbc/crashlink, 多了 nbytes 段
  │
  ▼
明确目标
  │
  ├─ 内容 mod (皮肤/关卡/语言) → Steam Workshop / Polymod
  ├─ 数值 cheat (hp/gold) → hashlink-debugger 实时改 / crashlink patch
  ├─ 行为 mod (新技能/AI) → 字节码 patch + Hot Reload 迭代
  ├─ 反编译研究 → hlbc decompile / 参考 N3rdL0rd/DeadCellsDecomp 风格
  ├─ 联网 cheat → 不要做(mpman 校验 + 封号风险)
  └─ 资源提取 → CellPacker (pak) 或 Heaps loader 写 dump 工具
```

## 26. 更新版工具索引(完整)

| 工具 | 仓库 | 语言 | 角色 |
|---|---|---|---|
| **HashLink VM** | HaxeFoundation/hashlink | C | 引擎本体 |
| **Heaps.io** | HeapsIO/heaps | Haxe | 游戏引擎 |
| **HIDE** | HeapsIO/hide | Haxe/HTML5 | 关卡/资源编辑器 |
| **HxBit** | HeapsIO/hxbit | Haxe | 序列化/网络 |
| **CastleDB** | ncannasse/castle | Haxe | 数据库编辑器 |
| **HScript** | HaxeFoundation/hscript | Haxe | 脚本解释器 |
| **hlbc** | Gui-Yom/hlbc | Rust | **★ 主力** 反汇编/反编译/GUI |
| **crashlink** | N3rdL0rd/crashlink | Python | **★ 主力** IDAPython 兼容 |
| **vshaxe-debugger** | vshaxe/hashlink-debugger | Haxe | **★** VSCode 调试,无源码也能用 |
| **HLCC** | Yanrishatum/HLCC | Haxe | HL/C 编译辅助 |
| **alivecells** | N3rdL0rd/alivecells | Python | **★ Dead Cells extract** |
| **CellPacker** | ReBuilders101/CellPacker | Java | Dead Cells res.pak GUI |
| **DeadCellsDecomp** | N3rdL0rd/DeadCellsDecomp | (反编译产物) | Dead Cells 源参考 |
| **DeadCellsCoreModding** | dead-cells-core-modding/core | C#/.NET | mod loader 范本 |
| **HashlinkNET** | DreamBoxSpy/HashlinkNET | C# | C# ↔ HL 互操作 |
| **MonoMod** | MonoMod/MonoMod | C# | 运行时方法替换 |
| **Polymod** | FunkinCrew/polymod | Haxe | Haxe 通用 atomic mod 框架 |
| **Hashlink Modding Discord** | (邀请见 crashlink) | — | 社区 |
| **Heaps Discord** | discordapp.com/channels/... | — | 引擎社区 |

## 27. 已知盲区(诚实声明)

- **PS/Switch/Xbox 主机版**: HL/C AOT 编译,本技能给出方向但缺具体案例
- **DRM 处理**: 没具体讲 Steamless 等脱壳工具用法
- **Shader 抓取实战**: HxSL → HLSL 转换的 dump,只给思路没给完整 hook 代码
- **OnLine 联机协议**: mpman 闭源,只能猜测; hxbit 是底层,具体协议每游戏不同
- **反编译完美度**: hlbc decompile 不能 100% 还原 for 循环和复杂 closure
- **中文社区资料几乎为空**: 本技能本身就是填补这块空白

## 28. 附录:本技能所有附属文件索引

```
heaps-hashlink-reverse/
├── SKILL.md                                  ← 主文档(本文件)
├── references/
│   ├── opcodes-cheatsheet.md                 ← 全部 98 个 opcode 速查
│   ├── libhl-symbols.md                      ← libhl/hdll 关键 native 函数 + hl_type 结构体
│   ├── dead-cells-playbook.md                ← Dead Cells 专项手册
│   ├── hot-reload-and-injection.md           ← Hot Reload + DLL 注入 + Hook 实战
│   ├── sdk-dumping.md                        ← ★ SDK Dump 完整手册(Il2CppDumper 等价物)
│   ├── frida-hashlink.md                     ← ★ Frida + HashLink 集成手册(填补空白)
│   └── deep-dive.md                          ← JIT/GC/HMD/CDB/平台/反作弊/社区深度
├── research/
│   ├── 01-stack-overview.md
│   ├── 02-hashlink-vm-internals.md
│   └── 04-tooling.md
└── scripts/
    ├── crashlink_autoname.py                 ← IDA 自动命名脚本
    └── hl_sdk_dumper.py                      ← ★ SDK 自动导出器(C++ + Haxe)
```

每份文件都是**独立可读**的,处理特定子任务时可直接打开对应文件。
本 SKILL.md 是"开场指南",其它是"专项手册"。

## 版本/更新记录

- v1.0 (2026/05/09 初版): 章节 0-16, 覆盖 95% 通用需求
- v1.1 (2026/05/09 扩充): 章节 17-28, 加入 Dead Cells 案例 / Hot Reload / 调试协议 /
  注入式 mod loader / 工具索引扩展。新增 references/dead-cells-playbook.md 和
  references/hot-reload-and-injection.md。
- v1.2 (2026/05/09 SDK Dump): 章节 29 — **SDK Dump 完整方案**。
  新增 `references/sdk-dumping.md` 与 `scripts/hl_sdk_dumper.py`,
  填补 HashLink 生态里 Il2CppDumper / SDKGenerator 等价物的空缺。
- v1.3 (2026/05/09 终版): 章节 30-31 — **Frida 集成 + 深度专题**。
  新增 `references/frida-hashlink.md`(填补 Frida+HL 空白)和
  `references/deep-dive.md`(JIT/GC/HMD/CDB/平台/反作弊/社区状态)。
  覆盖第 4 轮自检发现的所有遗漏话题。

> **使用指引**: 拿到 HL/Heaps 游戏 → 看本 SKILL.md 第 0 章判定 → 第 23 章走 30 分钟流程 →
> 遇到具体子问题查 references/ 对应专项手册。

## 29. SDK Dump(★ 必读 ★)

**SDK Dump 是逆向 HL/Heaps 游戏最关键的一步**, 类比:
- Unity → **Il2CppDumper** 生成 dummy.dll + headers
- Unreal → **SDKGenerator** 生成 SDK.hpp
- HashLink → **本技能 `scripts/hl_sdk_dumper.py`**

完整手册见 [`references/sdk-dumping.md`](references/sdk-dumping.md)。

### 29.1 为什么必须 dump SDK
- 字节码里**所有类名/字段/方法/继承关系都完整保留**, 但散落各段, 必须组织成 header
- 拿到 SDK 后:
  - IDA/Ghidra 可 import → 反汇编里看到 `player->hp` 而不是 `*(float*)(rcx+0x18)`
  - Cheat dll 可 `#include "SDK.hpp"` → 类型安全
  - Frida 脚本有结构定义可用
  - 跨版本适配只需重跑 dumper

### 29.2 三种 dump 方式

**方式 A — 用本仓库 `hl_sdk_dumper.py`(自动化, 推荐)**:
```bash
pip install crashlink
python scripts/hl_sdk_dumper.py hlboot.dat ./sdk_out/
```
输出 `SDK.hpp` (C++ struct 含字段偏移) + `SDK.haxe` (Haxe 风格) +
`enums.hpp` + `functions.txt` + `globals.txt` + `strings.txt`。

**方式 B — 用 hlbc CLI 单类反编译(包含方法体)**:
```bash
hlbc hlboot.dat
> sfn Player                # 找 findex
> decompt 458               # 反编译类#458 含方法体
```
hlbc 的 `decompt` 输出**比 SDK dumper 更完整**, 含方法体反编译。

**方式 C — 用 hlbc-gui 浏览(无 CLI 阻力)**:
图形界面浏览 types/functions/strings,适合不熟 CLI 的人。

### 29.3 SDK.hpp 样例片段
```cpp
// from haxe class: game.Player
struct game_Player {  // : game_Entity
    hl_type* __type;     // +0  (always)
    int32_t  hp                ; // +0x10
    int32_t  maxHp             ; // +0x14
    float    stamina           ; // +0x18
    void* /*game_Inventory*/ inv; // +0x20
    // findex=4521  takeDamage(...)
    // findex=4522  heal(...)
    // [static] findex=4530  spawn
};
```

### 29.4 Cheat dll 中使用 SDK
```cpp
#include "SDK.hpp"

void hook_thread() {
    // 假设我们已知 game.Game 单例的全局索引为 12
    auto game = (game_Game*) hl_module_context->globals_data[12];
    auto player = game->localPlayer;
    player->hp = 99999;       // 类型安全的字段访问!
    player->maxHp = 99999;
}
```

### 29.5 字段偏移精度

`hl_sdk_dumper.py` 按 x64 对齐计算偏移,**与运行时极大概率一致**。
但务必动态验证:
1. 启动游戏带 `--debug=6112`
2. attach hashlink-debugger
3. 在 Variables 面板看实际字段(地址相减反推偏移)
4. 对照 SDK.hpp,差异修正

### 29.6 把 SDK 注入 IDA
```
1. IDA: File → Load File → Parse C Header File → 选 SDK.hpp
2. 在反汇编里给寄存器/变量 set type:  Y → game_Player*
3. 运行 scripts/crashlink_autoname.py 给函数名重命名
4. → IDA 数据库基本等于"半源码状态"
```

### 29.7 重大空白(2026 现状)
- **没有现成的 Ghidra/IDA HashLink 加载器/类型导入插件** —
  在这个生态里写一个会有市场
- crashlink (Pure Python) 是事实上的 IDAPython 桥
- 本技能的 `hl_sdk_dumper.py` 填补"自动 SDK 导出"空缺

### 29.8 游戏更新后的版本适配
```bash
# 重新 dump
python scripts/hl_sdk_dumper.py hlboot_new.dat ./sdk_v2/

# diff 关键字段
diff sdk_v1/SDK.hpp sdk_v2/SDK.hpp | grep -E "(struct|hp|gold|exp)"
```
HL 字节码因为符号完整, 跨版本适配比 Unity/Unreal 简单 10 倍。

### 29.9 没有 hlboot.dat 时怎么办(主机版/HL/C)
1. 进程内扫 `hl_module_context` 符号
2. `module->code` 指向 hl_code 结构 = 内存中的字节码镜像
3. dump 该区域到磁盘 → 用 hl_sdk_dumper.py 处理
4. 或者 IDA 里直接读 `module->code->types` / `code->functions` 数组解析
   (HL/C 编译版的符号已经是可读的 mangled 名)

## 30. Frida + HashLink

详见 [`references/frida-hashlink.md`](references/frida-hashlink.md)。

### 30.1 关键事实
- 截至 2026/05 **没有专门的 Frida HashLink 项目** — 这是空白,本手册填补
- Frida 是通用 native hook,可以直接 hook libhl.dll 任何导出
- **比 MinHook DLL 简单 5 倍**,适合快速实验和小规模 cheat

### 30.2 极简模板
```javascript
const libhl = Process.getModuleByName('libhl.dll');
Interceptor.attach(libhl.findExportByName('hl_alloc_obj'), {
    onEnter(args) { this.t = args[0]; },
    onLeave(ret) {
        const t = this.t;
        const kind = t.readU32();
        if (kind === 11) {  // HOBJ
            const objDef = t.add(8).readPointer();
            const namePtr = objDef.add(0x18).readPointer();
            const name = namePtr.readUtf16String();
            console.log(`[alloc] ${name} @ ${ret}`);
        }
    }
});
```

### 30.3 与 SDK Dumper 配合
```bash
# 1. 用 SDK dumper 找目标 findex
python scripts/hl_sdk_dumper.py hlboot.dat ./sdk/
grep "Player.takeDamage" sdk/functions.txt
# > f@4521 ...

# 2. Frida 脚本里通过 functions_ptrs[4521] 拿地址 → hook
```

## 31. 深度专题(JIT / GC / HMD / CDB / 平台 / 反作弊 / 社区)

详见 [`references/deep-dive.md`](references/deep-dive.md)。

### 31.1 速查
| 话题 | 关键事实 |
|---|---|
| **JIT** | 一段连续 RX 内存; 函数地址进程内不变,跨启动会变 |
| **调用约定** | x64 Windows = MS x64; this 永远是第一参数 |
| **GC** | mark-and-not-sweep, 64 KB 页, stop-the-world; hook 内不要乱建 HL 对象 |
| **HMD 模型** | 结构化 binary,可写 Heaps 项目调 `hxd.fmt.hmd.Library.load` 提取 |
| **CDB 嵌入** | macro 编译期内联,常量池里搜 `{"sheets":[` 即可拿原 JSON |
| **平台差异** | Linux Dead Cells 直接有 hlboot.dat(更易研究); 主机版没字节码文件 |
| **反作弊** | Shiro/Dead Cells 都没第三方反作弊,单机改自由 |
| **联网** | 改字节码后通常无法联机, 不要做联网作弊 |

### 31.2 HashLink 真空地带(机会窗口)
当前 HashLink 逆向生态不存在的工具:
- ❌ Ghidra/IDA HashLink 加载器
- ❌ Frida HashLink 标准 helper 库(本仓库 frida-hashlink.md 是初步)
- ❌ HL 主机版字节码恢复工具
- ❌ HL 网络协议解码器
- ❌ 自动 trainer 生成器

→ 在这些领域写工具会有市场, 类似 Unity 早期 Il2CppDumper 出现前的状态。

## 32. 终极总结(看完整篇这一节就够)

### 32.1 一张图记住所有要点
```
┌─────────────────────────────────────────────────────────┐
│ 拿到 HL/Heaps 游戏的 SOP                                │
└─────────────────────────────────────────────────────────┘
   1. 指纹: 找 hlboot.dat / libhl.dll / *.hdll
        ↓ (Dead Cells: alivecells extract)
   2. SDK: python hl_sdk_dumper.py hlboot.dat ./sdk/
        ↓
   3. 浏览: hlbc hlboot.dat → REPL → classes/strings/decompt
        ↓
   4. 选择介入方式:
        ├─ 调试式 cheat → hl --debug=6112 + VSCode attach (最快)
        ├─ Frida hook → references/frida-hashlink.md (中等)
        ├─ 字节码 patch → crashlink + Hot Reload (持久)
        └─ 注入 DLL → MinHook + libhl 符号 (生产级)
        ↓
   5. 验证: 跑游戏看效果, 跨版本时重跑 SDK dumper
```

### 32.2 三条铁律
1. **永远先 dump SDK** — 没 SDK 的逆向就像没字典翻书
2. **永远不要联机作弊** — Steam VAC / 服务端校验会封号
3. **永远先备份 hlboot.dat** — patch 出错才能回退

### 32.3 本技能解决了什么 / 没解决什么

**已解决**:
- ✅ HL 字节码格式 + 全部 98 opcode 速查
- ✅ HL 类型系统 + 内存布局 + GC 行为
- ✅ libhl native API + hl_type 结构体精确定义
- ✅ 工具链选型 (hlbc / crashlink / vshaxe-debugger)
- ✅ Dead Cells 专项(社区最完善的 HL 游戏)
- ✅ Hot Reload + 注入 + 调试协议三种 hook 模式
- ✅ SDK Dump (Il2CppDumper 等价物) 含可用脚本
- ✅ Frida + HL 集成模板
- ✅ JIT / GC / 平台差异 / 反作弊状态深度

**未解决(诚实声明)**:
- ❌ HL 主机版(Switch/PS/Xbox)逆向缺案例
- ❌ DRM 脱壳具体步骤(用 Steamless 等通用工具)
- ❌ 多人协议解码(每游戏不同,要逐个分析)
- ❌ 反编译完美度(hlbc decomp 不能 100% 还原 for/closure)

### 32.4 把本技能用在新游戏上(套用模板)
当你遇到一个新的 HL/Heaps 游戏:
```bash
# 1. 指纹判定
ls *.exe libhl.* hlboot.dat *.hdll

# 2. 提取字节码(若内嵌 exe)
python ~/.claude/skills/heaps-hashlink-reverse/<extract>  # 见 dead-cells-playbook

# 3. 生成 SDK
python ~/.claude/skills/heaps-hashlink-reverse/scripts/hl_sdk_dumper.py \
    hlboot.dat ./sdk/

# 4. 浏览
hlbc hlboot.dat
> sstr <你关心的关键词>
> classes | grep <类名>
> decompt <类索引>

# 5. 介入
# 选 32.1 里的某种方式
```

### 32.5 阅读顺序建议
- **小白**: 0 → 1 → 2 → 7 → 13 → 23
- **逆向老手**: 3 → 4 → 9 → 29(SDK)→ 30(Frida)
- **写工具**: 4 → 5 → 6 → 31(深度) → references/ 全部
- **找特定话题**: 14(反作弊) / 17(案例) / 18(hot reload) / 21(调试协议) / 31(JIT)

### 32.6 维护与扩展
- 当 HashLink 出新版本(目前 v1.13+),检查字节码 magic version 字节
- 当 Heaps 引擎大改 hxd.fmt 格式时, 重新看源码
- 追踪 Gui-Yom/hlbc 与 N3rdL0rd/crashlink 的更新, 跟随同步
- 新游戏发布时,跑一次本技能 SOP 就能验证套用度

---

**结语**:
本技能是 HashLink/Heaps 逆向的**目前最完整中文知识库**(2026/05)。
3000+ 行覆盖从字节码格式到 SDK dump 到 Hook 全流程, 配套两个即用 Python 脚本。
核心价值: 让你拿到任何 HL 游戏 30 分钟内进入"半源码"工作状态。

