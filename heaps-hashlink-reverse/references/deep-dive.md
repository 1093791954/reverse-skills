# HashLink 深度专题手册

> 收录前几轮没充分覆盖的剩余话题:JIT 内部、GC 安全点、HMD/CDB schema、平台差异、社区状态。

## 1. HashLink JIT 内部细节

### 1.1 JIT 流程
```
hlboot.dat 载入 (hl_code_read)
   ↓
hl_module_alloc(code) — 分配模块上下文
   ↓
hl_module_init(module) — 解析 globals/natives
   ↓
hl_jit_code(ctx, module) — 把每个函数 JIT 成 x64 native
   ↓
module->functions_ptrs[i] = native_addr
   ↓
跳到 entry findex 的 native 地址 — 游戏开始运行
```

### 1.2 JIT 输出的内存布局
- JIT 把所有函数代码塞到一段 **可执行 + 可写**(后改 RX)的 region
- 用 `VirtualAlloc(MEM_COMMIT, PAGE_READWRITE)` → 写完后 `VirtualProtect(PAGE_EXECUTE_READ)`
- 一段连续 8-32 MB 的 region(看游戏大小)

### 1.3 找到 JIT region 的方法
- 启动游戏后 dump 进程内存映射(VMMap / Process Hacker)
- 找一段 `EXECUTE | READ` 但**不属于任何 .dll**的 region
- 或者 hook `VirtualProtect`,看哪次给 RX 权限,记录地址

### 1.4 函数地址稳定性
- **每次启动重 JIT**,地址会变(由 OS 随机化和 jit 内部状态决定)
- 但**进程内运行期间地址不变**(没 GC/重定位 native code)
- → cheat 启动时算一次 functions_ptrs 即可,运行中地址恒定

### 1.5 JIT 调用约定
- x86: cdecl
- x64 Windows: MS x64(rcx, rdx, r8, r9, 栈)
- x64 Linux/Mac: SysV(rdi, rsi, rdx, rcx, r8, r9)
- **第一参数永远是 this**(对实例方法)
- 浮点参数走 xmm0-3
- 返回值: 整数 → rax,浮点 → xmm0,小结构体 → rax+rdx

### 1.6 阅读 JIT 代码
- 函数 prologue: `push rbp; mov rbp, rsp; sub rsp, ?` (标准)
- HL 寄存器是**栈上的槽**,不是 CPU 寄存器
  → JIT 后看到大量 `mov [rbp-0x18], reg`(把 reg 写到 HL 寄存器槽)
- 调用其它 HL 函数: `call qword [rip+disp32]`,disp32 指向 functions_ptrs 表

## 2. GC 行为与 hook 安全点

### 2.1 GC 类型
- **mark-and-not-sweep**(不是 mark-and-sweep)
- 64 KB 页对齐
- mark 阶段是 **stop-the-world**,所有 mutator 线程 park

### 2.2 GC 触发时机
- 主要在 `hl_gc_alloc*` 系列函数内部检查阈值后触发
- 可以手动 `hl_gc_major()` 强制 full GC

### 2.3 hook 时的 GC 安全规则
| 操作 | hook 内是否安全 |
|---|---|
| 读 HL 对象字段 | ✓ 安全 |
| 写已存在对象的非指针字段 | ✓ 安全 |
| 写已存在对象的指针字段(指向 HL 堆) | ✓ 安全 |
| 写已存在对象的指针字段(指向**非 HL 堆**) | ✗ GC 误读崩溃 |
| **新分配 HL 对象** | ⚠ 可能触发 GC,慎用 |
| 把自己的 native 数据指针存进字段 | ✗ 必须用 `hl_add_root` |
| 调用 HL 闭包(hl_dyn_call) | ⚠ 可能触发 GC,但通常 OK |

### 2.4 安全模式
**只读 hook**: `Interceptor.attach onEnter` 里只读参数 → 100% 安全
**只写 hook**: 改 `args[N]` 的内置类型(int/float/bool) → 安全
**复杂 hook**: 在 hook 里要新建对象时,**确保对方持有引用** → 用 `hl_add_root` 注册

## 3. HMD 模型格式(Heaps Mesh Data)

### 3.1 用途
- Heaps 自有 3D 模型容器
- 由 HIDE / Heaps 工具从 FBX 烘焙
- 内含: mesh 几何 / 材质引用 / 骨骼 / 动画

### 3.2 高层结构(参考 `hxd.fmt.hmd.Data`)
```
HMD 文件 = header + dataPosition + 数据 blob
header (JSON/二进制头):
   - version
   - geometries[] — 顶点/索引/属性
   - materials[]  — 材质引用(颜色/纹理 path)
   - skins[]      — 骨骼蒙皮
   - animations[] — 动画曲线
   - models[]     — 模型节点树
   - data offset → dataPosition + 实际 binary blob
binary blob (从 dataPosition 起):
   每个 geometry 的顶点+索引
```

### 3.3 关键观察
- HMD 是**结构化的**,不是任意二进制
- 文件解析器即源码可读: `hxd/fmt/hmd/Reader.hx` `Library.hx` `Data.hx`
- 想 dump 模型: 写 Heaps 项目调 `hxd.fmt.hmd.Library.load` 拿 `h3d.scene.Object`

### 3.4 实战提取流程
```haxe
// dumpHMD.hx
class DumpHMD {
    static function main() {
        var bytes = sys.io.File.getBytes("model.hmd");
        var lib = new hxd.fmt.hmd.Library(new hxd.fmt.hmd.Data(), bytes);
        var obj = lib.makeObject();
        // 现在 obj 是 h3d.scene.Object,可以遍历 mesh / 导出 OBJ
    }
}
```

## 4. CastleDB Schema 还原

### 4.1 CDB 数据嵌入字节码的方式
通过 macro `cdb.Module.build("data.cdb")` **编译期内联** → 数据进字符串/常量池。

### 4.2 还原方式
1. **找 cdb.Data 类**: hlbc → `sfn cdb.Data` 或 `classes | grep cdb`
2. **看它的字段**: 每个 sheet 一个静态字段
3. **解码 JSON**: 数据可能直接以 JSON 字符串放在常量池,搜 `{"sheets":[`
4. **若已 zip/序列化**: 看类的 init 方法,跟踪解码逻辑

### 4.3 实战寻找步骤
```bash
hlbc hlboot.dat
> sstr {"sheets":           # 找 CDB JSON 头
> sstr "name":"Items"        # 找具体 sheet 名
> classes | grep -i data
```
找到字符串引用 → 该字符串在常量池索引 → 这就是原始 CDB JSON,可直接复制保存。

## 5. 平台差异(Windows/Linux/macOS)

### 5.1 Windows
- `hl.exe` + `libhl.dll` + `*.hdll`
- 多数游戏分发模式
- Dead Cells: 字节码内嵌 exe

### 5.2 Linux
- `hl` + `libhl.so` + `*.hdll`(也是 .hdll 命名,虽然是 .so)
- **Dead Cells Linux 直接有 hlboot.dat**(不内嵌)
- mod 调试更容易,推荐研究环境

### 5.3 macOS
- `hl` + `libhl.dylib`
- Code signing / notarization 可能阻碍注入
- Steam macOS 版用得不多

### 5.4 主机版(Switch/PS/Xbox)
- HL/C 编译,**没有 .hl 文件**
- 字节码已经被翻译成 C 然后 native 编译
- 符号 mangling: `<Pkg>__<Class>_<method>`
- 只能静态分析二进制(IDA/Ghidra)
- 用导出符号 + 类型描述符变量(全局 `<TypeName>__val`)恢复

## 6. Steam Workshop 集成(对 Shiro 系列)

### 6.1 官方 mod 工作流(不动字节码)
- Northgard / Wartales 通过 Steam Workshop 分发内容 mod
- 游戏自带 mod loader,读特定目录的 zip/folder
- mod 通常含: 修改后的 CDB / 翻译 / 贴图 / 关卡 prefab
- 不需要逆向,跟 Polymod 模式类似

### 6.2 与字节码 mod 的关系
- Workshop mod **不能修改游戏逻辑**(代码层)
- 字节码 mod 改逻辑,但**会被 Steam 文件校验拦** → 单机才能用
- 两者**不兼容**:你只能选一种

### 6.3 实战识别
- 看游戏目录有没有 `mods/` 或 `<game>/mods/` 子目录
- 看 hlboot.dat 字符串里有没有 "workshop" / "modloader"
- 看是否有 `steam_modloader.cdb` 之类配置

## 7. 反作弊 / DRM 真实状态

### 7.1 Shiro Games 系列
- **没有第三方反作弊**(EAC/BattlEye 都没)
- Steam Sandbox 是默认保护
- 单机模式: 自由改

### 7.2 Dead Cells
- 没有反作弊
- Steam achievement 由游戏内部判定,可改

### 7.3 联网模式
- Northgard/Wartales 多人有服务端校验
- 改本地字节码会失败联机
- **不要在多人模式作弊**:封号风险

### 7.4 加固检测罕见
- 我们没看到任何 HL 游戏带反调试/反 hook 检测
- 因为 Heaps 玩家群体小,不像 Unity/Unreal 是反作弊重点

## 8. 社区现状(2026/05)

### 8.1 主要社区
- **Hashlink Modding Community Discord**: crashlink README 有邀请
- **Heaps Discord**: 引擎讨论, 不是 mod
- **Haxe Discord/Forum**: 语言层面
- **r/deadcells**: Reddit, 内容 mod 多,逆向少
- **Reddit r/hashlinks**: ❌ 不存在(此名是加密学概念)

### 8.2 知名贡献者
- **Nicolas Cannasse** — Heaps + HashLink 主作者, Shiro 创始人
- **Sébastien Bénard / Deepnight** — Heaps 推广者, 早期 Dead Cells 团队
- **Gui-Yom** — hlbc 作者
- **N3rdL0rd** — crashlink + alivecells + DeadCellsDecomp 作者
- **DreamBoxSpy** — HashlinkNET 作者
- **Tomat0** — sharplink 作者(已删库?)

### 8.3 信息密度评估
- 一手文档(Haxe 博客 + GitHub wiki): **充足**
- 工具(hlbc/crashlink): **完备**
- 实战教程: **几乎为零** — 本技能填补此空白
- 视频教程: **没有**
- 中文资料: **完全空白**

## 9. 性能影响(hook 后游戏会卡吗?)

### 9.1 单 hook 性能
- Frida Interceptor.attach 单个 hook ≈ 50-200 ns
- 60 FPS 游戏每帧 16 ms,hook 100 次 ≈ 0.02 ms,无感知
- 大量 hook(比如 hook hl_alloc_obj)在分配密集场景可能掉帧

### 9.2 优化建议
- 只 hook 必要函数, 不 hook hot path
- 用 onEnter 判断后再决定 onLeave 处理(filter early)
- 用 Stalker 替代 Interceptor 在某些场景更轻

## 10. 还没解决的真空地带

| 真空 | 状态 |
|---|---|
| Ghidra/IDA HashLink 加载器 | 不存在,等人写 |
| Frida HashLink 标准 helper 库 | 不存在,本手册是初步替代 |
| HL 主机版字节码恢复工具 | 不存在 |
| HL Anti-cheat(给开发者用) | 不存在 |
| HL Mod 应用商店 | Steam Workshop 是事实标准 |
| HL 自动 trainer 生成 | 用 SDK + 模板可凑出 |
| HL 网络协议解码工具 | 不存在,要自己手写 |

这些真空意味着 **HashLink 逆向工具生态还在早期**,在这个领域写工具有市场。
