# Deliverables Builder

Before drafting or reviewing user-facing Chinese material, read `references/13-writing-style.md` and `references/06-document-rules.md`. Apply the writing guidance to all prose deliverables and run a language review before final export. This review checks factual support, clarity, redundancy, empty promotional language, unnecessary number-label headings, and misuse of slashes; preserve source code, technical identifiers, paths, URLs, quotations, and required terminology unchanged.

After facts are locked, create a clearly numbered package in the task output
directory. Use the profile as the sole identity source and cite feature graph
evidence while drafting.

1. `01-软件信息确认表.md`: confirmed facts and unresolved items, if any.
2. `02-软件说明书.docx` (and a reviewable PDF when the runtime supports it):
   select a user manual, API/design document, or CLI operation guide based on
   the product. Do not invent screenshots.
3. `03-源程序鉴别材料.pdf` and `.docx`: use the source selector, page builder,
   secret scanner, page validator, and renderer. Keep redaction reports.
4. `04-申请信息填写指引.md`: guidance only, never an imitation official form.
5. `05-功能证据清单.json`: evidence map and feature graph.
6. `06-敏感信息检查报告.json` and `07-最终材料检查报告.html`.

For DOCX/PDF generation, use the target Agent's document/PDF tooling and render
for visual review when available. If a renderer is unavailable, retain the
editable draft and state that visual QA remains pending.
