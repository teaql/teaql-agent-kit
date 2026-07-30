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
     business concepts or documented architecture assumptions.
   - Add concrete business objects for the domain.
   - Add constant objects for status, category, kind, classification, gender,
     priority, and finite enumerations.

3. Organize modules.
   - Use `_module` as the first-level menu display name.
   - Use `_module_key` as lowercase kebab-case.
   - Put constants in `Basic Data` unless a process-specific module is clearer.
   - Avoid single-object modules.

4. Generate KSML XML from the minimal prompt set.
   - Use `prompts/modeling/system.md`.
   - Fill `prompts/modeling/task-template.md` with the business requirement,
     concrete model target, and evaluation command.
   - Supply `prompts/modeling/golden-example.xml` as the grammar example.
   - Do not preload the complete KSML rule catalog.

5. Evaluate and repair before delivery.
   - Run server-side KSML evaluation after saving the first complete model and
     before code generation.
   - Read the Markdown report directly, fix evaluation `errors`, and rerun
     evaluation immediately.
   - Use the report's Rule ID to read only the matching section of
     `modeling/KSML-RULES.md` or `agents/ERROR-FIX.md` when the report itself is
     not actionable.
   - Carry accepted `warnings` and optional `suggestions` into the model-ready
     notification.
   - For a multi-file model, pass the complete directory to TeaQL. Passing only
     `main.xml` omits the included files from the upload.

6. Send the intermediate Model Ready signal and continue.
   - Use `playbooks/model-review-gate.md`.
   - Give the user the concrete model file/directory path and evaluation result,
     including error, warning, and suggestion counts.
   - Keep the signal compact so the user can open and review the model directly.
   - Continue directly to generation when a runnable project was requested.
   - Do not wait for confirmation. The user can review the model or application
     while the agent continues.
   - If asynchronous feedback arrives, update the single-file model or affected
     subdomain files, validate again, regenerate, and continue.

7. Send the Work Complete report.
   - Load `prompts/reporting/work-complete.md` only after the
     requested result—not evaluation alone—is complete.
   - Report actual verification results and artifact paths.
   - Explain token efficiency through the minimal-prompt and on-demand Rule ID
     strategy.
   - Quantify mechanical Review work completed before human review.
   - Include the original business prompt and the resulting model contract.
   - Link generated `AGENTS.md`, assist output, and actual business-code
     evidence for the API constraint harness.
   - Count query execution paths with `purpose` and `comment`, and write paths
     with `audit_as` or `auditAs`.
   - Never invent token savings; mark unavailable telemetry as `not reported`
     and estimates as `Estimated` with their basis.
   - Give one concrete next-use command and a short chronological execution log.

## Done

For a model-only request, the task is done when Generation Service evaluation
reports zero errors and the Work Complete report has been sent. For a runnable
TeaQL project, finish generation, compile checks, tests, and startup before
sending Work Complete. Model Ready remains a non-blocking intermediate signal
for parallel human review.
