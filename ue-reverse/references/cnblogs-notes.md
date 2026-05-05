# CNBlogs UE Reverse Notes

This file records notes extracted from the public blog post:

- Title: `ue5游戏逆向之寻找GWorld，GName和GUObjectArray`
- URL: `https://www.cnblogs.com/revercc/p/17641855.html`

## Main points

- For UE4, if symbols are exposed, `GWorld` and `GUObjectArray` can be recovered directly from exports.
- For older UE4 versions before `4.23`, `GName` can be located through older `GNames`-related logic.
- For `4.23+` and UE5, the more stable path is to recover `GName` through the `FNamePool::FNamePool` constructor.
- The author treats the UE5 “three-piece set” as:
  - `GWorld`
  - `GName`
  - `GUObjectArray`

## GWorld recovery path

- `GWorld` is defined in `Engine/Source/Runtime/Engine/Private/World.cpp`.
- The post uses `UWorld* FSeamlessTravelHandler::Tick()` as the source-side anchor.
- The locating strategy is:
  1. inspect source references to `GWorld`
  2. identify the nearby literal `SeamlessTravel FlushLevelStreaming`
  3. search that string in IDA
  4. move upward from the string xref to the code that writes `GWorld`
  5. note the earlier initialization to `NULL` to confirm the global slot

### Practical takeaway

- `SeamlessTravel FlushLevelStreaming` is a high-value locator string for `GWorld`.
- This matches and strengthens the `GWorld` guidance already present in the Kanxue notes.

## GName recovery path

- UE5 stores names in an `FNamePool`.
- The constructor initializes built-in names such as:
  - `None`
  - `ByteProperty`
  - `IntProperty`
- The locating strategy is:
  1. search `ByteProperty` in IDA
  2. jump to the xref that lands in the `FNamePool` constructor
  3. find callers or references to that constructor
  4. treat the passed `this` pointer as the `GName` / `NamePool` base

### Practical takeaway

- `ByteProperty` is a strong locator string for `FNamePool` / `GName`.
- This provides a direct operational bridge from the `FName` concepts in the Kanxue notes to a concrete UE5 locating method.

## GUObjectArray recovery path

- `GUObjectArray` is defined in `Engine/Source/Runtime/CoreUObject/Private/UObject/UObjectHash.cpp`.
- The post uses `int32 FEngineLoop::PreInitPostStartupScreen(const TCHAR* CmdLine)` as the source-side anchor.
- The locating strategy is:
  1. inspect source references to `GUObjectArray`
  2. use the literal `CloseDisregardForGC`
  3. search that string in IDA
  4. move near the string xref to the `GUObjectArray` access/write site

### Practical takeaway

- `CloseDisregardForGC` is a high-value locator string for `GUObjectArray`.
- This strengthens the dump-tool path, because once `GUObjectArray` is found, object enumeration and SDK dumping become much easier.

## Dump workflow

- The post references a modified dumper project:
  - `https://github.com/revercc/UE4Dumper.git`
- The stated goal is compatibility with `UE4.25+` and `UE5`.

### Example commands from the post

```text
./ue4dumper64 --newue+ --strings --gname 0x72C9F40 --package 包名 --output /sdcard/Download dump Strings
./ue4dumper64 --newue+ --sdkw --gworld 0x7488768 --gname 0x72C9F40 --package 包名 --output /sdcard/Download dump SDK
```

## UE-reverse takeaways

- Prefer a `source anchor -> characteristic string -> IDA xref -> global slot` workflow when recovering the UE5 runtime globals.
- Keep these concrete locators handy:
  - `SeamlessTravel FlushLevelStreaming` for `GWorld`
  - `ByteProperty` for `GName` / `FNamePool`
  - `CloseDisregardForGC` for `GUObjectArray`
- Use this post to connect abstract engine knowledge to concrete UE5 locating tactics and dumper invocation.
