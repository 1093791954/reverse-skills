# CSDN Notes

This file captures reusable conceptual material from public CSDN pages about VMP/VMProtect. Use it as a vocabulary and model refresher before deeper sample-specific work.

## Core VMP Model

Representative links:

- https://blog.csdn.net/CSNN2019/article/details/114042760
- https://blog.csdn.net/weixin_43114209/article/details/150575091
- https://blog.csdn.net/weixin_52236586/article/details/144318502
- https://blog.csdn.net/dubingxin/article/details/149478791

Reusable concepts:

- VMP is a virtualization-based protection technique: selected native code is translated into custom bytecode and executed by an embedded VM/interpreter.
- VMProtect is commonly described as a stack-based VM protection system.
- The protected region is often entered through a native stub that bridges parameters, return values, and machine state into the VM runtime.
- The important analysis objects are:
  - virtual instruction pointer
  - virtual stack/frame
  - handler dispatch
  - bytecode decode
  - handler semantics
  - native escape points for calls, memory, and returns

Use this model to explain why VMP is different from UPX-style unpacking: there may be no fully restored native body for the protected function.

## Protection Modes and SDK Markers

Useful official manual source:

- https://vmpsoft.com/vmprotect/user-manual

Reusable concepts:

- VMProtect supports virtualization, mutation, and combined/ultra-style protection modes.
- SDK marker functions are labels used to mark protected code boundaries before protection.
- Marker names and SDK library references can be removed during protection, so absence of obvious SDK imports does not disprove VMProtect usage.
- Official service functions include debugger/VM detection, image CRC checks, string decrypt helpers, and licensing/activation helpers.

Analysis value:

- Marker and service-function vocabulary helps interpret string residue, import residue, logs, and developer-side build artifacts.
- If the analyst has source/PDB/MAP/project files from an authorized engagement, those can help map protected boundaries without guessing from the binary alone.

## Static Signals

Look for:

- unusual section names, permissions, entropy, or overlay data
- sparse imports or loader-like import shape
- VMProtect-related strings, error messages, or service-function residue
- dense computed branches, dispatch patterns, and handler-like blocks
- heavy stack/register noise around selected functions
- different behavior between protected and unprotected builds when the client can provide both

Do not rely on any single signal. Detector labels, section names, and strings are useful hints but not proof.

## Runtime Signals

Look for:

- memory regions created or permission-changed during startup
- transition from loader/protector code into stable native code
- selected functions entering VM runtime rather than normal compiler-shaped code
- anti-debug, anti-VM, CRC, or "corrupted file" reactions
- native API bridges or calls emitted from VM-managed execution

Record observations with timestamps, module ranges, and hashes so they can be tied back to artifacts.

## Devirtualization Concepts

Common phases:

1. Locate the native-to-VM boundary.
2. Identify VM state containers.
3. Classify handlers by semantic family.
4. Decode or model bytecode operands.
5. Track virtual stack/register/flag state.
6. Simplify expressions and remove junk.
7. Reconcile branches and loops.
8. Validate reconstructed behavior with tests.

For small protected algorithms, manual semantic notes may be cheaper than a full lifter. For repeated engagements or large functions, a custom IR/lifting pipeline may be justified.

## Performance and Engineering Tradeoffs

- Virtualization increases reverse-engineering cost but can also increase runtime overhead.
- Protectors are commonly applied to selected functions instead of whole programs.
- Protected files may trigger antivirus false positives because packed/virtualized code is difficult for scanners to analyze.
- From a defensive or commissioned-analysis perspective, false positives and crash behavior should be documented, not assumed to prove maliciousness.

## Practical Selection Guide

- For "什么是VMP保护", use `Core VMP Model`.
- For "怎么判断是不是VMProtect", use `Static Signals` and `Runtime Signals`.
- For "为什么脱完还有乱码/虚拟机代码", use `Devirtualization Concepts`.
- For "客户给了未保护版本/符号文件", use `Protection Modes and SDK Markers`.
