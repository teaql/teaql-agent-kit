# AGENTS.md — Rules for AI Agents

## READ THIS BEFORE CODING

### Core Framework Rules
1. **Never guess method names**: Read the generated entity source files for the exact method names (e.g., `update_status`, not `set_status`).
2. **Never edit generated files**: Do not manually modify files under `generate-lib/` or `generate-workspace/` or `bizcore/` (unless instructed otherwise).
3. **Query constraints**: Every query using `execute_for_list()` or `execute()` must be preceded by `.purpose("why")` and `.comment("what")`.
4. **Save constraints**: Every save using `.save()` or `.update()` must be preceded by `.audit_as("description")`.

### KSML Modeling Rules (Hard)
5. Every business object must have `_name`, `_module`, and `_module_key`.
6. Constant objects must have `id="id()"`, `name="string()"`, `code="string()"`.
7. Constant objects must have `_constant="true"` and `_identifier="code"`.
8. Never use `id="id()"` on business objects.
9. Never use `_constant="true"` on business objects.
10. References to business objects must use `object_name()` directly (e.g., `school="school()"`), NOT `school="object(school)"`.
11. Status and finite-set fields must reference constant objects (e.g., `status="appointment_status()"`).
12. Use typical real-world values for business object fields (e.g., `species="dog"`), NOT `species="string()"`.
13. Only constant objects use `string()` for `name` and `code`.
14. Do not add `merchant`, `tenant`, or `platform` unless explicitly modeling a multi-tenant system.
15. Single-tenant systems have no tenant boundary fields.
16. Multi-tenant systems must use `{tenant_owner}="merchant(context)"` on tenant-owned objects.
17. Object names and attribute names must use lowercase `snake_case`.
18. Attribute names must not exactly match SQL2016 reserved keywords (e.g., use `item_kind` instead of `type`).
19. There must be exactly one `<root>` element at the top level.
20. All objects must be direct children of `<root>`.
21. Root metadata `name` must be `kebab-case` with `-service` suffix.
22. Every non-root business object must reference at least one other business object or constant object (no disconnected graphs).
23. `_module_key` must be lowercase `kebab-case` (e.g., `basic-data`), never with spaces.
24. Constant objects' `<_value>` children must have an `id` starting from `1001` and sequentially incrementing.
25. Constant objects' `<_value>` code values must be UPPERCASE with underscores (e.g., `IN_PROGRESS`).

### Output Rules for Generators
26. Output XML only for pure model generation. No markdown fences.
27. Do not include narrative explanations in the output.
28. No duplicate elements in the KSML.
29. No nested business objects.

*See `ERROR-FIX.md` if you encounter issues during validation or generation.*
