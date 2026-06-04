---
name: china-official-documents
description: Draft, revise, format, and review mainland China official documents and related Word/DOCX tables under GB/T 9704-2012 and the Party and Government Organs Official Document Handling Regulation. Use for Chinese mainland公文 tasks such as 通知、请示、报告、函、批复、纪要、公告、通报、意见, red-head document layout, Word/DOCX formatting, attachments, seals/signature blocks, page setup, official-document tables, and compliance checklists.
---

# China Official Documents

## Core Rule

Use this skill for mainland China official-document drafting, revision, and formatting. Treat `GB/T 9704-2012《党政机关公文格式》` and `《党政机关公文处理工作条例》` as the baseline, then follow the user's agency, province, industry, or office template when it is provided.

Do not present a generated document as legally issued, approved, stamped, or filed. When content may affect rights, obligations, discipline, procurement, personnel, finance, secrecy, or administrative legality, flag that the drafting output needs responsible-office review.

## Workflow

1. Classify the document.
   - Read `references/document-types.md` when choosing between 通知、请示、报告、函、批复、纪要 and other statutory document types.
   - Check行文关系: 上行文、下行文、平行文、内部流转, and avoid using a文种 that conflicts with the requested action.

2. Gather missing facts before drafting when they are material.
   - Required facts usually include发文机关, 主送机关, 事由, 依据, 事项/措施, 时间地点, 办理要求, 联系方式, 附件, 成文日期, and whether the document is上行文 or联合行文.
   - If facts are unavailable, draft with visible placeholders such as `〔发文字号〕`, `（单位名称）`, and `XXXX年X月X日`.

3. Draft in official style.
   - Use accurate, concise, directive Chinese. Prefer "请", "现将", "经研究", "为", "根据", "决定", "请予", "妥否，请批示" only where the文种 supports them.
   - Read `references/writing-patterns.md` for title formulas, body structures, endings, common pitfalls, and reusable skeletons.

4. Format the document.
   - Read `references/format-standard.md` for A4 page setup, fonts,字号,版头,主体,版记,page numbers,附件, seal/date blocks, and横排表格.
   - For DOCX output, use the existing document tooling available in the environment, set page geometry explicitly, then render or inspect the resulting file when possible.

5. Validate before delivery.
   - Verify文种, title,主送机关,正文层次,附件说明,署名日期,页码,版记, and table orientation.
   - Check that请示 is one文一事, does not copy to lower-level units, and ends with a request for approval/instruction; check that报告 does not ask for approval.
   - Mention any unresolved placeholders or assumptions in the final response.

## References

- `references/format-standard.md`: GB/T 9704-2012 layout parameters and Word/DOCX formatting checklist.
- `references/document-types.md`: statutory公文 types, use cases,行文方向, and selection guidance.
- `references/writing-patterns.md`: drafting patterns, title/body formulas, and reusable outlines.

## Source Hygiene

Use current official or authoritative sources when the user asks for legal effect, institutional process, or "latest" requirements. Baseline sources used in this skill:

- `《党政机关公文处理工作条例》`, 中国政府网: https://www.gov.cn/zwgk/2013-02/22/content_2337704.htm
- Public copies of `GB/T 9704-2012《党政机关公文格式》`; verify against the user's official standard copy or local template when strict compliance is required.
