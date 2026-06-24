#!/usr/bin/env python3
"""Bulk-replace outdated snippets in TeaQL documentation files.

This script walks through a directory of Markdown documentation and applies a
set of textual replacements that align the docs with the current TeaQL tooling.
It is intentionally simple (plain string replacement) so that authors can see
exactly what changed in the resulting diff.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


# Replacements are applied in order. Each tuple is ``(old, new)``.
DEFAULT_REPLACEMENTS: list[tuple[str, str]] = [
    # Maven plugin coordinates used in older samples.
    ("teaql-maven-plugin:1.0.1:gen-lib", "teaql-maven-plugin:1.1.0:generate -Dservice=java-lib"),
    ("teaql-maven-plugin:1.0.1:gen-workspace", "teaql-maven-plugin:1.1.0:generate -Dservice=java-workspace"),
    ("teaql-maven-plugin:1.0.1:gen-doc", "teaql-maven-plugin:1.1.0:generate -Dservice=markdown-doc"),
    ("teaql-maven-plugin:1.0.1:gen-model", "teaql-maven-plugin:1.1.0:generate -Dservice=frontend-model"),
    ("teaql-maven-plugin:1.1.0:gen-lib", "teaql-maven-plugin:1.1.0:generate -Dservice=java-lib"),
    ("teaql-maven-plugin:1.1.0:gen-workspace", "teaql-maven-plugin:1.1.0:generate -Dservice=java-workspace"),
    ("teaql-maven-plugin:1.1.0:gen-doc", "teaql-maven-plugin:1.1.0:generate -Dservice=markdown-doc"),
    ("teaql-maven-plugin:1.1.0:gen-model", "teaql-maven-plugin:1.1.0:generate -Dservice=frontend-model"),
    # Version references for Rust tooling.
    ("version `0.2.2`", "version `1.1.0`"),
    ("cargo-teaql >= 0.2.2", "cargo-teaql >= 1.1.0"),
]


def apply_replacements(content: str, replacements: list[tuple[str, str]] | None = None) -> str:
    """Apply an ordered list of replacements to ``content``.

    Args:
        content: The original file content.
        replacements: A list of ``(old, new)`` string pairs.

    Returns:
        The updated content.
    """
    if replacements is None:
        replacements = DEFAULT_REPLACEMENTS
    for old, new in replacements:
        content = content.replace(old, new)
    return content


def fix_file(path: Path, replacements: list[tuple[str, str]] | None = None) -> bool:
    """Apply replacements to a single file, returning whether it was modified.

    Args:
        path: Path to the file to update in place.
        replacements: Replacements to apply.

    Returns:
        ``True`` if the file content changed, otherwise ``False``.
    """
    original = path.read_text(encoding="utf-8")
    updated = apply_replacements(original, replacements)
    if original == updated:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def fix_docs(directory: Path, replacements: list[tuple[str, str]] | None = None) -> int:
    """Apply replacements to all ``.md`` files under ``directory``.

    Args:
        directory: Root directory to scan.
        replacements: Optional custom replacements. Defaults to
            :data:`DEFAULT_REPLACEMENTS`.

    Returns:
        Number of files modified.
    """
    if replacements is None:
        replacements = DEFAULT_REPLACEMENTS

    changed = 0
    for root, _dirs, files in os.walk(directory):
        for filename in files:
            if not filename.endswith(".md"):
                continue
            file_path = Path(root) / filename
            if fix_file(file_path, replacements):
                print(f"Updated: {file_path.relative_to(directory)}")
                changed += 1
    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Bulk-update outdated snippets in TeaQL Markdown docs."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="Directory to scan for Markdown files (default: current directory).",
    )
    args = parser.parse_args(argv)

    target = Path(args.directory).resolve()
    if not target.is_dir():
        print(f"Error: not a directory: {target}", file=sys.stderr)
        return 1

    changed = fix_docs(target)
    print(f"Updated {changed} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
