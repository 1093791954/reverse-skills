# HashLink 注入 / Hook / Hot Reload 实战手册

> 本手册聚焦运行时介入 HashLink 进程的具体技术。
> 适用对象: 不想改字节码或想做实时调试的逆向工程师。

## 1. Hot Reload(HashLink ≥ 1.12)

### 1.1 启用方式

**方法 A: 直接命令行**
```bash
hl --hot-reload hlboot.dat
```
VM 会监控 `hlboot.dat` 的 mtime, 改变时尝试重 JIT 并替换调用。

**方法 B: VSCode launch.json**
```json
{
    "type": "hl",
    "request": "launch",
    "name": "Run with hot reload",
    "program": "hlboot.dat",
    "hotReload": true
}
```

**方法 C: 游戏代码主动检查**(只适用开发版)
```haxe
// 主循环里
if (hl.Api.checkReload()) {
    // 重新初始化
}
```
Heaps 项目可加 `-D hot-reload` 自动注入。

### 1.2 限制

| 操作 | 是否支持 |
|---|---|
| 改函数体 | ✓ |
| 加新函数 | ✓ |
| 加新类 | ✓(但静态变量不会重新初始化) |
| **改类字段(加/删/改/移动)** | ✗ 失败,因为已有实例的内存布局不变 |
| 改全局表大小 | ✗ |

### 1.3 逆向利用 hot reload
1. 启动游戏带 hot reload
2. 用 crashlink/hlbc-cli 修改字节码并落盘
3. 游戏自动重载 → 实时验证 patch 效果
4. **不需要重启游戏**,迭代速度远超改 dll/inject

## 2. DLL 注入 hl.exe(经典手法)

### 2.1 启动期注入
```cpp
// 用 CreateProcess CREATE_SUSPENDED 启 hl.exe
// 然后 LoadLibrary 远程注入自己的 dll
// dll 在 DllMain 里 hook hl_alloc_obj / hl_module_init
```

### 2.2 替代启动器
仿造 DeadCellsCoreModding 做法:
```cpp
// MyLauncher.exe (代替 hl.exe)
HMODULE hl = LoadLibraryA("libhl.dll");
auto p_hl_main = (int(*)(int, char**))GetProcAddress(hl, "hl_main");
// 自己的初始化
hook_libhl_functions();
// 启动 VM
return p_hl_main(argc, argv);
```

### 2.3 DLL hijack
- 替换 `libhl.dll` 同名 dll
- 自己的 dll 转发原 API,在转发前后插入 hook
- 优点: 不需要修改 exe,不需要管理员权限

## 3. 函数级 Hook (运行时方法替换)

### 3.1 拿到 JIT 后函数地址
```c
// hl_module 全局
extern hl_module *hl_module_context;

// 第 N 个 findex 对应的 native 函数地址:
void *fn_native = hl_module_context->functions_ptrs[findex];

// 函数类型(签名):
hl_type *fn_type = hl_module_context->code->functions[idx].type;
// fn_type->fun->args[i] / fn_type->fun->ret
```

### 3.2 经典 trampoline hook (MinHook)
```c
#include "MinHook.h"

typedef int (*PlayerTakeDamage)(Player*, int);
PlayerTakeDamage orig_TakeDamage;

int hook_TakeDamage(Player *self, int dmg) {
    // 改成 0 伤害
    return orig_TakeDamage(self, 0);
}

void install_hooks() {
    void *target = hl_module_context->functions_ptrs[FINDEX_TakeDamage];
    MH_CreateHook(target, hook_TakeDamage, (void**)&orig_TakeDamage);
    MH_EnableHook(target);
}
```

### 3.3 HashLink 专用调用约定细节
- HL/JIT 在 x64 用平台 cdecl(Windows: MS x64, Linux: System V)
- 第一个参数永远是 `this`(对实例方法)
- 返回值: 整数寄存器或 xmm 浮点
- 不需要特殊适配, 当成普通 native 函数 hook 即可

## 4. C# / .NET 方式(HashlinkNET / DeadCellsCoreModding)

### 4.1 思路
- 加载 .NET runtime 到 hl 进程
- 把 vclosure → C# delegate
- 把 C# 方法 → HL native 函数(用 DEFINE_PRIM 注册)

### 4.2 优势
- mod 用 C# 写,不用 C/C++
- IDE 支持好(Rider / VS)
- 反射 + Roslyn 让 mod loader 极其灵活

### 4.3 参考实现
- **HashlinkNET**: https://github.com/DreamBoxSpy/HashlinkNET (查最新位置)
- **DeadCellsCoreModding**: https://github.com/dead-cells-core-modding/core
- **MonoMod**: https://github.com/MonoMod/MonoMod (运行时方法替换基础)

## 5. 用调试协议做"无修改"hook

### 5.1 启动调试服务
```bash
hl --debug=6112 --debug-wait hlboot.dat
```

### 5.2 协议交互
- 简单 socket TCP 协议
- 可发命令: `step`, `breakpoint <file> <line>`, `eval <expr>`, `vars`,
  `continue`, `pause`, `kill`
- 完整定义在 hashlink 源码 `src/debugger.c`

### 5.3 用脚本通过协议 cheat
```python
import socket
sock = socket.socket(...)
sock.connect(("127.0.0.1", 6112))
# 发协议消息: 暂停 → 找 Player 实例 → 写 hp=99999 → 继续
# 这是最优雅的方案:不改任何文件,不注入任何 dll
```

### 5.4 vshaxe-debugger 客户端
- Haxe 写的客户端实现,Haxe `hashlink-debugger` haxelib
- 可作协议参考实现

## 6. 资源 hot swap

如果只想换贴图/声音/CDB 数据,**不必动字节码**:

### 6.1 hook FileSystem.get
- Heaps 资源走 `hxd.fs.FileSystem`
- 在 mod loader 里 hook 这个方法,优先返回 mod 目录的文件
- DeadCellsCoreModding 这么做的

### 6.2 替换 res.pak
- CellPacker 解包/打包
- 整个 pak 替换简单粗暴

## 7. 实战示例:做一个简单 Cheat DLL

```cpp
// MinHook + libhl 的最简 cheat dll
#include <windows.h>
#include <hl.h>

// 假设我们已知 Player.hp 的 setter findex 是 1234
#define HP_SETTER_FINDEX 1234

typedef void (*HpSetter)(void *self, float hp);
HpSetter orig_SetHp;

void hook_SetHp(void *self, float hp) {
    // 强制 999
    orig_SetHp(self, 999.0f);
}

DWORD WINAPI hook_thread(LPVOID) {
    // 等 libhl 加载完
    Sleep(2000);
    HMODULE hl = GetModuleHandleA("libhl.dll");
    // 通过自己已知的 hl_module_context 符号偏移读
    // (实战中要扫描 / 用 PDB / IDA 找)
    auto module_ctx = *(hl_module**)((char*)hl + KNOWN_OFFSET);
    void *target = module_ctx->functions_ptrs[HP_SETTER_FINDEX];

    MH_Initialize();
    MH_CreateHook(target, hook_SetHp, (void**)&orig_SetHp);
    MH_EnableHook(target);
    return 0;
}

BOOL APIENTRY DllMain(HMODULE h, DWORD r, LPVOID) {
    if (r == DLL_PROCESS_ATTACH)
        CreateThread(0,0,hook_thread,0,0,0);
    return TRUE;
}
```

注入方式: 用 Process Hacker / inject.exe 把 dll 注入到 hl.exe。

## 8. 推荐技术栈选择

| 需求 | 推荐方案 |
|---|---|
| 一次性数值 cheat | hashlink-debugger 协议(最简单) |
| 持久 mod (单人) | crashlink patch + hot reload |
| 复杂行为 mod | C# loader (HashlinkNET 路线) |
| 内容替换(贴图/CDB) | CellPacker / 直接覆盖 res |
| 多 mod 兼容 | Polymod 或 atomic patch 框架 |
| 反向研究 | hlbc + DeadCellsDecomp 风格反编译 |
