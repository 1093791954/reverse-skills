# UE UHT / Reflection Pipeline Notes

This file records notes extracted from the public CSDN article:

- Title: `UE里的反射(Reflections)机制`
- URL: `https://blog.csdn.net/alexhu2010q/article/details/129988937`

## Scope

This note strengthens `ue-reverse` on the "how UE reflection metadata is generated and wired into runtime" branch. It is useful when the task involves:

- `UHT`
- `UCLASS` / `USTRUCT` / `UENUM`
- `UFUNCTION` / `UPROPERTY`
- `GENERATED_BODY`
- `.generated.h`
- `.gen.cpp`
- `uhtmanifest`
- reverse mapping from runtime `UClass` / `FProperty` back to build-time codegen steps

## Core model

The article describes UE reflection as a custom metadata/codegen system layered on top of C++:

- developers mark code with UE macros
- `UnrealHeaderTool` scans the headers before normal compilation
- UHT emits generated code and metadata glue
- the generated code makes classes, properties, and functions visible to the runtime object system

Practical reverse takeaway:

- UE reflection is not "magic RTTI"
- the runtime object graph is backed by generated registration code
- when reversing property or function metadata, think in terms of a codegen pipeline, not only memory layouts

## The minimum source-side contract

The article highlights the common rules:

- use `UENUM`, `UCLASS`, `USTRUCT`, `UFUNCTION`, `UPROPERTY`
- reflected classes live in the `UObject` ecosystem
- headers include `FileName.generated.h`
- class bodies use `GENERATED_BODY()`

Practical reverse takeaway:

- if a field or function is missing from runtime reflection, first ask whether it was actually marked for UHT processing
- reverse helpers that assume every native field is reflected will be wrong

## Editor template origin of new reflected classes

The article walks through creating a new `Actor` in the UE editor and shows that:

- the editor generates starter `.h` / `.cpp` files from templates
- the templates already inject:
  - `#include "ClassName.generated.h"`
  - `UCLASS()`
  - `GENERATED_BODY()`

Practical reverse takeaway:

- many recurring class-layout patterns in shipped projects come from editor templates, not only from manual coding style
- if you are trying to reason about how common actor classes are shaped, template defaults are a good prior

## How generated files are created

The article captures the console output when a new reflected class is created:

- `UnrealHeaderTool` is invoked explicitly
- input includes the `.uproject`
- input also includes a `.uhtmanifest`
- output says reflection code was generated for the editor target

Practical reverse takeaway:

- UHT is a concrete build step you can reproduce and debug
- if you want to understand why a reflected symbol exists, inspect UHT inputs and outputs rather than treating generated files as opaque artifacts

## `uhtmanifest`

The article characterizes `uhtmanifest` as the manifest describing project/module dependency context for UHT.

Practical reverse takeaway:

- module boundaries matter for reflection generation
- when reconstructing where a class came from, module-level build structure is part of the answer

## `.generated.h` and `.gen.cpp`

The article treats these files as the direct bridge between handwritten code and the runtime reflection system.

What matters for reverse work:

- `.generated.h`
  - injects declarations and macro expansions needed by the class body
  - ties `GENERATED_BODY()` to concrete generated declarations
- `.gen.cpp`
  - carries registration-side glue and supporting generated implementation pieces

Practical reverse takeaway:

- when a runtime helper such as `StaticClass()` or property registration exists, there is usually generated code behind it
- when symbol names look unfamiliar in disassembly, check whether they come from `.gen.cpp` emission patterns

## Why `GENERATED_BODY()` matters

The article emphasizes that UHT can generate convenience and framework glue such as:

- constructors
- `StaticClass`
- other boilerplate needed for the object system

Practical reverse takeaway:

- `GENERATED_BODY()` is not decorative
- it is the insertion point that lets the handwritten class participate in reflection, registration, and object construction scaffolding

## Reverse-facing interpretation of the macro set

Map the common macros to likely runtime consequences:

- `UCLASS`
  - class-level participation in UE object metadata
- `USTRUCT`
  - struct-level reflective metadata
- `UENUM`
  - enum registration and editor/serialization visibility
- `UPROPERTY`
  - field metadata used by editor details panels, serialization, replication, GC reachability, and generic property access
- `UFUNCTION`
  - callable metadata used by Blueprints, RPC, reflection invocation, and function lookup

Practical reverse takeaway:

- when building a dumper or property-access helper, the question is not only "what is the offset?"
- it is also "did UHT emit metadata for this symbol, and what systems depend on it?"

## Reproducible debugging angle

The article explicitly notes that:

- deleting generated files and rerunning UHT regenerates them
- UHT can be invoked manually with the captured arguments
- the UHT project can be debugged

Practical reverse takeaway:

- when studying reflection generation on a source-available engine version, you can instrument the build step itself
- this is often cleaner than inferring everything from shipped binaries

## Why this matters for `ue-reverse`

This note complements the runtime-oriented reflection helpers in `reflection-system-notes.md`.

Use this note when the question is:

- how did this runtime `UClass` / `FProperty` metadata come to exist?
- why does a reflected field appear in one title but not another?
- what build-time artifacts explain `StaticClass`, generated registration code, or reflected offsets?

Pair it with:

- `reflection-system-notes.md` for runtime field access APIs
- `kanxue-notes.md` for reflection-design motivation
- `cnblogs-notes.md` and `series.md` when moving from reflection understanding into concrete reverse workflows
