#!/usr/bin/env python3
"""Check rendered PDF page count and extracted text; review visual layout separately."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

def audit(pdf: Path, source: Path, expected_pages: int) -> dict:
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("Install pymupdf: pip install pymupdf") from exc
    document = fitz.open(pdf)
    failures, warnings = [], []
    if len(document) != expected_pages:
        failures.append({"code": "PAGE_COUNT_MISMATCH", "expected": expected_pages, "actual": len(document)})
    rendered = [page.get_text("text") for page in document]
    originals = source.read_text(encoding="utf-8").split("\f")
    if len(originals) != len(rendered):
        failures.append({"code": "SOURCE_PAGE_MISMATCH"})
    for index, (raw, actual) in enumerate(zip(originals, rendered), 1):
        absent = [line.strip()[:80] for line in raw.splitlines()
                  if len(line.strip()) > 12 and line.strip() not in actual]
        if absent:
            warnings.append({"code": "TEXT_NOT_VERIFIED", "page": index,
                             "count": len(absent), "sample": absent[:5]})
    return {"status": "NEEDS_FIX" if failures or warnings else "READY_FOR_VISUAL_REVIEW",
            "failures": failures, "warnings": warnings, "pages": len(document)}

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("pdf", type=Path)
    p.add_argument("source_text", type=Path)
    p.add_argument("--expected-pages", type=int, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    result = audit(args.pdf, args.source_text, args.expected_pages)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    if result["status"] == "NEEDS_FIX":
        raise SystemExit(2)

if __name__ == "__main__":
    main()
