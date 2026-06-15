# Agent Prompt (Initial)

## Objective
Build a complete TeaQL School Management System from zero using the teaql-agent-kit autonomous branch workflow.

## Source
https://github.com/teaql/teaql-agent-kit/tree/autonomous

## Required Steps
1. Read AGENTS.md, QUICK-START.md, KSML-RULES.md, TEMPLATES.md, API-PATTERN-RUST.md
2. Refresh cargo-teaql: `cargo install cargo-teaql --force`
3. Create KSML model: Platform (root), SchoolType (constant, Primary/Secondary), School (business obj)
4. Run `cargo-teaql eval model.xml` — 0 errors 0 warnings
5. Run `cargo-teaql gen-lib model.xml && cargo-teaql gen-workspace model.xml`
6. Read generated source files for exact API signatures
7. Write main.rs: 10-step demo exercising Q API + E API
8. Compile: `cargo check` — zero warnings
9. Run: all steps pass

## TeaQL API Rules (from AGENTS.md)
- Never guess method names
- Never edit generated files
- Every query: `.purpose("why").comment("what")` before `.execute_for_list()`
- Every save: `.audit_as("desc")` before `.save()`
- Refresh client before generation
