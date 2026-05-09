#!/usr/bin/env python3
"""
hl_sdk_dumper.py — Dump HashLink bytecode (.hl / hlboot.dat) into C++/Haxe-style SDK.

为什么要 dump SDK
================
HashLink/Heaps 游戏的 hlboot.dat **包含完整类型系统**:
- 所有类的字段名、类型、偏移
- 所有方法签名
- 所有 enum 构造器和参数
- 父类继承关系

把这些导成 SDK header 后,你可以:
1. 在 IDA/Ghidra 里 import 类型,直接看到 obj->hp 而不是 *(float*)(rcx+0x18)
2. 写 Cheat dll 时直接 #include "Player.hpp" 就能 obj->fields[idx] 访问
3. 给 Frida/x64dbg 提供结构体定义
4. 比对不同游戏版本的字段偏移变化

类似工具对照
============
- Unity     → Il2CppDumper / Il2CppInspector  (生成 dummy.dll + headers)
- Unreal    → SDKGenerator / Dumper-7         (生成 SDK.hpp)
- HashLink  → 此脚本                          (生成 sdk.hpp + sdk.haxe)

依赖
====
    pip install crashlink

用法
====
    python hl_sdk_dumper.py hlboot.dat ./sdk_out/

输出
====
    sdk_out/
    ├── SDK.hpp              ← 全部类的 C++ struct (含字段偏移)
    ├── SDK.haxe             ← Haxe 风格类定义(可读性好)
    ├── enums.hpp            ← 所有 enum 定义
    ├── functions.txt        ← findex → 函数全限定名 + 签名
    ├── globals.txt          ← global index → 类型(用于在内存里找静态数据)
    └── strings.txt          ← 全部字符串(供 grep)
"""
from __future__ import annotations
import os
import sys
from pathlib import Path
from typing import Optional

try:
    from crashlink import Bytecode
    from crashlink.core import (
        Type, Obj, Virtual, Enum, Fun, Native, Function,
    )
    from crashlink.disasm import (
        type_name, type_to_haxe, func_header, is_static,
    )
except ImportError:
    print("ERROR: pip install crashlink", file=sys.stderr)
    sys.exit(1)


# ============================================================
#                   类型尺寸表(C 视角)
# ============================================================
# 用于计算字段偏移; x64 假设
TYPE_SIZE_X64 = {
    "Void": 0,
    "U8": 1,
    "U16": 2,
    "I32": 4,
    "I64": 8,
    "F32": 4,
    "F64": 8,
    "Bool": 1,         # 实际占 4 字节对齐,看编译器
    "Bytes": 8,        # 指针
    "Dyn": 8,          # vdynamic*
    "Fun": 8,          # vclosure*
    "Obj": 8,          # ptr
    "Array": 8,        # varray*
    "Type": 8,
    "Ref": 8,
    "Virtual": 8,
    "DynObj": 8,
    "Abstract": 8,
    "Enum": 8,
    "Null": 8,
    "Method": 8,
    "Struct": 8,
    "Packed": 8,
}
TYPE_ALIGN_X64 = TYPE_SIZE_X64.copy()
TYPE_ALIGN_X64["Bool"] = 1


def hl_type_to_cpp(code: Bytecode, t: Type) -> str:
    """把 HL 类型转 C++ 风格"""
    kind = type_name(code, t)
    mapping = {
        "Void":   "void",
        "U8":     "uint8_t",
        "U16":    "uint16_t",
        "I32":    "int32_t",
        "I64":    "int64_t",
        "F32":    "float",
        "F64":    "double",
        "Bool":   "bool",
        "Bytes":  "vbyte*",
        "Dyn":    "vdynamic*",
        "Array":  "varray*",
        "DynObj": "vdynobj*",
        "Type":   "hl_type*",
    }
    if kind in mapping:
        return mapping[kind]
    # 用户类
    safe = kind.replace(".", "_").replace("$", "").replace("<", "_").replace(">", "_")
    return f"struct {safe}*"


# ============================================================
#                   字段偏移计算
# ============================================================
def field_size_align(type_name_str: str) -> tuple[int, int]:
    return (
        TYPE_SIZE_X64.get(type_name_str, 8),
        TYPE_ALIGN_X64.get(type_name_str, 8),
    )


def compute_field_offsets(code: Bytecode, obj: Obj) -> list[tuple[str, str, int]]:
    """
    返回该类(含父类)所有字段: (field_name, type_string, absolute_offset).
    注意 HL 字段索引是父类继承累加,但内存布局 = 父类布局 + 本类 fields。
    """
    parents = []
    cur = obj
    while True:
        parents.append(cur)
        super_t = cur.super.resolve(code) if hasattr(cur, "super") and cur.super.value >= 0 else None
        if super_t is None or not isinstance(super_t.definition, Obj):
            break
        cur = super_t.definition
    parents.reverse()  # 从根到叶

    # 跨过 hl_type* 头(8 字节)
    offset = 8
    out = []
    for p in parents:
        for f in p.fields:
            fname = f.name.resolve(code)
            ftype_obj = f.t.resolve(code)
            ftn = type_name(code, ftype_obj)
            sz, al = field_size_align(ftn)
            # align
            if offset % al != 0:
                offset += al - (offset % al)
            out.append((fname, ftn, offset))
            offset += sz
    return out


# ============================================================
#                   导出 C++ SDK
# ============================================================
def safe_id(s: str) -> str:
    return (s.replace(".", "_")
             .replace("$", "")
             .replace("<", "_")
             .replace(">", "_")
             .replace(",", "_")
             .replace(" ", "")
             .replace("[", "_")
             .replace("]", "_"))


def dump_cpp_sdk(code: Bytecode, out_dir: Path) -> None:
    out = []
    out.append("// AUTO-GENERATED HashLink SDK (C++ struct view)")
    out.append("// Field offsets are x64 estimates, verify vs runtime!")
    out.append("// First field of every HL object is hl_type *$type")
    out.append("")
    out.append("#pragma once")
    out.append("#include <stdint.h>")
    out.append("")
    out.append("typedef uint8_t vbyte;")
    out.append("struct hl_type;")
    out.append("struct vdynamic;")
    out.append("struct varray;")
    out.append("struct vdynobj;")
    out.append("")

    # 前向声明所有类
    obj_types = [t for t in code.types if isinstance(t.definition, Obj)]
    out.append("// ===== Forward declarations =====")
    for t in obj_types:
        cls_name = t.definition.name.resolve(code)
        out.append(f"struct {safe_id(cls_name)};")
    out.append("")

    # 每个类
    out.append("// ===== Class definitions =====")
    for t in obj_types:
        obj: Obj = t.definition
        cls_name = obj.name.resolve(code)
        safe = safe_id(cls_name)

        # super
        super_str = ""
        if obj.super.value >= 0:
            super_t = obj.super.resolve(code)
            if isinstance(super_t.definition, Obj):
                super_str = f"  // : {safe_id(super_t.definition.name.resolve(code))}"

        out.append(f"// from haxe class: {cls_name}")
        out.append(f"// {len(obj.fields)} own fields, {len(obj.protos)} methods, {len(obj.bindings)} bindings")
        out.append(f"struct {safe} {{{super_str}")
        out.append(f"    hl_type* __type;     // +0  (always)")

        # 字段(继承链合并 + 偏移)
        try:
            fields = compute_field_offsets(code, obj)
            for (fname, ftn, off) in fields:
                cpp_t = hl_type_to_cpp_simple(ftn)
                out.append(f"    {cpp_t:20} {safe_id(fname):30} ; // +0x{off:X}")
        except Exception as e:
            out.append(f"    // ERROR computing fields: {e}")

        # 方法(只列签名,不实现)
        if obj.protos:
            out.append("    // --- Methods (vtable / direct call) ---")
            for proto in obj.protos:
                pname = proto.name.resolve(code)
                findex = proto.findex.value
                out.append(f"    // findex={findex}  {safe_id(pname)}(...)")
        if obj.bindings:
            out.append("    // --- Static bindings ---")
            for b in obj.bindings:
                fld = obj.fields[b.field.value] if b.field.value < len(obj.fields) else None
                fld_n = fld.name.resolve(code) if fld else f"f{b.field.value}"
                out.append(f"    // [static] findex={b.findex.value}  {safe_id(fld_n)}")
        out.append("};")
        out.append("")

    (out_dir / "SDK.hpp").write_text("\n".join(out), encoding="utf-8")
    print(f"  wrote SDK.hpp ({len(obj_types)} classes)")


def hl_type_to_cpp_simple(tn: str) -> str:
    """简化版,只用于字段类型字符串"""
    mapping = {
        "U8": "uint8_t", "U16": "uint16_t",
        "I32": "int32_t", "I64": "int64_t",
        "F32": "float", "F64": "double",
        "Bool": "bool", "Bytes": "vbyte*",
        "Dyn": "vdynamic*", "Array": "varray*",
        "DynObj": "vdynobj*", "Type": "hl_type*",
        "Void": "void",
    }
    if tn in mapping:
        return mapping[tn]
    return f"void* /*{safe_id(tn)}*/"


# ============================================================
#                   导出 Haxe 风格 SDK
# ============================================================
def dump_haxe_sdk(code: Bytecode, out_dir: Path) -> None:
    out = []
    out.append("// AUTO-GENERATED Haxe-style SDK (read-only reference)")
    out.append("// Reconstructed from hlboot.dat type table.")
    out.append("")

    obj_types = [t for t in code.types if isinstance(t.definition, Obj)]
    for t in obj_types:
        obj: Obj = t.definition
        cls_name = obj.name.resolve(code)

        # super
        ext = ""
        if obj.super.value >= 0:
            super_t = obj.super.resolve(code)
            if isinstance(super_t.definition, Obj):
                ext = f" extends {super_t.definition.name.resolve(code)}"

        out.append(f"// global=#{obj.global_value.value if hasattr(obj, 'global_value') else '?'}")
        out.append(f"class {cls_name}{ext} {{")
        for f in obj.fields:
            fname = f.name.resolve(code)
            ft = f.t.resolve(code)
            ftn = type_name(code, ft)
            haxe_t = type_to_haxe(ftn)
            out.append(f"    public var {fname} : {haxe_t};")
        for proto in obj.protos:
            pname = proto.name.resolve(code)
            out.append(f"    public function {pname}() : Dynamic; // findex={proto.findex.value}")
        for b in obj.bindings:
            if b.field.value < len(obj.fields):
                fld_n = obj.fields[b.field.value].name.resolve(code)
                out.append(f"    public static var {fld_n}; // findex={b.findex.value}")
        out.append("}")
        out.append("")

    (out_dir / "SDK.haxe").write_text("\n".join(out), encoding="utf-8")
    print(f"  wrote SDK.haxe")


# ============================================================
#                   导出 Enum
# ============================================================
def dump_enums(code: Bytecode, out_dir: Path) -> None:
    out = ["// AUTO-GENERATED HashLink Enum dump", ""]
    enum_types = [t for t in code.types if isinstance(t.definition, Enum)]
    for t in enum_types:
        e: Enum = t.definition
        ename = e.name.resolve(code)
        out.append(f"enum class {safe_id(ename)} {{   // origin: {ename}")
        for i, ctor in enumerate(e.constructs):
            ctor_name = ctor.name.resolve(code)
            params = ", ".join(
                hl_type_to_cpp_simple(type_name(code, p.resolve(code)))
                for p in ctor.params
            )
            out.append(f"    {i:3}: {ctor_name}({params})")
        out.append("};")
        out.append("")
    (out_dir / "enums.hpp").write_text("\n".join(out), encoding="utf-8")
    print(f"  wrote enums.hpp ({len(enum_types)} enums)")


# ============================================================
#                   导出 函数列表
# ============================================================
def dump_functions(code: Bytecode, out_dir: Path) -> None:
    lines = []
    for f in code.functions:
        try:
            lines.append(func_header(code, f))
        except Exception:
            lines.append(f"f@{f.findex.value}  (??? error reading)")
    for n in code.natives:
        try:
            lines.append(func_header(code, n))
        except Exception:
            pass
    (out_dir / "functions.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote functions.txt ({len(lines)} entries)")


# ============================================================
#                   导出 Globals
# ============================================================
def dump_globals(code: Bytecode, out_dir: Path) -> None:
    lines = []
    for i, g in enumerate(code.globals):
        try:
            tname = type_name(code, g.resolve(code))
        except Exception:
            tname = "?"
        lines.append(f"global[{i}] : {tname}")
    (out_dir / "globals.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote globals.txt ({len(code.globals)} entries)")


# ============================================================
#                   导出 Strings
# ============================================================
def dump_strings(code: Bytecode, out_dir: Path) -> None:
    lines = []
    for i, s in enumerate(code.strings):
        try:
            txt = s if isinstance(s, str) else s.decode("utf-8", "replace")
        except Exception:
            txt = "<unreadable>"
        lines.append(f"#{i:6}: {txt}")
    (out_dir / "strings.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote strings.txt ({len(code.strings)} strings)")


# ============================================================
#                   主入口
# ============================================================
def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    hl_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("sdk_out")
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[+] Loading {hl_path} ...")
    code = Bytecode.from_path(str(hl_path))
    print(f"    types={len(code.types)}, funcs={len(code.functions)},"
          f" natives={len(code.natives)}, strings={len(code.strings)}")

    print(f"[+] Generating SDK in {out_dir} ...")
    dump_cpp_sdk(code, out_dir)
    dump_haxe_sdk(code, out_dir)
    dump_enums(code, out_dir)
    dump_functions(code, out_dir)
    dump_globals(code, out_dir)
    dump_strings(code, out_dir)

    print(f"[+] Done. Open {out_dir}/SDK.hpp to start exploring.")


if __name__ == "__main__":
    main()
