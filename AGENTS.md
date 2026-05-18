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
7. If generating a TeaQL project, run the appropriate code generation and checks
   after the model is created.

## Code Generation Workflow

When the user asks to generate Java or Rust TeaQL code:

1. Complete the modeling workflow first.
2. Read `playbooks/generate-with-toolchains.md`.
3. Choose the Java Maven plugin path, the Rust Cargo CLI path, or both based on
   the user's target runtime.
4. Keep generated output in the target project or demo project, not in this kit
   repository.
5. Run generation, compile checks, and tests where the target project provides
   them.
6. Treat TeaQL service generated code as read-only. If generation or compilation
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
- Project mode: keep lightweight TeaQL config and project-specific rules inside
  the user's repository, and pin the kit version.
- Enterprise mode: keep model changes in a dedicated model repository, keep one
  or more runtime repositories for core Java/Rust application scenarios, and let
  downstream applications choose the runtime artifact that fits their scenario.
  Integrate model validation, code generation, compatibility checks, and runtime
  publishing into the enterprise CI/CD process.
