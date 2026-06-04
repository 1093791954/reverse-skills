# HashLink 字节码 Opcode 速查表

> 共 98 个 opcode。本表按使用频率分类整理,逆向 hlboot.dat 时随时查阅。

## 1. 数据移动 / 常量加载

| Opcode | 语义 | 备注 |
|---|---|---|
| `mov dst, src` | dst := src | 寄存器拷贝 |
| `int dst, @idx` | dst := ints[idx] | i32 常量 |
| `float dst, @idx` | dst := floats[idx] | f64 常量 |
| `string dst, @idx` | dst := strings[idx] | UCS-2 string |
| `bytes dst, @idx` | dst := strings[idx] (raw) | UTF-8/二进制字节 |
| `true dst` | dst := true | |
| `false dst` | dst := false | |
| `null dst` | dst := null | |

## 2. 算术(numeric types only)

| Opcode | 语义 |
|---|---|
| `add dst, a, b` | dst := a + b |
| `sub dst, a, b` | dst := a - b |
| `mul dst, a, b` | dst := a * b |
| `sdiv dst, a, b` | dst := a / b (signed) |
| `udiv dst, a, b` | dst := a / b (unsigned, int 专用) |
| `smod dst, a, b` | dst := a % b (signed) |
| `umod dst, a, b` | dst := a % b (unsigned, int 专用) |
| `neg dst, a` | dst := -a |
| `incr dst` | dst := dst + 1 |
| `decr dst` | dst := dst - 1 |

## 3. 位运算(integer types only)

| Opcode | 语义 |
|---|---|
| `shl dst, a, b` | a << b |
| `sshr dst, a, b` | a >> b (signed) |
| `ushr dst, a, b` | a >>> b (unsigned) |
| `and dst, a, b` | a & b |
| `or dst, a, b` | a \| b |
| `xor dst, a, b` | a ^ b |
| `not dst, a` | !a (bool only) |

## 4. 函数调用

| Opcode | 语义 |
|---|---|
| `call dst, FuncName(args...)` | 静态调用,findex 已知 |
| `callmethod dst, obj[field](args...)` | 通过类原型槽,虚调用 |
| `callclosure dst, func(args...)` | 调用 vclosure 寄存器 |
| `callthis dst, [field](args...)` | 同 callmethod 但 obj=r0 |

## 5. 闭包构造

| Opcode | 语义 |
|---|---|
| `staticclosure dst, FuncName` | 从静态函数生成 vclosure |
| `instanceclosure dst, FuncName(obj)` | 绑定 this 的闭包 |
| `virtualclosure dst, obj[field]` | 从原型槽取方法做闭包 |
| `setmethod obj[field], FuncName` | 写类原型槽(罕见) |

## 6. 全局表

| Opcode | 语义 |
|---|---|
| `getglobal dst, idx` | dst := globals[idx] |
| `setglobal idx, r` | globals[idx] := r |

## 7. 控制流

> offset 单位: opcode 数(不是字节)。负 offset 必须跳到 `label`。

| Opcode | 语义 |
|---|---|
| `ret r` | return r |
| `jtrue r, off` | if r jump |
| `jfalse r, off` | if !r jump |
| `jnull r, off` | if r==null jump |
| `jnotnull r, off` | if r!=null jump |
| `jslt a, b, off` | if a<b (signed) |
| `jsgt a, b, off` | if a>b (signed) |
| `jslte a, b, off` | if a<=b (signed) |
| `jsgte a, b, off` | if a>=b (signed) |
| `jult a, b, off` | if a<b (unsigned) |
| `jugte a, b, off` | if a>=b (unsigned) |
| `jeq a, b, off` | == |
| `jnoteq a, b, off` | != |
| `jalways off` | 无条件跳 |
| `label` | 循环目标(必须存在,负跳目标) |
| `switch r [offsets...] end` | 多路跳转 |

## 8. 类型转换

| Opcode | 语义 |
|---|---|
| `todyn dst, r` | 装箱 |
| `tosfloat dst, r` | 转 float (signed) |
| `toufloat dst, r` | 转 float (unsigned) |
| `toint dst, r` | 转 int |
| `safecast dst, r` | 带运行时检查的 cast |
| `unsafecast dst, r` | 不检查直接当类型用(可能崩) |
| `tovirtual dst, r` | object/virtual → virtual |

## 9. 对象 / 字段(★ 逆向最常用 ★)

| Opcode | 语义 | 备注 |
|---|---|---|
| `new dst` | 分配 dst 类型的未初始化对象 | dst 寄存器类型决定 |
| `nullcheck r` | r==null 抛异常 | |
| `field dst, obj[i]` | dst := obj.fields[i] | i 是字段索引(继承链累加) |
| `setfield obj[i], r` | obj.fields[i] := r | |
| `getthis dst, [i]` | obj=r0 的 field | |
| `setthis [i], r` | obj=r0 的 setfield | |
| `dynget dst, obj[f]` | 按字段名(寄存器 f)动态读 | f 是字段名字符串 |
| `dynset obj[f], r` | 动态写 | |

## 10. 异常

| Opcode | 语义 |
|---|---|
| `throw r` | 抛 r |
| `rethrow r` | 重抛(保留原栈) |
| `trap r, off` | try 起点,异常存 r,跳 off |
| `endtrap` | 关 try |

## 11. Bytes 读写(无边界检查!)

| Opcode | 语义 |
|---|---|
| `getui8 dst, bytes[pos]` | 读 1 字节 |
| `getui16 dst, bytes[pos]` | 读 2 字节 |
| `geti32 dst, bytes[pos]` | 读 4 字节 int |
| `getf32 dst, bytes[pos]` | 读 4 字节 float |
| `getf64 dst, bytes[pos]` | 读 8 字节 double |
| `setui8 bytes[pos], r` | 写 1 字节 |
| `setui16 bytes[pos], r` | 写 2 字节 |
| `seti32 bytes[pos], r` | 写 4 字节 int |
| `setf32 bytes[pos], r` | 写 4 字节 float |
| `setf64 bytes[pos], r` | 写 8 字节 double |

## 12. 数组(无边界检查)

| Opcode | 语义 |
|---|---|
| `getarray dst, arr[pos]` | dst := arr[pos] |
| `setarray arr[pos], r` | arr[pos] := r |
| `arraysize dst, arr` | dst := arr.length |

## 13. Enum(代数数据类型)

| Opcode | 语义 |
|---|---|
| `makenum dst, CID, args...` | 用构造器 CID + 参数构造 |
| `enumalloc dst, CID` | 默认值构造 |
| `enumindex dst, r` | dst := r 的构造器编号 |
| `enumfield dst, r, CID, FID` | 取构造器 CID 的字段 FID |
| `setenumfield e, FID, r` | 写构造器 0 的字段 FID |

## 14. 类型操作

| Opcode | 语义 |
|---|---|
| `type dst, T` | dst := T(类型自身作为值) |
| `gettype dst, r` | dst := typeof(r) |
| `gettid dst, r` | dst := type-kind id(int) |

## 15. 引用

| Opcode | 语义 |
|---|---|
| `ref dst, r` | dst := &r |
| `unref dst, r` | dst := *r |
| `setref r, v` | *r := v |

## 16. 杂项

| Opcode | 语义 |
|---|---|
| `nop` | 占位(优化器留空) |

---

## 实战提示

**修改字节码常用招式**:
1. **去掉条件**: 把 `jslt`/`jsgt` 改 `jalways` 或 `nop`,直接走某分支
2. **常量化数值**: 把 `field` 读改成 `int dst, @<想要的常量索引>`
3. **去掉 setfield**: 改成 `nop`,字段不被修改
4. **把扣血改加血**: `sub` 改 `add`(寄存器布局相同)
5. **跳过校验**: 找 `safecast` 改 `unsafecast`,或在 throw 前 `ret`

**常见反编译陷阱**:
- 看到一堆 `todyn` 是因为 Haxe Dynamic 类型,代码本来不复杂
- `virtualclosure` 链 → Haxe 接口调用,展开后是 vtable 调用
- `enumfield` 多次访问同一构造器 → Haxe `switch` 模式匹配
- 大量 `nullcheck` → Haxe 编译器自动插入,不是真正的运行时检查代码
