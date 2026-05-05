# Kanxue UE Reverse Notes

This file records only the content visibly accessible from the supplied Kanxue thread pages without bypassing site restrictions. All four threads below stop at a `回复或点赞可查看完整内容` gate, so treat these notes as public previews plus image/link metadata.

## Thread 287862

- Title: `[原创]unreal engine逆向学习之反射设计(一)`
- URL: `https://bbs.kanxue.com/thread-287862.htm`
- Forum: `逆向工程`
- Visible page count: `4`
- Gate: `回复或点赞可查看完整内容`
- Visible images directly exposed in page HTML: no article attachments were visible on the first page preview

### Visible text summary

- Motivates using a game engine instead of pure process-style C code by comparing a simple console game with a future 3D game that would otherwise need duplicated code and hand-written subsystems.
- Frames `reflection` as the ability of a program to inspect and modify its own type/state/behavior at runtime.
- Uses the practical need to spawn different monster classes by string name as the motivating problem.
- Introduces a base class plus derived custom classes as the minimal reflection design.
- Moves from a naive factory-create approach to a registration model:
  - map string names to object-construction methods
  - provide a string-to-constructor lookup interface
  - have newly added classes register their own constructor and name automatically
- Mentions a global hash table for storing object names.
- Concludes that the design allows string-driven object creation through a shared `object` base class, while noting that this is still far from a commercial reflection system.

### UE-reverse takeaways

- Reflection is not just an engine design concept; it is a reverse-engineering foothold for:
  - class-name discovery
  - runtime object-type discrimination
  - object creation and metadata registration reasoning
- This thread strengthens the conceptual bridge between `FName`/name systems and higher-level object recovery.
- When reversing UE titles, do not treat object naming and type lookup as unrelated tricks. They are part of the engine’s reflection architecture.

## Thread 288113

- Title: `[原创]unreal engine逆向学习之数据挖掘(四)`
- URL: `https://bbs.kanxue.com/thread-288113.htm`
- Forum: `逆向工程`
- Visible page count: `4`
- Gate: `回复或点赞可查看完整内容`

### Visible text summary

- States that engine-based data can be obtained through `world address + offset`.
- Describes `GWorld` as the global pointer for the active game world / current game instance.
- Gives visible `GWorld` locating hints: `SeamlessTravel` and `FlushLevelStreaming`.
- Explains `TArray` as UE’s dynamic-array structure analogous to a vector-like container.
- Explains `ULevel` as the container for all elements in a level and distinguishes persistent / streaming level concepts.
- Notes `PersistentLevel` as the current scene root and links streaming sublevels under `UWorld`.
- States that `AActor` instances are stored beneath that world/level structure.
- Suggests the workflow `string -> IDA locate -> CE verify structure`, and mentions that UE matrices are relatively stable.
- Moves into actor hierarchy:
  - `AActor` as the base in-scene entity
  - `APawn` as a controllable or control-oriented subclass
  - `ACharacter` as a movement-capable humanoid-style subclass
- Introduces world-to-screen conversion and explicitly names `pitch`, `yaw`, and `roll`.

### Exposed image URLs

The first page preview exposes these attachment URLs directly:

1. `https://bbs.kanxue.com/upload/attach/202508/1001878_WQ6SGCCGG9X576U.jpg`
2. `https://bbs.kanxue.com/upload/attach/202508/1001878_JKGKRPJ4HR7R7NF.jpg`
3. `https://bbs.kanxue.com/upload/attach/202508/1001878_382YMB5BDBN3TN3.jpg`
4. `https://bbs.kanxue.com/upload/attach/202508/1001878_SWQW8FPEFJ9RAEX.jpg`
5. `https://bbs.kanxue.com/upload/attach/202508/1001878_UFYHRQZW75ZPRSY.jpg`
6. `https://bbs.kanxue.com/upload/attach/202508/1001878_4EU33P3FY9SUMM4.jpg`
7. `https://bbs.kanxue.com/upload/attach/202508/1001878_9KM6ZQ9P7HTAEK9.jpg`
8. `https://bbs.kanxue.com/upload/attach/202508/1001878_RQ6Q5DRZQ8SMSHY.jpg`
9. `https://bbs.kanxue.com/upload/attach/202508/1001878_WNGPBDXT7ZAP8RU.jpg`
10. `https://bbs.kanxue.com/upload/attach/202508/1001878_HRWBXNX8P9ZP53A.jpg`
11. `https://bbs.kanxue.com/upload/attach/202508/1001878_HZT9HETD4PZBZVY.jpg`
12. `https://bbs.kanxue.com/upload/attach/202508/1001878_2CT85GWDYFCBDHC.jpg`
13. `https://bbs.kanxue.com/upload/attach/202508/1001878_Z5VW9F8KAF3B2V6.jpg`
14. `https://bbs.kanxue.com/upload/attach/202508/1001878_K34RPFAX6PP3SQE.jpg`
15. `https://bbs.kanxue.com/upload/attach/202508/1001878_56G45Q6MBK6A54A.jpg`

### UE-reverse takeaways

- This thread reinforces the practical runtime chain:
  - `GWorld`
  - `UWorld`
  - `PersistentLevel`
  - actor arrays / `TArray`
  - actor hierarchy
  - transform / camera math
  - world-to-screen output
- It also strengthens the recommended workflow:
  - use strings or characteristic literals to locate candidate logic in IDA
  - validate memory structures in CE
  - only then lift offsets and structs into code

## Thread 287863

- Title: `[原创]unreal engine逆向学习之FName(二)`
- URL: `https://bbs.kanxue.com/thread-287863.htm`
- Forum: `逆向工程`
- Visible page count: `3`
- Gate: `回复或点赞可查看完整内容`

### Visible text summary

- Uses UE `4.23` as the demonstrated version and `SCUM.exe` as the practical target example.
- Repeats the requirement to link Epic and GitHub so the engine source can be used as the semantic reference.
- Explains `FName` as a lightweight string-like system that does not store raw strings inline, but references entries stored in a global `NamePool`.
- Emphasizes the performance reason behind `FName`: operations compare or pass compact identifiers rather than full strings.
- Points to `NameTypes.h` and `UnrealNames.cpp` as the source-side anchors.
- Highlights `bNamePoolInitialized` and `NamePoolData` initialization flow.
- Suggests using the string `FloatProperty` as the IDA locator feature to recover the relevant initialization path in the game binary.
- Notes validating `NamePoolData + 0x10`.
- Describes `FNameEntryId` as a compact `uint32` key carrying block index and offset information.
- Explains `WITH_CASE_PRESERVING_NAME` as the split between editor and packaged behavior for case handling.
- Distinguishes `FString`, `FText`, and `FName`.
- Names `GetPlainNameString`, `GetDisplayNameEntry`, `GetDisplayIndex`, and `Resolve` as the important follow-up functions in the name pipeline.

### Exposed image URLs

The first page preview exposes these attachment URLs directly:

1. `https://bbs.kanxue.com/upload/attach/202508/1001878_ESY7TRE59QVXS56.jpg`
2. `https://bbs.kanxue.com/upload/attach/202508/1001878_E2EB6SFDYYYKEYR.jpg`
3. `https://bbs.kanxue.com/upload/attach/202508/1001878_MRDXH2TMVKKWHCY.jpg`
4. `https://bbs.kanxue.com/upload/attach/202508/1001878_DDXRQY7NR3EQ989.jpg`
5. `https://bbs.kanxue.com/upload/attach/202508/1001878_6FNT2VNAANP7VXB.jpg`
6. `https://bbs.kanxue.com/upload/attach/202508/1001878_V7B3MVDMEWGQ248.jpg`
7. `https://bbs.kanxue.com/upload/attach/202508/1001878_BB4SR473E558SAQ.jpg`
8. `https://bbs.kanxue.com/upload/attach/202508/1001878_AM67BYHU6XHYKNH.jpg`
9. `https://bbs.kanxue.com/upload/attach/202508/1001878_VX6SVGZ3XZA6U4J.jpg`
10. `https://bbs.kanxue.com/upload/attach/202508/1001878_4UVGKPN2EPQ2CQP.jpg`
11. `https://bbs.kanxue.com/upload/attach/202508/1001878_YRU6VQH36PZKG3E.jpg`
12. `https://bbs.kanxue.com/upload/attach/202508/1001878_6VDGZQX6PEF46A6.jpg`

### UE-reverse takeaways

- This thread deepens the name-system path by adding practical recovery anchors:
  - `FloatProperty`
  - `NamePoolData`
  - `FNameEntryId`
  - `GetDisplayNameEntry`
  - `Resolve`
- It strengthens the rule that source-code reading and binary locating should move together:
  - inspect `NameTypes.h` / `UnrealNames.cpp`
  - search for characteristic literals in IDA
  - verify the resulting candidate structure in memory

## Thread 287880

- Title: `[原创]unreal engine逆向学习之dump工具使用(三)`
- URL: `https://bbs.kanxue.com/thread-287880.htm`
- Forum: `逆向工程`
- Visible page count: `4`
- Gate: `回复或点赞可查看完整内容`

### Visible text summary

- Positions the article as a continuation after hand-written `GetName` / `FName` dumping, but shifts the focus toward using open-source dump tooling instead of repeating all manual work.
- Identifies `GUObjectArray` as the global `FUObjectArray` manager for all `UObject` instances.
- Explains `FUObjectItem` as the storage unit for an object inside the global object list.
- Mentions recovering the `GetObjectPtr` path and points to `UObjectBaseInit` as a key initialization anchor.
- Recommends locating `UObjectBaseInit` by string in the binary.
- Gives a compact taxonomy of reflected UE object categories:
  - `U/FProperty`
  - `UEnum`
  - `UStruct`
  - `UFunction`
  - `UClass`
  - `UScriptStruct`
- Notes the engine transition from `UProperty` to `FProperty` starting in `4.2x`, along with the reason: reducing `UObject`-based overhead.
- Mentions two open-source UE dump projects and frames them as:
  - a smaller codebase suited for learning and modification
  - a more automated tool that repairs signatures through feature matching and reflection traversal

### Exposed image URLs

The first page preview exposes these attachment URLs directly:

1. `https://bbs.kanxue.com/upload/attach/202508/1001878_34THFN6FWYB4B77.jpg`
2. `https://bbs.kanxue.com/upload/attach/202508/1001878_ANGN2H2Y8895A6R.jpg`
3. `https://bbs.kanxue.com/upload/attach/202508/1001878_7DTYGF539RUC7WK.jpg`
4. `https://bbs.kanxue.com/upload/attach/202508/1001878_ATVYAEJ3JQGHXZZ.jpg`
5. `https://bbs.kanxue.com/upload/attach/202508/1001878_KRF5BY6N3GV2WRF.jpg`
6. `https://bbs.kanxue.com/upload/attach/202508/1001878_KB6D3XTRGVTZBN2.jpg`
7. `https://bbs.kanxue.com/upload/attach/202508/1001878_8U9PX2JKT4FHZGF.jpg`
8. `https://bbs.kanxue.com/upload/attach/202508/1001878_X3QM62J64F9FCBS.jpg`

### UE-reverse takeaways

- This thread reinforces the object-dump path:
  - recover `GUObjectArray`
  - understand `FUObjectItem`
  - classify reflected object categories
  - decide between manual recovery and open-source dumper reuse
- It also improves the version-awareness rule:
  - `UProperty` vs `FProperty` is not cosmetic
  - dump output and type interpretation depend on the engine generation

## How to use these notes

- Use this file to supplement [series.md](series.md) when the user asks for:
  - reflection architecture as a reverse-engineering clue
  - `FName` / `NamePool` / `GetDisplayNameEntry` recovery hints
  - `GUObjectArray` / dump-tool usage and `UProperty` to `FProperty` migration context
  - `GWorld` / `ULevel` / `PersistentLevel` conceptual mapping
  - public preview content from the Kanxue UE series
- Do not claim access to the gated parts of the threads.
- Treat the visible preview as a conceptual reinforcement layer, not as a complete implementation guide.
