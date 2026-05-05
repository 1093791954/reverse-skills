---
name: packed-sample-analysis
description: Analyze packed or virtualized Windows samples in a lawful research context. Use when the task involves shell identification, PE triage, UPX or PEiD basics, suspicious sample runtime observation, VMP or VMProtect or Themida protection-model explanation, OEP candidate validation, memory-artifact consistency checks, IAT or section repair reasoning, or turning forum notes into a safe unpacking-analysis workflow without providing commercial-protector bypass steps.
---

# Packed Sample Analysis

Use this skill to turn validated forum material into a repeatable workflow for analyzing packed or virtualized Windows binaries. The focus is defensive reverse engineering, malware analysis, incident response, and research on self-owned or explicitly authorized samples.

## Safety Boundary

- Do not provide step-by-step instructions to crack commercial software, bypass licensing, defeat DRM, or produce a working VMProtect or Themida unpacker for unauthorized targets.
- For `VMP`, `VMProtect`, `Themida`, and similar requests, stay at the level of protection-model explanation, triage strategy, observation points, artifact validation, and lawful lab analysis.
- If the user asks for a direct bypass or working devirtualization path against a third-party binary, refuse that portion and continue with safe help such as packer identification, lab setup, reporting, or malware-analysis framing.

## Workflow

1. Classify the sample first: simple compression packer, runtime decryptor, staged loader, or virtualization-based protector.
2. Read only the matching section in [references/csdn-notes.md](references/csdn-notes.md).
3. Read [references/kanxue-notes.md](references/kanxue-notes.md) when the task benefits from public Kanxue discussions or book-style summaries around `OEP`, stack-balance heuristics, dump validation, or IAT reconstruction edge cases.
4. Read [references/gitcode-notes.md](references/gitcode-notes.md) when the task benefits from GitCode-hosted project writeups around `VMProtect`, custom PE packers, `DIE`, or anti-debug compatibility notes.
5. Build a static triage picture before running the sample:
   - file type and architecture
   - section layout and entropy anomalies
   - import-table shape
   - TLS callbacks or suspicious startup behavior
   - compiler or runtime fingerprints when available
   - relocation, exception, resource, and load-config signals when present
   - whether directory-level evidence contradicts section-name or detector-label assumptions
6. Move to isolated runtime observation only after the static picture is clear.
7. Treat the runtime phase as evidence collection, not as blind unpacking:
   - note module loads, new executable memory, and process-tree changes
   - look for transitions from stub behavior to stable program logic
   - preserve candidate memory artifacts and compare them against the on-disk image
8. Validate any candidate unpacked artifact before deeper reversing:
   - does the code layout look consistent
   - does the import-table story make sense
   - do section boundaries and entrypoint expectations align
   - are there signs that the dump is still half-initialized or integrity-bound
9. Write the result as a short analysis memo: what protector class it resembles, what evidence supports that judgment, what was recovered, what remains protected, and what next lawful analysis step is justified.

## Source Quality Rules

- Prefer claims that were confirmed by opening the article page, not just by search-result snippets or titles.
- If a source contains both sound concepts and direct bypass procedure, keep the concepts and omit the bypass procedure.
- Treat article-specific addresses, hardcoded breakpoints, and debugger scripts as non-transferable unless the task is a lawful analysis of the user's own sample and the guidance remains safety-compliant.

## Request Map

- Read `Concept and taxonomy` when the user needs a clean distinction between compression packers, encrypting loaders, and virtualization protectors.
- Read `VMP and VMProtect` when the user asks about `VMP`, `VMProtect`, register rotation, bytecode handlers, stack VMs, or why virtualized code is different from classic OEP-based unpacking.
- Read `Basic PE triage` when the task starts with a normal PE sample and the user needs a safe first-pass workflow.
- Read `Dump validation` when the user already has a memory artifact and needs to reason about sections, imports, `INT/IAT` state, and whether the dump is actually analyzable or runnable.
- Read `Malware-analysis angle` when the request is about suspicious binaries, incident response, or defensive unpacking in a sandbox.
- Read `Kanxue OEP and IAT notes` when the task is specifically about classical `OEP`-finding heuristics, stack-balance reasoning, `IAT` size detection, or why a dump still fails after nominal repair.
- Read `Kanxue OEP and IAT notes` when the task involves classical shells such as `ASPack`, or when compiler-startup fingerprints and stack-balance heuristics are likely stronger than anti-VM reasoning.
- Read `Kanxue OEP and IAT notes` when the task involves `Enigma` or `Armadillo` and you need to distinguish between import encryption, anti-debug noise, exception-driven control flow, and dual-process behavior before discussing repair.
- Read `Kanxue OEP and IAT notes` when the task involves `ASProtect`, especially if the sample shows stolen code, destroyed imports, resolver stubs, or integrity-sensitive behavior.
- Read `Kanxue VMP model notes` when the task is specifically about why `VMProtect 3.x` style samples require staged reasoning such as VM-state modeling, first-pass collection, and second-pass cleanup.
- Read `GitCode project notes` when the task benefits from project-centered framing for `VMProtect`, custom PE packers, `DIE`, or layered anti-debug observation surfaces.

## Analysis Paths

### Basic PE Triage Path

Use this when the user starts with an unknown executable and needs a first-pass assessment.

1. Confirm architecture, subsystem, and high-level PE health.
2. Inspect section names, sizes, permissions, and entropy for packer-like patterns.
3. Inspect imports for unusually small startup stubs, late-loading behavior, or intentionally sparse APIs.
4. Inspect supporting PE evidence before naming a shell family:
   - TLS callbacks
   - relocation and exception directories
   - resource shape
   - whether the sample is native, .NET, or another runtime
5. Resolve common false assumptions before trusting a classifier:
   - a detector label such as `ASPack` or `UPX` is only a hint until PE structure and runtime behavior agree
   - absence of a `.tls` section name does not prove absence of TLS data or callbacks
   - unusual section names alone do not prove which heuristic caused a tool to classify the sample
6. Use section geometry as a clue, not a verdict:
   - compression-oriented shells often leave a strong mismatch between `VirtualSize` and `SizeOfRawData`
   - a small-on-disk but larger-in-memory placeholder section can support a compression-shell hypothesis
   - these signs still need to be reconciled with imports, directories, and runtime behavior
7. Record whether the sample looks closer to `UPX`-style compression, a custom loader, an integrity-heavy protector, or a virtualization product.
8. If PE structure looks comparatively normal but the disassembly looks unnaturally distorted, consider a different branch:
   - repeated equivalent instruction substitutions
   - fake or dead basic blocks
   - flattened dispatch-style control flow
   - VM-like handler dispatch without a strong compression-shell section story
   These signs suggest obfuscation or virtualization rather than a simple compressed PE.
9. When the case is still classical rather than virtualized, you can reuse the public Kanxue-style heuristics:
   - cross-section transfer back into a normal code section
   - stack-balance clues around `pushad/popad` style loaders
   - compiler-family startup fingerprints such as early imported API patterns
10. If `TLS` is suspected, parse the TLS directory rather than relying on section names:
   - locate `StartAddressOfRawData` / `EndAddressOfRawData`
   - locate `AddressOfCallBacks`
   - determine which section actually holds the TLS template and callback array
11. If the case resembles a stronger non-VM protector such as `Enigma` or `Armadillo`, classify the extra burden before going deeper:
   - mostly import encryption
   - anti-debug noise
   - exception-driven code restoration
   - parent-child or dual-process execution
12. If the case resembles `ASProtect`, classify whether the main problem is:
   - stolen code
   - resolver-based import reconstruction
   - file or memory integrity coupling
   - safer packed-state analysis instead of full artifact restoration

The goal of this phase is classification, not extraction.

### Runtime Observation Path

Use this when static evidence suggests packing or staged decryption.

1. Run only in an isolated lab with snapshots.
2. Observe when the sample changes from loader behavior into stable application or payload logic.
3. Record memory regions, loaded modules, and integrity checks that may explain why a raw dump would fail.
4. Preserve artifacts and notes so later analysis can explain what was captured and at which phase.

Avoid giving rote breakpoint recipes. The useful output is the transition model, not a debugger keystroke list.

### VMP and Virtualization Path

Use this when the sample appears protected by `VMP`, `VMProtect`, `Themida`, or another virtualization-oriented protector.

1. Start from the conceptual distinction: virtualized code is not just compressed and restored; parts of the original logic may be translated into a custom instruction set and interpreted by a VM-like dispatcher.
2. Explain why classic `find OEP -> dump -> repair imports` reasoning is often incomplete for virtualized regions.
3. Focus on identifying:
   - where native code hands off to a VM dispatcher
   - what parts remain native versus virtualized
   - whether the user's real goal is algorithm understanding, malware triage, or simple packer classification
4. If the user only needs to understand behavior, guide them toward surrounding native scaffolding, data flow, and observable side effects instead of promising full devirtualization.
5. Reuse only the validated conceptual points from the CSDN notes:
   - `VMProtect` differs from classic shells by translating protected code into VM-level pseudo-instructions
   - bytecode interpretation, stack-based operation, fake control flow, and rotating register mappings are common reasons the code looks meaningless in a normal disassembler
6. Reuse the public Kanxue OEP discussion only at a high level:
   - some `VMProtect` cases can still expose useful OEP-adjacent stack or environment differences
   - those observations are case-specific and should not be treated as a universal recipe
7. Reuse the public Kanxue `VMProtect 3.5.1` modeling discussion only at a high level:
   - treat VM-state tracking, expression reduction, branch reconciliation, and second-pass cleanup as separate reasoning phases
   - use that model to explain why a single dump or a single breakpoint story is often insufficient

### Dump Validation Path

Use this when the user already has a dumped memory image or recovered artifact.

1. Compare the dumped artifact against the runtime state it came from.
2. Check whether sections still reflect in-memory layout rather than a runnable disk layout.
3. Check whether imports, relocations, TLS behavior, and entrypoint assumptions were preserved or need reinterpretation.
4. Distinguish between:
   - a useful research artifact
   - a runnable restored executable
   - an incomplete memory snapshot
5. Check whether the apparent import recovery is structural or merely cosmetic:
   - static naming or signature recognition can help identify likely APIs
   - that does not by itself prove the import table is valid for loading or rerunning
6. Reuse the validated classic heuristics carefully:
   - OEP candidates are often identified by a transition from the shell region back into a normal code region
   - import-call shape such as direct call versus IAT-mediated call can help explain what the dump still needs
7. Reuse the public Kanxue repair notes when relevant:
   - `IAT` size can often be reasoned about from contiguous import-call references and terminating null regions
   - non-contiguous or tampered `IAT` layouts require artifact review instead of assuming one clean table
   - some malware samples intentionally poison `IAT` reconstruction with stolen or simulated API stubs
   - if `OriginalFirstThunk` is missing while `FirstThunk` reflects runtime-resolved addresses, section repair alone may not be enough
   - a file that disassembles cleanly after realignment may still contain runtime residue that breaks re-execution

Do not assume a dump that opens in a disassembler is actually correct.

## Output Style

- Prefer concise, evidence-led conclusions over tutorial narration.
- State uncertainty explicitly, especially for high-end protectors.
- When a user asks for `VMP脱壳`, translate that into one of three safer deliverables:
  - protection-model explanation
  - lawful sample-analysis workflow
  - artifact-validation checklist

## References

- Use [references/csdn-notes.md](references/csdn-notes.md) as the curated notebook built from the CSDN search results.
- Use [references/kanxue-notes.md](references/kanxue-notes.md) as the curated notebook built from validated public Kanxue pages.
- Use [references/gitcode-notes.md](references/gitcode-notes.md) as the curated notebook built from validated GitCode blog pages and project writeups.
- Load only the relevant section instead of the whole file when possible.
