---
name: build-teaql-app
description: "Build or change a TeaQL Java or Rust application from a natural-language business requirement. Mandatory order: first draft and save a complete KSML model, then verify the client and evaluate that saved model, repair it through repeated evaluation rounds, and generate only after evaluation reaches zero errors. Use for KSML modeling, TeaQL generation, generated assist APIs, auditable business logic, application verification, or parallel human review."
---

# Build TeaQL App

Turn a business requirement into a KSML contract and a verified TeaQL
application. Never run model evaluation before the first complete KSML model
has been written and saved.

## Mandatory Workflow Order

Do not reorder these stages:

1. Understand the requirement and choose the model target.
2. Draft and save the first complete KSML model.
3. Only after the model exists, verify the TeaQL client.
4. Evaluate the saved model.
5. Repair from the report and re-evaluate repeatedly.
6. At zero Errors, signal Model Ready and continue without waiting.
7. Generate, implement, compile, test, run, and report.

## Prepare the Model Target

1. Read the target repository's nearest `AGENTS.md`.
2. Capture the original business requirement, model target path, requested
   Java/Rust outputs, and runnable or testable outcome.
3. Keep a compact evidence ledger while working. Record commands, evaluation
   counts, generated guides, assist calls, policy checks, tests, and artifact
   paths as they occur.

Do not load a full KSML rule catalog before modeling. Use
[`references/golden-example.xml`](references/golden-example.xml) as the grammar
example and adapt its structure—not its pet-clinic concepts—to the domain.
The golden example exists only to demonstrate KSML syntax. Never carry over its
domain names (clinic, pet, appointment, species, microchipped) or its
organizational structure into a different business domain.

<!-- phase:model_generation -->
## Model First

Create and save a complete KSML model before running any TeaQL command. Do
not evaluate an absent, empty, or placeholder model target.

If the model is large (e.g., more than 15 objects), you MUST split it into multiple module files.
- Group objects by business domain into separate XML files (e.g., `auth.xml`, `operations.xml`).
- Keep each file to around 15 objects maximum to avoid exceeding generation limits.
- Create a main entry file with one outer `<root>` and include the modules using `<_include file="module.xml" />`.

Apply this minimal contract:

- Make root `name` the sole model name, in lowercase kebab-case ending with
  `-service`.
- Use `org="example"` when the user does not specify an organization.
- Put objects directly below `<root>` or within the included module files.
- Give every object `_name`, `_module`, and `_module_key`.
- Use representative literals for ordinary fields so TeaQL can infer types.
- Express a relationship as `target_object()`.
- Do not declare `id` on business objects.
- Represent reusable finite states as constant objects; only constant objects
  contain `<_value>` children.
- Use generated functions such as `createTime()` only for their intended
  semantics.
- IMPORTANT: When writing large split models, create and write the files one by one using sequential tool calls. Do not attempt to output the entire schema for all modules in a single response.

When you finish the model generation phase and evaluation passes with zero errors, output `<phase-complete>model_generation</phase-complete>`.
<!-- /phase:model_generation -->

<!-- phase:evaluate_repair -->
## Evaluate and Repair the Saved Model

Now—and only now—load
[`references/toolchains.md`](references/toolchains.md). Verify the installed
client against the exact version required by the target repository or that
reference. Stop and report a mismatch.

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

### Repair Budget

Run at most **5 evaluation–repair rounds** by default. If errors remain after
5 rounds, stop and present the current evaluation report to the user with a
summary of what was fixed and what still fails. Ask the user to provide
additional guidance or model corrections before continuing. Do not loop
indefinitely.

On small-context models (≤ 64K tokens), evaluation may be treated as
best-effort: if the evaluation report itself exceeds the available context
budget, skip detailed evaluation parsing and proceed to generation with the
best available model, noting the limitation in the work-complete report.

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

When you finish the repair phase and reach zero errors, output `<phase-complete>evaluate_repair</phase-complete>`.
<!-- /phase:evaluate_repair -->

## Generate and Implement

<!-- phase:codegen -->
Generate only the outputs requested by the user.
Use the exact Java or Rust generation commands in `references/toolchains.md`.

When generation commands complete successfully, output `<phase-complete>codegen</phase-complete>`.
<!-- /phase:codegen -->

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
