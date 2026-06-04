---
name: vmp-unpack-analysis
description: Analyze legally authorized VMP or VMProtect protected Windows binaries, including protection classification, VMProtect/VMP protection-model reasoning, native-to-VM boundary mapping, OEP and unpack-artifact validation, VM dispatcher or handler model analysis, virtual stack/register state reasoning, devirtualization planning, and report writing. Use when the task mentions VMP, VMProtect, VMP保护, 过VMP, 脱VMP, 脱壳, OEP, IAT, VM handler, dispatcher, bytecode, virtualized code, or devirtualization for a self-owned or explicitly authorized sample.
---

# VMP Unpack Analysis

Use this skill to turn VMP/VMProtect forum notes, public documentation, and sample evidence into an authorized analysis workflow. The goal is to understand what protection is present, separate classical unpacking from virtualization work, validate recovered artifacts, and produce a defensible analysis record.

## Boundary

- Confirm the work is for a self-owned, commissioned, malware-analysis, incident-response, or explicitly authorized sample.
- Do not help bypass licensing, DRM, trial limits, game anti-cheat, payment checks, or third-party commercial protection without authorization.
- When authorization is present, keep outputs evidence-led: classify the protector, explain which parts are native versus virtualized, state what was recovered, and define validation criteria before claiming success.
- If the request jumps straight to "过VMP" or "脱壳", translate it into: target intake, static triage, runtime observation, VM model analysis, artifact validation, and reportable result.

## Workflow

1. Classify the request:
   - simple protector identification
   - classical unpacking/OEP and PE reconstruction
   - VMProtect virtualized-region analysis
   - devirtualization or algorithm recovery
   - recovered artifact validation
   - written report or handoff notes
2. Read [references/kanxue-notes.md](references/kanxue-notes.md) for public Kanxue material around VMProtect 3.31 OEP, VMProtect 3.5.1 VM-state modeling, VMProtect 3.8.1 changes, and PE reconstruction cautions.
3. Read [references/csdn-notes.md](references/csdn-notes.md) for compact VMP/VMProtect concepts: stack VM model, bytecode, handlers, dispatcher, SDK markers, mutation, virtualization, and performance tradeoffs.
4. Read [references/stackoverflow-notes.md](references/stackoverflow-notes.md) for general engineering and research framing around virtualizers, false positives, anti-debug complexity, stack-machine lifting, and why VM analysis is a multi-week project.
5. Build a static evidence packet before runtime work:
   - file type, architecture, subsystem, compiler/runtime hints
   - section layout, entropy, permissions, overlay, resources
   - imports, delayed imports, TLS, load config, exceptions, relocations
   - strings that suggest VMProtect SDK markers, service functions, licensing functions, or protector messages
   - whether the detector label agrees with PE structure and code shape
6. Decide whether the target is mostly:
   - packed/encrypted loader logic
   - mutation/obfuscation without full virtualization
   - virtualized function fragments
   - mixed native scaffolding plus VM bytecode interpreter
7. Only then plan runtime observation in an isolated lab:
   - capture process/module/memory-region changes
   - identify transitions from loader/protector code into stable program logic
   - preserve dumps and traces as evidence, not as proof of success
8. Validate recovered artifacts before deeper reversing:
   - sections reflect a coherent disk image, not only mapped memory
   - entrypoint and control-flow assumptions match observed execution
   - imports are structurally meaningful, not just cosmetically named
   - TLS, relocations, exceptions, resources, and load config are accounted for
   - the artifact can be explained even if it is not runnable
9. Write the result as an analysis memo:
   - protection class and version evidence
   - static and runtime facts
   - native/VM boundary map
   - recovered artifact status
   - remaining protected regions
   - next authorized analysis step

## Static Triage Path

Use this when the user provides an unknown executable, screenshots, tool labels, or PE metadata.

1. Treat detector names as hints only. Corroborate them with section geometry, imports, strings, and code shape.
2. Look for VMProtect-facing evidence:
   - VMProtect section names or loader regions
   - sparse or suspicious imports
   - service-function strings or SDK marker residue
   - "file corrupted", debugger, VM, CRC, serial, or activation-related signals
   - dense control-flow flattening, stack noise, opaque predicates, or VM-like dispatch
3. Separate "shell restored native code" from "function virtualized into bytecode":
   - classical shell work aims to recover a coherent native image
   - VMP virtualization work may require modeling a VM interpreter, not just finding an OEP
4. If the PE shape is mostly normal but selected functions disassemble as unnatural dispatcher/handler code, switch to the VM Model Path.
5. If the entry loader reconstructs code and imports before native execution, combine this path with Dump Validation.

## OEP and Dump Validation Path

Use this when the task asks for OEP, dump repair, IAT repair, or "脱壳后能不能用".

1. Define the goal first:
   - analyzable memory artifact
   - statically readable PE
   - runnable restored PE
   - algorithm understanding without full restoration
2. Compare the candidate OEP or recovered entry with runtime evidence:
   - stack/register context at transition
   - section containing the candidate code
   - surrounding compiler/runtime startup shape
   - consistency across repeated runs or builds
3. Treat IAT, INT, relocations, TLS, and section mapping as separate validation problems.
4. Do not assume "opens in IDA" means "successfully unpacked".
5. If virtualized regions remain, state that the dump is only a scaffold for analysis and not a full devirtualized restoration.

## VM Model Path

Use this when the protected logic appears translated into a custom instruction set.

1. Identify the native-to-VM boundary:
   - prologue/stub that enters the VM
   - virtual instruction pointer source
   - virtual stack or frame base
   - dispatcher or threaded-dispatch pattern
   - handler blocks or duplicated handler families
2. Track VM state at a conceptual level before trying to rebuild native code:
   - virtual instruction pointer
   - virtual stack pointer/frame pointer
   - virtual registers or register slots
   - rolling key or bytecode decode state when visible
   - flag/state propagation
   - memory reads and writes that escape the VM
3. Classify handlers by semantics:
   - data movement
   - arithmetic/logical operations
   - stack/frame movement
   - flag-producing operations
   - branch and conditional branch behavior
   - calls, returns, and native API bridges
4. Normalize expressions in stages:
   - remove junk and identity operations
   - fold constants
   - collapse register copies
   - simplify equivalent boolean/arithmetic forms
   - preserve uncertainty instead of forcing a fake native instruction
5. Expect second-pass work. VMProtect 3.x style analysis often needs one pass to collect mappings and another pass to resolve earlier ambiguities.
6. For VMProtect 3.8+ claims, assume old 3.5.1-source-derived assumptions are incomplete until verified against the specific sample.

## Devirtualization Planning Path

Use this when the user has authorization and wants to recover a protected algorithm.

1. Scope the smallest protected region that answers the business question.
2. Prefer behavior recovery over whole-program restoration when the target is heavily virtualized.
3. Pick an intermediate representation strategy:
   - human-readable handler notes for small functions
   - symbolic expressions for arithmetic-heavy functions
   - custom IR or LLVM-like lifting when handler coverage and control flow justify the cost
4. Track branch and loop handling explicitly. Incorrect branch reconciliation is a common source of convincing but wrong output.
5. Validate any lifted or reconstructed logic with input/output tests against the authorized original.
6. Record unsupported handlers, unresolved state, and sample-specific assumptions in the report.

## Report Template

Use this compact shape for handoff:

1. Authorization and target summary
2. Hashes, architecture, timestamp, and tool versions
3. Protection evidence and likely VMProtect/VMP version band
4. Static triage findings
5. Runtime observation findings
6. OEP/dump/artifact status
7. VM boundary and handler/state model
8. Recovered behavior or algorithm summary
9. Validation tests and failures
10. Remaining risks and next steps

## Troubleshooting

- If the sample crashes only under a debugger, separate anti-debug observation from VM handler analysis.
- If OEP looks plausible but the artifact fails to run, validate section layout, imports, TLS, relocations, and runtime-mutated data separately.
- If reconstructed code has extra moves or dead temporaries, check whether virtual-register mapping was learned too early.
- If branch output is wrong, revisit virtual flags, rolling-key state, and bytecode decode state before changing arithmetic handlers.
- If 3.5.1 notes do not match a newer target, switch to a version-difference hypothesis before assuming your analysis is wrong.
- If a function is too large to devirtualize economically, narrow to the protected business rule, input transform, or comparison path.

## Reference Use

- Use [references/kanxue-notes.md](references/kanxue-notes.md) for detailed forum-derived workflow notes and version-sensitive cautions.
- Use [references/csdn-notes.md](references/csdn-notes.md) for concept refreshers and vocabulary.
- Use [references/stackoverflow-notes.md](references/stackoverflow-notes.md) for general engineering tradeoffs and VM/lifting framing.
- Search references for `3.31`, `3.5.1`, `3.8.1`, `OEP`, `IAT`, `dispatcher`, `handler`, `virtual stack`, `register escape`, `second pass`, `LLVM`, or `false positive`.
