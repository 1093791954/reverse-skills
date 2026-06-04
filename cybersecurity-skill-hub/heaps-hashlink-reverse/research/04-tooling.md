# Round 4: HashLink/Heaps 逆向工具链

## 核心工具(按推荐顺序)

### 1. **hlbc** (Rust) — 主力字节码反汇编/反编译
- 仓库: https://github.com/Gui-Yom/hlbc
- 功能:
  - 加载、反汇编 `.hl` / `hlboot.dat`
  - 反编译(进行中,部分支持)
  - 字节码汇编器(可重新组装)
  - GUI 浏览字节码
- crates: `hlbc`(核心库) `hlbc-cli` `hlbc-decompiler` `hlbc-derive` `hlbc-gui` `hlbc-indexing`
- 内置 `wiki` 命令显示字节码格式说明
- **专门为 Shiro 系游戏 (Northgard / Wartales / Dune: Spice Wars) 设计 mod 工具**

### 2. **crashlink** (Pure Python) — IDAPython 兼容
- 仓库: https://github.com/N3rdL0rd/crashlink
- 安装: `pip install crashlink[extras]`
- 特点:
  - 零依赖, IDAPython 内可直接 import
  - 反序列化 / 反汇编 / 反编译 / 重新序列化
  - 字节码 patcher
  - 字节码 assembler(从零生成)
  - CLI 类似 hlbc
- 代码示例:
  ```python
  from crashlink import *
  code = Bytecode.from_path("hlboot.dat")
  print(disasm.func(code.fn(22)))   # 22 / 240 是常见入口 findex
  ```
- 配套: `crashtest auto` 评分反编译输出
- 配套 Hashlink Modding Community Discord

### 3. **vshaxe/hashlink-debugger** — 官方 VSCode 调试器
- 仓库: https://github.com/vshaxe/hashlink-debugger
- 在 VSCode 内附加到正在运行的 hl 进程,可下断点、查看变量

### 4. **HLCC** (Yanrishatum) — HL/C 相关
- 仓库: https://github.com/Yanrishatum/HLCC

### 5. **HashLink 自带 dump 工具**
- 编译时 `-D dump` → `dump/hlcode.txt` 完整字节码
- `-D hl-dump-spec` → 求值规范
- `-D hl-no-opt` → 无优化字节码

### 6. **Ghidra/IDA 用法**
当目标是 HL/C 编译版(主机端,GCC/MSVC 链接的原生二进制),
或对 `libhl.dll`/`hl.exe`/`*.hdll` 做静态分析:
- 函数命名规则: `<package>__<Class>_<method>`
- 全局命名规则: `global$<N>`, 字符串: `string$<N>`
- 类型结构体首字段总是 `hl_type *$type`
- crashlink 可作为 IDAPython 模块使用,**反向给函数命名**

## Shiro Games 文件打包模型 (绝对关键!)
hlbc README 揭示:
```
<game>.exe        — 极轻可执行,内嵌或加载 HashLink VM
hlboot.dat        — 真正的字节码(=.hl 重命名),启动时 VM 自动加载
*.hdll            — 普通 native dll,加 hdll 后缀,提供 native binding
fonts/, res/, ... — 资源(详见 pak/资源轮)
```
**结论**: 拿到一个 Shiro 游戏文件夹后,**第一件事就是用 hlbc/crashlink 加载 hlboot.dat**,
立即得到所有类、方法、字符串、源行号。

## 已知 Mod / 周边参考实现
- `dibertz/northgard-camera-move` — 修改 Northgard 相机距离限制
- `grnt426/Vanishing-Whispers-Northgard-Mod` — Northgard 内容 mod
- `FirowMD/Northgard-Auto-Accept` — Northgard 自动点击外挂
- `jetpropulsioncloud/northgard-analyzer` — Northgard 数据分析

## 工具选择决策树
```
拿到 Shiro 游戏 → 找到 hlboot.dat
   │
   ├─ 想批量分析/写脚本 → crashlink (Python, IDAPython)
   ├─ 想交互式浏览/反编译 → hlbc (Rust, GUI)
   ├─ 想动态调试 → vshaxe hashlink-debugger (需源码端)
   └─ 想做内存外挂 → x64dbg / Cheat Engine + libhl.dll
                     符号 + 自己 hook
```
