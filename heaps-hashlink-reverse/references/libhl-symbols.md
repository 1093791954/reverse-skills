# libhl 关键 Native 函数索引

> 这些是 `libhl.dll`(Windows)/ `libhl.so`(Linux)的导出函数。
> 在 IDA / Ghidra 里把它们打 label,逆向 HL/C 主机版二进制立刻有语义。

## 1. 内存分配(GC 集成)

```c
// 只分纯字节数据,不会被 GC 扫描指针
void* hl_gc_alloc_noptr(int size);

// 分含 HL 指针的内存(GC 会扫)
void* hl_gc_alloc_raw(int size);

// 含终结器的内存,首字段是 finalize 函数指针
void* hl_gc_alloc_finalizer(int size);

// 给定 hl_type 分配
void* hl_gc_alloc(hl_type *t, int size);

// HL 高级值分配
varray*    hl_alloc_array(hl_type *t, int size);
vdynamic*  hl_alloc_dynamic(hl_type *t);
vdynamic*  hl_alloc_obj(hl_type *t);          // ★ 最常 hook
venum*     hl_alloc_enum(hl_type *t, int idx);
vvirtual*  hl_alloc_virtual(hl_type *t);
vdynobj*   hl_alloc_dynobj();
vbyte*     hl_alloc_bytes(int size);

vclosure*  hl_alloc_closure_void(hl_type *t, void *fvalue);
vclosure*  hl_alloc_closure_ptr(hl_type *fullt, void *fvalue, void *ptr);
```

## 2. GC Root 管理

```c
void hl_add_root(void **r);     // 注册根
void hl_remove_root(void **r);  // 取消注册
void hl_gc_major();             // 强制 full GC(很慢)
void hl_gc_disable(bool b);     // 暂停 GC(危险)
```

## 3. 动态字段访问

```c
int    hl_dyn_geti(vdynamic *d, int hfield, hl_type *t);
void*  hl_dyn_getp(vdynamic *d, int hfield, hl_type *t);
float  hl_dyn_getf(vdynamic *d, int hfield);
double hl_dyn_getd(vdynamic *d, int hfield);

void hl_dyn_seti(vdynamic *d, int hfield, hl_type *t, int value);
void hl_dyn_setp(vdynamic *d, int hfield, hl_type *t, void *ptr);
void hl_dyn_setf(vdynamic *d, int hfield, float f);
void hl_dyn_setd(vdynamic *d, int hfield, double v);

// 字段名 hash(必须用这个,直接用字符串无效)
int hl_hash_utf8(const char *name);
int hl_hash(vbyte *ucs2_name);
```

## 4. 调用 HL 函数

```c
vdynamic* hl_dyn_call(vclosure *c, vdynamic **args, int nargs);
vdynamic* hl_dyn_call_safe(vclosure *c, vdynamic **args, int nargs, bool *isException);
vdynamic* hl_dyn_call_obj(vdynamic *obj, hl_type *ft, int hfield, void **args, vdynamic *out);

// vclosure 结构:
struct vclosure {
    hl_type *t;       // +0
    void    *fun;     // +8  函数指针(JIT 后的 native 地址)
    int      hasValue;// +16 是否绑定 this
    void    *value;   // +24 绑定的 this
};
```

## 5. 类型描述读取

```c
// 常见预定义类型
extern hl_type hlt_void;
extern hl_type hlt_i32;
extern hl_type hlt_i64;
extern hl_type hlt_f64;
extern hl_type hlt_f32;
extern hl_type hlt_dyn;
extern hl_type hlt_array;
extern hl_type hlt_bytes;
extern hl_type hlt_dynobj;
extern hl_type hlt_bool;
extern hl_type hlt_abstract;

// 类型 kind 数字
enum hl_type_kind {
    HVOID  = 0,
    HUI8   = 1,
    HUI16  = 2,
    HI32   = 3,
    HI64   = 4,
    HF32   = 5,
    HF64   = 6,
    HBOOL  = 7,
    HBYTES = 8,
    HDYN   = 9,
    HFUN   = 10,
    HOBJ   = 11,    // ★ Haxe class
    HARRAY = 12,
    HTYPE  = 13,
    HREF   = 14,
    HVIRTUAL = 15,
    HDYNOBJ = 16,
    HABSTRACT = 17,
    HENUM   = 18,
    HNULL   = 19,
    HMETHOD = 20,
    HSTRUCT = 21,
    HPACKED = 22,
};
```

## 6. 异常 / 调用栈

```c
void hl_throw(vdynamic *v);
void hl_rethrow(vdynamic *v);
vdynamic* hl_get_exception();
void hl_dump_stack();
varray* hl_exception_stack();
void hl_setup_exception(void *handler, void *jmpbuf);
```

## 7. 字符串 API

```c
// HL String 全部是 UCS-2
vstring* hl_to_string(vdynamic *v);
char*    hl_to_utf8(const uchar *ucs2);
uchar*   hl_to_utf16(const char *utf8);
int      hl_ucs2_length(const uchar *str);

// 在内存里识别 String:
// 偏移 0  : hl_type* ($String 类型描述)
// 偏移 8  : uchar*  (UCS-2 字节)
// 偏移 16 : int     (字符数)
```

## 8. 模块 / 加载器(分析 hl.exe 时用)

```c
hl_module*    hl_module_alloc(hl_code *c);
bool          hl_module_init(hl_module *m, bool hot_reload);
hl_code*      hl_code_read(unsigned char *data, int size, char **error);
void          hl_code_free(hl_code *c);
void*         hl_jit_code(hl_jit_ctx *ctx, hl_module *m, int *codesize, hl_debug_infos **debug, hl_module *previous);
hl_jit_ctx*   hl_jit_alloc();
void          hl_jit_free(hl_jit_ctx *ctx, bool keep_function_table);
```

## 9. 常用全局符号

```c
extern hl_module *hl_module_context;  // 当前模块
extern void**     hl_globals;          // globals 表
extern int        hl_globals_size;
```

## 10. .hdll 扩展导出约定

每个 `.hdll` 用 `DEFINE_PRIM` 注册函数,IDA 中找:

```c
#define DEFINE_PRIM(rettype, name, args) \
    HL_PRIM hl_register_prim_t HL_NAME(__hxhl_##name) = \
        { #rettype, #name, args, (void*)HL_NAME(name) };
```

→ 二进制里能搜到符号 `__hxhl_<funcname>`,这就是 hdll 暴露给 HL 字节码的入口点。

**hdll 命名规则**:
- 库前缀 + 下划线 + 蛇形命名
- 示例: `directx_clear` `sdl_event_loop` `fmt_inflate` `openal_play_sound`

## 11. 在 IDA 里识别 .hdll 函数列表

1. 打开 `*.hdll`
2. 搜导出符号 `__hxhl_*`
3. 每个对应一个 `hl_register_prim_t` 结构: 4 个 char* + 1 个函数指针
4. 解析这些结构得到完整 (返回类型, 函数名, 参数签名, 实现地址)

## 12. JIT 后函数地址查找

```
hl_module_context->functions_ptrs : void**
hl_module_context->functions_types : hl_type**
hl_module_context->code->nfunctions : int
```

→ 给定 findex,直接 `functions_ptrs[findex]` 拿到 native 函数地址,可下断/hook。

## 13. 抓 hl_type 的实战

给定任意 HL 对象指针 `obj`:
```c
hl_type *t = *(hl_type**)obj;   // 第一字段
if (t->kind == HOBJ) {
    hl_type_obj *o = t->obj;
    const uchar *name_ucs2 = o->name;
    char name_utf8[256];
    hl_to_utf8_buf(name_ucs2, name_utf8, 256);
    printf("class: %s, fields: %d\n", name_utf8, o->nfields);

    for (int i = 0; i < o->nfields; i++) {
        hl_obj_field *f = &o->fields[i];
        printf("  +%d: %s : kind=%d\n", offset_of(f), f->name_utf8, f->t->kind);
    }
}
```
