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
   explicitly accepted listed assumptions for autonomous quick try work.
3. Read `playbooks/generate-with-toolchains.md`.
4. Choose the Java Maven plugin path, the Rust Cargo CLI path, or both based on
   the user's target runtime.
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

## Quick Try vs Project Mode

- Quick try: use local directories outside the user's project repository. Do not
  require git repositories or artifact publishing. Keep generated TeaQL runtime
  code in one directory and user experiment code, query functions, and scenario
  files in another directory, connected by a local path dependency when needed.
  Quick try may call `ensure_schema()` automatically so the first local run can
  create demo tables and show real data.
- Project mode: keep lightweight TeaQL config and project-specific rules inside
  the user's repository, and pin the kit version. Treat schema creation and
  schema migration as explicit project decisions, not hidden runtime
  initialization side effects.
- Enterprise mode: keep model changes in a dedicated model repository, keep one
  or more runtime repositories for core Java/Rust application scenarios, and let
  downstream applications choose the runtime artifact that fits their scenario.
  Integrate model validation, code generation, compatibility checks, and runtime
  publishing into the enterprise CI/CD process.
  Production runtime initialization must not automatically mutate database
  schema. Run schema bootstrap, migration, or validation through an explicit
  CI/CD, DBA, admin command, or deployment workflow.
