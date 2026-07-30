---
name: build-teaql-app
description: Build or change a TeaQL Java or Rust application from a natural-language business requirement. Use when a task involves KSML domain modeling, TeaQL model evaluation, typed domain generation, generated assist APIs, auditable query/save implementation, application verification, or reporting a model and runnable result for parallel human review.
---

# Build TeaQL App

Turn a business requirement into an evaluated KSML contract and a verified
TeaQL application. Work autonomously through modeling, generation,
implementation, and verification; notify the user when the model is ready so
human review can happen in parallel.

## Establish the Contract

1. Read the target repository's nearest `AGENTS.md`.
2. Before any TeaQL evaluation or generation, verify the installed client
   against the exact version required by that repository, or the defaults in
   [`references/toolchains.md`](references/toolchains.md). Stop and report a
   mismatch.
3. Capture the original business requirement, model target path, requested
   Java/Rust outputs, and runnable or testable outcome.
4. Keep a compact evidence ledger while working. Record commands, evaluation
   counts, generated guides, assist calls, policy checks, tests, and artifact
   paths as they occur.

Do not load a full KSML rule catalog before modeling. Use
[`references/golden-example.xml`](references/golden-example.xml) as the grammar
example and adapt its structure—not its pet-clinic concepts—to the domain.

## Model First

Create and save one complete KSML model before generating application code.

Apply this minimal contract:

- Use one outer `<root>`.
- Make root `name` the sole model name, in lowercase kebab-case ending with
  `-service`.
- Use `org="example"` when the user does not specify an organization.
- Put objects directly below `<root>`.
- Give every object `_name`, `_module`, and `_module_key`.
- Use representative literals for ordinary fields so TeaQL can infer types.
- Express a relationship as `target_object()`.
- Do not declare `id` on business objects.
- Represent reusable finite states as constant objects; only constant objects
  contain `<_value>` children.
- Use generated functions such as `createTime()` only for their intended
  semantics.

Submit the complete model target to the repository's Generation Service
evaluation command. For Rust, every model-derived operation must include:

```bash
cargo teaql --input <model-file-or-directory> evaluate
```

Repair from the Markdown evaluation report:

1. Fix all Errors, largest repeated pattern first.
2. Preserve Solids and already-correct model sections.
3. Re-evaluate after each repair round.
4. Resolve Warnings using the business requirement.
5. Treat Suggestions as optional.
6. Follow the report's concrete repair guidance rather than guessing or
   memorizing a separate rule catalog.

Do not generate from a model with errors.

## Signal Model Ready

As soon as evaluation reaches zero errors, notify the user without pausing:

```text
Model Ready
- Model: <absolute model path>
- Evaluation: passed — <errors>, <warnings>, <suggestions>
```

Continue working. Human model or application review is asynchronous, not an
approval gate. Incorporate review feedback when it arrives, then re-evaluate
and regenerate if the domain contract changed.

## Generate and Implement

Generate only the outputs requested by the user.
Load [`references/toolchains.md`](references/toolchains.md) now, not during
modeling, and use its exact Java or Rust commands.

- Never edit generated domain-library files.
- Find and read the generated local `AGENTS.md` before business code. If an
  expected generated application guide is missing, stop and report it.
- Read current model-aware help and object-specific assist for each
  entity/action. Never guess generated methods.
- Inspect generated source only when the local guide permits it or assist is
  incomplete; record the reason.
- Keep editable business logic in the generated application workspace.

Enforce the API constraint harness:

- Every query execution has `.purpose("why")` and `.comment("what")`.
- Every Rust `.save()` or `.update()` has `.audit_as("description")`.
- Every Java save/update has the generated equivalent, normally
  `.auditAs("description")`.
- Use the identity/request context required by the generated API.

Compile, test, and smoke-test the requested result. Repair model-derived
problems at the model level and regenerate.

## Report Work Complete

Load
[`references/work-complete.md`](references/work-complete.md) only after the
requested result—not evaluation alone—is complete. Report actual evidence:

- original requirement and modeling result;
- model path and final evaluation counts;
- generated guide and exact assist/API facts used;
- query and write policy coverage;
- generated files left untouched;
- compile, test, and runtime results;
- token/context usage honestly, with estimates labeled;
- mechanical review work completed and business judgment still needed;
- one simple next-use command and a short chronological log.

Never invent token savings, harness evidence, or verification results.
