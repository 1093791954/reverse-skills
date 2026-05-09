# HashLink SDK Dump 完整手册

> SDK dump 是逆向 HL/Heaps 游戏的**杀手级工具** —
> 类比 Unity Il2CppDumper / Unreal SDKGenerator,
> 把 hlboot.dat 转成 C++/Haxe 风格 header,IDA 可 import,Cheat dll 可 #include。

## 1. 为什么 SDK Dump 是金钥匙

游戏字节码本来就是**完全符号化**的(类名/字段/方法都在),但散落在字节码各个段里。
SDK dumper 把这些信息组织成"类似源码头"的形态:

| 没有 SDK | 有 SDK |
|---|---|
| `*(float*)(player + 0x18) = 9999` | `player->hp = 9999` |
| `call sub_140012345` | `Player::takeDamage(0)` |
| 不知道字段叫什么 | `// +0x28 maxStamina f32` |
| Cheat 跨版本失效 | SDK 重新生成即可 |

## 2. 跟其他引擎对照

| 引擎 | SDK 工具 | 输出 | HL 等价 |
|---|---|---|---|
| **Unity (IL2CPP)** | Il2CppDumper / Il2CppInspector | dummy.dll + .h | `hl_sdk_dumper.py` |
| **Unity (Mono)** | dnSpy | C# 源码 | `hlbc decompt <idx>` |
| **Unreal** | SDKGenerator / Dumper-7 | SDK.hpp 千行 | `hl_sdk_dumper.py` |
| **GameMaker** | UndertaleModTool | GML 源码 | `hlbc` decomp |
| **HashLink** | **本手册** | SDK.hpp + SDK.haxe | (本仓库 scripts/) |

## 3. 字节码里的"类型信息"对照表

HL 字节码(参考 SKILL.md 第 3 章)包含完整 SDK 所需的全部数据:

```
ntypes  →  所有类型(Obj/Enum/Virtual/Fun/...)
              ├── Obj.name        →  C++ struct 名
              ├── Obj.super       →  继承关系
              ├── Obj.fields[]    →  字段 → C++ 成员(含类型)
              ├── Obj.protos[]    →  虚方法 → C++ method 签名
              └── Obj.bindings[]  →  静态方法 → static fn

nfunctions →  所有方法字节码 → 反编译得 method body
nglobals   →  全局变量类型 → 找单例(Engine.CURRENT 等)
nnatives   →  hdll 暴露的 C 函数 → "import library"
strings    →  类名/方法名/字段名/源文件名(完整保留)
```

## 4. 三种 SDK Dump 方式

### 4.1 用本仓库 `scripts/hl_sdk_dumper.py` (推荐)
```bash
pip install crashlink
python scripts/hl_sdk_dumper.py hlboot.dat ./sdk_out/
```
输出:
```
sdk_out/
├── SDK.hpp           ← C++ struct + 字段偏移注释
├── SDK.haxe          ← Haxe 风格 (像源码)
├── enums.hpp         ← 全部 enum 构造器
├── functions.txt     ← findex → 完整签名
├── globals.txt       ← global[N] → 类型
└── strings.txt       ← 全部字符串(供 grep)
```

**SDK.hpp 长这样**:
```cpp
// from haxe class: game.Player
// 8 own fields, 12 methods, 3 bindings
struct game_Player {  // : game_Entity
    hl_type* __type;     // +0  (always)
    int32_t  hp                            ; // +0x10
    int32_t  maxHp                         ; // +0x14
    float    stamina                       ; // +0x18
    float    maxStamina                    ; // +0x1C
    void* /*game_Inventory*/ inv           ; // +0x20
    // --- Methods (vtable / direct call) ---
    // findex=4521  takeDamage(...)
    // findex=4522  heal(...)
    // findex=4523  update(...)
    // --- Static bindings ---
    // [static] findex=4530  spawn
};
```

**SDK.haxe 长这样**:
```haxe
class game.Player extends game.Entity {
    public var hp : Int;
    public var maxHp : Int;
    public var stamina : Float;
    public function takeDamage() : Dynamic; // findex=4521
    public function heal() : Dynamic;       // findex=4522
    public static var spawn;                // findex=4530
}
```

### 4.2 用 hlbc CLI(快速,无需写脚本)
```bash
hlbc hlboot.dat -c "decompt ..; exit" > full_classes.txt
# decompt 把每个类反编译成 Haxe 风格(带方法体!)
```
**注意**: `decompt` 包含**方法体反编译**, 比 hl_sdk_dumper 更完整,
但更慢且并非所有方法都能正确反编译。

```bash
# 单类查看
hlbc hlboot.dat
> sfn Player                  # 找类名为 Player 的 findex
> decompt 458                 # 反编译类#458 (你刚找到的 Player 类)
```

### 4.3 用 hlbc-gui 浏览
```bash
hlbc-gui                       # 启动图形界面
# File > Open > hlboot.dat
# 树状浏览 types / functions / strings
```

## 5. 字段偏移精确计算

字段在内存里的实际偏移 = 父类字段 + 对齐 + 本类字段。

**对齐规则(x64)**:
| HL 类型 | size | align |
|---|---|---|
| void | 0 | — |
| ui8 | 1 | 1 |
| ui16 | 2 | 2 |
| i32 / f32 | 4 | 4 |
| i64 / f64 | 8 | 8 |
| bool | 1 (有时 4) | 1 |
| 所有指针类型 | 8 | 8 |

**偏移 = 8(hl_type*头) + 父类布局 + 本类字段排列**

`hl_sdk_dumper.py` 已实现该算法,但**生产环境务必跑动态验证**:
1. 用调试器跑游戏 → break 在 hl_alloc_obj
2. 看实际分配的内存
3. 对照 SDK.hpp 的偏移值

## 6. 把 SDK 导入 IDA / Ghidra

### 6.1 IDA Pro
```
1. File → Load File → Parse C Header File
2. 选 SDK.hpp
3. (可能需要先去掉 "void* /* xxx */" 注释里的非法字符)
4. Local Types 窗口看到所有结构体
5. 在反汇编里给变量 set type:  Y → struct game_Player*
```

**IDAPython 自动化**(配合 crashlink_autoname.py):
```python
import idaapi, idc
# 1. parse header
idaapi.parse_decls("game_Player", ..., 0)

# 2. 用 hl_sdk_dumper 生成的 functions.txt 给函数命名
with open("functions.txt") as f:
    for line in f:
        # f@1234 game.Player.takeDamage (Player, I32) -> Void
        m = re.match(r"f@(\d+)\s+(\S+)", line)
        if m:
            findex, name = int(m.group(1)), m.group(2)
            addr = find_addr_for_findex(findex)  # 你自己实现
            idc.set_name(addr, name.replace(".","_"), idc.SN_FORCE)
```

### 6.2 Ghidra
```
1. File > Parse C Source...
2. 加 SDK.hpp 到 Source files
3. Parse to Program
4. Data Type Manager 多了 game_Player 等
5. 在反汇编/反编译窗口右键 → Auto Create Structure / Set Datatype
```

### 6.3 Cheat Engine
- 不直接用 .hpp,但 SDK 给你的字段偏移可以填进 CE 的 Pointer Map / Structure Dissect

## 7. 全局变量(Singletons)定位

`hlboot.dat` 的 globals 段 = 静态变量。每个类的 static 字段都从这里取。

```
globals.txt 内容:
global[0]  : hl.types.BaseType
global[1]  : String
global[12] : game.Game            ← 这是游戏单例!!!
global[13] : game.Engine
global[42] : MyCheat              ← 用户定义类的静态实例
```

**实战找 game 单例**:
1. 看 `globals.txt` 找形如 `game.*` 的全局
2. 在 hlbc 里 `g 12` 看完整定义
3. 该全局对应内存中 `hl_module_context->globals_data + offsetof(global_12)`
4. 解引用得到 `game.Game` 实例
5. 后续从 `Game` 一路走出 World / Player / Inventory

## 8. 跨版本对比(游戏更新后字段偏移变了怎么办)

```bash
# 旧版本
python hl_sdk_dumper.py hlboot_v1.dat ./sdk_v1/
# 新版本
python hl_sdk_dumper.py hlboot_v2.dat ./sdk_v2/

# diff 关键类
diff sdk_v1/SDK.hpp sdk_v2/SDK.hpp | grep -E "(struct|hp|gold|exp)"
```
重新跑 dump → 重新写 cheat dll 用新偏移 → 5 分钟搞定版本适配。

## 9. 在没有 hlboot.dat 时怎么 dump SDK

主机版/HL/C 编译版本,字节码已经编译进 native exe,没有独立 hlboot.dat。
此时:
1. **从内存 dump**: 游戏运行时,扫 `hl_module_context` 全局,
   它的 `code` 字段指向 `hl_code` 结构,**就是 .hl 在内存中的镜像**
2. dump `code` 整个区域到磁盘 → 用 `hl_sdk_dumper.py` 处理
3. 或在 IDA 里直接看 `code->types` / `code->functions` 数组解析

**HL/C 编译版**:
- 符号在二进制里(`<Pkg>__<Class>_<method>`)
- 用 IDA 导入函数名(symbols 已经是可读的)
- 字段偏移要手工反推(看 `hl_alloc_obj(struct_name__val)` 调用)

## 10. 已知社区状态

**截至 2026/05**:
- **没有现成的 IDA/Ghidra HashLink 插件** — 这是空白,机会窗口
- crashlink (Pure Python) 是 IDAPython 事实标准
- hlbc(Rust) 有最完善的反编译,但不是 IDA 集成
- 本仓库 `hl_sdk_dumper.py` 填补"自动 SDK 导出"空缺

## 11. 检查清单(做完一次完整 SDK dump 应该有的产物)

- [ ] `SDK.hpp` — 至少几百到上千个 struct
- [ ] `SDK.haxe` — Haxe 风格类(可用作开发对照)
- [ ] `enums.hpp` — 全部 enum + 构造器
- [ ] `functions.txt` — N 万行的函数索引
- [ ] `globals.txt` — 几百行全局
- [ ] `strings.txt` — 几万行字符串
- [ ] **配套**: 在 IDA 里 import SDK.hpp,运行 crashlink_autoname.py 重命名所有函数
- [ ] **进阶**: 写一个 IDAPython 脚本读 globals.txt,在 .data 段标注每个 global 的类型

完成上述步骤,你的 IDA 数据库基本等于"半源码状态"。
