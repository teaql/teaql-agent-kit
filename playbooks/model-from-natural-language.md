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
   - Platform, merchant, and employee are required baseline objects.
   - Add concrete business objects for the domain.
   - Add constant objects for status, type, category, gender, priority, and
     finite enumerations.

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
   - Pay special attention to constant object rules and `merchant(context)`.

## Done

The task is done when the model is valid KSML XML and follows the checklist. If
the user asked for a runnable TeaQL project, continue with code generation,
compile checks, and repair loops.
