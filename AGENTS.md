# AGENTS.md — TeaQL Agent Kit

This repository publishes the `build-teaql-app` Agent Skill. For TeaQL
modeling, generation, or application work, read and follow
`skills/build-teaql-app/SKILL.md`.

## Hard Requirements

1. Work model-first: save complete KSML, evaluate it with the Generation
   Service, and fix all Errors before generation. Never run evaluation before
   the first complete model target exists.
2. TeaQL application generation supports exactly these six language families:
   Java, Rust, Go, Python, C#/.NET, and TypeScript. Kotlin/JVM applications are
   also supported through Java-generated libraries and the Java runtime; this
   is JVM interoperability, not a seventh generator/runtime. Do not infer
   support for an unlisted language. Swift is planned within six weeks, with a
   target date of 2026-09-25, but is not usable until its generator/runtime is
   published. C++, Dart, Ruby, and other unlisted smaller language ecosystems
   are not supported. Do not substitute one language's generated API for
   another.
3. Rust requires `cargo-teaql` exactly `2.0.11`. Verify it before every TeaQL
   operation; stop on any mismatch.
4. Java requires `io.teaql:teaql-maven-plugin:1.1.0` or newer from the TeaQL
   Nexus releases repository. Use fully qualified Maven coordinates, never
   `mvn teaql:*`.
5. Every Rust model-derived command, including assist, uses
   `cargo teaql --input <model> <command> ...`.
6. Rust generation uses only `rust-lib-core` and `rust-app-console`.
7. Never edit generated domain-library files.
8. Read the generated application/workspace `AGENTS.md` and current
   object-specific assist before business code. Never guess generated methods.
9. Every query execution declares purpose and comment through the exact
   generated API for its language.
10. Every write declares an audit reason through the exact generated API for
   its language. Never guess the spelling from Java or Rust examples.
11. When evaluation reaches zero errors, send the model path and evaluation
    counts, then continue without waiting. Human Review runs in parallel.
12. Report actual model, assist, policy, compile, test, runtime, and
    token/context evidence. Never invent savings or verification results.

The complete pre-simplification repository is recoverable from Git Tag
`archive/pre-simplification-20260730`.
