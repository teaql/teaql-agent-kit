# TeaQL KSML Error Fixes

| Rule ID | Explanation & Fix |
|---------|-------------------|
| `KSML-STRUCTURE-001` | **Nested Object Definition**. You placed an object tag INSIDE another object tag (e.g. `<school target="school()"/>` inside `<platform>`). In KSML, object definitions CANNOT be nested. All `<foo>` object definitions must be direct children of `<root>`. To define a relationship, use an attribute like `platform="platform()"` on the child object instead of nesting XML tags. Remove any nested relationship tags. |
| `KSML-LOG-004` | **Missing user field**. A logging object (like `audit_log` or `activity_log`) MUST include a user/operator field (e.g. `action_user="string()"`, `created_by="string()"`). Add a field representing the user to the log object. |
| `KSML-KEYWORD-002` | **Reserved keyword**. The field name you used conflicts with language reserved keywords (e.g., `operator`, `type`). Rename the field to something else (e.g., `action_operator`, `record_type`). |
| `KSML-XML-005` | **Empty Attribute**. You left an attribute empty (e.g., `company_name=""`). Empty values are not allowed in KSML definitions. Provide a valid type definition like `company_name="string()"`. |
