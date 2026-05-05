# UE IoStore / ZenLoader Notes

This file records notes extracted from the public CSDN article:

- Title: `UE4 IO Store`
- URL: `https://blog.csdn.net/freeman8/article/details/127797941`

## Scope

This note extends `ue-reverse` with the runtime loading and container-format branch behind modern UE4.25+ and UE5 packaging. It is useful when the task involves:

- `Use Io Store`
- `.ucas` / `.utoc`
- `global.ucas` / `global.utoc`
- `AsyncLoader2`
- `IoDispatcher` / `IoService`
- DLC or hot-update compatibility problems caused by IoStore packaging

## High-level model

The article frames IoStore as part of the newer loading path introduced around UE4.25 experimental and used broadly in UE5:

- legacy direction: `AsyncLoader`
- newer direction: `AsyncLoader2` + `Zen Loader`
- package output changes from only `.pak` to `.pak + .utoc + .ucas`

Practical reverse takeaway:

- if a title uses IoStore, treating `.pak` as the only asset container is wrong
- the actual bulk asset data may live in `.ucas`
- the directory / chunk lookup data lives in `.utoc`

## Packaging toggle and visible symptoms

The key packaging switch is:

- `Project Settings > Packaging > Use Io Store`

When disabled:

- build output primarily contains `.pak`

When enabled:

- build output contains `.pak`
- per-container `.ucas`
- per-container `.utoc`
- extra `global.ucas`
- extra `global.utoc`

For reverse and mod workflows this explains why some older `PakLoader`-style assumptions fail on UE5 targets.

## Container roles

The article's practical split is:

- `.pak`
  - with IoStore off, stores packaged assets directly
  - with IoStore on, keeps less frequently accessed supporting content such as config / shader / project-side data, while asset payloads move to `.ucas`
- `.ucas`
  - asset container
  - stores `.uasset`, `.umap`, `.ubulk`, `.uptnl`, `.uexp` style payload data
  - layout is arranged for faster aligned IO
- `.utoc`
  - table-of-contents / directory metadata
  - links chunk metadata to offsets in `.ucas`
  - includes header and entry structures such as `FIoStoreTocHeader` and `FIoStoreTocEntry`

Practical reverse takeaway:

- if you can parse `.utoc`, you gain the chunk map
- if you can read the referenced offsets from `.ucas`, you gain the payload stream
- parser failures often come from treating IoStore like classic Pak-only layout

## Global containers

The article also highlights additional global files:

- `global.ucas`
  - global loader metadata container
  - includes content classes such as:
    - `LoaderGlobalMeta`
    - `LoaderInitialLoadMeta`
    - `LoaderGlobalNames`
    - `LoaderGlobalNameHashes`
- `global.utoc`
  - mostly header-side directory information for the global container

Practical reverse takeaway:

- global name and loader metadata are not just "extra files"; they are part of the loader contract
- a tool that only consumes per-chunk containers may miss name or initial-load metadata needed for correct reconstruction

## Loader pipeline shift

The article contrasts the old and new load paths.

Legacy path:

- `GameThread`
- `AsyncLoadingThread`
- pool/threaded file IO
- reads from `.pak`

Newer path:

- `GameThread`
- `AsyncLoadingThread2`
- `IoDispatcher`
- `IoService`
- reads from `.ucas`

Practical reverse takeaway:

- when tracing load behavior in modern UE5 targets, start from `AsyncLoadingThread2`, `IoDispatcher`, and `IoService`, not only the older Pak path
- if a breakpoint strategy only follows classic Pak reads, it may miss the actual content fetch path

## Build / invocation clues

The article lists three common ways to enable IoStore packaging:

1. enable `Use Pak File` and `Use Io Store` in project settings
2. enable UnrealPak and I/O Store in Project Launcher profiles
3. use UAT `BuildCookRun` with flags such as `-iostore` and `-pak`

Practical reverse takeaway:

- these flags are useful when reconstructing how a target project was built
- build scripts, launcher profiles, and UAT command lines can reveal whether IoStore should exist even before opening the package

## Performance angle

The article cites measured load-time improvements on Epic samples when IoStore is enabled, and ties the gain to:

- more efficient container layout
- lower CPU overhead
- better direct IO behavior

It also recommends `Unreal Insights` for profiling:

- `GameThread`
- `AsyncLoading`
- `IoService`
- `IoDispatcher`

Practical reverse takeaway:

- if the user is studying a title's startup or streaming behavior, IoStore is both a format topic and a performance topic
- `Unreal Insights` trace categories can help map loader stages to concrete engine threads before deeper static reverse work

## Reverse-oriented guidance

Use this note when:

- `.utoc` / `.ucas` appear beside `.pak`
- a mod loader expects `.pak` only and fails
- a parser succeeds on classic Pak titles but breaks on UE5 titles
- the user needs to understand where asset bytes really come from in the modern loader path

Combine this note with:

- `asset-unpack-notes.md` for tool repair, AES tracing, and parser adaptation
- `mod-pipeline-notes.md` for practical FModel / usmap / mod deployment workflows
