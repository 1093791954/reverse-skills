# Toolchain：OLLVM 反混淆 / 控制流平坦化 - notes

## 一、OLLVM 三大 Pass

OLLVM (Obfuscator-LLVM) 来自瑞士西北应用科技大学安全实验室，三大核心 Pass：

### 1. BCF（Bogus Control Flow，虚假控制流）
- 在原始基本块前后插入永远为真的不透明谓词分支。
- `if (always_true) { real_code; } else { fake_code; }`，但混淆器会让 `always_true` 看起来像运行时值。
- IDA F5 反编译会看到大量"看似有意义实则永不执行"的死分支。

### 2. FLA / CFF（Flatten / Control Flow Flattening，控制流平坦化）
- 把所有基本块"扁平化"成一个 switch-state 机：
```c
state = 0;
while (1) {
    switch (state) {
        case 0: /* original BB1 */ state = 5; break;
        case 5: /* original BB2 */ state = 3; break;
        case 3: /* original BB3 */ state = -1; break;
        case -1: return;
    }
}
```
- 每个 case 是一个原 BB；状态 transition 由 dispatcher 决定。
- 在 ARM64 用 CSEL 类指令做条件 dispatch（小红书 libtiny 的"BR 花指令"就是这种）。

### 3. SUB（Substitution，指令替换）
- 把简单算术替换成等价但更复杂的形式。
- `a + b` → `(a^b) + 2*(a&b)`、`a - b` → `a + (~b) + 1` 之类。
- 不影响功能但反编译可读性极差。

## 二、还原工具链

### D-810（事实标准）
- IDA microcode 级别的去 OLLVM 插件。
- 项目：[gitlab.com/eshard/d810](https://gitlab.com/eshard/d810)
- 使用：把文件夹放到 IDA plugins 目录，重启 IDA → Edit → Plugins → D-810 → 选目标函数 → "Deobfuscate"。
- 优点：纯静态、IDA 内一键完成；FLA 还原效果非常好。
- 缺点：对深度自定义的"魔改 OLLVM"可能不奏效（如小红书 libtiny 的 BR 花指令需要单独脚本）。

### Triton 符号执行
- [JonathanSalwan/Triton](https://github.com/JonathanSalwan[/Triton)
- 适合：BCF 不透明谓词的"自动判定"——Triton 会把 always_true 识别为永真。
- 用法：from triton import * ; ctx.processing(...) ; ctx.simplify(expr)。

### Miasm / cdong1012/ollvm-unflattener
- [cdong1012/ollvm-unflattener](https://github.com/cdong1012/ollvm-unflattener) 用 Miasm 框架自动识别 dispatcher 状态机+恢复原始 CFG。
- 适合：x86_64 OLLVM。

### angr 兜底
- 当 D-810 + Triton 都失效时，用 angr 符号执行从 BR/dispatcher 入口走出每条路径。
- 详见小红书 libtiny "类 8" 处理（[xhs-libtiny-notes.md](../android/xhs-libtiny-notes.md)）。

## 三、移动端实践（ARM64）

### 字符串解密器识别
- 风控 SO 普遍带"字符串解密器"，6 特征签名（详见 [SKILL.md](../../SKILL.md) "String Decryptor Discovery Path"）。
- 解掉后能露出 `getprop` key、JSON 路径、API endpoint。

### BR 花指令去除
- 8 类（详见 [SKILL.md](../../SKILL.md) "Native Obfuscation Path"）：
  1. 常量构造型
  2. 静态表读型
  3. CSEL/CSET 条件分派型
  4. 真实副作用型
  5. 纯载体垃圾块
  6. 保存域链型
  7. 真调用尾分派型
  8. 小型索引开关 + angr 兜底

### iOS Pluto
- [bluesadi/Pluto-Obfuscator](https://github.com/bluesadi/Pluto-Obfuscator) 是 Hikari 死后 iOS LLVM 主流 fork。
- 对 iOS App 的"自带 OLLVM 加固"逆向时也用同一套 D-810/Triton 工具链。

## raw-hits 来源

- 见 [toolchain-batch1.md Q4](../raw-hits/toolchain-batch1.md)。

## 关键 URL

入门：
- [[原创] Ollvm 混淆还原学习 (看雪 2025-11)](https://bbs.kanxue.com/thread-289179.htm)
- [去除控制流平坦化 (linkpwn 2025-09)](https://linkpwn.github.io/2025/09/09/去除控制流平坦化/)
- [去 ollvm 平坦化 (viol1t 2024-07)](https://viol1t.com/2024/07/24/去ollvm平坦化/)
- [0 基础学习 ollvm 反混淆 (iosre 2024-09)](https://iosre.com/t/0基础学习ollvm反混淆之-0x02-控制流平坦化-fla/24880)

进阶：
- [反 OLLVM 控制流扁平化工具 Miasm (知乎)](https://zhuanlan.zhihu.com/p/1890330591536338937)
- [OLLVM 混淆原理深度解析 BCF/FLA (yunpan 2025-12)](https://yunpan.plus/t/4559-1-1)
- [D810 安装和使用 (吾爱破解 2023-12)](https://www.52pojie.cn/thread-1872852-1-1.html)

公开仓库：
- [obfuscator-llvm/obfuscator (官方原版)](https://github.com/obfuscator-llvm/obfuscator)
- [cdong1012/ollvm-unflattener (Miasm)](https://github.com/cdong1012/ollvm-unflattener)
- [bluesadi/Pluto-Obfuscator (iOS LLVM)](https://github.com/bluesadi/Pluto-Obfuscator)

## 工作流建议

1. **先识别**：看 IDA F5 是否大量 case 0/case 1...switch-state——FLA 标志。
2. **D-810 试一刀**：能解决 80% 的 OLLVM。
3. **不行用 Triton**：单函数符号执行恢复。
4. **angr 兜底**：跨函数复杂控制流。
5. **手写 patch**：对魔改 OLLVM（小红书 libtiny 的 BR 花指令），写专用 IDA Python 模拟器 + ELF 段重写。
