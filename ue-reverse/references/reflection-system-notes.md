# UE Reflection System Notes

This file records notes extracted from the public article:

- Title: `UE5中使用反射系统进行结构体字段值的获取与设置（c++编写、蓝图调用）`
- URL: `https://blog.csdn.net/u010804261/article/details/136362741`

## Scope

This note is not mainly about cheat-style game reverse engineering. Its value for `ue-reverse` is that it turns the UE reflection system into concrete runtime field-access operations. It helps connect:

- `USTRUCT`
- `UPROPERTY`
- `UStruct`
- `FProperty`
- string-based field lookup
- import/export through reflection

This is useful whenever a reverse task crosses from “locate engine objects” into “programmatically read or write reflected fields”.

## Problem framing from the article

The article comes from a practical engineering scenario:

- a large communication struct with hundreds of fields
- frequent upstream data updates
- a need to both read fields and write them back
- a desire to avoid hand-writing one getter/setter per field

The chosen solution is to use UE’s reflection system so that:

- only the struct definition changes when fields change
- generic get/set logic stays the same
- Blueprint can call the generic get/set helpers by field name

## Reflection prerequisites

The article explicitly notes:

- if you want reflection support, the struct and its fields must be marked with UE metadata macros

Example pattern:

```text
USTRUCT(BlueprintType)
struct FTestStruct
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "TestStruct")
    double aa;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "TestStruct")
    double bb;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "TestStruct")
    int cc;
}
```

## Runtime read path

The article shows the reflective read chain:

1. obtain the reflected struct type through `FTestStruct::StaticStruct()`
2. call `FindPropertyByName(*FieldName)` on the `UStruct`
3. use `ContainerPtrToValuePtr<void>(&testStruct)` to locate the field storage
4. use `ExportTextItem(...)` to convert the field value into string form

### Practical takeaway

For `ue-reverse`, this is a very important bridge:

- locating a reflected field in memory is one step
- turning it into a generic runtime accessor is the next step

This note shows the engine-native path for that second step.

## Runtime write path

The article shows the reflective write chain:

1. obtain the target `UStruct`
2. resolve `FProperty*` via `FindPropertyByName`
3. get the target field address through `ContainerPtrToValuePtr<void>(...)`
4. call `ImportText(...)` to parse a string into the field storage

### Practical takeaway

This is useful for:

- rapid data patching tools
- Blueprint-exposed field editors
- config or protocol bridging
- reverse-side experiments where writing a field by symbolic name is easier than adding hard-coded setters

## Key APIs highlighted by the article

- `StaticStruct()`
- `FindPropertyByName`
- `ContainerPtrToValuePtr`
- `ExportTextItem`
- `ImportText`
- `BlueprintFunctionLibrary`
- `BlueprintCallable`

## UE-reverse takeaways

- Reflection is not only a concept for understanding `FName`/type systems; it also enables generic field tooling once the struct type is known.
- Use this note when the task is:
  - “read a reflected field by name”
  - “write a reflected field by name”
  - “build a generic Blueprint bridge for many struct fields”
  - “avoid hand-writing accessors for large reflected structs”
- Pair this note with:
  - [kanxue-notes.md](kanxue-notes.md) for reflection-design motivation
  - [series.md](series.md) and [cnblogs-notes.md](cnblogs-notes.md) for locating runtime globals and name/object systems

## Limits

- This note assumes you already have the reflected type and are operating inside UE code or injected runtime code with access to UE types.
- It does not replace lower-level reverse work needed to recover stripped or game-specific structures from a packaged target.
