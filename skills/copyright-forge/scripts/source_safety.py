"""Validate paths before reading repository-controlled source manifests."""
from __future__ import annotations
from pathlib import Path, PurePosixPath

class InvalidSourcePath(ValueError):
    pass

def resolve_source(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative or "\x00" in relative:
        raise InvalidSourcePath("Invalid source path")
    p = PurePosixPath(relative)
    if p.is_absolute() or any(part in (".", "..") for part in relative.split("/")):
        raise InvalidSourcePath(f"Unsafe source path: {relative}")
    root = root.resolve(strict=True)
    candidate = (root / relative).resolve(strict=True)
    if not candidate.is_relative_to(root) or not candidate.is_file():
        raise InvalidSourcePath(f"Not a regular file inside the project: {relative}")
    return candidate
