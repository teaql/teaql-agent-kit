#!/usr/bin/env python3
"""Exercise a minimal concept graph line protocol against the AMD endpoint."""

from __future__ import annotations

import csv
import json
import os
import re
import time
import urllib.request
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ENDPOINT = "https://developer.amd.com.cn/radeon/api/v1/chat/completions"
MODEL = "Qwen3.8-Flash-Next"

REQUIREMENT = """A moving-company system covering operations and logistics
(moves, routes, time slots, fulfillment events, addresses); employees and
payroll (staff registry, job assignments, worked hours, payroll calculations,
bonuses, leave); private and corporate customers, contacts, billing information
and history; products and services (moving, cleaning, box rentals,
configurations and pricing); marketing and sales (campaigns, discount codes,
leads and conversion metrics); finance and accounting (payments, invoices,
expenses, VAT and summaries); assets (vehicles, equipment, consumables and
maintenance); administration and compliance (contracts, insurance, documents
and audit logs); user and role management; authentication, RBAC, activity
audit, versioning, soft deletes, notifications, automation hooks and API
integration."""

RESERVED = {
    "abstract", "all", "alter", "and", "any", "as", "asc", "async", "await",
    "base", "between", "bool", "break", "case", "catch", "class", "column",
    "const", "constraint", "continue", "create", "database", "default", "defer",
    "delete", "desc", "distinct", "do", "drop", "dynamic", "else", "enum",
    "event", "exists", "export", "extends", "false", "final", "finally", "fn",
    "for", "foreach", "from", "full", "func", "function", "go", "grant",
    "group", "having", "if", "impl", "import", "in", "index", "inner",
    "insert", "interface", "internal", "is", "join", "key", "left", "let",
    "like", "limit", "lock", "match", "mod", "move", "mut", "namespace",
    "new", "nil", "not", "null", "offset", "operator", "or", "order", "out",
    "outer", "override", "package", "primary", "private", "protected",
    "protocol", "public", "ref", "references", "return", "revoke", "right",
    "schema", "select", "self", "static", "struct", "super", "switch", "table",
    "throw", "trait", "trigger", "true", "try", "type", "typeof", "union",
    "unsafe", "update", "use", "user", "using", "values", "var", "view",
    "virtual", "void", "where", "while", "with", "yield",
}

SYSTEM = """You are the concept-discovery worker in a deterministic modeling
harness. Return only the requested line protocol. Do not return Markdown, CSV,
JSON, prose, comments, code fences, fields, types, database design, APIs, KSML,
or implementation. Use lowercase snake_case terms. Every line is one fact."""


def prompt() -> str:
    reserved = ", ".join(sorted(RESERVED))
    return f"""Requirement:\n{REQUIREMENT}

Discover 40 to 60 durable business concepts in exactly 14 coherent groups,
then connect them with at most 70 coarse directed relations. The concepts
include exactly one root named moving_company. Use `ambiguous` only when a term
that actually appears in the requirement has multiple plausible business
meanings; emit zero to three ambiguous concepts, and add one matching unresolved
line for each. Do not classify ordinary attributes, statuses, categories,
methods, dates, payloads, or enum values as concepts merely to fill the budget.

Avoid bare reserved words from Java, Rust, TypeScript, Go, Swift, C#, Python,
and SQL. In particular, use descriptive names such as move_order rather than
move and user_account rather than user. A compound snake_case term may contain
a reserved word as one segment, but the complete term must not itself be a
reserved word.

Reserved-word denylist: {reserved}

Return only these line forms:
group <group_key>
concept <term> <root|entity|ambiguous>
relation <from_term> <verb> <to_term>
unresolved <term>

`group` starts a section. Every following `concept` belongs to the current group
until the next `group` line. A relation line must contain exactly four whitespace-separated
tokens. Its verb is exactly one lowercase snake_case token: write
`relation user_account authenticates_via authentication_token`, never
`relation user_account authenticates via authentication_token`. Relation verbs
must avoid the denylist. Do not assign IDs."""


def call() -> tuple[str, dict]:
    token = os.environ.get("AMD_API_TOKEN")
    if not token:
        raise RuntimeError("AMD_API_TOKEN is required")
    payload = {
        "model": MODEL,
        "temperature": 0,
        "max_tokens": 1800,
        "reasoning_effort": "none",
        "chat_template_kwargs": {"enable_thinking": False},
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt()},
        ],
    }
    (HERE / "request.json").write_text(json.dumps(payload, indent=2) + "\n")
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    started = time.monotonic()
    with urllib.request.urlopen(request, timeout=240) as response:
        body = json.loads(response.read())
    elapsed = round(time.monotonic() - started, 3)
    (HERE / "response.json").write_text(json.dumps(body, indent=2) + "\n")
    content = body["choices"][0]["message"]["content"]
    (HERE / "concept-graph.txt").write_text(content.rstrip() + "\n")
    usage = body.get("usage", {})
    return content, {
        "elapsed_seconds": elapsed,
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "total_tokens": usage.get("total_tokens"),
        "cost": usage.get("cost"),
    }


def parse(content: str) -> dict:
    groups: list[str] = []
    concepts: list[dict[str, str]] = []
    relations: list[dict[str, str]] = []
    unresolved: list[str] = []
    syntax_errors: list[str] = []
    current_group: str | None = None
    for number, raw in enumerate(content.splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) == 2 and parts[0] == "group":
            current_group = parts[1]
            groups.append(current_group)
        elif len(parts) == 3 and parts[0] == "concept" and current_group:
            concepts.append({"term": parts[1], "group_key": current_group, "kind": parts[2]})
        elif len(parts) == 4 and parts[0] == "relation":
            relations.append({"from_term": parts[1], "verb": parts[2], "to_term": parts[3]})
        elif len(parts) == 2 and parts[0] == "unresolved":
            unresolved.append(parts[1])
        else:
            syntax_errors.append(f"line {number}: {raw}")
    findings = list(syntax_errors)
    if len(groups) != len(set(groups)):
        findings.append("duplicate group")
    terms = [row["term"] for row in concepts]
    if len(terms) != len(set(terms)):
        findings.append("duplicate concept")
    group_set = set(groups)
    term_set = set(terms)
    pattern = re.compile(r"[a-z][a-z0-9_]*")
    for group in groups:
        if not pattern.fullmatch(group):
            findings.append(f"invalid group: {group}")
    for row in concepts:
        if not pattern.fullmatch(row["term"]):
            findings.append(f"invalid concept: {row['term']}")
        if row["term"] in RESERVED:
            findings.append(f"reserved concept: {row['term']}")
        if row["group_key"] not in group_set:
            findings.append(f"unknown group: {row['term']} -> {row['group_key']}")
        if row["kind"] not in {"root", "entity", "ambiguous"}:
            findings.append(f"invalid concept kind: {row['term']} -> {row['kind']}")
    for row in relations:
        if row["from_term"] not in term_set or row["to_term"] not in term_set:
            findings.append(f"unknown relation endpoint: {row}")
        if not pattern.fullmatch(row["verb"]) or row["verb"] in RESERVED:
            findings.append(f"invalid/reserved relation verb: {row['verb']}")
    roots = [row for row in concepts if row["kind"] == "root"]
    if len(roots) != 1 or roots[0]["term"] != "moving_company":
        findings.append(f"invalid root set: {roots}")
    if not 40 <= len(concepts) <= 60:
        findings.append(f"concept count outside 40..60: {len(concepts)}")
    if len(relations) > 70:
        findings.append(f"relation count above 70: {len(relations)}")
    if len(unresolved) > 3:
        findings.append(f"unresolved count above 3: {len(unresolved)}")
    counts = Counter(row["group_key"] for row in concepts)
    for group in groups:
        if counts[group] == 0:
            findings.append(f"empty group: {group}")
    ambiguous = {row["term"] for row in concepts if row["kind"] == "ambiguous"}
    if set(unresolved) != ambiguous:
        findings.append(
            f"unresolved mismatch: flags={sorted(ambiguous)} lines={sorted(set(unresolved))}"
        )
    ids = {term: f"C{index:03d}" for index, term in enumerate(terms, 1)}
    return {
        "groups": groups,
        "concepts": [
            {"concept_id": ids[row["term"]], **row} for row in concepts
        ],
        "relations": [
            {
                "from_concept_id": ids.get(row["from_term"], ""),
                "verb": row["verb"],
                "to_concept_id": ids.get(row["to_term"], ""),
            }
            for row in relations
        ],
        "unresolved": unresolved,
        "findings": findings,
    }


def write_csv(name: str, fields: list[str], rows: list[dict[str, str]]) -> None:
    with (HERE / name).open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    content, metrics = call()
    result = parse(content)
    write_csv("concepts.csv", ["concept_id", "term", "group_key", "kind"], result["concepts"])
    write_csv(
        "relations.csv",
        ["from_concept_id", "verb", "to_concept_id"],
        result["relations"],
    )
    report = {
        **metrics,
        "group_count": len(result["groups"]),
        "concept_count": len(result["concepts"]),
        "relation_count": len(result["relations"]),
        "unresolved_count": len(result["unresolved"]),
        "findings": result["findings"],
        "accepted": not result["findings"],
    }
    (HERE / "result.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
