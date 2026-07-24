# Model From Natural Language

Use this playbook when a user describes a business application in natural
language and wants a TeaQL/KSML domain model.

## Inputs

- Business domain name or description.
- Optional target runtime: Java, Rust, or both.
- Optional constraints: required entities, workflow states, tenant model,
  reporting needs, authorization boundaries, or existing database concepts.

## Steps

1. Normalize the domain name.
   - `alias_model_name`: snake_case.
   - `english_name`: Title Case.
   - `chinese_name`: translate the domain name when possible.
   - `name`: kebab-case plus `-service`.

2. Identify the core model.
   - Do not assume multi-tenancy by default.
   - Classify tenancy as single-tenant, multi-tenant, platform-managed
     multi-tenant, or undecided.
   - Add platform, merchant, tenant, employee, organization, company, school,
     hospital, store, or similar baseline objects only when they are real
     business concepts or confirmed architecture assumptions.
   - Add concrete business objects for the domain.
   - Add constant objects for status, category, kind, classification, gender,
     priority, and finite enumerations.
   - Do not use object or attribute names that exactly match reserved keywords in
     Java, JavaScript, Dart, Rust, Go, or Python.
   - Do not use attribute names that exactly match SQL2016 reserved keywords.

3. Organize modules.
   - Use `_module` as the first-level menu display name.
   - Use `_module_key` as lowercase kebab-case.
   - Put constants in `Basic Data` unless a process-specific module is clearer.
   - Avoid single-object modules.
   - Count business and constant objects together. When the total is greater
     than 20, prefer a multi-file model split by business subdomain.
   - If a subdomain still contains more than 20 objects, split it again by a
     smaller cohesive business process and use nested includes.

4. Generate KSML XML.
   - Use `prompts/modeling/ksml-rules.md`.
   - Use `prompts/modeling/task-template.md`.
   - For 20 or fewer objects, output one `model.xml` with direct child objects.
   - For more than 20 objects, create a model directory whose mandatory
     entrypoint is `main.xml`. Keep authoritative root metadata there and add
     `<_include>` entries for subdomain XML files.
   - Wrap each included file in `<root>`. Treat its objects as direct children
     of the logical root after expansion.

5. Validate before delivery.
   - Use `prompts/modeling/checklist.md`.
   - Repair any rule violation.
   - Pay special attention to constant object rules and explicit tenancy.
   - If a TeaQL client toolchain with `evaluate` is available, run server-side KSML
     evaluation after checklist validation and before code generation. Fix
     evaluation `errors`; carry `warnings` and `suggestions` into the model
     review.
   - For a multi-file model, pass the complete directory to TeaQL. Passing only
     `main.xml` omits the included files from the upload.

6. Run the model review gate before code generation.
   - Use `playbooks/model-review-gate.md`.
   - Summarize entities, fields, relationships, tenancy classification, tenant
     boundary if any, constants, and assumptions in business language.
   - Get user confirmation, or record explicit assumptions when the user asked
     for autonomous playground execution.
   - If the user asks for changes, update the single-file model or the affected
     subdomain files, validate again, and repeat the review gate.

## Done

The task is done when the model is valid KSML XML, follows the checklist, and
has passed the model review gate. If the user asked for a runnable TeaQL project,
continue with code generation, compile checks, and repair loops after the model
is confirmed.
