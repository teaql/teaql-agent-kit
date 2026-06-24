#!/usr/bin/env python3
"""Bulk-update cargo-teaql version references in documentation files.

The script scans a configurable set of Markdown files and normalizes every
cargo-teaql version mention to a single target version. It is the companion to
``fix_docs.py`` and is intended to be run whenever a new ``cargo-teaql`` release
is published.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DEFAULT_TARGET_VERSION = "2.0.2"

# Regexes that match different ways the cargo-teaql version is written in docs.
# Each pattern must contain a single capturing group for the version digits.
DEFAULT_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(cargo-teaql` version `)[0-9\.]+"), r"\g<1>{version}"),
    (re.compile(r"(cargo-teaql >= )[0-9\.]+"), r"\g<1>{version}"),
    (re.compile(r"(cargo-teaql )0\.2\.0"), r"\g<1>{version}"),
    (re.compile(r"(cargo-teaql` `)[0-9\.]+"), r"\g<1>{version}"),
]


def compile_patterns(version: str) -> list[tuple[re.Pattern[str], str]]:
    """Return regex patterns parameterized for ``version``.

    Args:
        version: The target cargo-teaql version.

    Returns:
        A list of ``(compiled_pattern, replacement_template)`` pairs.
    """
    return [(pattern, template.format(version=version)) for pattern, template in DEFAULT_PATTERNS]


def update_content(content: str, version: str) -> str:
    """Normalize cargo-teaql version references inside ``content``.

    Args:
        content: The original file content.
        version: The target cargo-teaql version.

    Returns:
        The updated content.
    """
    for pattern, replacement in compile_patterns(version):
        content = pattern.sub(replacement, content)
    return content


def update_file(path: Path, version: str) -> bool:
    """Update a single Markdown file, returning whether it was modified.

    Args:
        path: Path to the file to update in place.
        version: The target cargo-teaql version.

    Returns:
        ``True`` if the file content changed, otherwise ``False``.
    """
    original = path.read_text(encoding="utf-8")
    updated = update_content(original, version)
    if original == updated:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def collect_files(root: Path, globs: list[str] | None = None) -> list[Path]:
    """Collect Markdown files matching ``globs`` under ``root``.

    Args:
        root: Base directory for glob expansion.
        globs: Glob patterns to collect. Defaults to the project's doc layout.

    Returns:
        Sorted list of unique file paths.
    """
    if globs is None:
        globs = ["playbooks/*.md", "*.md", "agents/*.md"]

    files: set[Path] = set()
    for pattern in globs:
        files.update(root.glob(pattern))
    return sorted(files)


def update_versions(
    root: Path,
    version: str = DEFAULT_TARGET_VERSION,
    globs: list[str] | None = None,
) -> int:
    """Update cargo-teaql version references in the project's docs.

    Args:
        root: Project root directory.
        version: Target cargo-teaql version.
        globs: Optional glob patterns limiting which files are scanned.

    Returns:
        Number of files modified.
    """
    changed = 0
    for md_file in collect_files(root, globs):
        if update_file(md_file, version):
            print(f"Updated {md_file.relative_to(root)}")
            changed += 1
    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Bulk-update cargo-teaql version references in Markdown docs."
    )
    parser.add_argument(
        "--version",
        default=DEFAULT_TARGET_VERSION,
        help=f"Target cargo-teaql version (default: {DEFAULT_TARGET_VERSION}).",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root directory (default: current directory).",
    )
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"Error: not a directory: {root}", file=sys.stderr)
        return 1

    changed = update_versions(root, version=args.version)
    print(f"Updated {changed} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
