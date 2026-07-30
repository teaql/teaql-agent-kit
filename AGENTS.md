# AGENTS.md — TeaQL Agent Kit

This repository publishes the `build-teaql-app` Agent Skill. For TeaQL
modeling, generation, or application work, read and follow
`skills/build-teaql-app/SKILL.md`.

## Hard Requirements

1. Work model-first: save complete KSML, evaluate it with the Generation
   Service, and fix all Errors before generation.
2. Rust requires `cargo-teaql` exactly `2.0.10`. Verify it before every TeaQL
   operation; stop on any mismatch.
3. Java requires `io.teaql:teaql-maven-plugin:1.1.0` or newer from the TeaQL
   Nexus releases repository. Use fully qualified Maven coordinates, never
   `mvn teaql:*`.
4. Every Rust model-derived command, including assist, uses
   `cargo teaql --input <model> <command> ...`.
5. Rust generation uses only `rust-lib-core` and `rust-app-console`.
6. Never edit generated domain-library files.
7. Read the generated application/workspace `AGENTS.md` and current
   object-specific assist before business code. Never guess generated methods.
8. Every query execution declares `.purpose("why")` and `.comment("what")`.
9. Every write declares `.audit_as("description")` in Rust or the generated
   Java equivalent, normally `.auditAs("description")`.
10. When evaluation reaches zero errors, send the model path and evaluation
    counts, then continue without waiting. Human Review runs in parallel.
11. Report actual model, assist, policy, compile, test, runtime, and
    token/context evidence. Never invent savings or verification results.

The complete pre-simplification repository is recoverable from Git Tag
`archive/pre-simplification-20260730`.
