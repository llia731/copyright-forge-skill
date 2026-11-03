#!/usr/bin/env python3
"""Render a Graphviz DOT source as reviewable software diagrams."""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Render a DOT file into SVG, PNG or PDF")
    parser.add_argument("--dot", required=True, type=Path, help="Existing .dot source")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--formats", default="svg,png", help="Comma-separated: svg,png,pdf")
    parser.add_argument("--dpi", type=int, default=200)
    parser.add_argument("--name", help="Output basename (defaults to DOT filename stem)")
    args = parser.parse_args(argv)
    source = args.dot.resolve()
    if not source.is_file() or source.suffix.lower() != ".dot":
        parser.error("--dot must name an existing .dot file")
    name = args.name or source.stem
    if not name or name in (".", "..") or "/" in name or "\\" in name:
        parser.error("invalid output basename")
    formats = list(dict.fromkeys(part.strip().lower() for part in args.formats.split(",")))
    if not formats or any(fmt not in {"svg", "png", "pdf"} for fmt in formats):
        parser.error("--formats only supports svg,png,pdf")
    if not 72 <= args.dpi <= 600:
        parser.error("--dpi must be between 72 and 600")
    binary = shutil.which("dot")
    if binary is None:
        parser.error("Graphviz 'dot' is not installed or not on PATH")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for fmt in formats:
        dest = args.output_dir / f"{name}.{fmt}"
        cmd = [binary, f"-T{fmt}"]
        if fmt == "png":
            cmd.append(f"-Gdpi={args.dpi}")
        cmd.extend([str(source), "-o", str(dest)])
        try:
            process = subprocess.run(cmd, capture_output=True, text=True, timeout=60, check=False)
        except subprocess.TimeoutExpired:
            parser.error(f"Graphviz timed out rendering {fmt}")
        if process.returncode or not dest.is_file() or dest.stat().st_size == 0:
            parser.error(f"Graphviz failed to render {fmt}: {process.stderr.strip()}")
        records.append({"format": fmt, "file": dest.name, "sha256": sha256(dest)})
    manifest = {"dot": source.name, "dot_sha256": sha256(source), "rendered": records}
    (args.output_dir / f"{name}.diagram.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
