# UE Mod Pipeline Notes

This file records notes extracted from the public article:

- Title: `Unreal Engine 5 逆向工程与游戏开发 - 黑神话悟空`
- URL: `https://blog.realduang.com/blogs/others/black-myth-ue5-reverse-engineering.html`

## Scope

This note extends `ue-reverse` into a practical UE5 modding and asset-replacement pipeline using `Black Myth: Wukong` as the example target. It complements the lower-level `asset-unpack-notes.md` by focusing on:

- AES-key acquisition
- `Mappings.usmap` dumping
- FModel-driven asset export
- asset editing in DCC tools
- repack / replacement in UE5
- UE4SS-based mod loading

## High-level pipeline

The article frames the workflow as:

1. obtain the AES key
2. dump `Mappings.usmap`
3. load/export with `FModel`
4. edit or create assets in 3D tools
5. import into UE5 and package
6. install with a mod loader

## AES key acquisition

The post treats AES retrieval as the first required step for unpacking.

### Mentioned approach

- locate the game executable directory
- use a tool such as `AES_finder`
- extract the AES key from the executable / runtime context

### Practical takeaway

- In game-specific modding work, AES recovery is a prerequisite for the rest of the pipeline.
- This note is more tool-and-practice oriented than `asset-unpack-notes.md`, which focuses more on reverse repair when common tools fail.

## `Mappings.usmap` acquisition

The article emphasizes that `Mappings.usmap` is required to correctly unpack and interpret game data in many UE5 scenarios.

### Mentioned approach

- use a DLL injector
- inject `UE Mapping Dumper`
- run the game
- wait for `Mappings.usmap` to be generated from runtime memory

### Practical takeaway

- `Mappings.usmap` should be treated as a first-class dependency alongside AES for UE5 content work.
- When export quality or field interpretation is wrong in FModel, verify whether mappings are missing or mismatched before blaming the assets.

## FModel-centered export workflow

The article recommends:

- `FModel`
- `UE Viewer` / `UModel`

### Workflow

1. install and open `FModel`
2. load `Mappings.usmap`
3. load target Pak files
4. provide the AES key
5. inspect and export the needed resources

### Practical takeaway

- This is the “standard success path” before moving into parser repair or deeper reverse engineering.
- Keep `FModel + AES + usmap` together as the default working set for UE5 asset extraction.

## Asset editing pipeline

The article lists typical DCC tools:

- `Blender`
- `3ds Max`
- `3D Viewer`
- `Maya`

It mentions exporting or working with UE-compatible formats such as:

- `.fbx`
- `.psk` (for Blender scenarios)

### Practical takeaway

- `ue-reverse` should not assume the workflow ends at extraction.
- For modding tasks, the reverse pipeline often continues into DCC editing and format conversion.

## UE5 import and repack path

The post describes a straightforward repack path:

1. open or create a UE5 project
2. import the new or modified assets
3. replace or add models
4. package the project
5. generate a Pak-oriented output for mod deployment

### Practical takeaway

- This creates a bridge from reverse analysis to production-like asset replacement.
- For user requests around “replace this model/texture/mesh in a UE5 game”, this note is the practical pipeline reference.

## Mod installation with UE4SS

The article recommends injecting a mod loader first:

- `RE-UE4SS`

It gives a directory-style example containing:

```text
BlackMythWukong\b1\Binaries\Win64
dwmapi.dll
ue4ss
UE4SS-settings.ini
UE4SS.dll
VTableLayout.ini
Mods
```

### Practical takeaway

- `UE4SS` is part of the practical deployment branch of `ue-reverse`.
- For mod-installation tasks, distinguish:
  - pure asset unpack/export
  - asset replacement/repack
  - runtime mod loader deployment

## Black Myth–specific gameplay notes

The article includes a few extracted gameplay values discovered during unpacking, for example:

- dodge invulnerability windows
- perfect-dodge window
- combo timing and action durations

### Practical takeaway

- Reverse or unpack work can surface balancing / timing data, not just meshes and textures.
- For data-mining tasks, keep gameplay tables, timing windows, and config assets in scope.

## UE-reverse takeaways

- Use this note when the task is not just “how do I find a UE global?” but “how do I turn extracted data into a working asset or mod?”
- Treat the standard UE5 content pipeline as:
  - AES
  - `Mappings.usmap`
  - `FModel`
  - DCC editing
  - UE5 import/package
  - `UE4SS` deployment
- Pair this note with:
  - [asset-unpack-notes.md](asset-unpack-notes.md) for non-standard loader / decrypt troubleshooting
  - [cnblogs-notes.md](cnblogs-notes.md) for runtime-global recovery
