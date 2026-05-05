---
name: ue-reverse
description: Summarize and apply Unreal Engine reverse-engineering workflows from setup through runtime object access and overlay drawing. Use when the task involves UE or UE4/UE5 reverse analysis, engine source preparation, GName or FName reconstruction, UObject or FUObjectArray traversal, UWorld lookup, actor enumeration, world-to-screen conversion, object-name rendering, enemy filtering, bone access, or skeleton ESP drawing.
---

# UE Reverse

Use this skill to map the UE article series into a repeatable reverse-engineering workflow. The series moves from environment preparation, to name/object-system recovery, to runtime object traversal, and finally to visual overlay features such as actor labels and skeleton drawing. The skill also covers the modern UE5 packaging/loading branch (`IoStore`, `ZenLoader`, `.utoc`, `.ucas`) and the build-time reflection generation branch (`UHT`, `.generated.h`, `.gen.cpp`).

## Workflow

1. Classify the request into one of seven stages: setup, name-system recovery, object-system recovery, visual feature building, asset-unpack / pak-decrypt analysis, IoStore / loader analysis, or reflection codegen / metadata-pipeline analysis.
2. Read only the matching article band in [references/series.md](references/series.md).
3. Read [references/kanxue-notes.md](references/kanxue-notes.md) when the user needs extra conceptual framing around reflection design, `FName` / `NamePool`, `GUObjectArray`, `GWorld`, `PersistentLevel`, actor hierarchy, dump-tool usage, or world-to-screen math from the public preview content of the Kanxue threads.
4. Read [references/cnblogs-notes.md](references/cnblogs-notes.md) when the task is specifically about recovering the UE5 global trio `GWorld`, `GName`, and `GUObjectArray`, or when the user needs concrete locator strings and example dumper commands.
5. Read [references/asset-unpack-notes.md](references/asset-unpack-notes.md) when the task involves Pak extraction, AES-key recovery, CUE4Parse repair, UnrealPak workflows, custom loader tracing, or non-standard UE asset encryption.
6. Read [references/mod-pipeline-notes.md](references/mod-pipeline-notes.md) when the task involves `Mappings.usmap`, FModel export, DCC editing, UE5 repack, `UE4SS`, or a full asset-to-mod pipeline.
7. Read [references/reflection-system-notes.md](references/reflection-system-notes.md) when the task involves `UStruct`, `FProperty`, generic field get/set, string-based property lookup, Blueprint bridges, or runtime reflective read/write helpers.
8. Read [references/iostore-zenloader-notes.md](references/iostore-zenloader-notes.md) when the task involves `Use Io Store`, `AsyncLoader2`, `IoDispatcher`, `IoService`, `.utoc`, `.ucas`, `global.ucas`, `global.utoc`, or modern UE5 loader behavior.
9. Read [references/uht-reflection-pipeline-notes.md](references/uht-reflection-pipeline-notes.md) when the task involves how `UHT` generates `.generated.h` / `.gen.cpp`, how `GENERATED_BODY()` participates in reflection, or how build-time codegen becomes runtime `UClass` / `FProperty` metadata.
10. Prefer engine-structure reasoning over blind pointer chasing. The series is valuable because it ties runtime addresses back to UE concepts such as `FName`, `UObject`, `FUObjectArray`, `UWorld`, `IoStore`, and the reflection registration pipeline.
11. Keep version sensitivity explicit. Offsets, layouts, helper paths, mappings, generated glue, and resource formats may differ across UE4/UE5 titles.

## Article Map

- Read articles `1-2` for Epic/GitHub linkage, engine-source access, and Visual Studio preparation.
- Read articles `3-9` for `GName`, `FName`, name decryption, manual CE-assisted lookup, and code-side `GetName` reconstruction.
- Read articles `10-15` for `UObject`, `FUObjectArray`, and object dumping across objects, enums, functions, and structs.
- Read articles `16-18` for `UWorld`, actor lookup, and actor/world position extraction.
- Read articles `19-22` for world-to-screen conversion, object label rendering, and enemy-only filtering.
- Read articles `23-27` for bone position lookup, bone names, `GetBoneMatrix`, bone indices, and skeleton-stickman drawing.
- Read [references/kanxue-notes.md](references/kanxue-notes.md) for two extra public-preview threads:
  - reflection-design motivation and automatic type registration
  - `FName` / `NamePool` / `GetDisplayNameEntry` recovery hints
  - `GUObjectArray` and dump-tool usage notes
  - `GWorld -> UWorld -> PersistentLevel -> Actor/TArray -> W2S` conceptual chain
- Read [references/cnblogs-notes.md](references/cnblogs-notes.md) for a compact UE5 locator playbook:
  - `SeamlessTravel FlushLevelStreaming` for `GWorld`
  - `ByteProperty` for `GName` / `FNamePool`
  - `CloseDisregardForGC` for `GUObjectArray`
  - sample `UE4Dumper` commands for strings and SDK dumping
- Read [references/asset-unpack-notes.md](references/asset-unpack-notes.md) for the asset-unpack branch:
  - standard UE unpack toolchain
  - AES-key locating via `FAES::DecryptData`
  - `PakFile` / `LoadIndex` / `DecryptData` tracing
  - `CUE4Parse` repair workflow
  - native decrypt reuse for non-standard encryption
- Read [references/mod-pipeline-notes.md](references/mod-pipeline-notes.md) for the practical content-mod branch:
  - AES + `Mappings.usmap`
  - `FModel` export
  - DCC editing
  - UE5 import / package
  - `UE4SS` deployment
- Read [references/reflection-system-notes.md](references/reflection-system-notes.md) for the runtime reflection-API branch:
  - `StaticStruct`
  - `FindPropertyByName`
  - `ContainerPtrToValuePtr`
  - `ExportTextItem`
  - `ImportText`
- Read [references/iostore-zenloader-notes.md](references/iostore-zenloader-notes.md) for the modern package / loader branch:
  - `Use Io Store`
  - `.pak + .utoc + .ucas`
  - `global.ucas` / `global.utoc`
  - `AsyncLoader2`
  - `IoDispatcher`
  - `IoService`
- Read [references/uht-reflection-pipeline-notes.md](references/uht-reflection-pipeline-notes.md) for the reflection codegen branch:
  - `UnrealHeaderTool`
  - `uhtmanifest`
  - `.generated.h`
  - `.gen.cpp`
  - `GENERATED_BODY`
  - `StaticClass`

## Setup Path

Use this when the user is still preparing to analyze a UE title.

1. Start with articles `1-2`.
2. Confirm the user can access Epic's UnrealEngine GitHub source and open it in Visual Studio.
3. Use the source tree as the semantic reference for runtime structures, not just as a codebase to browse.

The expected outcome of this phase is not a working cheat feature. It is a working research environment that lets you resolve runtime concepts against engine code.

## Name-System Path

Use this when the user needs to recover class names, object names, or the engine naming pipeline.

1. Read articles `3-5` for conceptual grounding: `FName`, `UObjectBase`, `GName`, and the relevant name storage structure.
2. Read articles `6` and `9` when the immediate task is locating `GName` or validating it manually in Cheat Engine.
3. Read article `8` when the task is implementing `GetName` in code instead of using CE-only validation.
4. Read the reflection-design section in [references/kanxue-notes.md](references/kanxue-notes.md) when the user needs a cleaner explanation of why name systems, type systems, and object factories are part of the same reverse target.
5. Read [references/reflection-system-notes.md](references/reflection-system-notes.md) when the task moves from “what is the reflected type?” to “how do I generically read or write a reflected field at runtime?”

Focus on:

- How names are stored and indexed.
- How display indices or blocks are resolved.
- How to validate recovered strings before building logic on top of them.

## Object-System Path

Use this when the user needs runtime object enumeration or dump tooling.

1. Read articles `10-11` for `UObject` access and `FUObjectArray` layout understanding.
2. Read articles `12-15` for dump tooling across object categories.
3. Read article `16` to bridge object traversal into `UWorld`.
4. Read the `GWorld` / level notes in [references/kanxue-notes.md](references/kanxue-notes.md) when the user needs a quick conceptual map before doing low-level pointer validation.
5. Read [references/cnblogs-notes.md](references/cnblogs-notes.md) when the task is specifically to recover `GUObjectArray` or wire recovered globals into a dumper workflow.

Keep these constraints in mind:

- Treat `FUObjectArray` layout as version-sensitive.
- Validate candidate pointers with recognizable class or object-name evidence before bulk traversal.
- When dumping, separate raw traversal, type classification, and output formatting.

## Visual Feature Path

Use this when the user wants world data on screen.

1. Read articles `17-18` for actor lookup and coordinate extraction.
2. Read article `19` for screen projection.
3. Read articles `20-22` for object labels, decrypted names, and enemy filtering.
4. Read articles `23-27` for bone positions, names, matrices, indices, and final skeleton drawing.
5. Read the second Kanxue note in [references/kanxue-notes.md](references/kanxue-notes.md) when the task needs a compact explanation of `GWorld`, `PersistentLevel`, actor hierarchy, and `pitch/yaw/roll`.

Build these features in order:

1. Actor enumeration
2. Stable world position extraction
3. World-to-screen conversion
4. Text rendering
5. Enemy filtering
6. Bone lookup
7. Skeleton rendering

Do not jump straight to skeleton ESP before actor and projection data are already trusted.

## Asset-Unpack Path

Use this when the user wants to extract assets, recover Pak keys, patch an unpacker, or analyze a custom resource-loader implementation.

1. Start with [references/asset-unpack-notes.md](references/asset-unpack-notes.md).
2. Confirm the engine version first and align to the matching UE source.
3. Prefer the standard toolchain first:
   - `AESDumpster`
   - `FModel`
   - `CUE4Parse`
   - `UnrealPak`
   - `UnrealLocres`
4. If the user’s real goal is a working asset replacement or mod, switch to [references/mod-pipeline-notes.md](references/mod-pipeline-notes.md) and verify:
   - AES
   - `Mappings.usmap`
   - FModel export
   - UE5 import / repack
   - `UE4SS` or equivalent loader placement
5. If standard tooling fails, shift into reverse mode:
   - trace `FPakPlatformFile`, `FPakFile`, `FAES::DecryptData`
   - inspect `PakFile.cpp`, `IPlatformFilePak.cpp`, and related source
   - validate loader timing and whether a launcher causes late attachment
6. Use parser repair before greenfield reimplementation when the file format is only partially modified.
7. Consider native decrypt-function reuse when the crypto is AES-like but non-standard and full reimplementation is not cost-effective.

Build this branch in order:

1. Version identification
2. Source alignment
3. Standard-tool validation
4. AES-key recovery
5. Pak/index/offset validation
6. Parser repair or native decrypt reuse

## IoStore Path

Use this when the user is dealing with UE5-era packaged assets, loader tracing, or hot-update / DLC behavior that breaks because the title is not using classic Pak-only assumptions.

1. Start with [references/iostore-zenloader-notes.md](references/iostore-zenloader-notes.md).
2. Confirm whether the title is packaged with `Use Io Store`.
3. Treat `.utoc` as the directory / chunk map and `.ucas` as the actual asset container.
4. If tooling only understands `.pak`, verify whether the failing title actually stores the payload in `.ucas`.
5. When tracing runtime loading, pivot to:
   - `AsyncLoadingThread2`
   - `IoDispatcher`
   - `IoService`
6. If the task is asset extraction or parser repair, combine this path with [references/asset-unpack-notes.md](references/asset-unpack-notes.md).
7. If the task is mod deployment or DLC packaging compatibility, combine this path with [references/mod-pipeline-notes.md](references/mod-pipeline-notes.md).

Build this branch in order:

1. Detect IoStore usage
2. Classify container roles
3. Validate `.utoc` / `.ucas` expectations
4. Map runtime loader path
5. Repair tool or workflow assumptions

## Reflection-Codegen Path

Use this when the user needs to understand how build-time metadata generation becomes runtime reflection data.

1. Start with [references/uht-reflection-pipeline-notes.md](references/uht-reflection-pipeline-notes.md).
2. Identify the source-side markers:
   - `UCLASS`
   - `USTRUCT`
   - `UENUM`
   - `UFUNCTION`
   - `UPROPERTY`
   - `GENERATED_BODY`
3. Verify inclusion of `ClassName.generated.h`.
4. Follow the build-time generation step through `UnrealHeaderTool` and `uhtmanifest`.
5. Use `.generated.h` and `.gen.cpp` as the bridge between handwritten declarations and runtime registration behavior.
6. Switch to [references/reflection-system-notes.md](references/reflection-system-notes.md) once the task changes from "how was metadata generated?" to "how do I read or write reflected fields at runtime?"

Build this branch in order:

1. Macro markers
2. Generated file inclusion
3. UHT invocation
4. Generated glue inspection
5. Runtime metadata interpretation

## Troubleshooting

- If names look wrong, go back to the `GName` and `GetName` articles before debugging overlay code.
- If object traversal returns many invalid entries, revisit `FUObjectArray` assumptions and validate version/layout first.
- If `GWorld`, `GName`, or `GUObjectArray` cannot be recovered, fall back to the concrete locator strings in [references/cnblogs-notes.md](references/cnblogs-notes.md) before broadening the search.
- If `FModel` or `CUE4Parse` fails even with a recovered key, move to [references/asset-unpack-notes.md](references/asset-unpack-notes.md) and validate Pak header, index, offsets, alignment, and decrypt behavior before assuming the key is wrong.
- If a UE5 content workflow behaves like assets are "missing" even though the build is valid, verify whether the payload moved to `.ucas` and the directory data moved to `.utoc` before debugging keys or paths.
- If export output is incomplete or field parsing looks wrong in UE5, verify `Mappings.usmap` availability and version match before changing the unpack path.
- If the unpack succeeded but the mod does not load, check the `UE4SS` / loader layout and repack path from [references/mod-pipeline-notes.md](references/mod-pipeline-notes.md).
- If a generic field read/write helper fails, verify that the target struct and fields actually carry UE reflection macros and that the access path uses the correct owning container pointer.
- If runtime metadata looks inconsistent, separate build-time reflection questions from runtime access questions:
  - use [references/uht-reflection-pipeline-notes.md](references/uht-reflection-pipeline-notes.md) for generated glue and registration origin
  - use [references/reflection-system-notes.md](references/reflection-system-notes.md) for live field access APIs
- If you never hit `Initialize` or `LoadIndex`, consider whether a launcher or late attach is hiding the real loader path.
- If world coordinates look plausible but render positions are wrong, isolate the world-to-screen step before changing actor logic.
- If skeleton lines are distorted, verify bone index mapping and `GetBoneMatrix` output before blaming projection.
- If an enemy-only filter misses targets, verify team or ownership logic separately from draw logic.
- If the source material comes from a gated forum or partial preview, separate:
  - what was directly visible on the page
  - what is inferred from UE structure knowledge
  - what still needs validation in IDA, CE, or a live target

## Reference Use

- Use [references/series.md](references/series.md) as the full notebook for all 27 UE articles.
- Use [references/kanxue-notes.md](references/kanxue-notes.md) for public-preview notes from two supplementary Kanxue threads.
- Use [references/cnblogs-notes.md](references/cnblogs-notes.md) for a focused UE5 `GWorld` / `GName` / `GUObjectArray` locating recipe.
- Use [references/asset-unpack-notes.md](references/asset-unpack-notes.md) for UE resource-unpack and non-standard Pak reverse workflows.
- Use [references/mod-pipeline-notes.md](references/mod-pipeline-notes.md) for practical UE5 asset replacement and mod deployment workflows.
- Use [references/reflection-system-notes.md](references/reflection-system-notes.md) for runtime reflected field access and Blueprint-oriented property tooling.
- Use [references/iostore-zenloader-notes.md](references/iostore-zenloader-notes.md) for modern loader/container behavior around `.utoc`, `.ucas`, `AsyncLoader2`, and `IoDispatcher`.
- Use [references/uht-reflection-pipeline-notes.md](references/uht-reflection-pipeline-notes.md) for `UHT`, `.generated.h`, `.gen.cpp`, `uhtmanifest`, and `GENERATED_BODY`.
- Search by article number or keyword such as `GName`, `FName`, `FUObjectArray`, `UWorld`, `Aactor`, `屏幕坐标转换`, `GetBoneMatrix`, `骨骼`, `IoStore`, `utoc`, `ucas`, `UHT`, or `generated.h`.
- Search `kanxue-notes.md` for `反射`, `GWorld`, `PersistentLevel`, `TArray`, `AActor`, `pitch`, `yaw`, or `roll`.
- Search `cnblogs-notes.md` for `SeamlessTravel FlushLevelStreaming`, `ByteProperty`, `CloseDisregardForGC`, or `UE4Dumper`.
- Search `asset-unpack-notes.md` for `FAES::DecryptData`, `LoadIndex`, `CUE4Parse`, `FPakPlatformFile`, `CloseDisregardForGC`, `AESDumpster`, or `winhttp.dll`.
- Search `mod-pipeline-notes.md` for `Mappings.usmap`, `FModel`, `UE4SS`, `dwmapi.dll`, or `BlackMythWukong`.
- Search `reflection-system-notes.md` for `FindPropertyByName`, `ContainerPtrToValuePtr`, `ExportTextItem`, `ImportText`, or `BlueprintFunctionLibrary`.
- Search `iostore-zenloader-notes.md` for `Use Io Store`, `AsyncLoader2`, `IoDispatcher`, `IoService`, `FIoStoreTocHeader`, `global.ucas`, or `global.utoc`.
- Search `uht-reflection-pipeline-notes.md` for `UnrealHeaderTool`, `uhtmanifest`, `generated.h`, `gen.cpp`, `GENERATED_BODY`, or `StaticClass`.
- When producing code or guidance, convert the tutorial series into engine concepts, validation checkpoints, and implementation order, and call out explicitly when a forum source was only partially visible.
