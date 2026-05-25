# KSML Modeling Checklist

Use this checklist before delivering or generating code from a KSML model.

## Root

- Exactly one `<root>` element.
- Root `name` is present and non-empty.
- `alias_model_name` is snake_case.
- `english_name` is Title Case.
- `chinese_name` is domain-specific.
- `name` is kebab-case ending in `-service`.
- `data_service="sqlite"`.
- `org="doublechaintech"`.
- `_module_key="root"`.

## Structure

- All objects are direct children of `<root>`.
- No nested objects except `<_value>` children inside constant objects.
- Object names are lowercase snake_case.
- Each element type is unique.
- Object names and attribute names do not exactly match reserved keywords from
  Java, SQL2016, JavaScript, Dart, Rust, Go, and Python.

## Business Objects

- Must have `_name`, `_module`, and `_module_key`.
- Must not have `id="id()"`.
- Must not have `_constant="true"`.
- Must not have `_identifier`.
- Must not have `<_value>` children.
- Exactly one business object is the domain root object.
- The domain root object matches the user's stated largest system boundary,
  not merely the system title.
- If the model includes both `platform` and `school`, and the platform manages,
  hosts, registers, or contains schools, `platform` is the domain root and
  `school` references `platform`.
- `school` is the domain root only when one school is the largest scope and no
  higher-level platform, operator, group, organization, company, or owner object
  manages that school.
- The domain root business object does not reference any other object.
- Every non-root business object references at least one other object and is
  connected to the domain root graph.
- Use concrete example values, not `string()`, for normal business fields.
- Do not assume multi-tenancy by default.
- Include tenant ownership only when the user confirmed a tenant boundary or the
  model records an explicit autonomous playground assumption.
- Use `merchant="merchant(context)"` only when `merchant` is the confirmed
  tenant owner.
- Put attributes in this order: identity, relationships, tenant boundary if
  confirmed, system fields.

## Constant Objects

- Must have `id="id()"`.
- Must have `name="string()"`.
- Must have `code="string()"`.
- Must have `_constant="true"`.
- Must have `_identifier="code"`.
- Must have `<_value>` children.
- Must not have `merchant="merchant(context)"`.
- Must reference the domain root business object directly unless explicitly
  modeled as cross-system global platform data.
- `<_value>` ids start from `1001` and increment sequentially.
- `<_value>` code values are `UPPERCASE_WITH_UNDERSCORES`.

## References

- Use `object_name()` directly.
- Do not use `_id` suffixes for references.
- Status, category, kind, classification, gender, priority, and boolean-like
  states reference constant objects.

## Tenancy

- Classify the model as single-tenant, multi-tenant, platform-managed
  multi-tenant, or undecided.
- Do not add `platform`, `merchant`, `tenant`, or `merchant(context)` only
  because an example template included them.
- For single-tenant models, do not add tenant boundary fields unless they are
  real business concepts.
- For multi-tenant models, identify the tenant owner object explicitly and apply
  tenant ownership only to data that must be isolated by that boundary.
- Record the tenancy decision or assumption in the model review summary.

## Modules

- `_module` is a display name, usually Title Case with spaces.
- `_module_key` is lowercase kebab-case.
- Group objects by functional domain or business process.
- Avoid single-object modules.
