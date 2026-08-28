#!/usr/bin/env python3
"""Resolve and verify TeaQL runtime sources without involving the generator."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


LANGUAGES = ("java", "rust", "golang", "typescript", "swift", "dotnet", "python")


def load_config(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read JSON-compatible YAML config {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("configuration root must be an object")
    if data.get("schemaVersion") != 1:
        raise ValueError("schemaVersion must be 1")
    if data.get("runtimeSource") not in {"workspace", "release"}:
        raise ValueError("runtimeSource must be workspace or release")
    runtimes = data.get("runtimes")
    if not isinstance(runtimes, dict):
        raise ValueError("runtimes must be an object")
    missing = sorted(set(LANGUAGES) - set(runtimes))
    extra = sorted(set(runtimes) - set(LANGUAGES))
    if missing or extra:
        raise ValueError(f"runtime keys mismatch: missing={missing}, extra={extra}")
    return data


def git_value(repo: Path, *args: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], text=True, capture_output=True, check=False
    )
    return result.stdout.strip() if result.returncode == 0 else None


def resolve(config_path: Path, data: dict) -> dict:
    source = data["runtimeSource"]
    rows = {}
    errors = []
    for language in LANGUAGES:
        entry = data["runtimes"][language]
        if not isinstance(entry, dict):
            errors.append(f"{language}: configuration must be an object")
            continue
        version = entry.get("version")
        path_value = entry.get("path")
        if source == "workspace":
            if not path_value:
                errors.append(f"{language}: workspace mode requires path")
                continue
            repo = (config_path.parent / path_value).resolve()
            if not repo.is_dir():
                errors.append(f"{language}: runtime path does not exist: {repo}")
                continue
            commit = git_value(repo, "rev-parse", "HEAD")
            if commit is None:
                errors.append(f"{language}: runtime path is not a Git repository: {repo}")
                continue
            status = git_value(repo, "status", "--porcelain")
            rows[language] = {
                "source": "workspace",
                "declaredVersion": version,
                "resolvedPath": str(repo),
                "commit": commit,
                "dirty": bool(status),
            }
        else:
            if path_value:
                errors.append(f"{language}: release mode forbids path overrides")
            if not version:
                errors.append(f"{language}: release mode requires version")
            if not entry.get("package"):
                errors.append(f"{language}: release mode requires package")
            rows[language] = {
                "source": "release",
                "declaredVersion": version,
                "resolvedPackage": entry.get("package"),
            }
    return {
        "schemaVersion": 1,
        "runtimeSource": source,
        "resolvedAt": datetime.now(timezone.utc).isoformat(),
        "runtimes": rows,
        "errors": errors,
    }


def write_evidence(workspace: Path, evidence: dict) -> Path:
    target = workspace.resolve() / ".teaql" / "runtime-source-evidence.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(prog="teaql-workspace")
    parser.add_argument("command", choices=("apply", "verify"))
    parser.add_argument("--config", default="teaql-workspace.yaml", type=Path)
    parser.add_argument("--workspace", default=Path.cwd(), type=Path)
    args = parser.parse_args()
    try:
        config = args.config.resolve()
        evidence = resolve(config, load_config(config))
    except ValueError as exc:
        print(f"teaql-workspace: {exc}", file=sys.stderr)
        return 2
    if evidence["errors"]:
        for error in evidence["errors"]:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if args.command == "apply":
        target = write_evidence(args.workspace, evidence)
        print(f"runtime source evidence written: {target}")
    else:
        print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
