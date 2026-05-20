# TeaQL Vibe Kit Agent Instructions

This repository is the agent-native entry point for TeaQL vibe coding.

## Core Rule

Use TeaQL as Semantic Guardrails for AI Coding. Do not jump directly from vague
business requirements to arbitrary application code. First create a semantic
domain model, then generate Java or Rust TeaQL code from that model.

## Modeling Workflow

When the user asks to model a business domain:

1. Read `playbooks/model-from-natural-language.md`.
2. Use `prompts/modeling/system.md` as the modeling role.
3. Use `prompts/modeling/ksml-rules.md` as the source of truth for KSML XML.
4. Use `prompts/modeling/task-template.md` to frame the user's domain.
5. Produce a `model.xml` candidate.
6. Validate the model against `prompts/modeling/checklist.md`.
7. If generating Java or Rust TeaQL code, run the model review gate in
   `playbooks/model-review-gate.md` and get confirmation before generation.
8. If generating a TeaQL project, run the appropriate code generation and checks
   after the model is created.

## Code Generation Workflow

When the user asks to generate Java or Rust TeaQL code:

1. Complete the modeling workflow first.
2. Complete the model review gate in `playbooks/model-review-gate.md`. Do not
   generate TeaQL service code until the model is confirmed or the user has
   explicitly accepted listed assumptions for autonomous playground work.
3. Read `playbooks/generate-with-toolchains.md`.
4. Choose the Java Maven plugin path, the Rust Cargo CLI path, or both based on
   the user's target runtime. For Java, use the TeaQL Maven plugin from Maven
   Central or the configured Maven repository. For Rust, use `cargo-teaql` from
   crates.io. Do not clone, search for, or build local or remote toolchain source
   code for normal generation work. If the generation client cannot be
   installed, resolved, invoked, or executed, stop immediately and report the
   blocker instead of trying source builds or alternate generation paths.
5. Keep generated output in the target project or demo project, not in this kit
   repository.
6. Run generation, compile checks, and tests where the target project provides
   them.
7. Treat TeaQL service generated code as read-only. If generation or compilation
   fails because the model is wrong, update `model.xml` and regenerate instead
   of hand-editing generated code.

## Generated Code Rule

TeaQL service generated Java or Rust code must not be modified directly.

If generated code is wrong, fix the semantic model, generator configuration,
TeaQL generator, or TeaQL runtime, then regenerate. Customer code, playground
code, query functions, tests, runtime wiring, and integration configuration may
be edited, but generated TeaQL service code is not a maintenance surface.

The only acceptable exception is an explicitly requested temporary investigation
patch. Such a patch must be reported as temporary and must not be presented as a
deliverable project change.

## Query API Rule

When a task needs dynamic query construction, such as user-selected fields,
runtime-selected operators, or other filters that are not known at compile time,
use the high-level TeaQL JSON query APIs:

- Rust: use `find_with_json_expr`.
- Java / Spring Boot: use the documented `findByJson` /
  `findWithJsonExpr` dynamic query surface.

Reference:
<https://teaql.io/docs/working-with-teaql-and-springboot/find-by-json-dynamic-query>

These dynamic query APIs support field filters, chain-field filters, sorting,
offset/limit, and page/page-size. Do not build dynamic application queries by
calling lower-level filter primitives such as Rust `add_filter` or Java
`addFilter` directly. Keep fixed business and security constraints, such as
tenant scope and permission boundaries, in typed TeaQL request code around the
dynamic JSON query.

## Rust Entity Creation Rule

When Rust customer code, playground code, examples, or tests need to create a
new TeaQL entity instance, use the generated `Q` collection factory:

```rust
let entity = Q::<entities>().new_entity(&ctx);
```

For example, use `Q::products().new_entity(&ctx)` for a `product` entity. Do not
construct generated entity structs directly with struct literals, `Default`, or
ad hoc builders in customer code. The `Q` factory is the semantic creation
surface that keeps context-aware defaults, generated conventions, and future
runtime hooks in one place.

## Output Discipline

- For pure modeling tasks, output only valid KSML XML unless the user asks for an
  explanation.
- For implementation tasks, keep generated artifacts in the target project, not
  in this kit repository.
- Do not edit generated Java or Rust TeaQL service files directly. Update the
  model, generator configuration, TeaQL generator, or runtime, then regenerate.
- If a business rule is ambiguous, write a short assumption before generating
  code, or encode the safest domain assumption in the model when the user asked
  for autonomous execution.

## Working Modes

- Playground mode: use an `app-playground` directory outside the user's project
  repository. Do not require git repositories or artifact publishing. Put the
  generated `model.xml` and related model inputs under `app-playground/models`,
  and put generated TeaQL runtime code under `app-playground/generate-lib` so
  users can review both in one playground. Keep user experiment code, query
  functions, and scenario files in normal playground source/test directories,
  connected to the generated library by a local path dependency when needed.
  Playground mode may call `ensure_schema()` automatically so the first local
  run can create demo tables and show real data.
- Debugging mode: only enter this mode when the user explicitly asks to debug
  TeaQL toolchains, generated output, or integration failures. State that the
  task has switched to debugging mode before using local toolchain source
  repositories, source checkouts, temporary investigation patches, or other
  actions forbidden in playground mode.
- Future modes may be added later. Until a mode is explicitly defined, use
  playground mode for local trials and debugging mode only for explicit
  debugging requests.

## Generation Client Stop Rule

For normal generation, the Java and Rust generation clients are the boundary of
the workflow:

- Java: TeaQL Maven plugin from Maven Central or the configured Maven
  repository.
- Rust: `cargo-teaql` from crates.io.

If either generation client cannot be installed, resolved, invoked, or executed,
stop immediately and report the exact blocker. Do not search for source code,
clone a repository, build a local toolchain, hand-write generated service code,
patch generated service code, or try an alternate generation path unless the
user explicitly switches the task to debugging mode.
