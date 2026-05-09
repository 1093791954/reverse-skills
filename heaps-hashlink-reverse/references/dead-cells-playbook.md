# Dead Cells 专项逆向手册

> Dead Cells 是 HashLink 生态里**社区资料最丰富**的游戏,
> 它的工具和技巧 90% 可以直接套用到任何 HL/Heaps 游戏。

## 1. 文件布局(Windows)

**关键陷阱**: `hlboot.dat` **不是单独文件**,而是**附加在 deadcells.exe 末尾**!

```
<Steam>\steamapps\common\Dead Cells\
├── deadcells.exe          ← DX 后端,字节码在尾部
├── deadcells_gl.exe       ← OpenGL 后端
├── libhl.dll              ← HashLink VM
├── *.hdll                 ← native 绑定(heaps/dx/sdl/...)
├── res.pak                ← 主资源包(纹理/声音/CDB)
├── ld_*.png / ld_*.bnk     ← 加载图 / 音频
└── userdata\saves\        ← 存档(.sav)
```

**Linux/Mac**: `hlboot.dat` 在游戏目录, 不需要 extract。

## 2. 字节码提取流程

### 用 alivecells (推荐)
```bash
git clone https://github.com/N3rdL0rd/alivecells
cd alivecells
pip install -r requirements.txt
python alivecells.py extract /path/to/deadcells.exe --output hlboot.dat
```

### 手动提取(无 alivecells 时)
1. 打开 `deadcells.exe` 用 hex 编辑器
2. 搜 `HLB` 三字节(HashLink magic)
3. 从该位置到 EOF 全部 dump 出来 → 就是 hlboot.dat
4. 注意: 末尾可能有 padding 或附加数据,通常不影响 hlbc 解析

### 完整 mod 环境部署
```bash
python alivecells.py install ./mymod /path/to/Dead\ Cells/
# ./mymod 现在是独立 HashLink 运行环境,可以放心改字节码
```

## 3. res.pak 解包

```bash
# 用 CellPacker (Java GUI)
java -jar CellPacker.jar
# File > Open > 选 res.pak
# 树状显示所有资源,可导出 PNG/OGG/CDB
# 修改后 File > Save 重新打包
```

**res.pak 内容**:
- 纹理图集(PNG)
- 角色精灵
- 音效 (OGG)
- CastleDB 文件 (data.cdb 格式) — **游戏所有数值数据**
- 字体, shader source 等

## 4. CastleDB (game data) 编辑

Dead Cells 的所有装备、敌人、关卡数据都在 `data.cdb` 里。

```
res.pak / data.cdb (JSON 文本)
{
  "sheets": [
    {"name": "Items", "columns": [...], "lines": [...]},
    {"name": "Enemies", ...},
    {"name": "Levels", ...},
  ]
}
```

**编辑工具**:
- HIDE(Heaps IDE) — 集成 CDB 编辑器
- 独立 CastleDB 编辑器: castledb.org
- 直接文本编辑(JSON)

**典型 mod 操作**:
- 改武器伤害: `Items` 表 → 找武器 → 改 damage 列
- 加敌人血量: `Enemies` 表 → 改 hp 列
- 解锁全部物品: `Items` 表 → 改 unlocked 字段

## 5. 字节码反编译参考

**N3rdL0rd/DeadCellsDecomp** 提供 Dead Cells 的反编译产物:
- 类层次图(完整)
- 关键类: `Game.hx`, `Player.hx`, `Hero.hx`, `Weapon.hx`, `Skill.hx`
- 核心战斗循环和伤害计算逻辑

**用途**: 写其它 HL 游戏 mod 时,DeadCellsDecomp 是最好的"风格参考":
- 看 Motion-Twin 怎么组织代码
- 看典型 Haxe + Heaps 项目结构
- 抄它的命名/反命名约定

## 6. 调试式 cheat (无修改方案)

```bash
# 1. 启动游戏带调试服务
hl --debug=6112 --debug-wait hlboot.dat

# 2. VSCode 配置 attach
# launch.json:
{
    "type": "hl",
    "request": "attach",
    "name": "Attach DC",
    "host": "localhost",
    "port": 6112
}

# 3. 命中游戏内断点后:
#    - Variables 面板看 Player.hp, Player.gold
#    - 直接改值,Continue,游戏内立即生效
```

## 7. 常见 mod patch 范例

### 7.1 一击必杀
```python
from crashlink import Bytecode
c = Bytecode.from_path('hlboot.dat')

# 找 Enemy.takeDamage 函数
for f in c.functions:
    name = f.resolve_name(c)
    if name and 'Enemy' in name and 'takeDamage' in name:
        # 找 hp -= damage 的 sub 操作,改成 hp = 0
        for i, op in enumerate(f.ops):
            if op.kind == 'Sub':
                # 替换为 mov hp, 0
                ...
        break

c.serialize('hlboot.dat')
```

### 7.2 无伤
```python
# 找 Hero.hurt / Player.takeDamage
# 把方法体改成 ret 0
```

### 7.3 无限金币
- CDB 路径:改 starting_gold 为 99999
- 字节码路径:hook gold 字段的 setfield,过滤减少操作

## 8. Hot Reload 加速迭代

```bash
# 启动游戏
hl --hot-reload hlboot.dat &

# 改字节码
python my_patch.py

# 游戏自动 reload (前提是 deadcells 主循环里调了 hl.Api.checkReload)
# 注意: Dead Cells 不是开发版,这个调用可能没启用
# → 只能 Shiro 一些游戏开发分支或自己 inject 才能用上
```

## 9. 已知陷阱

1. **`deadcells.exe` vs `deadcells_gl.exe`**: 用前者(DirectX)进行 extract
2. **Steam Cloud 同步会覆盖修改的存档** → 关 Cloud sync
3. **Steam 文件校验** → mod 完无法连 Workshop, 但单机 ok
4. **不同游戏版本字节码不同** → mod 跨版本兼容性差

## 10. 社区入口

- **Hashlink Modding Community Discord**: 见 N3rdL0rd/crashlink README 邀请链接
- **Dead Cells Modding subreddit**(零散)
- **Steam Workshop**(官方内容 mod)

## 11. 推广到其他 HL 游戏

Dead Cells 工具能直接套用到:
- **Northgard / Wartales / Dune Spice Wars**: 不需要 extract,字节码直接在
- **Farever**: 同 Shiro 标准布局
- **Evoland 1/2**: 同 Shiro
- **小品 HL 游戏**: 看是否单独 hlboot.dat,否则 alivecells 也能 extract

唯一需要调整的是 **CDB schema 不同 / 类名不同 / 字段名不同**, 但思路完全一样。
