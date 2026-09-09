---
name: build-teaql-app
description: "Build or change a TeaQL application in Java, Rust, Go, Swift, Python, C#/.NET, or TypeScript, including Kotlin/JVM applications that consume Java-generated libraries. Mandatory order: first draft and save a complete KSML model, then verify the client and evaluate that saved model, repair it through repeated evaluation rounds, and generate only after evaluation reaches zero errors. Use for KSML modeling, seven-language TeaQL generation, generated assist APIs, auditable business logic, application verification, or parallel human review."
---

# Build TeaQL App

Turn a business requirement into a KSML contract and a verified TeaQL
application. Never run model evaluation before the first complete KSML model
has been written and saved.

## Core Operating Contract (`compact-v1`)

Build the requested business outcome through Vibe Coding. Understand the
project from application-owned workspace documentation and generated
`AGENTS.md`. Use model-aware Assist only for the next application edit. Treat
generated domain-library source as opaque. Verify through evaluation,
compilation, tests, runtime execution, and retained evidence.

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
   language and outputs, and runnable or testable outcome. Supported language
   families are Java, Rust, Go, Swift, Python, C#/.NET, and TypeScript. A
   Kotlin/JVM application uses the Java-generated library and Java runtime; do not look
   for a separate Kotlin generator. Swift uses the `swift-lib-core` target for
   a generated Swift package with local SQLite and TFP client support. C++,
   Dart, Ruby, and other unlisted smaller language ecosystems are not supported.
3. Keep a compact evidence ledger while working. Record commands, evaluation
   counts, generated guides, assist calls, policy checks, tests, and artifact
   paths as they occur.

Do not load a full KSML rule catalog before modeling. Use
[`references/golden-example.xml`](references/golden-example.xml) as the grammar
example and adapt its structure—not its pet-clinic concepts—to the domain.
The golden example exists only to demonstrate KSML syntax. Never carry over its
domain names (clinic, pet, appointment, species, microchipped) or its
organizational structure into a different business domain.

<!-- BLOCK_ID: phase_modeling -->
## Model First

Create and save a complete KSML model before running any TeaQL command. Do
not evaluate an absent, empty, or placeholder model target.

If the model is large (e.g., more than 15 objects), you MAY split it into
multiple module files using `<_include file="module.xml" />`, but this is
optional. The system supports dynamic output limits so a single-file model
will also work.

For a split model, follow the complete
[`multi-file-golden-example`](references/multi-file-golden-example/README.md).
Every included file MUST be a well-formed XML document with exactly one
top-level `<root>` element. Put all module objects inside that `<root>`.
Never write multiple bare top-level objects in an included file. Only the
entry file's `<root>` carries service-level attributes such as `name`, `org`,
`data_service`, and `_module_key`; an included module normally uses plain
`<root>...</root>`.

Incorrect included file:

```xml
<customer_account ... />
<sales_order ... />
```

Correct included file:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root>
  <customer_account ... />
  <sales_order ... />
</root>
```

- **CRITICAL**: To avoid keyword collisions in any of the seven generated
  languages, **ALWAYS use two-word field names and entity names** when there
  is any risk of conflict (e.g. use `bonus_type` instead of `type`,
  `move_order` instead of `move`, `leave_type` instead of `type`). Do not use
  bare single words like `type` or `move` as entity or field names.

Apply this minimal contract:

- Make root `name` the sole model name, in lowercase kebab-case ending with
  `-service`.
- Use `org="example"` when the user does not specify an organization.
- Put objects directly below `<root>` or within the included module files.
- Give every object `_name`, `_module`, and `_module_key`.
- Use representative literals for ordinary fields so TeaQL can infer types.
- Choose types by domain meaning: use `integer()` or `long()` for ordinal,
  count, and whole-percentage fields such as `display_order` and `progress`
  (`0`-`100`); reserve `number()` for values that need decimal semantics, such
  as precise ratios or amounts.
- Express a relationship as `target_object()`.
- Do not declare `id` on business objects.
- Represent reusable finite states as constant objects; only constant objects
  contain `<_value>` children.
- In a constant object, every `<_value>` must explicitly provide every declared
  data field, including `id`, `name`, `code`, and additional fields such as
  `display_order`, `color`, or `progress`. Nullable declarations still require
  a concrete representative value. Do not repeat `_...` model metadata,
  version, Fix-managed `createTime()`/`updateTime()` fields, or the domain-root
  relationship injected from context in each `<_value>`.
- Use generated functions such as `createTime()` only for their intended
  semantics.
- IMPORTANT: When writing large split models, create and write the files one by one using sequential tool calls. Do not attempt to output the entire schema for all modules in a single response.

### Validation Pitfalls — Avoid on First Attempt

These are the most common first-attempt failures. Avoiding them saves multiple
repair rounds:

1. **Non-empty attribute values.** EVERY attribute MUST have a non-empty
   representative value. Never write `attr=""` or `attr=" "`. Use a realistic
   example (e.g., `email="john@example.com"`, `url="https://example.com/doc.pdf"`).
2. **Language keyword avoidance.** Entity and field names must not collide with
   programming language keywords (Rust: `move`, `type`, `match`, `self`, `ref`,
   `mod`, `box`, `trait`, `impl`, `use`, `let`, `fn`, `async`, `yield`;
   Java/C#: `class`, `new`, `import`, `public`, `default`, `return`;
   Go: `type`, `map`, `range`, `go`, `select`, `interface`;
   Swift: `class`, `struct`, `protocol`, `extension`, `actor`, `associatedtype`,
   `inout`, `some`, `any`, `Self`, `init`, `deinit`, `subscript`, `operator`;
   Python: `class`, `def`, `from`, `import`, `lambda`, `yield`;
   Kotlin/JVM application code: `object`, `when`, `is`, `fun`, `val`, `var`;
   TypeScript: `class`, `interface`, `function`, `import`, `export`, `typeof`;
   SQL: `select`, `table`, `transaction`). When a natural business concept is a
   single keyword (e.g., "move"), always use a **two-word compound name** instead
   (e.g., `move_order`, `move_task`, `type_code`, `match_record`).
3. **Privacy audit masking.** Person-like objects (`user`, `customer`, `employee`,
   `driver`, etc.) that hold sensitive fields (`password`, `password_hash`,
   `token`, `magic_link_token`, `api_key`, `secret`, `ssn`, `id_card`,
   `mobile_phone`) MUST declare `_audit_mask_fields` listing those fields.
   Example: `<user _audit_mask_fields="password_hash,magic_link_token" .../>`
4. **No circular reference chains.** If A references B, B references C, and C
   references A, the parser may fail at depth limit. Keep reference chains short
   and acyclic.
5. **Audit log user field.** Logging/audit objects (`audit_log`, `change_log`,
   etc.) MUST include a recognizable user/operator field (e.g.,
   `operator="user()"`, `actor="user()"`).
6. **No isolated entities (Disconnected Graphs).** To avoid `KSML-DOMAIN-ROOT-002`, ensure that ALL entities are connected via relationships (references) to the main graph. Do not leave any entity as an isolated island. Every object should either reference another object or be referenced by another object in the domain model.
7. **No XML special characters in attribute values.** Never use `&`, `<`, `>`,
   `"` directly in attribute values. Use `and` instead of `&` (e.g.,
   `_module="Operations and Logistics"` not `_module="Operations & Logistics"`).
8. **Complete constant value records.** Every `<_value>` must provide every
   declared constant data field. A nullable type declaration does not permit a
   value record to omit that business field. Version, Fix-managed
   `createTime()`/`updateTime()` fields, and the domain-root relationship are
   runtime managed and omitted from each row.

   ```xml
   <school_type platform="platform()" id="id()" name="string()"
                code="string()" display_order="integer()" color="string()?"
                _constant="true" _identifier="code">
     <_value id="1001" name="Primary" code="PRIMARY"
             display_order="1" color="#2563EB"/>
     <_value id="1002" name="Secondary" code="SECONDARY"
             display_order="2" color="#16A34A"/>
   </school_type>
   ```

   Constant `color` values use the portable `#RRGGBB` form; named CSS colors
   such as `blue` or `green` do not satisfy `KSML-UI-012`.

When you finish the model generation phase and evaluation passes with zero errors, output `<phase-complete>model_generation</phase-complete>`.

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
IMPORTANT: If your model is split into multiple files in a directory (e.g., `models/`), you MUST pass the directory path (e.g., `--input models/`), NOT the main entry file (`main.xml`). Passing only the main file will cause the evaluator to fail with missing included files.

Repair from the Markdown evaluation report:

1. Fix all Errors, largest repeated pattern first.
2. Preserve Solids and already-correct model sections.
3. Re-evaluate after each repair round.
4. Resolve Warnings using the business requirement.
5. Treat Suggestions as optional.
6. Follow the report's concrete repair guidance rather than guessing or
   memorizing a separate rule catalog.
7. **IMPORTANT:** When dealing with extremely long evaluation logs (e.g., thousands of lines), DO NOT use paginated reading commands (like `sed -n '1,300p'`) in an endless loop to read the entire file. Use targeted `grep` (e.g., `grep -A 15 -B 5 "Error"` or `grep -A 10 -B 10 "error:"`) or read only the head/tail to quickly isolate and fix issues without wasting context.

Do not generate from a model with errors.

### Repair Budget

Run at most **5 evaluation–repair rounds** by default. If errors remain after
5 rounds, stop and present the current evaluation report to the user with a
summary of what was fixed and what still fails. Ask the user to provide
additional guidance or model corrections before continuing. Do not loop
indefinitely.

On small-context models, keep the zero-error evaluation gate. Read the summary
and only the reported error locations needed for the current repair round; do
not stream the complete report into context. If the remaining errors cannot be
resolved within the repair or context budget, stop with the current report.
Never proceed to generation with evaluation errors.

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

CRITICAL: Do NOT output `<phase-complete>evaluate_repair</phase-complete>` if there are ANY `❌ Errors (Must Fix)` listed in the text output of your evaluation command, even if the command execution returned `success=true` (which can happen if you pipe to `tee`). You MUST open the corresponding XML files and fix the errors (e.g., renaming fields that conflict with Rust keywords) before outputting the phase-complete tag.

When you finish the repair phase and reach zero errors, output `<phase-complete>evaluate_repair</phase-complete>`.
<!-- /BLOCK_ID: phase_modeling -->

## Generate and Implement

<!-- BLOCK_ID: phase_codegen -->
Generate only the outputs requested by the user.
Use the exact language target and verification guidance in
`references/toolchains.md`. Generate only targets actually advertised by the
Generation Service; never manufacture a target name.

IMPORTANT: If your model is split into multiple files in a directory (e.g., `models/`), you MUST pass the directory path (e.g., `--input models/`), NOT the main entry file (`main.xml`) to the generation commands. Passing only the main file will cause the generation to fail with missing included files.

CRITICAL: Do NOT output `<phase-complete>codegen</phase-complete>` if ANY generation command returns an error or `success=false`. You MUST fix the command (e.g., incorrect directory paths) and retry until it succeeds. 
WARNING: When chaining commands, do NOT use `cd dir && cmd && cd dir && cmd`. The second `cd` will fail because you are already in `dir`. Instead, use `cd dir && cmd1 && cmd2` or use subshells `(cd dir && cmd1) && (cd dir && cmd2)`.

### CLI path semantics

`--cwd` is the base directory for every relative `--output` path. When both
flags are present, pass the workspace directory once: use an absolute
`--cwd /path/to/app-playground` together with a child-only output such as
`--output rust-lib-core`. Never repeat the cwd suffix in output (for example,
do not combine `--cwd app-playground` with
`--output app-playground/rust-lib-core`), because that creates
`app-playground/app-playground/rust-lib-core`.

Before generation, resolve the intended output path conceptually as
`<cwd>/<relative-output>` and confirm it equals the requested destination. An
absolute `--output` is also valid and is not joined to `--cwd`, but do not mix
the two styles within one generation run.

When generation commands complete successfully with `success=true`, output `<phase-complete>codegen</phase-complete>`.
<!-- /BLOCK_ID: phase_codegen -->

- Follow the `compact-v1` contract above. If the generated application
  `AGENTS.md` is missing, stop and report it. Never prefetch Assist or guess a
  generated method.
- For queries, first request `<language>-assist-query/<entity>` using the exact
  KSML entity name. This returns the executable base query and a compact field
  index. Before using a field-specific select, filter, order, group, facet, or
  aggregate method, request
  `<language>-assist-query/<entity>.<field>` using the exact case-sensitive
  KSML field name from that index. Do not translate `snake_case` KSML into a
  language member name in the Assist location, and do not request nested paths
  such as `order.customer.name`. Query Assist is intentionally progressive so
  the agent does not load every combinatorial field API into context.
- If current entity/action and required field Assist do not expose the needed
  operation, stop that path and report
  `MISSING_ASSIST` with the language, entity, action, missing operation, and
  exact compiler diagnostic when available.
- Generated-source fallback is never self-authorized. Only after the user or
  orchestrator explicitly authorizes it, read the bounded request format in
  [references/source-fallback.md](references/source-fallback.md).
- Keep editable business logic in the generated application workspace. Read
  `TOOL_API_GUIDE.md` or `RUNTIME_CUSTOM_GUIDE.md` only when the next edit
  directly needs that integration; guides are not verification evidence.
- Create an application-owned file once. After its first compile attempt,
  follow the patch-only repair loop in
  [references/incremental-editing.md](references/incremental-editing.md).

Enforce the API constraint harness:

- Every query execution has purpose and comment through the generated
  language-specific API. Comment may be added earlier in the query chain;
  purpose is the capability boundary that exposes execution.
- Every save/update has an audit reason through the generated
  language-specific API.
- Read progressive model-aware Assist before using those APIs. Java and Rust
  spellings are examples, not names to copy into Go, Swift, Python, .NET, or
  TypeScript.
- Use the identity/request context required by the generated API.

Compile, test, and smoke-test the requested result. Repair model-derived
problems at the model level and regenerate.

For a verification-only task in which no business code will be written, use
only evaluation summaries, build/test output, runtime output, and artifact
hashes. Generated source, unused Assist, and implementation guides are outside
the verification scope.

### Runtime source selection

Do not edit a generated dependency declaration to switch between a local
runtime checkout and a published runtime. If the target repository contains
`teaql-workspace.yaml`, run the repository's `teaql_workspace.py verify`
before compiling and retain its output as evidence.

- In `workspace` mode, the config must resolve each selected runtime to a Git
  repository. Record its absolute path, commit, and dirty state. Apply the
  language's native workspace override outside the generated domain library.
- In `release` mode, every runtime must declare a package and version; local
  path, patch, replace, editable install, or project-reference overrides are
  forbidden.
- KSML may declare the required runtime version, but it never declares local
  paths. The generator always emits published dependency coordinates.
- Runtime repository examples use repository-local source. Published release
  regression belongs in a separate consumer workspace.

Use [`../../examples/teaql-workspace.workspace.yaml`](../../examples/teaql-workspace.workspace.yaml)
as the seven-language workspace configuration example.

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
