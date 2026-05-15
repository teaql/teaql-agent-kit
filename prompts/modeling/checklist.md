# KSML Modeling Checklist

Use this checklist before delivering or generating code from a KSML model.

## Root

- Exactly one `<root>` element.
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

## Business Objects

- Must have `_name`, `_module`, and `_module_key`.
- Must not have `id="id()"`.
- Must not have `_constant="true"`.
- Must not have `_identifier`.
- Must not have `<_value>` children.
- Use concrete example values, not `string()`, for normal business fields.
- Include `merchant="merchant(context)"` for tenant-owned business objects.
- Put attributes in this order: identity, relationships, merchant, system fields.

## Constant Objects

- Must have `id="id()"`.
- Must have `name="string()"`.
- Must have `code="string()"`.
- Must have `_constant="true"`.
- Must have `_identifier="code"`.
- Must have `<_value>` children.
- Must not have `merchant="merchant(context)"`.
- `<_value>` ids start from `1001` and increment sequentially.
- `<_value>` code values are `UPPERCASE_WITH_UNDERSCORES`.

## References

- Use `object_name()` directly.
- Do not use `_id` suffixes for references.
- Status, type, category, gender, priority, and boolean-like states reference
  constant objects.

## Modules

- `_module` is a display name, usually Title Case with spaces.
- `_module_key` is lowercase kebab-case.
- Group objects by functional domain or business process.
- Avoid single-object modules.
