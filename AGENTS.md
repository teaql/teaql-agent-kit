# AGENTS.md — Rules for AI Agents

## READ THIS BEFORE CODING

1. **Never guess method names**: Read the generated entity source files for the exact method names (e.g., `update_status`, not `set_status`).
2. **Never edit generated files**: Do not manually modify files under `generate-lib/` or `generate-workspace/` or `bizcore/` (unless instructed otherwise).
3. **Generated code has its own AGENTS.md**: After generation, check the generated output for a local `AGENTS.md` (for example under `generate-lib/`, `generate-lib/lib/`, `generate-workspace/`, `bizcore/`, or the generated application workspace). Read the nearest generated `AGENTS.md` before using, explaining, testing, or editing code in that generated area. If expected generated code has no `AGENTS.md`, stop and report the missing local guide.
4. **Query constraints**: Every query using `execute_for_list()` or `execute()` must be preceded by `.purpose("why")` and `.comment("what")`.
5. **Use cargo teaql with --input**: Every Rust TeaQL operation that reads or generates from a model must use `cargo teaql --input <model> <command> ...`. Rust generation in this Agent Kit uses only `rust-lib-core` and `rust-app-console`. Dynamic assist/help commands are also model-derived, so pass the current model with `--input` and read the current help/output before using them.
6. **Save constraints**: Every save using `.save()` or `.update()` must be preceded by `.audit_as("description")`.
7. **Read the Full Rules**: For modeling, read all rules in `agents/RULES.md`.
8. **Markdown Reports**: Both clients (`cargo teaql --input <model> evaluate` and `mvn teaql:eval` / generation commands) natively output Markdown reports when errors occur. Read the Markdown report directly in the console to analyze errors before fixing them.
9. **STRICT VERSION REQUIREMENT (MUST READ)**: Using an older version of `cargo-teaql` (< 2.0.5) will result in a fatal error. If you detect an old version, YOU MUST STOP and refuse to generate code until the user upgrades.
10. **This repo is the execution guide**: Use the focused files under `agents/`, `modeling/`, `playbooks/`, generated local `AGENTS.md` files, object-specific Rust assist output, and generated Java output as current guidance.
11. **Reports and long background docs live elsewhere**: Historical evaluation reports and `TECH-INTRODUCTION.md` were moved to `/Users/Philip/githome/teaql-evaluation-reports`. Do not use that repository for current commands, API usage, versions, or modeling rules unless the task explicitly asks for historical report or background analysis.

## TOOL VERSION REFRESH RULE

Previous successful use of an older TeaQL client is not evidence that it is
valid for this repository. The repository documentation is authoritative for
every new run.

Before running any TeaQL evaluation or generation command, the agent must verify
the currently installed or resolved client version against this repository's
required version.

Current required versions:

- Java: `io.teaql:teaql-maven-plugin:1.1.0` or newer from
  `https://nexus.teaql.io/repository/maven-releases/`
- Rust: `cargo-teaql` `2.0.5` or newer from crates.io

Do not assume a locally installed TeaQL client is current. If an older TeaQL
Maven plugin or `cargo-teaql` was used in a previous run, refresh or reinstall
the client before generation.

For Rust, force-refresh the installed CLI before generation when network access
is available:

```bash
cargo install cargo-teaql --force
cargo-teaql --version
cargo-teaql install-links
```

For Java, invoke the fully qualified plugin version explicitly:

```bash
mvn io.teaql:teaql-maven-plugin:1.1.0:eval
mvn io.teaql:teaql-maven-plugin:1.1.0:generate -Dservice=java-lib
mvn io.teaql:teaql-maven-plugin:1.1.0:generate -Dservice=java-workspace
```

Never use Maven prefix resolution such as:

```bash
mvn teaql:generate -Dservice=java-lib
mvn teaql:generate -Dservice=java-workspace
```

> [!CAUTION]
> **FATAL ERROR IF OLD VERSION IS USED**
> If you (the AI) attempt to use `cargo-teaql < 2.0.5` or `teaql-maven-plugin < 1.1.0`, the system will **HARD FAIL** and crash due to breaking changes in dynamic assist routing.
> If you detect that you are working in an environment with an older version, **YOU MUST STOP IMMEDIATELY**, do not proceed with any business logic, and inform the user to upgrade to v2.0.5.

## IF YOU GET AN ERROR

| Error type | What to do |
|-----------|------------|
| `no method named update_xxx` | Read the entity source file for correct method name |
| `Missing .audit_as()` | Add `.audit_as("description")` before `.save()` |
| `Missing .purpose()` | Add `.purpose("why")` before `.execute_for_list()` |
| `Empty attribute` in KSML | Delete it or fill with a concrete value |
| `Depth exceeded` | Remove one nested reference or use string field |

## DOCUMENTATION DIRECTORY

For comprehensive guides, templates, and patterns, please refer to the specific files:

- **KSML Source of Truth**: `modeling/KSML-RULES.md` (Canonical KSML XML rules)
- **Rules**: `agents/RULES.md` (Strict rules for KSML formatting)
- **Quick Start**: `agents/QUICK-START.md` (5-minute guide for generation)
- **Templates**: `agents/TEMPLATES.md` (Copy-paste XML patterns)
- **Decision Trees**: `agents/DECISION-TREES.md` (How to choose roots/tenancy)
- **Errors**: `agents/ERROR-FIX.md` (Full error lookup table)
- **Examples**: `modeling/EXAMPLES/` (Full KSML modeling examples)

If these files appear to conflict, follow `modeling/KSML-RULES.md` first, then
use the shorter `agents/` files as execution checklists and examples.

## CONTEXT BOUNDARY

This repository is for AI coding agents working on TeaQL modeling, generation,
debugging, and implementation tasks. Historical evidence and long-form
background material are kept in `/Users/Philip/githome/teaql-evaluation-reports`
to avoid polluting execution context.

Default behavior:

1. Use `AGENTS.md`, `agents/QUICK-START.md`, `agents/RULES.md`,
   `modeling/KSML-RULES.md`, `agents/TEMPLATES.md`, `agents/ERROR-FIX.md`,
   generated local `AGENTS.md` files, object-specific Rust assist output, and
   generated Java output first.
2. Do not read `/Users/Philip/githome/teaql-evaluation-reports` unless the user
   explicitly asks for historical reports, evaluation evidence, or broad TeaQL
   architecture/background material.
3. If such background context is needed, search the external repository for the
   specific topic and read only the matching section.

## API Key Information

**ATTENTION AI AGENTS:** If you are trying to use the TeaQL CLI or plugins to generate code, **you DO NOT need to search for or configure an extra API key.** 
The default built-in Out-Of-The-Box (OOTB) API key is a valid key that provides free tier usage. The CLI and service will work perfectly fine with this default setting.
