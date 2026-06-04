# Round 2: HashLink VM 内部原理 (字节码格式、运行时、HL/C)

## 来源
- https://haxe.org/blog/hashlink-indepth/  (Part 1)
- https://haxe.org/blog/hashlink-in-depth-p2/  (Part 2)

## 1. HashLink 概述
- Haxe 新虚拟机, NekoVM 后继者, 为游戏优化
- **严格类型 + 寄存器式字节码**
- 既能 JIT (.hl 文件), 也能 AOT 转 C (HL/C)
- 与 C `__cdecl` 完全互通(x86 / x86-64)

## 2. 二进制布局: `.hl` 文件结构
**Magic**: 文件以 `HLB` 开头(Header BLock)
**字节码段(从 dump/hlcode.txt 可见结构):**
```
hl v1
entry @<func_idx>     ; 入口函数索引
N strings             ; UTF-8 编码,运行时展开为 UCS2
N ints                ; i32 常量表
N floats              ; f64 常量表
N globals             ; 类的静态变量 + enum 值; 只存类型不存名(可恢复目标)
N natives             ; C 函数列表(libhl + .hdll), 含签名
N functions           ; 字节码函数, 带源行号 + 完整方法名(!!)
N objects (protos)    ; 类原型: 父类、字段、方法槽
```

## 3. 字节码示例(关键: 行号与方法名都被保留!)
```
fun@14(Eh) ():void
; Main.hx:3 (Main.main)        <-- 文件名+行号+完整 Haxe 方法名
    r0 void
    r1 bytes
    r2 #String
    r3 i32
    .3  @0 new 2
    .3  @1 string 1,@33
    .3  @2 setfield 2[0],1
    ...
```

→ **逆向重大利好**: HL 二进制保留了所有 Haxe 类名、方法名、字段名、源文件名、源行号。
→ JIT/release 与 dev 没有区别, 玩家拿到的是完整符号版!

## 4. HL 类型系统 (寄存器/字段类型)
**基础值类型** (按值存储):
- `void`, `ui8` (1B), `ui16` (2B), `i32` (4B), `bool` (1或4B), `f32` (4B), `f64` (8B)

**引用类型** (x86=4B / x64=8B 指针):
- `bytes`     - 类似 C `char*`, 无边界检查
- `dyn`       - Dynamic, 第一个内存地址存类型
- `fun(args)->ret` - 严格类型函数(可为闭包或直接调用)
- `array`     - 非类型化数组, 固定长度, 无边界检查
- `#object`   - 单继承的固定对象
- `dynobj`    - 动态字段对象, 实现为按 hash 排序数组(O(log n))
- `virtual(...)` - 虚接口, 持有底层 object/dynobj 的字段引用
- `enum(name)` - 含构造器索引(4B) + 字段数据
- `ref(T)`    - T 的内存引用
- `null(T)`   - 可空基础类型
- `type`      - 类型自身作为值
- `abstract(name)` - 通常是 C 接口暴露的抽象值

**Haxe ↔ HL 类型映射**:
| Haxe | HL |
|---|---|
| Void | void |
| Int | i32 |
| Bool | bool |
| Float | f64 |
| Single | f32 |
| String | #String (object) |
| Dynamic | dyn |
| 匿名结构体/接口 | virtual(...) |

## 5. 对象布局
### Static Object (Haxe class)
```
Point @658
    extends Geometry
    2 fields
      @0 x f64       ; 偏移 0
      @1 y f64       ; 偏移 8
    2 methods
      @0 add fun@456
      @1 toString fun@82[0]   ; [0] = override slot
```
- **每对象首 4/8 字节是 hl_type* 指针**(运行时类型)
- 字段按声明顺序、按对齐排列
- **静态对象的字段访问 = 直接内存偏移**(JIT 后等同 C struct)

### String 内部结构
```c
struct _String {
    hl_type *$type;   // 偏移 0
    vbyte   *bytes;   // 偏移 8 (x64)  UCS-2 字节
    int      length;  // 偏移 16
};
```

### DynObj
- 字段按 hash 排序的数组, O(log n) 查找
- 用于 Reflect.setField 等动态需求

### Virtual
- 三种形态:
  1. **of static object**: 存底层对象引用 + 各字段地址引用
  2. **of dynobj**: 同上,但有 NULL 引用回退到 dynamic 访问
  3. **compact virtual**: 字段数据内嵌在 virtual 自身

## 6. 完整字节码 opcode 参考
### 数据移动
- `mov dst,src` / `int`/`float`/`string`/`bytes`/`true`/`false`/`null`

### 算术
- `add`/`sub`/`mul`/`sdiv`/`udiv`/`smod`/`umod`
- `shl`/`sshr`/`ushr`/`and`/`or`/`xor`/`neg`/`not`/`incr`/`decr`

### 调用
- `call dst, FuncName(args)` - 静态调用
- `callmethod dst, obj[field](args)` - 通过原型槽
- `callclosure dst, func(args)` - 闭包
- `callthis dst, [field](args)` - obj=r0

### 闭包/方法
- `staticclosure dst, FuncName`
- `instanceclosure dst, FuncName(obj)`
- `virtualclosure dst, obj[field]`
- `setmethod obj[field], FuncName`

### 全局
- `getglobal dst, idx` / `setglobal idx, r`

### 控制流(offset 单位为 opcode)
- `ret r`
- `jtrue/jfalse/jnull/jnotnull`
- `jslt/jsgt/jslte/jsgte` (signed)
- `jult/jugte` (unsigned)
- `jeq/jnoteq/jalways`
- `label` - 循环目标
- `switch r [offsets] end`

### 转换
- `todyn` - 装箱
- `tosfloat`/`toufloat`/`toint`
- `safecast`/`unsafecast`
- `tovirtual`

### 字段(关键!)
- `new dst` - 分配未初始化对象
- `nullcheck r`
- `field dst, obj[i]` / `setfield obj[i], r`
- `getthis dst, [i]` / `setthis [i], r` (obj=r0)
- `dynget`/`dynset` - 按字段名(寄存器)动态访问

### 字节(无边界检查!)
- `getui8/getui16/geti32/getf32/getf64`
- `setui8/setui16/seti32/setf32/setf64`

### 数组
- `getarray`/`setarray`/`arraysize`

### Enum
- `makenum dst, CID, args` - 构造
- `enumalloc dst, CID`
- `enumindex dst, r` - 取构造器编号
- `enumfield dst, r, CID, FID`
- `setenumfield e, FID, r`

### 异常
- `throw r`/`rethrow r`
- `trap r, offset` - try/catch
- `endtrap`

### 类型
- `type dst, T` - 类型即值
- `gettype dst, r` - 取运行时类型
- `gettid dst, r` - 类型 kind id

### 引用
- `ref dst, r` (=&r) / `unref dst, r` (=*r) / `setref r, v` (*r=v)

## 7. HL/C 输出 (主机/优化场景)
```c
// 编译: haxe -hl main.c -main Main
#define HLC_BOOT
#include <hlc.h>

typedef struct _String *String;

struct _String {
    hl_type *$type;
    vbyte *bytes;
    int length;
};

static void Main_main() {
    String r2;
    int r3;
    vbyte *r1;
    r2 = (String)hl_alloc_obj(String__val);
    r1 = string$33;
    r2->bytes = r1;
    r3 = 11;
    r2->length = r3;
    Sys_println(((vdynamic*)r2));
    return;
}
```
**关键观察:**
- 函数命名: `<Class>_<method>` (双下划线分隔)
- 全局: `global$N`, 字符串: `string$N`
- 类型名: `<package>__<Type>` (双下划线)
- HL/C 编译产物 = 普通 native 二进制, **Haxe 类名直接成为 C 符号名**
- IDA/Ghidra 中通过这些 mangled 名直接还原原始 Haxe 类结构

## 8. HashLink Runtime (libhl)
组成:
- C 函数 API 操作 Object/Bytes/Function
- UCS-2 String API (UTF-8 互转)
- 自定义 GC
- 异常 + 调用栈
- 文件/网络/数学等系统 API

`libhl` 在 Windows 是 `libhl.dll`, Linux 是 `libhl.so`. JIT 编译器和字节码读取器在 `hl` 可执行文件中,**不在 libhl**.

## 9. 装箱规则(hook 写值时极关键)
- **可直接装入 dyn 而不分配**: Function/Object/Virtual/Array/Null/DynObj
  (因为它们首字段就是 hl_type*)
- **需要装箱(`todyn` 操作码)**: 基础类型 + bytes/type/ref/abstract/enum

## 10. 调试期辅助开关
- `-D dump` → `dump/hlcode.txt` (字节码 dump)
- `-D hl-check` → 编译期类型检查
- `-D hl-no-opt` → 关闭字节码优化
- `-D hl-dump-spec` → `dump/hlspec.txt` 求值规范
- `-D interp` → 旧 Haxe 编译器内置的 HL 字节码解释器(测试)

## 11. 关键逆向意义
1. **`.hl` 文件是符号完整的**: 类、方法、字段、源行号都在
2. **HL/C 二进制中的 Haxe 类名 → C 符号名**: 通过 demangling 可恢复
3. **GC 对象首字段总是 `hl_type*`**: 给定任意对象指针, 可通过它定位类型,
   再通过类型描述结构定位字段
4. **静态对象字段是固定偏移**: 一旦确定类的 type, 字段偏移立即可算
5. **String 是已知偏移**: bytes 指针 + length, 易于扫描所有 UCS-2 字符串
