# AGENTS.md — Rules for AI Agents

## READ THIS BEFORE CODING

### Core Framework Rules
1. **Never guess method names**: Read the generated entity source files for the exact method names (e.g., `update_status`, not `set_status`).
2. **Never edit generated files**: Do not manually modify files under `rust-lib-core/`, `generate-lib/`, `generate-workspace/`, or `bizcore/` (unless instructed otherwise).
3. **Generated AGENTS.md**: After generation, check for a local `AGENTS.md` in generated workspace/app outputs. Workspace outputs such as `rust-app-console/` and `java-workspace/` must have `AGENTS.md`; if missing, stop and report. Library outputs such as `rust-lib-core/` may not have `AGENTS.md`; use generated source plus `rust-assist-*` commands for API discovery instead.
4. **Query constraints**: Every query using `execute_for_list()` or `execute()` must be preceded by `.purpose("why")` and `.comment("what")`.
5. **Save constraints**: Every save using `.save()` or `.update()` must be preceded by `.audit_as("description")`.

### KSML Modeling Rules (Hard)
6. Every business object must have `_name`, `_module`, and `_module_key`.
7. Constant objects must have `id="id()"`, `name="string()"`, `code="string()"`.
8. Constant objects must have `_constant="true"` and `_identifier="code"`.
9. Never use `id="id()"` on business objects.
10. Never use `_constant="true"` on business objects.
11. References to business objects must use `object_name()` directly (e.g., `school="school()"`), NOT `school="object(school)"`.
12. Status and finite-set fields must reference constant objects (e.g., `status="appointment_status()"`).
13. Use typical real-world values for business object fields (e.g., `species="dog"`), NOT `species="string()"`.
14. Only constant objects use `string()` for `name` and `code`.
15. Do not add `merchant`, `tenant`, or `platform` unless explicitly modeling a multi-tenant system.
16. Single-tenant systems have no tenant boundary fields.
17. Multi-tenant systems must use `{tenant_owner}="merchant(context)"` on tenant-owned objects.
18. Object names and attribute names must use lowercase `snake_case`.
19. Attribute names must not exactly match SQL2016 reserved keywords (e.g., use `item_kind` instead of `type`).
20. There must be exactly one `<root>` element at the top level.
21. All objects must be direct children of `<root>`.
22. Root metadata `name` must be `kebab-case` with `-service` suffix.
23. Every non-root business object must reference at least one other business object or constant object (no disconnected graphs).
24. `_module_key` must be lowercase `kebab-case` (e.g., `basic-data`), never with spaces.
25. Constant objects' `<_value>` children must have an `id` starting from `1001` and sequentially incrementing.
26. Constant objects' `<_value>` code values must be UPPERCASE with underscores (e.g., `IN_PROGRESS`).

### Output Rules for Generators
27. Output XML only for pure model generation. No markdown fences.
28. Do not include narrative explanations in the output.
29. No duplicate elements in the KSML.
30. No nested business objects.

*See `ERROR-FIX.md` if you encounter issues during validation or generation.*
