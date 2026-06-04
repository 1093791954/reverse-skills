# Frida + HashLink 实战手册

> 截至 2026/05,**没有现成的 Frida + HashLink 项目**。
> 这个文档填补这块空白,提供从零集成 Frida 到 HL 游戏的方案。
> Frida 是通用 native hook 框架,只要 libhl.dll 暴露符号,我们就能 hook。

## 1. 为什么选 Frida

| 工具 | 优势 | 劣势 |
|---|---|---|
| **Frida** | 跨平台、JS 脚本、无需编译、热加载 | 需了解协议 |
| MinHook (DLL) | 性能最高 | 写 C++,要编译,要重启 |
| hashlink-debugger | 官方调试协议 | 只能调试,不能注入逻辑 |

**结论**: 快速实验、跨版本迭代用 Frida; 生产级 cheat 用 MinHook DLL。

## 2. 基础设施: 找到 libhl 关键函数

```javascript
// frida-hl-base.js
const libhl = Process.getModuleByName('libhl.dll');
console.log(`libhl base = ${libhl.base}`);

const exports = {};
for (const name of [
    'hl_alloc_obj', 'hl_alloc_dynamic', 'hl_alloc_array', 'hl_alloc_bytes',
    'hl_dyn_call', 'hl_dyn_geti', 'hl_dyn_getp', 'hl_dyn_getf', 'hl_dyn_getd',
    'hl_dyn_seti', 'hl_dyn_setp', 'hl_dyn_setf', 'hl_dyn_setd',
    'hl_hash_utf8', 'hl_add_root', 'hl_remove_root',
    'hl_throw', 'hl_to_utf8',
]) {
    const sym = libhl.findExportByName(name);
    if (sym) exports[name] = sym;
    else console.warn(`Missing: ${name}`);
}
console.log(JSON.stringify(exports, null, 2));
```

## 3. 监控所有对象创建(类发现)

```javascript
// 把这段附加到游戏,会打印每次创建对象的类名
const hl_alloc_obj = libhl.findExportByName('hl_alloc_obj');

// 用 NativePointer 解 hl_type 取类名
function readClassName(hlTypePtr) {
    if (hlTypePtr.isNull()) return null;
    const kind = hlTypePtr.readU32();
    if (kind !== 11) return `<kind=${kind}>`;  // 不是 Obj
    // hl_type.obj 在偏移 +8 (x64)
    const objPtr = hlTypePtr.add(Process.pointerSize).readPointer();
    if (objPtr.isNull()) return null;
    // hl_type_obj.name 在偏移 +24 (x64): 4*int + ptr
    // 但布局会变,稳妥做法是从字段偏移 +0x18 起多探测
    const namePtr = objPtr.add(0x18).readPointer();
    if (namePtr.isNull()) return null;
    // UCS-2 串
    return namePtr.readUtf16String();
}

Interceptor.attach(hl_alloc_obj, {
    onEnter(args) {
        this.t = args[0];
    },
    onLeave(retval) {
        const name = readClassName(this.t);
        console.log(`[alloc] ${name} = ${retval}`);
    }
});
```

**注意**: `hl_type_obj` 的字段偏移**因 HL 版本变化**,
应跑一次取 dump 验证: `frida-trace -i 'hl_alloc_obj' -p <pid>`,
对比内存内容确定 `name` 字段实际偏移。

## 4. Hook 一个具体的 Haxe 方法

**前提**: 已用 hl_sdk_dumper.py 跑过,知道目标函数的 findex。

```javascript
// 假设 game.Player.takeDamage 是 findex=4521
// JIT 后函数地址 = hl_module_context->functions_ptrs[4521]

// 步骤 1: 找 hl_module_context 全局指针
//   方法 a: 在 libhl 导出表查
//   方法 b: 内存扫描,因为它在 .data 段
//   方法 c: 从 hl_module_init 函数的引用反推

// 假设你已经找到 hl_module_context 地址
const hl_module_context = ptr('0x...');

// 读 module_context.code -> functions_ptrs
const code = hl_module_context.add(0).readPointer();   // 偏移看版本
const functions_ptrs = code.add(0).readPointer();      // 同上

// 取 findex 4521 的 native 地址
const fn = functions_ptrs.add(4521 * Process.pointerSize).readPointer();
console.log(`Player.takeDamage @ ${fn}`);

// hook
Interceptor.attach(fn, {
    onEnter(args) {
        // args[0] 是 this (Player*)
        // args[1] 是 damage (int 或 float,看签名)
        console.log(`takeDamage(damage=${args[1].toInt32()})`);
        // 修改伤害
        args[1] = ptr(0);
    }
});
```

## 5. 通过字符串扫描找方法

如果不知道 findex 也不知道 hl_module_context,**用字符串特征**:
- 函数体里通常包含独特字符串(错误消息、日志)
- 用 frida 的 `Memory.scan` 找字符串
- 反向找 xref 到字节码

```javascript
// 找特定字符串引用
Memory.scanSync(libhl.base, libhl.size, '48 8D 0D ?? ?? ?? ?? E8')
    .forEach(m => {
        // x64 lea rcx, [rip+disp32]; call ...
        // 检查 lea 的目标是否是我们要找的字符串
    });
```

## 6. RPC 模式: Frida ↔ Python 控制台

```python
# host.py
import frida, sys

session = frida.attach('hl.exe')
script = session.create_script(open('frida_hl.js').read())

def on_message(msg, data):
    if msg['type'] == 'send':
        print(f">>> {msg['payload']}")

script.on('message', on_message)
script.load()
script.exports.set_hp(99999)   # 调用 JS 端 rpc.exports.setHp
sys.stdin.read()
```

```javascript
// frida_hl.js
const setPlayerHp = (val) => {
    // 找 player 单例
    // 写 hp 字段
    console.log(`set hp = ${val}`);
};

rpc.exports = {
    setHp: setPlayerHp
};
```

## 7. 实战陷阱

### 7.1 GC 暂停期不要分配 HL 对象
- HL GC 是 stop-the-world mark-sweep
- 在 hook 里调用 `hl_alloc_*` 期间有可能触发 GC
- **安全**: 在 hook 里只读不写, 或者写已存在对象的字段
- **危险**: 在 hook 里创建新 HL 对象可能死锁

### 7.2 函数地址在每次进程启动会变(JIT 重生成)
- JIT 输出的 native 代码地址**每次进程不同**
- 必须基于 `hl_module_context->functions_ptrs[findex]` 动态求
- 不能硬编码地址,否则更新后失效

### 7.3 Frida 注入到 hl.exe 主进程
```bash
# Windows
frida -l frida_hl.js -p $(pidof hl.exe)
# 或附加到游戏可执行
frida -l frida_hl.js -n game.exe
```

### 7.4 找 hl_module_context 的几种途径
1. **hl_init 函数引用**: 它会写这个全局,IDA 里看 `mov [hl_module_context], rax`
2. **JIT 后第一次调用 functions_ptrs**: 任何 HL 函数调用都会经过它
3. **AOB pattern**: hl.exe 的 PE 里搜常量模式
4. **导出?**: 某些 libhl 版本可能直接导出,findExportByName 试试

## 8. 完整脚本模板

```javascript
// frida_hl_template.js
'use strict';

const PTR_SIZE = Process.pointerSize;
const libhl = Process.getModuleByName('libhl.dll');

// === 字段偏移(x64,按你的版本验证)===
const HLTYPE_KIND_OFF = 0x0;     // u32
const HLTYPE_OBJ_OFF  = 0x8;     // ptr to hl_type_obj
const HLTYPE_OBJ_NAME_OFF = 0x18;  // 在 hl_type_obj 内,UCS-2 字串

function classOf(obj) {
    if (obj.isNull()) return null;
    const t = obj.readPointer();
    return readClassName(t);
}

function readClassName(t) {
    if (t.isNull()) return null;
    const kind = t.readU32();
    if (kind !== 11) return null;
    const objDef = t.add(HLTYPE_OBJ_OFF).readPointer();
    if (objDef.isNull()) return null;
    const np = objDef.add(HLTYPE_OBJ_NAME_OFF).readPointer();
    if (np.isNull()) return null;
    return np.readUtf16String();
}

// === Hook 所有 Player 创建并打印 ===
Interceptor.attach(libhl.findExportByName('hl_alloc_obj'), {
    onEnter(args) { this.t = args[0]; },
    onLeave(ret) {
        const cls = readClassName(this.t);
        if (cls && cls.endsWith('Player')) {
            console.log(`[alloc] ${cls} @ ${ret}`);
        }
    }
});

// === RPC 接口 ===
rpc.exports = {
    findClassByName(name) {
        // 通过字符串扫描找该类的 hl_type
        const matches = Memory.scanSync(libhl.base, libhl.size,
            // pattern: UCS-2 字符串,2 字节一字符
            Array.from(name).map(c => c.charCodeAt(0).toString(16).padStart(2,'0') + ' 00').join(' ')
        );
        return matches.map(m => m.address.toString());
    }
};
```

## 9. 与 SDK Dumper 配合

```bash
# 1. 用 hl_sdk_dumper 生成 SDK + functions.txt
python scripts/hl_sdk_dumper.py hlboot.dat ./sdk/

# 2. 从 functions.txt 提取你关心的 findex
grep "Player.takeDamage" sdk/functions.txt
# > f@4521 game.Player.takeDamage (Player, I32) -> Void

# 3. 把 4521 写进 frida_hl.js,attach 即可
```

这是**完整的 Frida + HL hook 工作流**, 比 MinHook DLL 简单 5 倍,
适合大部分逆向研究和小规模 cheat。
