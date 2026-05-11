# GB/T 9704-2012 Formatting Reference

Use this as the baseline for mainland China党政机关公文 formatting. Apply the user's agency template first when it differs by local rule.

## Page Setup

- Paper: A4, 210 mm x 297 mm.
- Margins: top 37 mm, bottom 35 mm, left/binding side 28 mm, right/cutting side 26 mm.
- Type area: about 156 mm x 225 mm.
- Grid: normally 22 lines per page and 28 Chinese characters per line.
- Printing: normally double-sided for formal issuance; bind on the left.
- Text color: black unless the standard or template specifies otherwise.
- Default font: 3号仿宋体 for most elements unless a specific element requires another font.

DOCX notes:
- Prefer Chinese fonts available on the machine: `FangSong`/`仿宋`, `SimSun`/`宋体`, `SimHei`/`黑体`, `KaiTi`/`楷体`.
- `小标宋体` is often not installed by default. If absent, use the user's supplied template or a close fallback and disclose the fallback.
- Set both East Asian and ASCII font properties when creating DOCX; otherwise Word may silently substitute fonts.

## Element Zones

Public official documents are commonly divided into:

- 版头: 份号, 密级和保密期限, 紧急程度, 发文机关标志, 发文字号, 签发人, 版头分隔线.
- 主体: 标题, 主送机关, 正文, 附件说明, 发文机关署名, 成文日期, 印章, 附注, 附件.
- 版记: 抄送机关, 印发机关, 印发日期, 版记分隔线.

## Red Header and Front Matter

- 发文机关标志: use the issuing organ's full name or standardized abbreviation, often plus "文件"; center it. Recommended font is red小标宋体. Joint issuance may list multiple organs.
- 份号: top-left within the版心, generally 6-digit Arabic numerals when required.
- 密级和保密期限: use items such as `秘密★1年`; do not invent secrecy classifications.
- 紧急程度: use approved urgency labels such as `特急` or `加急` when needed.
- 发文字号: format as `机关代字〔年份〕号`, for example `国办发〔2026〕1号`. Use six-angle brackets `〔〕`; do not use `[]` or `【】`; do not zero-pad the sequence number.
- 上行文 requires签发人. Put发文字号 left and签发人 right on the same line; use 3号仿宋 for `签发人` and 3号楷体 for the name.

## Title, Recipient, Body

- Title: normally `发文机关名称 + 事由 + 文种`; use 2号小标宋体 and center. Avoid punctuation unless laws, regulations, book titles, or special names require it.
- Title line breaking: keep semantic units together; avoid splitting names,文种, or fixed phrases awkwardly.
- 主送机关: place below the title, left aligned/top grid. End with a full-width colon.
- Body: place below主送机关. Each natural paragraph starts with two Chinese-character indents; wrapped lines return to the left margin.
- Body hierarchy: use `一、`, `（一）`, `1.`, `（1）`. Usually first level uses黑体, second level uses楷体, lower levels use仿宋.
- Avoid mixing Chinese and Western punctuation styles. Use Chinese full-width punctuation for Chinese prose unless numbers, formulas, URLs, or codes require otherwise.

## Attachments

- Attachment note in body: after the body, leave one blank line and write `附件：` with two-character indent.
- Multiple attachments: number as `1. 附件名称`; align wrapped lines under the attachment name, not under `附件：`.
- Do not add punctuation after an attachment title in the attachment note.
- Attachment body: on a new page or designated place before版记. Mark the first line with `附件` or `附件1` in 3号黑体; the attachment title normally follows centered below.
- Attachment numbering in正文 and actual附件 headings must match exactly.

## Signature, Date, Seal

- 成文日期 uses Arabic numerals with full year, month, and day, for example `2026年5月11日`; do not write `二〇二六年五月十一日`; do not zero-pad month/day.
- For a single issuing organ, place the issuing organ署名 above the date; keep both toward the right according to the document template.
- For sealed documents, the seal should be centered, upright, and press over the issuing-organ name and date without obscuring the text.
- If the remaining blank area cannot contain the seal/signature block, adjust line spacing or character spacing; do not put "此页无正文" merely to force layout unless the agency template requires it.
- 附注: place below成文日期, left indent two characters, enclosed in parentheses, commonly for disclosure scope or contact notes.

## Page Numbers and Back Matter

- Page numbers: use half-width Arabic numerals, usually 4号宋体, placed below the type area. Single pages are usually on the right; double pages on the left. Use the standard's dash marks around the number if the template requires it.
- 版记: place at the bottom of the final page. Use separator lines and 4号仿宋 for抄送机关,印发机关,印发日期.
- 抄送机关: list only necessary receiving units. Avoid copying units that should not receive请示 or confidential content.
- 印发机关 and印发日期: use the office responsible for printing/issuing and the actual print/issue date.

## Tables

- Use tables only when they improve clarity or are required by the agency template.
- For A4横排表格, keep page numbers consistent with the rest of the document. In formal printing, orient the table so odd-page headers face the binding side and even-page headers face the cutting side.
- Table text may use smaller字号 if necessary, but keep readability and official style. Keep units, dates, and serial numbers consistent.
- Repeat header rows across pages for long tables. Avoid splitting a row if it harms readability.

## Review Checklist

- Page setup matches A4 and margin/grid requirements.
- Fonts are Chinese official-document fonts, not generic UI fonts.
- Title includes the correct发文机关,事由,文种.
- 文种 matches行文关系 and intent.
- 发文字号 uses `〔〕` and no zero-padded serial number.
- 上行文 has签发人.
- 主送机关 and抄送机关 are appropriate.
- 正文层次序号 are ordered and styled consistently.
- 附件说明 and actual attachments match.
- 成文日期 uses Arabic numerals.
- Seal/signature block fits on the page.
- 页码,版记, and横排表格 orientation are correct.

## Baseline Sources

- `GB/T 9704-2012《党政机关公文格式》`, accessible public copies such as https://dzb.cumtb.edu.cn/info/1040/1184.htm and https://yb.jsut.edu.cn/2024/0610/c7386a181105/page.htm
- `《党政机关公文处理工作条例》`, 中国政府网: https://www.gov.cn/zwgk/2013-02/22/content_2337704.htm
