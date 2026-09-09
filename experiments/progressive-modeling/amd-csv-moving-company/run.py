#!/usr/bin/env python3
"""Build a moving-company KSML candidate through flat CSV LLM contracts."""

from __future__ import annotations

import csv
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr


HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"
OUTPUT = HERE / "output"
ENDPOINT = "https://developer.amd.com.cn/radeon/api/v1/chat/completions"
MODEL = "Qwen3.8-Flash-Next"
CONTRACT_FINDINGS: list[str] = []
RESOLUTION_FINDINGS: list[str] = []

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

GROUPS = [
    ("operations", "Operations and Logistics"),
    ("employees", "Employees and Payroll"),
    ("customers", "Customer Management"),
    ("products", "Products and Services"),
    ("marketing", "Marketing and Sales"),
    ("finance", "Finance and Accounting"),
    ("assets", "Asset Management"),
    ("administration", "Administration and Compliance"),
    ("user_role", "User and Role Management"),
    ("authentication", "Authentication and Permissions"),
    ("audit", "Activity Logging and Audit"),
    ("versioning", "Versioning and Soft Deletes"),
    ("notifications", "Notifications and Automation"),
    ("integrations", "API and Integrations"),
]

SYSTEM = """You are a bounded worker in a deterministic modeling harness.
Return only the requested sectioned RFC 4180 CSV. Do not return Markdown,
JSON, prose, code fences, KSML, database design, APIs, or implementation.
Use lowercase snake_case identifiers. Quote a CSV cell when required."""


def compact_usage(body: dict) -> dict:
    usage = body.get("usage", {})
    return {
        key: usage.get(key)
        for key in ("prompt_tokens", "completion_tokens", "total_tokens", "cost")
    }


def request_llm(name: str, prompt: str, max_tokens: int) -> tuple[str, dict]:
    token = os.environ.get("AMD_API_TOKEN")
    if not token:
        raise RuntimeError("AMD_API_TOKEN is required")
    payload = {
        "model": MODEL,
        "temperature": 0,
        "max_tokens": max_tokens,
        "reasoning_effort": "none",
        "chat_template_kwargs": {"enable_thinking": False},
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
    }
    request_path = RAW / f"{name}.request.json"
    response_path = RAW / f"{name}.response.json"
    request_path.write_text(json.dumps(payload, indent=2) + "\n")
    if response_path.exists() and os.environ.get("TEAQL_REUSE_RAW") == "1":
        body = json.loads(response_path.read_text())
        choice = body.get("choices", [{}])[0]
        content = choice.get("message", {}).get("content", "")
        return content, {
            "name": name,
            "elapsed_seconds": None,
            "finish_reason": choice.get("finish_reason"),
            "usage": compact_usage(body),
            "content_characters": len(content),
            "reused": True,
        }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    started = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=240) as response:
            body = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")
        raise RuntimeError(f"{name}: HTTP {exc.code}: {detail}") from exc
    elapsed = time.monotonic() - started
    response_path.write_text(json.dumps(body, indent=2) + "\n")
    choice = body.get("choices", [{}])[0]
    content = choice.get("message", {}).get("content", "")
    metrics = {
        "name": name,
        "elapsed_seconds": round(elapsed, 3),
        "finish_reason": choice.get("finish_reason"),
        "usage": compact_usage(body),
        "content_characters": len(content),
    }
    return content, metrics


def parse_sections(text: str) -> dict[str, list[dict[str, str]]]:
    sections: dict[str, list[str]] = defaultdict(list)
    active: str | None = None
    for raw_line in text.strip().splitlines():
        line = raw_line.strip()
        match = re.fullmatch(r"\[([a-z_]+)\]", line.lower())
        if match:
            active = match.group(1)
            continue
        if active and line:
            sections[active].append(raw_line)
    parsed: dict[str, list[dict[str, str]]] = {}
    for name, lines in sections.items():
        parsed[name] = list(csv.DictReader(io.StringIO("\n".join(lines))))
    return parsed


def parse_known_section(
    text: str,
    section_name: str,
    fieldnames: list[str],
) -> list[dict[str, str]]:
    """Parse one CSV section and retain a finding when its header is omitted."""
    lines: list[str] = []
    active = False
    for raw_line in text.strip().splitlines():
        marker = re.fullmatch(r"\[([a-z_]+)\]", raw_line.strip().lower())
        if marker:
            active = marker.group(1) == section_name
            continue
        if active and raw_line.strip():
            lines.append(raw_line)
    if not lines:
        return []
    reader = list(csv.reader(io.StringIO("\n".join(lines))))
    if reader and reader[0] == fieldnames:
        data_rows = reader[1:]
    else:
        CONTRACT_FINDINGS.append(f"{section_name}: required CSV header was omitted")
        data_rows = reader
    result: list[dict[str, str]] = []
    for row in data_rows:
        if len(row) != len(fieldnames):
            CONTRACT_FINDINGS.append(
                f"{section_name}: expected {len(fieldnames)} columns, got {len(row)}"
            )
            continue
        result.append(dict(zip(fieldnames, row)))
    return result


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def discover_concepts() -> tuple[list[dict[str, str]], list[dict[str, str]], dict]:
    group_rows = [{"group_key": key, "name": name} for key, name in GROUPS]
    groups_text = "; ".join(f"{key}={name}" for key, name in GROUPS)
    prompt = f"""Requirement:\n{REQUIREMENT}\n\nAllowed groups:\n{groups_text}

Discover 3 to 5 durable business concepts per group. Include exactly one
domain_root concept named moving_company in operations. Preserve genuinely
ambiguous source terms rather than silently choosing a meaning. Do not add
fields, types, definitions, status values, or relations.

Return exactly:
[concepts]
term,group_key,kind,ambiguous,source_term

kind is domain_root or entity. ambiguous is true or false. Every allowed group
must have at least 3 concepts. Terms must be unique."""
    content, metrics = request_llm("01-concept-discovery", prompt, 3200)
    candidates = parse_known_section(
        content,
        "concepts",
        ["term", "group_key", "kind", "ambiguous", "source_term"],
    )
    allowed_groups = {key for key, _ in GROUPS}
    seen: set[str] = set()
    rows: list[dict[str, str]] = []
    errors: list[str] = []
    for index, row in enumerate(candidates, 1):
        term = row.get("term", "").strip()
        group = row.get("group_key", "").strip()
        kind = row.get("kind", "").strip()
        ambiguous = row.get("ambiguous", "").strip().lower()
        if not re.fullmatch(r"[a-z][a-z0-9_]*", term):
            errors.append(f"invalid term: {term!r}")
            continue
        if term in seen:
            errors.append(f"duplicate term: {term}")
            continue
        if group not in allowed_groups:
            errors.append(f"unknown group for {term}: {group}")
            continue
        if kind not in {"domain_root", "entity"}:
            errors.append(f"invalid kind for {term}: {kind}")
            continue
        if ambiguous not in {"true", "false"}:
            errors.append(f"invalid ambiguity for {term}: {ambiguous}")
            continue
        seen.add(term)
        rows.append({
            "concept_id": f"C{index:03d}",
            "term": term,
            "group_key": group,
            "kind": kind,
            "ambiguous": ambiguous,
            "source_term": row.get("source_term", "").strip(),
            "status": "proposed",
        })
    roots = [row for row in rows if row["kind"] == "domain_root"]
    if len(roots) != 1 or roots[0]["term"] != "moving_company":
        errors.append(f"expected one moving_company root, got {roots}")
    counts = defaultdict(int)
    for row in rows:
        counts[row["group_key"]] += 1
    if errors:
        raise RuntimeError("concept validation failed:\n- " + "\n- ".join(errors))
    deficient = [(key, name) for key, name in GROUPS if counts[key] < 3]
    repair_metrics: list[dict] = []
    for group, group_name in deficient:
        existing = [row["term"] for row in rows if row["group_key"] == group]
        global_existing = ", ".join(sorted(seen))
        needed = 3 - len(existing)
        repair_prompt = f"""Repair one incomplete concept group from the same requirement.

Group: {group} ({group_name})
Existing terms: {', '.join(existing)}
Forbidden global terms: {global_existing}
Requirement: {REQUIREMENT}

Return exactly {needed} additional durable business concepts for this group.
Do not repeat existing terms and do not add fields, definitions, or relations.

Return exactly:
[concepts]
term,group_key,kind,ambiguous,source_term"""
        repair_content, repair_metric = request_llm(
            f"01-repair-{group}", repair_prompt, 700
        )
        repair_metrics.append(repair_metric)
        repair_rows = parse_known_section(
            repair_content,
            "concepts",
            ["term", "group_key", "kind", "ambiguous", "source_term"],
        )
        if len(repair_rows) != needed:
            retry_prompt = f"""The preceding response violated the CSV contract.
Return exactly {needed} new concepts for {group}. Existing terms are
{', '.join(existing)}. Do not use any of these global terms:
{global_existing}

The first line must be [concepts]. The second line must
be this exact header:
term,group_key,kind,ambiguous,source_term

Every data row must use group_key={group}, kind=entity, and ambiguous=false.
Return no other text."""
            repair_content, retry_metric = request_llm(
                f"01-repair-{group}-retry", retry_prompt, 700
            )
            repair_metrics.append(retry_metric)
            repair_rows = parse_known_section(
                repair_content,
                "concepts",
                ["term", "group_key", "kind", "ambiguous", "source_term"],
            )
            if len(repair_rows) != needed:
                raise RuntimeError(
                    f"repair retry for {group} returned {len(repair_rows)} concepts, expected {needed}"
                )
        for repair_row in repair_rows:
            term = repair_row.get("term", "").strip()
            repaired_group = repair_row.get("group_key", "").strip()
            if (
                not re.fullmatch(r"[a-z][a-z0-9_]*", term)
                or term in seen
                or repaired_group != group
            ):
                raise RuntimeError(f"invalid repair row for {group}: {repair_row}")
            seen.add(term)
            rows.append({
                "concept_id": "",
                "term": term,
                "group_key": group,
                "kind": "entity",
                "ambiguous": repair_row.get("ambiguous", "false").strip().lower(),
                "source_term": repair_row.get("source_term", "").strip(),
                "status": "proposed",
            })
    for index, row in enumerate(rows, 1):
        row["concept_id"] = f"C{index:03d}"
    metrics["repair_requests"] = repair_metrics
    return group_rows, rows, metrics


def scan_ambiguities(
    concepts: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict]:
    global_index = "; ".join(
        f"{row['concept_id']}={row['term']}@{row['group_key']}" for row in concepts
    )
    prompt = f"""Find overloaded concepts before field modeling.

Requirement: {REQUIREMENT}
Concept index: {global_index}

Return at most 8 concepts whose current term conflates two or more persisted
business objects that have distinct identities, lifecycles, or owners and are
explicitly supported by the source requirement. Do not split one object merely
because different teams view it differently, because it has many fields, or
because a more detailed future model is imaginable. Broad aggregates remain
one concept at this stage. Do not flag a term when its alternate meaning is
already represented by another term in the supplied global index. Do not flag
a persisted root merely because its name also describes the system or domain.
Do not infer distinctions absent from the source. Do not resolve or rename
anything in this step.

Return exactly:
[ambiguities]
concept_id,reason"""
    content, metrics = request_llm("02-ambiguity-scan", prompt, 1200)
    rows = parse_known_section(content, "ambiguities", ["concept_id", "reason"])
    if len(rows) > 8:
        raise RuntimeError(f"ambiguity scan returned {len(rows)} rows, maximum is 8")
    by_id = {
        row["concept_id"]: {**row, "ambiguous": "false"} for row in concepts
    }
    seen: set[str] = set()
    for row in rows:
        concept_id = row.get("concept_id", "").strip()
        if concept_id not in by_id or concept_id in seen:
            raise RuntimeError(f"invalid ambiguity row: {row}")
        seen.add(concept_id)
        by_id[concept_id]["ambiguous"] = "true"
    return [by_id[row["concept_id"]] for row in concepts], rows, metrics


def resolve_concepts(
    concepts: list[dict[str, str]],
    ambiguity_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict]]:
    ambiguous = [row for row in concepts if row["ambiguous"] == "true"]
    if not ambiguous:
        return concepts, [], []
    reasons = {row["concept_id"]: row["reason"] for row in ambiguity_rows}
    global_index = "; ".join(
        f"{row['concept_id']}={row['term']}@{row['group_key']}" for row in concepts
    )
    allowed_group_text = "; ".join(key for key, _ in GROUPS)
    rows: list[dict[str, str]] = []
    metrics: list[dict] = []

    def resolve_one(concept: dict[str, str]) -> tuple[list[dict[str, str]], dict]:
        prompt = f"""Resolve exactly one ambiguity.

Active concept: {concept['concept_id']}={concept['term']}@{concept['group_key']}
Reason: {reasons.get(concept['concept_id'], '')}
Global concept index: {global_index}
Allowed groups: {allowed_group_text}

Choose keep, rename, or split. A split has exactly two rows. Split only when
the source requirement explicitly supports distinct persisted identities,
lifecycles, or owners. Keep when the distinction is only a view, role, state,
implementation detail, speculative refinement, or is already represented by
another concept in the global index. A keep row must retain the exact current
term and group. A rename or split must not use any existing global term.

Return exactly:
[resolutions]
source_concept_id,operation,term,group_key"""
        content, metric = request_llm(
            f"03-resolve-{concept['concept_id']}", prompt, 650
        )
        parsed = parse_known_section(
            content,
            "resolutions",
            ["source_concept_id", "operation", "term", "group_key"],
        )
        return parsed, metric

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(resolve_one, concept): concept for concept in ambiguous}
        for future in as_completed(futures):
            parsed, metric = future.result()
            rows.extend(parsed)
            metrics.append(metric)
    ambiguous_ids = {row["concept_id"] for row in ambiguous}
    allowed_groups = {key for key, _ in GROUPS}
    replacements: dict[str, list[dict[str, str]]] = defaultdict(list)
    errors: list[str] = []
    for row in rows:
        source = row.get("source_concept_id", "").strip()
        operation = row.get("operation", "").strip()
        term = row.get("term", "").strip()
        group = row.get("group_key", "").strip()
        if source not in ambiguous_ids:
            errors.append(f"unknown resolution source: {source}")
            continue
        if operation not in {"keep", "rename", "split"}:
            errors.append(f"{source}: invalid operation {operation}")
            continue
        if not re.fullmatch(r"[a-z][a-z0-9_]*", term) or group not in allowed_groups:
            errors.append(f"{source}: invalid term/group {term}@{group}")
            continue
        replacements[source].append({
            "source_concept_id": source,
            "operation": operation,
            "term": term,
            "group_key": group,
        })
    for source in ambiguous_ids:
        candidates = replacements[source]
        if not candidates:
            errors.append(f"{source}: no resolution")
            continue
        operations = {row["operation"] for row in candidates}
        if "split" in operations and (operations != {"split"} or len(candidates) < 2):
            errors.append(f"{source}: malformed split")
        if "split" not in operations and len(candidates) != 1:
            errors.append(f"{source}: expected one keep/rename row")
    if errors:
        raise RuntimeError("resolution validation failed:\n- " + "\n- ".join(errors))
    concepts_by_id = {row["concept_id"]: row for row in concepts}
    global_terms = {row["term"]: row["concept_id"] for row in concepts}
    for source in sorted(ambiguous_ids):
        original = concepts_by_id[source]
        candidates = replacements[source]
        operation = candidates[0]["operation"]
        collision_terms = [
            row["term"]
            for row in candidates
            if row["term"] in global_terms and global_terms[row["term"]] != source
        ]
        if operation == "split" and original["kind"] == "domain_root":
            RESOLUTION_FINDINGS.append(
                f"{source}: rejected split of domain root; retained {original['term']}"
            )
        elif collision_terms:
            RESOLUTION_FINDINGS.append(
                f"{source}: rejected global term collisions {collision_terms}; retained {original['term']}"
            )
        else:
            continue
        replacements[source] = [{
            "source_concept_id": source,
            "operation": "keep",
            "term": original["term"],
            "group_key": original["group_key"],
        }]
    resolved: list[dict[str, str]] = []
    for concept in concepts:
        candidates = replacements.get(concept["concept_id"])
        if not candidates:
            resolved.append(dict(concept))
            continue
        for candidate in candidates:
            resolved.append({
                "concept_id": "",
                "term": candidate["term"],
                "group_key": candidate["group_key"],
                "kind": concept["kind"],
                "ambiguous": "false",
                "source_term": concept["term"],
                "status": "proposed",
            })
    seen: set[str] = set()
    for index, row in enumerate(resolved, 1):
        if row["term"] in seen:
            errors.append(f"resolution created duplicate term: {row['term']}")
        seen.add(row["term"])
        row["concept_id"] = f"C{index:03d}"
    if errors:
        raise RuntimeError("resolved catalog validation failed:\n- " + "\n- ".join(errors))
    flat_rows = [row for candidates in replacements.values() for row in candidates]
    return resolved, flat_rows, metrics


def complete_group(
    group_key: str,
    concepts: list[dict[str, str]],
    global_index: str,
    stage: str = "04-fields",
) -> tuple[list[dict[str, str]], list[dict[str, str]], dict]:
    local = [row for row in concepts if row["group_key"] == group_key]
    local_index = "; ".join(f"{row['concept_id']}={row['term']}" for row in local)
    prompt = f"""Complete only this bounded concept packet.

Group: {group_key}
Local concepts: {local_index}
Allowed reference targets (ID=term): {global_index}

For every local concept return 4 to 8 business fields. A domain_root may have
3 to 6 fields. Do not emit id, version, create_time, update_time, or the
moving_company ownership field; the deterministic assembler supplies them.
Use only these semantic types: string, text, integer, decimal, boolean, date,
timestamp, reference. A reference must have one allowed target ID. A scalar
must have an empty target_concept_id. Do not invent concepts. If a necessary
target is unavailable, report it under missing_concepts.
An identifier for a polymorphic or unspecified entity is a string, not a
reference. Return the exact headers even when a section has no data rows. Every
non-root concept must have at least 4 field rows.

Return exactly:
[fields]
concept_id,field_name,semantic_type,required,target_concept_id
[missing_concepts]
owner_concept_id,term,reason"""
    content, metrics = request_llm(f"{stage}-{group_key}", prompt, 2600)
    fields = parse_known_section(
        content,
        "fields",
        ["concept_id", "field_name", "semantic_type", "required", "target_concept_id"],
    )
    missing = parse_known_section(
        content,
        "missing_concepts",
        ["owner_concept_id", "term", "reason"],
    )
    return fields, missing, metrics


def validate_fields(
    concepts: list[dict[str, str]],
    candidate_fields: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[str]]:
    concept_ids = {row["concept_id"] for row in concepts}
    local_ids = concept_ids
    types = {"string", "text", "integer", "decimal", "boolean", "date", "timestamp", "reference"}
    forbidden = {"id", "version", "create_time", "update_time", "moving_company"}
    seen: set[tuple[str, str]] = set()
    counts = defaultdict(int)
    accepted: list[dict[str, str]] = []
    errors: list[str] = []
    for row in candidate_fields:
        owner = row.get("concept_id", "").strip()
        name = row.get("field_name", "").strip()
        semantic_type = row.get("semantic_type", "").strip()
        required = row.get("required", "").strip().lower()
        target = row.get("target_concept_id", "").strip()
        key = (owner, name)
        if owner == "concept_id" and name == "field_name":
            CONTRACT_FINDINGS.append("fields: duplicate CSV header appeared as a data row")
            continue
        if owner not in local_ids:
            errors.append(f"field {name}: unknown owner {owner}")
            continue
        if not re.fullmatch(r"[a-z][a-z0-9_]*", name) or name in forbidden:
            errors.append(f"{owner}: invalid/managed field {name!r}")
            continue
        if semantic_type not in types or required not in {"true", "false"}:
            errors.append(f"{owner}.{name}: invalid type/required")
            continue
        if semantic_type == "reference" and target not in concept_ids:
            errors.append(f"{owner}.{name}: invalid reference {target!r}")
            continue
        if semantic_type != "reference" and target:
            errors.append(f"{owner}.{name}: scalar has reference {target}")
            continue
        if key in seen:
            errors.append(f"duplicate field {owner}.{name}")
            continue
        seen.add(key)
        counts[owner] += 1
        accepted.append({
            "field_id": f"F{len(accepted) + 1:04d}",
            "concept_id": owner,
            "field_name": name,
            "semantic_type": semantic_type,
            "required": required,
            "target_concept_id": target,
            "status": "proposed",
        })
    for concept in concepts:
        count = counts[concept["concept_id"]]
        minimum = 3 if concept["kind"] == "domain_root" else 4
        if count < minimum or count > 8:
            errors.append(f"{concept['concept_id']} {concept['term']}: {count} fields")
    return accepted, errors


def sample_value(field: dict[str, str], target_terms: dict[str, str]) -> str:
    semantic_type = field["semantic_type"]
    name = field["field_name"]
    if semantic_type == "reference":
        return f"{target_terms[field['target_concept_id']]}()"
    if semantic_type == "boolean":
        return "true"
    if semantic_type == "integer":
        return "1"
    if semantic_type == "decimal":
        return "1.00"
    if semantic_type == "date":
        return "2026-09-10"
    if semantic_type == "timestamp":
        return "2026-09-10T12:00:00Z"
    if semantic_type == "text":
        return f"Example {name.replace('_', ' ')} details"
    return f"Example {name.replace('_', ' ')}"


def assemble_ksml(
    groups: list[dict[str, str]],
    concepts: list[dict[str, str]],
    fields: list[dict[str, str]],
) -> None:
    group_names = {row["group_key"]: row["name"] for row in groups}
    reserved_replacements = {"move": "move_order", "user": "user_account"}
    terms = {
        row["concept_id"]: reserved_replacements.get(row["term"], row["term"])
        for row in concepts
    }
    by_owner: dict[str, list[dict[str, str]]] = defaultdict(list)
    for field in fields:
        by_owner[field["concept_id"]].append(field)
    root = next(row for row in concepts if row["kind"] == "domain_root")
    ordered = [root] + [row for row in concepts if row is not root]
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<root name="moving-company-service"',
        '      cfg_mask_china_mobile="false"',
        '      data_service="sqlite"',
        '      org="example"',
        '      _module_key="root">',
    ]
    for concept in ordered:
        term = terms[concept["concept_id"]]
        concept_fields = by_owner[concept["concept_id"]]
        masks = [
            field["field_name"]
            for field in concept_fields
            if field["field_name"] in {"password_hash", "secret_key", "secret_token"}
        ]
        attrs = [
            ("_name", term.replace("_", " ").title()),
            ("_module", group_names[concept["group_key"]]),
            ("_module_key", concept["group_key"].replace("_", "-")),
        ]
        if masks:
            attrs.append(("_audit_mask_fields", ",".join(masks)))
        if concept["kind"] != "domain_root":
            attrs.append((terms[root["concept_id"]], f"{terms[root['concept_id']]}()"))
        for field in concept_fields:
            field_name = field["field_name"]
            if field["semantic_type"] == "boolean" and field_name.startswith("is_"):
                field_name = field_name[3:]
            if field_name in {"primary", "default", "public"}:
                field_name = f"{term}_{field_name}"
            attrs.append((field_name, sample_value(field, terms)))
        attrs.extend([("create_time", "createTime()"), ("update_time", "updateTime()")])
        lines.append(f"  <{term}")
        for index, (name, value) in enumerate(attrs):
            suffix = " />" if index == len(attrs) - 1 else ""
            lines.append(f"      {name}={quoteattr(value)}{suffix}")
    lines.append("</root>")
    (OUTPUT / "model.xml").write_text("\n".join(lines) + "\n")


def main() -> int:
    reuse = os.environ.get("TEAQL_REUSE_RAW") == "1"
    if (RAW.exists() or OUTPUT.exists()) and not reuse:
        print("raw/ or output/ already exists; archive it before rerunning", file=sys.stderr)
        return 2
    RAW.mkdir(parents=True, exist_ok=reuse)
    OUTPUT.mkdir(parents=True, exist_ok=reuse)
    metrics: list[dict] = []
    groups, discovered_concepts, discovery_metrics = discover_concepts()
    repair_metrics = discovery_metrics.pop("repair_requests", [])
    metrics.append(discovery_metrics)
    metrics.extend(repair_metrics)
    discovered_concepts, ambiguities, ambiguity_metrics = scan_ambiguities(discovered_concepts)
    metrics.append(ambiguity_metrics)
    write_csv(OUTPUT / "groups.csv", ["group_key", "name"], groups)
    write_csv(
        OUTPUT / "concepts-discovered.csv",
        ["concept_id", "term", "group_key", "kind", "ambiguous", "source_term", "status"],
        discovered_concepts,
    )
    write_csv(
        OUTPUT / "ambiguities.csv",
        ["concept_id", "reason"],
        ambiguities,
    )
    concepts, resolutions, resolution_metrics = resolve_concepts(
        discovered_concepts,
        ambiguities,
    )
    metrics.extend(resolution_metrics)
    write_csv(
        OUTPUT / "resolutions.csv",
        ["source_concept_id", "operation", "term", "group_key"],
        resolutions,
    )
    write_csv(
        OUTPUT / "concepts.csv",
        ["concept_id", "term", "group_key", "kind", "ambiguous", "source_term", "status"],
        concepts,
    )
    global_index = "; ".join(f"{row['concept_id']}={row['term']}" for row in concepts)
    all_fields: list[dict[str, str]] = []
    all_missing: list[dict[str, str]] = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(complete_group, key, concepts, global_index): key
            for key, _ in GROUPS
        }
        for future in as_completed(futures):
            key = futures[future]
            fields, missing, group_metrics = future.result()
            print(f"completed {key}: {len(fields)} fields, {len(missing)} missing")
            all_fields.extend(fields)
            all_missing.extend(missing)
            metrics.append(group_metrics)
    accepted_fields, field_errors = validate_fields(concepts, all_fields)
    concept_groups = {row["concept_id"]: row["group_key"] for row in concepts}
    affected_ids = {
        match.group(1)
        for error in field_errors
        if (match := re.search(r"(C\d+)", error))
    }
    affected_groups = sorted({concept_groups[concept_id] for concept_id in affected_ids})
    if affected_groups:
        replacement_fields: list[dict[str, str]] = []
        replacement_missing: list[dict[str, str]] = []
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {
                executor.submit(
                    complete_group,
                    group,
                    concepts,
                    global_index,
                    "05-fields-repair",
                ): group
                for group in affected_groups
            }
            for future in as_completed(futures):
                group = futures[future]
                fields, missing, group_metrics = future.result()
                print(f"repaired {group}: {len(fields)} fields, {len(missing)} missing")
                replacement_fields.extend(fields)
                replacement_missing.extend(missing)
                metrics.append(group_metrics)
        affected_concepts = {
            row["concept_id"] for row in concepts if row["group_key"] in affected_groups
        }
        all_fields = [
            row for row in all_fields if row.get("concept_id", "").strip() not in affected_concepts
        ] + replacement_fields
        all_missing = [
            row
            for row in all_missing
            if row.get("owner_concept_id", "").strip() not in affected_concepts
        ] + replacement_missing
        accepted_fields, field_errors = validate_fields(concepts, all_fields)
    write_csv(
        OUTPUT / "fields.csv",
        ["field_id", "concept_id", "field_name", "semantic_type", "required", "target_concept_id", "status"],
        accepted_fields,
    )
    write_csv(
        OUTPUT / "missing-concepts.csv",
        ["owner_concept_id", "term", "reason"],
        all_missing,
    )
    findings = {
        "concept_count": len(concepts),
        "field_count": len(accepted_fields),
        "ambiguous_concepts": [row for row in concepts if row["ambiguous"] == "true"],
        "missing_concepts": all_missing,
        "field_validation_errors": field_errors,
        "csv_contract_findings": list(dict.fromkeys(CONTRACT_FINDINGS)),
        "resolution_findings": list(dict.fromkeys(RESOLUTION_FINDINGS)),
        "assembly_ready": not field_errors and not all_missing,
    }
    (OUTPUT / "validation-findings.json").write_text(json.dumps(findings, indent=2) + "\n")
    (OUTPUT / "metrics.json").write_text(json.dumps(sorted(metrics, key=lambda item: item["name"]), indent=2) + "\n")
    if not field_errors:
        assemble_ksml(groups, concepts, accepted_fields)
    print(json.dumps(findings, indent=2))
    return 0 if findings["assembly_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
