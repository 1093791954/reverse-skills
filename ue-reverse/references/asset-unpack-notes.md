# UE Asset Unpack Notes

This file records notes extracted from the public blog post:

- Title: `UE5 游戏资源解包与逆向工程实践分享`
- URL: `https://piz-ewing.github.io/2026/01/09/ue5_asset_unpack_reverse/`

## Scope

This post expands `ue-reverse` beyond runtime globals and ESP-style workflows into the asset-unpack and non-standard Pak-decryption path. It is especially relevant when the user needs:

- Pak or IoStore resource extraction
- AES key recovery
- CUE4Parse repair or adaptation
- UnrealPak / UnrealLocres workflows
- analysis of custom or non-standard UE resource loaders

## Standard UE unpack toolchain

The post lists common tools and their roles:

- `AESDumpster`
  - fast extraction of in-memory UE AES keys
- `FModel`
  - popular UE4/UE5 asset browser and exporter
- `CUE4Parse`
  - the parsing/decryption library used by FModel
- `UModel`
  - older but stable UE viewer
- `UnrealPak`
  - official pack/unpack tool from Epic
- `UnrealLocres`
  - localization resource extraction / handling

### Advanced / reverse-adjacent tools

- `yinjector`
  - lightweight DLL injector for hooks and instrumentation
- `Dumper-7`
  - SDK / reflection dump support, including `.usmap`
- `RE-UE4SS`
  - runtime extension / modding framework
- `PalWorld-Server-Unoffical-Api`
  - example of UE runtime interaction and capability extension

## Non-standard unpack scenarios

The post calls out several reasons standard tools may fail:

- extracted AES key is wrong or incomplete
- AES key is generated dynamically or derived in multiple stages
- custom Pak loader or secondary wrapping exists
- encryption or validation algorithms were replaced or modified

### Practical takeaway

When standard tools fail, pivot from “tool usage” to “engine and loader reverse engineering”.

## Manual AES-key recovery

The suggested strategy:

1. Start from the UE Pak load / decrypt path.
2. Focus on:
   - `FPakPlatformFile`
   - `FPakFile`
   - `FAES::DecryptData`
3. Use strings, structure layout, and xrefs to track key initialization, passing, and use.
4. Break on key functions or writes at runtime.
5. Dump the final in-memory plaintext key or derived result at the right moment.

### Reverse tools

- `IDA / Ghidra` for structure, call graph, and static flow
- `x64dbg / WinDbg` for runtime key observation and timing

## Version and source preparation

Before unpack analysis:

1. Identify the target UE version.
2. Obtain the matching engine source.
3. Focus on:

```text
Engine/Source/Runtime/PakFile/Private/
```

Important files named in the post:

- `IPlatformFilePak.cpp`
  - contains Pak decrypt logic such as `DecryptData`
- `PakFile.cpp`
  - contains `LoadIndex`, `LoadIndexInternal`
- `SignedArchiveReader.cpp`
  - contains serialization logic around Pak index handling

## Concrete AES-key locating path

The post’s workflow:

1. Search Pak-decrypt-related strings in x64dbg.
2. Break around the related function path.
3. Observe `FAES::DecryptData`.
4. Read the AES key from `r8` at the breakpoint.

Additional observation:

- the key fetch helper `GetPakEncryptionKey` may be inlined by the compiler
- do not assume it exists as a separate function in the disassembly

## CUE4Parse adaptation workflow

When FModel fails even with a recovered key:

1. Move to `CUE4Parse` instead of writing a parser from scratch.
2. Rewire the example project for direct unpack testing.
3. Manually set:
   - archive directory
   - AES key
   - Pak file name
4. Trace the flow dynamically.

The post highlights these code paths:

- `CUE4Parse/UE4/Pak/PakFileReader.cs`
  - `PakFileReader -> FPakInfo.ReadFPakInfo -> new FPakInfo`
- `CUE4Parse/FileProvider/Vfs/AbstractVfsFileProvider.cs`
  - `SubmitKeysAsync -> MountTo -> PakFileReader.Mount -> ReadIndexUpdated -> ReadAndDecryptIndex`

### Practical takeaway

- If the Pak structure is slightly modified, start with header fields, offsets, sizes, alignment, and index handling.
- Assume the virtual filesystem model is mostly intact unless there is strong evidence of deeper redesign.

## Runtime sync and loader validation

The post recommends synchronizing static and dynamic analysis:

1. Use IDA to locate:
   - `Initialize`
   - `LoadIndex`
   - `LoadIndexInternal`
2. Bring the recovered offsets and call sites into x64dbg.
3. Validate:
   - Pak header fields
   - index offsets and sizes
   - alignment / padding
   - data before and after decryption
4. Compare runtime behavior with CUE4Parse’s implementation line by line.

## Attach timing and early injection

One failure mode is attaching too late because a launcher process starts the real game binary.

The post suggests:

- distinguishing late-attach issues from custom-load-path issues
- forcing earlier participation in process startup

Recommended tactic from the post:

- DLL search-order hijack, for example by placing a fake `winhttp.dll`
- using `AheadLib` to generate a quick hijack scaffold

### Practical takeaway

- Early loader-stage instrumentation matters for Pak reverse work.
- If you miss `Initialize` / `LoadIndex`, your problem may be timing rather than wrong analysis.

## Non-standard AES and native-decrypt reuse

The post reaches a case where:

- offsets and index structure were mostly corrected
- `DecryptData` still produced invalid results in `CUE4Parse`
- extracted cipher and key matched CUE4Parse’s result
- but differed from the game’s own decrypted output

Conclusion:

- the algorithm looked AES-like but was not standard AES internally

Instead of fully reversing the modified crypto, the post used a cheaper tactic:

- reuse the game’s own decrypt function
- forward decrypt requests into the game process through a simple RPC mechanism layered on the existing DLL injection path

### Practical takeaway

- Do not overcommit to full algorithm recovery when native-function reuse is cheaper and sufficient.
- In real projects, “call the game’s own decrypt routine” can beat “fully reimplement custom crypto”.

## UE-reverse takeaways

- Extend the reverse workflow beyond runtime globals:
  - version identification
  - source alignment
  - loader tracing
  - AES-key recovery
  - parser repair
  - native decrypt reuse
- Use this note whenever the task shifts from actor/object analysis to packaged-resource extraction.
- Treat `Pak`, `AES`, `LoadIndex`, `DecryptData`, and `CUE4Parse` as first-class reverse targets, not just tooling details.
