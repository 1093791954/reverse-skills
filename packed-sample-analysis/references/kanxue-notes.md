# Kanxue Notes

This file records only points that were validated by opening public Kanxue pages. It is intentionally limited to lawful analysis heuristics and artifact-validation ideas.

## Kanxue OEP and IAT Notes

### VMProtect3.31的 "OEP之旅"

Link: https://bbs.kanxue.com/thread-251250.htm

What the page actually contains:

- a case study on finding an `OEP` under `VMProtect 3.31`
- the author compares runtime environments before and near `OEP`
- one observation is that stack state may expose an `OEP`-adjacent return target even when simpler break strategies fail
- the post also notes that some apparent breakpoint ideas become unreliable once anti-debug behavior or emulation differences enter the picture

Safe takeaway:

- for high-end protectors, environment comparison can be more valuable than assuming one universal API or memory-breakpoint trick
- stack-state differences and late-stage runtime context can be useful evidence, but they are sample-specific rather than universal

Do not carry forward:

- the page's concrete step-by-step breakpoint choreography or patch instructions

### 根据栈平衡原理寻找OEP / 根据编译语言特点寻找OEP / 重建输入表

Link: https://bbs.kanxue.com/article-8698.htm

What the page actually contains:

- several classic `OEP` heuristics:
  - transition back into the real code section
  - stack-balance reasoning around saved register state
  - compiler-family startup fingerprints such as early imported API calls
- a dump reminder that the dumped image may need header or `SizeOfImage` correction
- `IAT` reconstruction notes, including how to reason about `IAT` start and size and what to do when the table is not contiguous

Safe takeaway:

- these are useful for classical packers and loader-style shells
- they should be treated as heuristic families, not rigid recipes
- `IAT` repair should be evidence-based, especially when the table is fragmented or partially transformed

Do not carry forward:

- the article's debugger hotkeys, exact breakpoint placements, and tool choreography

### 恶意软件PE文件重建指南

Link: https://bbs.kanxue.com/article-12841.htm

What the page actually contains:

- a malware-oriented discussion of manual PE reconstruction
- an explanation of why packers may destroy the original `IAT` form and resolve APIs outside the normal Windows loader path
- a specific anti-reconstruction pattern called `stolen API code`, where import recovery points into simulated or relocated API stubs rather than the real import target
- a reminder that exported memory images need file-alignment and layout review before they become valid disk artifacts

Safe takeaway:

- if automated import reconstruction fails, the problem may be the sample's import indirection model rather than the tool alone
- `IAT` recovery can be intentionally poisoned by trampoline or simulated stub logic
- a memory artifact can still be useful for study even when it is not yet a clean runnable PE

Do not carry forward:

- the page's code-level plugin implementation details for automating repair

### 进程 Dump & PE unpacking & IAT 修复 - Windows 篇

Link: https://bbs.kanxue.com/thread-274505.htm

What the page actually contains:

- a workflow-oriented discussion of recovering a program from a live process or memory dump when the original disk file is unavailable
- a strong distinction between the PE image as it exists in memory and the PE file as it should exist on disk
- a comparison between two families of repair outcomes:
  - converting a mapped image back toward a raw file layout
  - keeping a realigned image that remains structurally analyzable but may preserve runtime residue
- a practical explanation of why `.bss` and other runtime-mutated data can make a "fixed" file statically readable but not safely re-runnable
- an explanation of when `IAT` repair is actually necessary:
  - if `OriginalFirstThunk` remains usable, section repair alone may be enough
  - if `OriginalFirstThunk` is lost and `FirstThunk` points at runtime-resolved addresses, import parsing can fail and reconstruction becomes necessary
- two repair settings:
  - an offline case that relies on artifacts such as minidumps and environment-derived symbol mapping
  - an online case where a still-available host or process context makes import recovery easier

Safe takeaway:

- a dumped memory image is not the same thing as a runnable restored PE
- section repair, import repair, and runtime-state cleanup are separate validation steps
- preserving too much runtime state can create false confidence: the file may open in a disassembler yet still fail when relaunched
- `INT` versus `IAT` state matters when judging whether a dump needs import reconstruction or only layout repair
- import recovery should be tied to the target runtime environment when address-based evidence depends on ASLR or live module layout

Do not carry forward:

- the post's end-to-end tool choreography
- exact command lines, scripts, patch offsets, or workflow details that would serve as a turnkey unpacking recipe

### IDA静态分析中的“签名识别”快速修复导入表

Link: https://bbs.kanxue.com/thread-289563.htm

What the page actually contains:

- a short note proposing a static-analysis shortcut: use IDA signature recognition to label a suspected pointer array and rapidly recover likely API names
- the idea is presented as a speed-up for some post-unpacking cases where imports appear scrambled but the target still references standard libraries
- the single reply questions where this fits relative to classic ImportREC-style workflows, which highlights that the technique is more of a static-assistance trick than a universal repair path

Safe takeaway:

- signature-based naming can be a useful triage aid when a probable import region is already visible
- it is best treated as a labeling shortcut for static analysis, not proof that the import table is structurally correct
- this approach is most plausible when the sample still leans on recognizable standard-library usage; it is weaker for custom loaders, poisoned imports, or heavily transformed samples

Do not carry forward:

- the page's step-by-step keypress sequence as if it were a general-purpose import-repair method

### Enigma6.8脱壳+修复（上）

Link: https://bbs.kanxue.com/thread-268825.htm

What the page actually contains:

- a case study on `Enigma 6.8` that explicitly separates `OEP` discovery from later `IAT` handling
- the author describes stronger anti-debug behavior than in simpler packers and argues that naive single-stepping or software breakpoints can mislead the analysis
- the public portion distinguishes several `IAT`-handling styles for this protector:
  - simulated API execution
  - simple encryption
  - mixed encryption plus simulation
- the public text also frames `OEP` recovery as something that can still benefit from compiler- or language-specific startup fingerprints when the entry is not fully virtualized

Safe takeaway:

- `Enigma`-style cases still benefit from classical `OEP` reasoning, but anti-debug noise means evidence quality matters more than rote tracing
- it is useful to classify the protector's import behavior before assuming one `IAT` repair workflow
- compiler-startup fingerprints remain a practical way to confirm that a candidate region looks like real program code rather than shell scaffolding

Do not carry forward:

- the article's concrete breakpoint placement, byte patterns, and debugger choreography

### Armadillo_9.64加壳脱壳分析

Link: https://bbs.kanxue.com/thread-284527.htm

What the page actually contains:

- a principle-oriented analysis of `Armadillo 9.64` rather than only a stripped-down how-to
- a lowest-protection case where the visible problem is primarily encrypted imports
- a progression from simpler protection to cases involving debugger checks, dual-process behavior, exception-driven flow, and page-protection-based code restoration
- repeated emphasis that some observed options or UI toggles do not necessarily correspond to equally strong underlying protection in the tested sample
- a discussion of multiple exception types and debug-event handling as part of the protector's control flow rather than as accidental crashes

Safe takeaway:

- `Armadillo` should be modeled as more than an `OEP` problem: import handling, exception flow, and parent-child process behavior may all matter
- repeated structured exceptions can be part of the protector's intended execution path, so they should be logged and classified before being treated as generic faults
- dual-process or debug-event-driven protectors require a runtime model of which process is executing meaningful code
- brute-force tracking of import writes can be a fallback when cleaner structure recovery is unavailable

Do not carry forward:

- exact exception-handling patches
- specific branch bypasses
- operational instructions for reproducing a full unpacking workflow

### 脱壳之ASPack压缩壳

Link: https://bbs.kanxue.com/thread-271040.htm

What the page actually contains:

- a compact walkthrough for a classical compression packer workflow:
  - find `OEP`
  - dump memory
  - repair the file
- several public `OEP` heuristics:
  - stack-balance reasoning
  - binary-pattern recognition after code has been restored in memory
  - first imported API patterns associated with known compiler families
  - differences in import-call opcode style across compiler ecosystems
- the page presents `ASPack` as a relatively classical shell where the main task is recovering the restored original image rather than reasoning about a custom VM

Safe takeaway:

- `ASPack` is a good example of the classical-shell branch of the skill
- `OEP` discovery can often be triangulated using multiple weak signals:
  - stack restoration behavior
  - compiler-startup idioms
  - first imported API shape
  - known code-pattern matches after the sample has unpacked in memory
- for this packer class, dump and repair reasoning is usually more relevant than virtualization modeling

Do not carry forward:

- the post's exact byte signatures, breakpoint sequences, or direct manual unpacking steps

### ASProtect2.56脱壳分析及实例

Link: https://bbs.kanxue.com/thread-286248.htm

What the page actually contains:

- a broad analysis of `ASProtect 2.56`, presented as one of the classic strong protectors
- the page explicitly identifies two recurring features:
  - `stolen code`
  - import-table encryption or destruction
- it describes multiple import-resolution patterns:
  - replacing normal imports with jump stubs or resolver stubs
  - dynamically resolving APIs via loader functions
  - storing resolved addresses in shell-managed memory rather than preserving a clean original import layout
- it also discusses several surrounding protection layers:
  - resource handling
  - debugger checks
  - memory and file integrity verification
  - higher-grade import protection
  - registration or trial-flow logic
- the page's later sections argue that, when tooling is weak or shell-specific repair is expensive, direct packed-state analysis plus memory modification or API hooking can be a viable research strategy

Safe takeaway:

- `ASProtect` is not just a classical compression shell; it often combines `stolen code`, damaged imports, and integrity logic
- import recovery may require reasoning about resolver behavior and shell-managed memory rather than assuming one intact `IAT`
- file integrity checks can make on-disk patch assumptions unreliable, so runtime evidence should be separated from disk-restoration goals
- some requests are better answered as lawful packed-state analysis or behavior study rather than "full unpack and rebuild"

Do not carry forward:

- the page's direct bypass instructions for registration, trial, or other software-lock logic
- concrete patch points, hook payloads, or operational recipes that would enable cracking third-party protected software

### StudyPE+ 2.0 beta 4 工具帖

Link: https://bbs.kanxue.com/thread-289433.htm

What the page actually contains:

- a tool announcement for `StudyPE+`, a PE inspection and analysis utility rather than a shell-specific tutorial
- the relevant capabilities for this skill are:
  - integrated `DIE`-style packer detection
  - PE header and directory inspection
  - section operations and alignment review
  - TLS, exception, relocation, Rich Header, and .NET metadata parsing
  - import/export/resource inspection
  - RVA/FOA/VA conversion
  - string, pattern, and disassembly-oriented search
  - process-module, memory-region, and dump-related support

Safe takeaway:

- this is useful as a "pre-unpacking observation surface" rather than as an unpacker
- before assuming a shell class, it helps to inspect:
  - architecture and runtime model
  - section layout and anomalies
  - directory presence or destruction
  - TLS callbacks
  - relocation and exception metadata
  - whether the sample looks native, .NET, ARM-family, or mixed
- integrated detector labels are helpful hints, but they should be corroborated with actual PE structure and runtime evidence

Best use:

- strengthen the skill's first-pass classification workflow before discussing `OEP`, dumping, or import repair

### 《加密与解密（第4版）》目录摘录

Link: https://bbs.kanxue.com/thread-230052.htm

What the page actually contains:

- a table of contents showing a coherent progression:
  - shell loading process
  - finding `OEP`
  - dumping memory images
  - rebuilding the import table
  - DLL-specific unpacking issues
  - anti-dump and virtualization topics
  - `VMProtect` reverse and restoration chapters

Safe takeaway:

- this is useful as a curriculum map for structuring the skill
- it reinforces that classical unpacking and virtualization analysis are separate branches and should not be collapsed into one workflow

### VMProtect3.5.1脱壳临床指南

Link: https://bbs.kanxue.com/thread-286780.htm

What the page actually contains:

- a detailed study of `VMProtect 3.5.1` based on leaked source availability for that version
- a modeling approach that treats the VM as a stack-frame-based virtual execution system
- the author explicitly tracks a VM stack region, register-to-slot mappings, and expression evolution
- the post emphasizes that one pass is often not enough; it uses a first pass for information collection and a second pass for cleanup, disambiguation, and better reconstruction
- it discusses high-level problems such as branch handling, loop recovery, virtual-register elimination, and ambiguous instruction forms

Safe takeaway:

- advanced virtualization cases may require staged analysis rather than one-shot dumping
- a useful mental model is to separate:
  - VM state capture
  - expression normalization
  - branch or loop reconciliation
  - second-pass cleanup of earlier ambiguities
- even when exact restoration is out of scope, this model helps explain why `VMProtect` cases resist classic OEP-centric thinking

Do not carry forward:

- concrete pattern strings
- exact addresses
- direct reconstruction algorithms
- any operational recipe that materially enables devirtualization of third-party protected programs

### Windows逆向与安全分析：从入门到专家的体系化学习指南

Link: https://bbs.kanxue.com/thread-289872.htm

What the page actually contains:

- a broad learning roadmap for Windows reverse engineering and security analysis
- repeated emphasis on PE structure, debugger fluency, analysis-note discipline, and isolated malware-lab practice
- practical project suggestions such as PE inspection tooling, basic behavior analysis, and structured experiment environments
- explicit reminders about legality, isolation, and responsibility

Safe takeaway:

- this is not a shell-specific source, but it is useful for the skill's lab and workflow framing
- it supports turning the skill into a repeatable research process instead of a collection of one-off tricks

Best use:

- justify prerequisites for users who jump directly to `VMP` or `脱壳` questions without having PE, debugger, and lab basics in place

### 细说软件保护：从应用保护到算法保护

Link: https://bbs.kanxue.com/thread-284629.htm

What the page actually contains:

- a protection taxonomy that separates:
  - application protection
  - code protection
  - algorithm protection
- an application-protection branch that includes compression shells, encryption shells, extraction shells, protection shells, and virtualization-style protection
- an explanation that hidden or fake `OEP` is one of the classic goals of application shells
- a code-protection branch covering static obfuscation, dynamic obfuscation, control-flow manipulation, `SMC`, `VM`, and `VMP`
- a distinction between standard or official VM execution and custom instruction-set interpreters, which the author uses to separate `VM` from `VMP`

Safe takeaway:

- this page is strong for taxonomy and conceptual positioning
- it helps explain where `VMP` sits relative to ordinary packers, static obfuscation, and self-modifying code
- it also reinforces that runtime and loader understanding matter as much as disassembly in unpacking-analysis tasks

Do not carry forward:

- broad "simulate the shell logic" language as if it were a generic recipe for direct bypass

### [讨论]die0.64 查壳扫描算法的分析 （输入表判断，讨论）

Link: https://bbs.kanxue.com/thread-227097.htm

What the page actually contains:

- a discussion by a user who inspected how `DIE 0.64` identifies at least one classical packer case
- the post contrasts detector behavior after modifying different visible features:
  - entrypoint bytes
  - section names
  - import descriptors
- the author's conclusion is that the tool's final label is not necessarily tied to the obvious surface feature a beginner might expect
- the page also mentions import-table and compiler-library clues as part of shell-identification logic

Safe takeaway:

- packer-detector output should be treated as a heuristic label, not proof
- changing or preserving one superficial feature such as section name or entrypoint bytes does not tell you which internal heuristic actually triggered the detector
- import-table shape, runtime-library fingerprints, and embedded constants may all influence detector results
- if a detector says `ASPack` or another shell family, corroborate that with PE structure and runtime evidence before committing to an analysis path

Do not carry forward:

- the post's concrete reverse-engineering details about the detector's internal comparison logic as if they were a universal shell-recognition algorithm

### 从“.tls段消失”探秘 Windows TLS 底层实现

Link: https://bbs.kanxue.com/thread-290394.htm

What the page actually contains:

- a PE-structure article centered on `TLS`, `IMAGE_TLS_DIRECTORY`, callback arrays, and why a Release build may have no visible `.tls` section while still using TLS correctly
- a comparison showing that the TLS directory remains present even when the linker merges TLS template data into `.rdata`
- an explanation of the key TLS directory fields:
  - `StartAddressOfRawData`
  - `EndAddressOfRawData`
  - `AddressOfIndex`
  - `AddressOfCallBacks`
- a reverse-engineering reminder that callback code may execute before normal program startup and should be treated as part of early control flow

Safe takeaway:

- do not infer "no TLS" from the absence of a `.tls` section name
- for first-pass classification, prefer PE-directory evidence over section-label assumptions
- `TLS` callback presence is a real startup signal and may explain behavior that occurs before the apparent entrypoint
- locating TLS data and callbacks should be based on `IMAGE_TLS_DIRECTORY` fields, not on whether the linker kept a dedicated `.tls` section

Do not carry forward:

- the page's concrete debugger breakpoint suggestion as a default workflow recipe

### [讨论][求助]超级巡警脱壳机与UPX脱壳机脱壳后的烦恼。

Link: https://bbs.kanxue.com/thread-277152.htm

What the page actually contains:

- a short discussion where the poster compares outputs from different automatic unpacking tools against a sample identified as `UPX`
- the observed results differ in size, residual section content, and downstream antivirus behavior even though the poster believes the files were "unpacked"
- the single reply argues that, for this classical packer family, the native unpacker is the more faithful restoration route

Safe takeaway:

- for classical packers, tool choice matters because different "unpacked" outputs may preserve different amounts of loader residue
- a changed file size or lingering shell-specific section content can be evidence that the artifact is not the cleanest restoration of the original file
- detector output, entrypoint appearance, and antivirus verdicts do not by themselves prove that an artifact has been correctly restored

Do not carry forward:

- the reply's command-line advice as if it generalized to stronger protectors beyond the specific classical-packer context

### 壳小白关于压缩壳的学习心得及基础实战练习

Link: https://bbs.kanxue.com/thread-270918.htm

What the page actually contains:

- a beginner-oriented writeup that distinguishes compression shells from stronger protection-oriented shells before moving into an exercise
- a conceptual statement that compression shells aim to reduce PE size, while stronger protection shells aim to resist analysis, debugging, dumping, or reverse engineering
- a static-observation discussion around packed PE sections, including:
  - section names
  - the relationship between `VirtualSize` and `SizeOfRawData`
  - the idea of a placeholder or expansion section that is small on disk but larger in memory
- a later practical section with manual `OEP` search and dump steps

Safe takeaway:

- this page is useful for first-pass classification, not for the later manual workflow
- a useful early split is:
  - compression-oriented shell
  - analysis-resistant or protection-oriented shell
- one classical compression-shell signal is a section layout where on-disk data is much smaller than the in-memory footprint needed after restoration
- `VirtualSize` versus `SizeOfRawData` is a useful static clue, but it should be combined with import shape, directories, and runtime evidence rather than treated as proof by itself

Do not carry forward:

- the article's step-by-step `OEP` search, debugger actions, or dump workflow

### 代码混淆之我见（一）

Link: https://bbs.kanxue.com/thread-247128.htm

What the page actually contains:

- a concept-heavy article on code obfuscation rather than a classical PE compression-shell workflow
- an explicit split between:
  - data-flow obfuscation
  - control-flow obfuscation
- examples of how equivalent instruction patterns and unnatural stack or arithmetic forms can be used to break normal reading habits
- a discussion that compares flow-graph flattening with VM-like protection at a high level, emphasizing that both transform control flow rather than simply restoring original code from a compressed image
- repeated emphasis that some protections are about distorting program semantics and control structure, not about shrinking PE size

Safe takeaway:

- not every hard sample is best modeled as a "packed shell" problem
- if PE layout looks relatively normal but code shape is filled with equivalent substitutions, fake blocks, flattened dispatch flow, or VM-like dispatch structure, classify the case closer to obfuscation or virtualization than classical compression packing
- control-flow distortion and VM-style protection can defeat simple `OEP -> dump -> repair` thinking even when there is no obvious compressed section story
- a weird disassembly with stable PE structure can be a sign to shift from dump-centric reasoning toward control-flow and data-flow modeling

Do not carry forward:

- the article's implementation-oriented discussion of building obfuscators or using pattern replacement as an operational deobfuscation recipe

## Practical Selection Guide

- If the user asks why a classic packed sample still will not run after dumping, read the `article-8698` and `article-12841` notes together.
- If the user asks whether a dumped PE only needs section repair or also needs import reconstruction, read the `thread-274505` note together with `article-8698`.
- If the user asks whether static signature matching is enough to "repair IAT", read the `thread-289563` note together with `thread-274505`.
- If the user asks whether a detector label is trustworthy on its own, read the `thread-227097` note together with the `thread-289433` note.
- If the user asks about a classical compression shell such as `ASPack`, start with the `thread-271040` note and then combine it with `article-8698`.
- If the user asks how to distinguish a compression shell from a stronger protection shell before any runtime work, read the `thread-270918` note together with `thread-284629`.
- If the user asks whether a sample is really packed or instead obfuscated/flattened/VM-like, read the `thread-247128` note together with `thread-284629`.
- If the user asks whether the absence of a `.tls` section means there are no TLS callbacks, read the `thread-290394` note.
- If the user asks about `ASProtect`, read the `thread-286248` note first, then combine it with `article-12841` and `thread-274505` when imports or damaged artifacts are central.
- If the user asks how to do first-pass shell classification safely, use the `thread-289433` note together with the skill's static triage path.
- If the user asks why one automatic unpacker output looks "cleaner" than another for a classical packer, read the `thread-277152` note as a boundary case rather than as a general unpacking recipe.
- If the user asks why a protector behaves like a shell plus an exception machine, read the `thread-284527` note.
- If the user asks about `Enigma`, read the `thread-268825` note first to decide whether the hard part is `OEP`, anti-debug noise, or import-behavior classification.
- If the user asks what makes `VMProtect` cases feel different from `UPX`-style cases, combine the `VMProtect3.31` note with the CSDN `VMProtect` concept notes.
- If the user asks how to think about `VMProtect 3.x`, combine the `VMProtect3.5.1脱壳临床指南` note with the CSDN `VMProtect` concept notes.
- If the user needs a training roadmap rather than a one-off answer, use the book table-of-contents note to structure the response.
