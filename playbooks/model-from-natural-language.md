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
   - Do not use object or attribute names that are reserved keywords in Java,
     SQL2016, JavaScript, Dart, Rust, Go, or Python.

3. Organize modules.
   - Use `_module` as the first-level menu display name.
   - Use `_module_key` as lowercase kebab-case.
   - Put constants in `Basic Data` unless a process-specific module is clearer.
   - Avoid single-object modules.

4. Generate KSML XML.
   - Use `prompts/modeling/ksml-rules.md`.
   - Use `prompts/modeling/task-template.md`.
   - Output one `<root>` element with direct child objects.

5. Validate before delivery.
   - Use `prompts/modeling/checklist.md`.
   - Repair any rule violation.
   - Pay special attention to constant object rules and explicit tenancy.

6. Run the model review gate before code generation.
   - Use `playbooks/model-review-gate.md`.
   - Summarize entities, fields, relationships, tenancy classification, tenant
     boundary if any, constants, and assumptions in business language.
   - Get user confirmation, or record explicit assumptions when the user asked
     for autonomous playground execution.
   - If the user asks for changes, update `model.xml`, validate again, and
     repeat the review gate.

## Done

The task is done when the model is valid KSML XML, follows the checklist, and
has passed the model review gate. If the user asked for a runnable TeaQL project,
continue with code generation, compile checks, and repair loops after the model
is confirmed.
