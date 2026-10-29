# Additional quality safeguards for Codex

This is a mandatory supplement to the original project's workflows.

1. The deterministic reviewer status READY is an intermediate software check, **not** evidence of legal sufficiency or successful registration.
2. Identify the selected Git branch and commit, software boundary, and first-party code provenance. Exclude vendored, generated, and unrelated software.
3. Require a source page plan for final review. Render final DOCX and PDF and verify their actual pages, clipping, truncation, typography, and full content; never rely on the JSON logical page count alone.
4. Run `scripts/audit_rendered_pdf.py` against the generated PDF and source text, supply the expected final page count, and treat missing text or page differences as blockers requiring correction. Perform manual visual review as well.
5. Check functional claims against actual source paths and program behavior. Regex evidence is only a candidate hint, not semantic proof. Screenshots must come from the running software.
6. Review secrets and personal information in final artifacts as well as intermediate files. Preserve the unmodified input repository.
7. Mark unknown ownership, date, release status, rights chain, and special deposit conditions for human confirmation. Never invent facts or official application forms.
8. If final artifact verification was not performed or failed, do not report the package as submission-ready, even when the original review script returns READY.
