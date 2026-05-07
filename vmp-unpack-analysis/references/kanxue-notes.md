# Kanxue Notes

This file records reusable points from public Kanxue pages. Use it for authorized VMProtect/VMP analysis planning and validation. Avoid treating article-specific breakpoints, addresses, patch offsets, or scripts as transferable recipes.

## VMProtect 3.31 OEP Journey

Link: https://bbs.kanxue.com/thread-251250.htm

What the page contains:

- A case study around locating an OEP under VMProtect 3.31.
- The author compares early runtime context against a later OEP-adjacent context.
- Stack and register state are used as evidence, especially where simple breakpoint strategies are unreliable.
- Anti-debug behavior and emulation differences affect whether an observation path works.

Safe takeaways:

- OEP discovery under VMProtect should be evidence-led, not based on one universal breakpoint.
- Environment comparison can expose OEP-adjacent state when direct break strategies fail.
- Stack-state observations are sample-specific and must be repeated and validated.
- A recovered entry does not imply virtualized protected functions have been devirtualized.

Use when:

- The user has an OEP candidate and needs validation criteria.
- A dump exists but the transition from protector code to native code is uncertain.
- The case looks like loader/unpack work before or beside virtualization work.

Do not carry forward:

- Exact debugger choreography.
- Concrete breakpoint placements.
- Patch instructions.

## VMProtect 3.5.1 Clinical Guide

Link: https://bbs.kanxue.com/thread-286780.htm

What the page contains:

- A VMProtect 3.5.1-focused study that benefits from leaked-source availability for that version.
- Discussion of staged analysis: a first pass gathers mapping and state information; a later pass cleans up ambiguity.
- Examples of virtual-register mapping problems, including "register escape" style issues where a virtual register may not map cleanly back to a real register.
- Notes around simplifying expressions, removing redundant operations, and folding register copies or constants.
- High-level handler-feature discussion for stack/frame movement, arithmetic/logical operations, and VM stack behavior.

Safe takeaways:

- Treat VMProtect 3.x analysis as VM-state modeling, not only PE dumping.
- Keep VM stack/frame, virtual registers, flags, and branch behavior separate while collecting evidence.
- Devirtualization is usually iterative. A first pass may overproduce temporaries or miss later mappings; a second pass can resolve some ambiguity.
- If reconstructed code contains extra moves or false temporaries, suspect incomplete virtual-register lifetime or mapping knowledge.
- Expression simplification should preserve uncertainty instead of forcing a false native instruction.

Use when:

- The task asks why a one-pass devirtualization output is noisy or wrong.
- The target has arithmetic, branches, or loops inside VM-protected functions.
- The user needs to plan a handler/IR recovery pipeline for an authorized sample.

Do not carry forward:

- Exact pattern strings.
- Full handler reconstruction recipes.
- Code blocks or operational steps that directly reproduce a devirtualizer.

## VMProtect 3.8.1 Change Notes

Links:

- https://bbs.kanxue.com/thread-290726.htm?style=1
- https://bbs.kanxue.com/thread-288666.htm

What the pages contain:

- Public discussion that VMProtect 3.8+ changed substantially after the 3.5.1 source leak era.
- Claims that newer versions add stronger obfuscation strategies and change VM workflow details.
- A separate thread focuses on the 3.8.1 virtual-machine process.

Safe takeaways:

- Do not assume 3.5.1-derived source knowledge directly solves 3.8+ samples.
- Version identification matters before choosing handler, dispatcher, or bytecode assumptions.
- Treat old handler signatures and mapping rules as hypotheses requiring sample-specific validation.
- For 3.8+ work, first build a fresh native-to-VM boundary map and handler taxonomy.

Use when:

- A target appears newer than 3.5.x.
- Known 3.5.x models fail unexpectedly.
- The user asks whether a leaked-source workflow should apply to a modern sample.

Do not carry forward:

- Course-promotion content.
- Any article-specific operational bypass sequence.

## PE Reconstruction and Import Repair Context

Useful companion Kanxue references already curated in the repository include:

- `packed-sample-analysis/references/kanxue-notes.md`
- `packed-sample-analysis/SKILL.md`

Reusable points:

- A mapped memory image and a runnable disk PE are different artifacts.
- IAT naming is not the same as import-table structural correctness.
- Section alignment, `SizeOfImage`, relocations, TLS, exception metadata, and runtime-mutated data can each break a restored file independently.
- Strong protectors may preserve enough native scaffolding for study while leaving selected functions virtualized.

Use when:

- The user asks why a dump opens in IDA but does not run.
- A candidate OEP exists but protected functions still look VM-like.
- The user needs to explain partial success in a report.

## Practical Selection Guide

- For OEP or dump questions, start with `VMProtect 3.31 OEP Journey`, then combine with PE reconstruction notes.
- For handler/state/devirtualization planning, start with `VMProtect 3.5.1 Clinical Guide`.
- For modern targets, read `VMProtect 3.8.1 Change Notes` before applying older assumptions.
- For reporting, separate:
  - what the public source says
  - what the target sample proves
  - what remains an inference
