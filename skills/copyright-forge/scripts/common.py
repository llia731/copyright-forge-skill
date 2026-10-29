#!/usr/bin/env python3
"""Small standard-library helpers shared by Copyright Forge scripts."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

EXCLUDED_DIRS = {
    ".git", ".github", ".idea", ".vscode", "node_modules", "vendor", "dist",
    "build", "coverage", "target", ".next", ".nuxt", ".output", ".cache",
    "__pycache__", ".venv", "venv",
}
SOURCE_EXTENSIONS = {".go", ".java", ".py", ".js", ".jsx", ".ts", ".tsx", ".vue", ".cs", ".cpp", ".c", ".h", ".php", ".rb", ".rs", ".kt", ".sql"}
EXCLUDED_NAMES = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock", "go.sum", "cargo.lock"}


def iter_project_files(root: Path):
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_DIRS and not (Path(current) / d).is_symlink())
        for name in sorted(files):
            path = Path(current, name)
            if name in EXCLUDED_NAMES or name.endswith((".min.js", ".map", ".lock")) or path.is_symlink():
                continue
            yield path


def is_probably_text(path: Path) -> bool:
    try:
        return b"\0" not in path.read_bytes()[:4096]
    except OSError:
        return False


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_profile(path: Path) -> dict[str, Any]:
    """Parse JSON or YAML without silently dropping nested profile data."""
    content = path.read_text(encoding="utf-8")
    if content.lstrip().startswith("{"):
        data = json.loads(content)
    else:
        try:
            import yaml
        except ImportError as exc:
            raise RuntimeError("YAML profiles require PyYAML: pip install pyyaml") from exc
        data = yaml.safe_load(content)
    if not isinstance(data, dict):
        raise ValueError("Software profile must be a mapping")
    return data
