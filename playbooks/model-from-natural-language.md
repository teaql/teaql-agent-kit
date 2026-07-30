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
   - `name`: kebab-case plus `-service`.
   - Do not add `alias_model_name`, `english_name`, or `chinese_name`.

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

4. Generate KSML XML.
   - Use `prompts/modeling/ksml-rules.md`.
   - Use `prompts/modeling/task-template.md`.
   - Output one `<root>` element with direct child objects.

5. Validate before delivery.
   - Use `prompts/modeling/checklist.md`.
   - Repair any rule violation.
   - Pay special attention to constant object rules and explicit tenancy.
   - If a TeaQL client toolchain with `evaluate` is available, run server-side KSML
     evaluation after checklist validation and before code generation. Fix
     evaluation `errors`; carry `warnings` and `suggestions` into the
     model-ready notification.
   - For a multi-file model, pass the complete directory to TeaQL. Passing only
     `main.xml` omits the included files from the upload.

6. Send the Model Ready signal and continue.
   - Use `playbooks/model-review-gate.md`.
   - Give the user the concrete model file/directory path and evaluation result,
     including error, warning, and suggestion counts.
   - Keep the signal compact so the user can open and review the model directly.
   - Continue directly to generation when a runnable project was requested.
   - Do not wait for confirmation. The user can review the model or application
     while the agent continues.
   - If asynchronous feedback arrives, update the single-file model or affected
     subdomain files, validate again, regenerate, and continue.

## Done

The task is done when the model is valid KSML XML, follows the checklist, and
the Model Ready signal has been sent. If the user asked for a runnable TeaQL
project, continue with code generation, compile checks, and repair loops without
waiting for model confirmation.
