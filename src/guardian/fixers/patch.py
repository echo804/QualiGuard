from __future__ import annotations
import difflib


def generate_patch(original: str, fixed: str, file_path: str) -> str:
    diff = difflib.unified_diff(
        original.splitlines(keepends=True),
        fixed.splitlines(keepends=True),
        fromfile=file_path,
        tofile=file_path,
    )
    return "".join(diff)
