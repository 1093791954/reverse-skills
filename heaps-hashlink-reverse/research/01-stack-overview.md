# Round 1: Shiro Games / Heaps.io 技术栈总览

## 来源
- https://heaps.io/documentation/home.html
- https://heaps.io/documentation/fullstack.html
- https://heaps.io/documentation/hashlink.html

## 顶层包结构 (Heaps API)
- `h2d` - 2D 显示 (UI / 2D 游戏)
- `h3d` - 3D 模型渲染
- `hxd` - 跨平台基础类、Bitmap、资源加载与管理框架
- `hxsl` - Heaps Shader Language 实现
- `hide` - HIDE IDE 代码 (编辑器)
- `hrt` - 运行时 prefab 类(可被游戏使用)

## H2D 子模块
Object/Object trees, Scenes, Layers, 2D Camera, Drawable, Text, Graphics,
Animation, Filters, Shaders (h2d shaders), Flow, Drawing Tiles

## H3D 子模块
FBX Models, GPU Particles, Lights, Materials (PBR), Shadows, World Batching,
Render Target

## HXD 子模块
Resource management, Resource Baking, Sound

## 平台/渲染器矩阵
- HashLink/JIT + DirectX11 (`-lib hldx`)
- HashLink/JIT + DirectX12 (`-lib hldx -D dx12`)
- HashLink/JIT + SDL/OpenGL (`-lib hlsdl`)
- HashLink/C + NVN (Switch)
- HashLink/C + GNM (PS4)
- HashLink/C for XBoxOne SDK
- JS + WebGL2 (HTML5)

## 编译产物
两条路径:
1. **HL/JIT**: `-hl bin/game.hl` 输出 `.hl` 字节码,由 `hl` 解释/JIT 运行
2. **HL/C**: `-hl bin/hlout/game.c` 输出 C 源码,可由 GCC/MSVC 链接 `libhl + *.hdll`
   - GCC: `gcc -O3 -o mygame -std=c11 -I hlout hlout/game.c -lhl -lheaps.hdll -lui.hdll -lfmt.hdll`
   - MSVC: `-D hlgen.makefile=vs2019` 生成 `.sln`

## Native 库 (.hdll)
随 HashLink 分发: SDL2, DirectX11, OpenAL, LibUV (sockets), SSL, FMT (Zip/Ogg/Png/Jpg),
Steam (额外), 主机 SDK (受限)

## 关键工具
- **HashLink VM Native Debugger** - VSCode 插件
- **HashLink CPU Profiler** - 非侵入式
- **Memory Profile API** - 内存泄漏分析
- **NVidia NSight** - GPU 性能

## Shiro 完整栈
| 层 | 组件 |
|---|---|
| 语言 | Haxe |
| VM | HashLink (.hl JIT, 或 hl/c) |
| 引擎 | Heaps.io |
| 编辑器 | HIDE (HTML5 Heaps WebGL2) |
| 数据 | CastleDB (CDB) - 单文件多行 JSON |
| UI | DomKit (XHTML+CSS) |
| 脚本 | hscript |
| 序列化/网络 | HxBit |
| 多人 | MPMan (闭源) |

## 关键事实 (用于逆向)
- **没有 Debug/Release 区分**: 玩家版本与开发版本字节码一致,带有调用栈信息
- **CastleDB 数据嵌入**: 通过 macro `cdb.Module.build("data.cdb")` 编译期内联,
  运行时 enum 名仍可恢复
- **Northgard 全部内存 < 500 MB**: GC 开销极小,适合内存扫描
- **HxSL 在运行时组装**: shaders 不是单一大文件,而是小片段动态拼接 → 抓 shader
  需要在 D3D 提交点 hook,而非简单从二进制提取
- **HIDE Prefab 模型**: 关卡/特效 = `hrt.prefab.Prefab` 序列化
