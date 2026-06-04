# Encrypted GName / FNamePool Notes

Source thread:

- Kanxue: `[原创] 记一次对某二次元开放世界GName加密算法分析`
- URL: `https://bbs.kanxue.com/thread-290494.htm`
- Author shown on page: `0xLuna`
- Visibility note: unauthenticated HTML exposes the title, first paragraphs, and four image URLs. The user supplied a long screenshot of the article body; treat the algorithm-level details below as distilled workflow and validation guidance, not as a verbatim source transcript.

## What This Thread Adds

This case is useful when a UE title still exposes an `FNamePool`-like structure, but the actual `Blocks` entries do not contain plain strings such as `None`.

The article's opening workflow is:

1. Open `XXX-Win64-Shipping.exe` in IDA.
2. Use string search / cross references to locate the suspected `GName` / `FNamePool`.
3. Normalize the candidate as an RVA first, then validate it against the module image base in CE.
4. Inspect the `FNamePool`-like shape in memory.
5. Jump into one `Blocks` element. If the first entry is not the expected plaintext `None`, treat the name entries as encrypted or transformed.
6. Pivot from storage validation to the code path that registers or inserts names. The visible page names `sub_3248EF0` and an indirect call resembling `qword_8613B48(v29, v31)` as suspicious points.

The transferable lesson is not the exact offsets. It is the pivot:

- locate the pool structurally
- prove the strings are transformed
- trace the engine/game code that writes or resolves name entries
- lift the small byte transform
- validate by decoding known UE name entries

## Recovery Workflow

Use this order for custom encrypted `GName` / `FNamePool` work.

1. Identify the engine generation and expected name layout.
   - UE4.23+ commonly uses `FNamePool` / `NamePoolData`.
   - Earlier UE4 writeups and tools may still call the target `GName`.
   - Do not assume an older `GNames` chunk-pointer layout if the binary matches a modern `FNamePool`.

2. Locate the candidate pool.
   - Search source-level anchors such as `NameTypes.h`, `UnrealNames.cpp`, `FNamePool`, `GetPlainNameString`, `GetDisplayNameEntry`, and `Resolve`.
   - Search binary strings such as `ByteProperty`, `FloatProperty`, `IntProperty`, `MulticastDelegateProperty`, or other early reflected type names.
   - Convert consistently between RVA, static IDA VA, and runtime ASLR module base.

3. Validate the structure before thinking about decryption.
   - Confirm allocator / pool fields and plausible `Blocks` pointers.
   - Follow a block pointer and inspect the first few entries.
   - In normal plaintext pools, the earliest names should quickly reveal `None` and reflected property names.
   - If the shape is right but text is unreadable, mark this as "encrypted entry data", not "bad GName", until proven otherwise.

4. Find the transform boundary.
   - Trace name registration / insertion code first because games often transform bytes before storing them.
   - Also trace read-side APIs (`GetDisplayNameEntry`, `GetPlainNameString`, `Resolve`) because some games decrypt only on lookup.
   - For indirect calls, resolve the runtime target by breaking at the call, recording the function pointer, and rebasing it back to IDA.
   - Capture arguments before and after the call. Look for one argument that points at source text or an entry buffer, and one that points at an output / destination entry.

5. Lift the primitive carefully.
   - Preserve exact integer widths: `uint8_t`, `uint16_t`, and `uint32_t` behavior matters.
   - Preserve rotate direction, shift counts, carry-free wraparound, and signedness.
   - Separate header handling from string-byte handling. Some targets transform only the character data; others also encode length / flags.
   - If the routine has multiple small byte loops, name them by effect: header decode, byte stream decode, key update, terminator handling.

6. Validate with known plaintext.
   - The first decoded entry should be `None` in a typical pool.
   - Nearby entries should include early UE reflected type names such as `ByteProperty`, `IntProperty`, `BoolProperty`, `FloatProperty`, `ObjectProperty`, or `NameProperty`.
   - Validate more than one entry. A transform that only makes the first name plausible is not enough.
   - Check ANSI and wide entries separately when the header indicates both modes exist.

7. Integrate into tooling only after validation.
   - Put decryption immediately before `FNameEntry` parsing if the stored entry bytes are encrypted.
   - Put decryption after resolving the entry pointer but before string construction if only the payload is encrypted.
   - Keep the normal UE layout parser separate from the game-specific decrypt primitive, so version fixes and crypto fixes do not contaminate each other.

## Diagnostic Signals

- `FNamePool` fields and `Blocks` pointers look plausible, but names are unreadable.
- The entry that should decode to `None` is transformed.
- IDA's string references still lead to name-registration code, but CE inspection shows encrypted storage.
- A small routine near registration performs byte-wise arithmetic, xor, rotate, or table-based changes.
- An indirect call in the registration path mutates a buffer whose input/output length matches a name entry.

## Common Failure Modes

- Mixing IDA's preferred image base with CE's runtime module base.
- Treating an encrypted pool as the wrong UE version and rewriting the layout parser too early.
- Decoding from `GName[Block]` with old chunk-array assumptions when the target is actually a modern `FNamePool`.
- Applying the byte transform to the wrong region by including allocator metadata or skipping the entry header incorrectly.
- Ignoring case-preserving / non-case-preserving build differences.
- Testing only ASCII names and then failing on wide names or localized names.
- Inlining the game-specific transform into generic `GetName`, making later titles harder to support.

## Practical Output Shape

When answering a user who brings an encrypted `GName` case, produce:

1. The suspected pool address and how it was normalized (`RVA`, IDA VA, runtime VA).
2. Evidence that the pool layout is structurally correct.
3. Evidence that entry data is transformed.
4. The write-side and read-side functions inspected.
5. The recovered transform as pseudocode or code, with integer widths.
6. A validation table of several `NameId -> decoded string` results.
7. The minimal integration point in the dumper / SDK generator.

