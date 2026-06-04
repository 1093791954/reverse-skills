#!/usr/bin/env python3
"""
crashlink_autoname.py - 用 crashlink 解析 hlboot.dat,
                       批量给 IDA 中的函数命名为 Haxe 全限定名

用法:
    1. 在游戏运行后, dump 出 libhl 加载的 JIT 内存或主机版 .exe 到 IDA
    2. 同时把 hlboot.dat 拷出来
    3. 在 IDA 里 File → Script File → 选本文件
    4. (或 cli) python crashlink_autoname.py hlboot.dat names.txt

需要:
    pip install crashlink
"""

import sys
from crashlink import Bytecode

def dump_function_table(hl_path, out_path):
    """导出 findex → 全限定名 映射,供 IDA 重命名."""
    code = Bytecode.from_path(hl_path)

    # 1. 收集所有类的方法和字段绑定
    findex_to_name = {}

    for t in code.types:
        if t.kind != "Obj":
            continue
        cls = t.definition  # hl_type_obj
        cls_name = code.strings[cls.name].decode("utf-8", "replace")

        # 实例方法
        for proto in cls.protos:
            mname = code.strings[proto.name].decode("utf-8", "replace")
            findex_to_name[proto.findex] = f"{cls_name}.{mname}"

        # 静态方法 / 构造器(bindings)
        for binding in cls.bindings:
            field_name = code.strings[cls.fields[binding.field].name]
            field_name = field_name.decode("utf-8", "replace")
            findex_to_name[binding.findex] = f"{cls_name}.{field_name}"

    # 2. natives
    for n in code.natives:
        lib = code.strings[n.lib].decode("utf-8", "replace")
        nm  = code.strings[n.name].decode("utf-8", "replace")
        findex_to_name[n.findex] = f"native_{lib}_{nm}"

    # 3. 写文件 / 反馈给 IDA
    with open(out_path, "w", encoding="utf-8") as f:
        for findex in sorted(findex_to_name):
            f.write(f"{findex}\t{findex_to_name[findex]}\n")

    return findex_to_name


def find_main_entry(code):
    """打印入口函数 + 推断 Main.main 等关键函数."""
    print(f"Entry findex: {code.entrypoint}")
    print(f"Total functions: {len(code.functions)}")
    print(f"Total natives:   {len(code.natives)}")
    print(f"Total types:     {len(code.types)}")
    print(f"Total strings:   {len(code.strings)}")


def search_strings(code, keyword):
    """按关键词搜字符串池."""
    keyword = keyword.lower()
    hits = []
    for i, s in enumerate(code.strings):
        try:
            text = s.decode("utf-8", "replace")
        except:
            continue
        if keyword in text.lower():
            hits.append((i, text))
    return hits


def list_classes(code, filter_kw=None):
    """列出所有类,可加关键词过滤."""
    out = []
    for i, t in enumerate(code.types):
        if t.kind != "Obj":
            continue
        name = code.strings[t.definition.name].decode("utf-8", "replace")
        if filter_kw and filter_kw.lower() not in name.lower():
            continue
        out.append((i, name, len(t.definition.fields), len(t.definition.protos)))
    return out


def dump_class_fields(code, class_name):
    """给定类名,打印它的全部字段(含父类继承)."""
    for t in code.types:
        if t.kind != "Obj":
            continue
        nm = code.strings[t.definition.name].decode("utf-8", "replace")
        if nm == class_name:
            print(f"class {nm}:")
            for i, f in enumerate(t.definition.fields):
                fname = code.strings[f.name].decode("utf-8", "replace")
                ftype = f.t  # hl_type
                print(f"  @{i}  {fname}  : {ftype}")
            print(f"  ({len(t.definition.protos)} methods)")
            return
    print(f"class {class_name} not found")


# ---------------- IDA 部分(检测到 IDA 才执行) ----------------
def apply_to_ida(findex_map, get_findex_addr_fn):
    """
    在 IDA 内调用本函数:
        get_findex_addr_fn = lambda findex: 把 findex 翻译成 IDA 函数地址
    """
    import idaapi, idc
    for findex, name in findex_map.items():
        addr = get_findex_addr_fn(findex)
        if addr and addr != idc.BADADDR:
            # 替换非法字符
            safe = name.replace(".", "_").replace("<", "_").replace(">", "_")
            idc.set_name(addr, safe, idc.SN_NOWARN | idc.SN_FORCE)
    print(f"Renamed {len(findex_map)} functions")


# ---------------- main ----------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: crashlink_autoname.py <hlboot.dat> [out.txt]")
        sys.exit(1)

    hl_path  = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "names.txt"

    code = Bytecode.from_path(hl_path)

    print("=" * 60)
    find_main_entry(code)
    print("=" * 60)

    # 示例: 找所有含 "Player" 的类
    print("\n[Classes containing 'Player']")
    for i, nm, nf, np_ in list_classes(code, "Player"):
        print(f"  type#{i}  {nm}  fields={nf}  methods={np_}")

    # 示例: 搜含 "damage" 的字符串
    print("\n[Strings containing 'damage']")
    for i, s in search_strings(code, "damage")[:20]:
        print(f"  string#{i}: {s}")

    # 导出 findex 名字表
    findex_map = dump_function_table(hl_path, out_path)
    print(f"\n[Wrote {len(findex_map)} names to {out_path}]")
