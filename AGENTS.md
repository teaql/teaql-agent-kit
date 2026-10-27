# AGENTS.md — TeaQL Agent Kit

This repository publishes the `build-teaql-app` Agent Skill. For TeaQL
modeling, generation, or application work, read and follow
`skills/build-teaql-app/SKILL.md`.

## Repository infrastructure

The generic context runtime lives in `packages/agent-context-kit/` as the
independently publishable `@teaql/agent-context-kit` package. Its source, host
plugins, tests and Apache-2.0 license stay inside that package. The root MIT
license and TeaQL Skill entry point remain separate.

For context-runtime or repository infrastructure changes, use `npm ci` and
`npm run check` from the root; see `docs/context-runtime.md`. The workspace root
is private and must not be published. Publish or install the explicit child
package, not the repository root. Package-local paths in host manifests remain
relative to `packages/agent-context-kit/`.

TeaQL client/evaluation/generation requirements below apply when performing
TeaQL modeling or application operations. Parser, packaging and local runtime
tests do not require invoking the Generation Service. Do not claim that the
dedicated context-policy harness already executes the complete TeaQL workflow.

## Hard Requirements

1. Work model-first: save complete KSML, evaluate it with the Generation
   Service, and fix all Errors before generation. Never run evaluation before
   the first complete model target exists.
2. TeaQL application generation supports exactly these seven language families:
   Java, Rust, Go, Swift, Python, C#/.NET, and TypeScript. Kotlin/JVM
   applications are
   also supported through Java-generated libraries and the Java runtime; this
   is JVM interoperability, not an eighth generator/runtime. Do not infer
   support for an unlisted language. C++, Dart, Ruby, and other unlisted
   smaller language ecosystems are not supported. Do not substitute one
   language's generated API for another.
3. Rust requires `cargo-teaql` exactly `2.0.14`. Verify it before every TeaQL
   operation; stop on any mismatch.
4. Java requires `io.teaql:teaql-maven-plugin:1.1.1` or newer from the TeaQL
   Nexus releases repository. Use fully qualified Maven coordinates, never
   `mvn teaql:*`.
5. Every Rust model-derived command, including assist, uses
   `cargo teaql --input <model> <command> ...`.
6. Rust generation uses only `rust-lib-core` and `rust-app-console`.
7. Never edit generated domain-library files.
8. Read the generated application/workspace `AGENTS.md` and current
   object-specific assist before business code. Never guess generated methods.
   Do not inspect generated domain-library source for API discovery. If
   progressive Assist lacks the required operation, report `MISSING_ASSIST`
   instead of searching the generated library.
9. Create each application-owned source file once. After its first compile
   attempt, repair it with the smallest localized patch; do not rewrite the
   whole file. If a repair would replace more than 25% of an existing file,
   stop and report `LARGE_REWRITE_REQUEST` with the diagnostic and reason.
10. Every query execution declares purpose and comment through the exact
   generated API for its language.
11. Every write declares an audit reason through the exact generated API for
   its language. Never guess the spelling from Java or Rust examples.
12. When evaluation reaches zero errors, send the model path and evaluation
    counts, then continue without waiting. Human Review runs in parallel.
13. Report actual model, assist, policy, compile, test, runtime, and
    token/context evidence. Never invent savings or verification results.
14. Every `<_value>` in a constant object must explicitly provide every data
    field declared by that constant object, even when a field is nullable.
    Do not repeat `_...` metadata, version, `createTime()`/`updateTime()` fields,
    or the domain-root relationship injected by runtime Fix/Context.
15. Prefer XML-aware tools or libraries to create and repair KSML. Select
    nodes structurally and check match counts; avoid repeated string/regex
    replacements. Reparse saved XML and inspect the diff before semantic
    evaluation. Follow the Skill's "Edit KSML as XML" guidance.

16. Before every model-derived TeaQL operation, run the bundled runtime
    provenance helper from the Agent host (or transfer its fresh context for
    SSH execution). Stamp actual current Agent/version/provider/model on the
    entry root; preserve model_uuid and never use default config as run identity.

The complete pre-simplification repository is recoverable from Git Tag
`archive/pre-simplification-20260730`.
