# TeaQL KSML Model Generation Rules

KSML is a compact XML modeling format used as the semantic source for TeaQL code
generation. These rules are optimized for coding agents that turn natural
language business descriptions into generated Java or Rust TeaQL projects.

Source integrated and adapted from
`openclaw-modeling-factory/prompts/ksml_rules_en_v2.md`.

## Critical Rules

### Only Constant Objects Have `id="id()"`

Constant objects:

- Must have `id="id()"`.
- Must have `_constant="true"`.
- Must have `_identifier="code"`.
- Must have `<_value>` children.

Business objects:

- Must never have `id="id()"`.
- Must never have `_constant="true"`.
- Must never have `_identifier`.
- Must never have `<_value>` children.

Wrong:

```xml
<vm_instance id="id()" _name="VM Instance" .../>
```

Correct business object:

```xml
<vm_instance _name="VM Instance"
             _module="Compute"
             _module_key="compute"
             instance_name="web-server-01"
             status="resource_status()"
             merchant="merchant(context)"
             create_time="createTime()"
             update_time="updateTime()"/>
```

Correct constant object:

```xml
<resource_status _name="Resource Status"
                 _module="Basic Data"
                 _module_key="basic-data"
                 id="id()" name="string()" code="string()"
                 _constant="true" _identifier="code">
  <_value id="1001" name="Running" code="RUNNING"/>
</resource_status>
```

### Only Constant Objects Use `string()` for Name and Code

Constant objects use:

```xml
name="string()" code="string()"
```

Business objects use concrete values:

```xml
<employee name="John Smith" phone="13800138000"/>
```

### Attribute Order

Use this order for business object attributes:

1. Identity attributes: `name`, `number`, `code`, `type`.
2. Relationship references: `status`, `provider`, `region`, parent objects.
3. `merchant="merchant(context)"`.
4. System fields: `create_time`, `update_time`.

This reads as: who you are, who you belong to, then system records.

## Root Definition

The model must contain exactly one `<root>` element.

Generate root metadata dynamically from the user's domain. Do not copy example
values.

For domain `pet hospital management`, generate:

- `alias_model_name`: `pet_hospital_management`.
- `english_name`: `Pet Hospital Management`.
- `chinese_name`: domain-specific translation, such as `宠物医院管理`.
- `name`: kebab-case plus `-service`, such as `pet-hospital-service`.
- `cfg_mask_china_mobile`: always `false`.
- `data_service`: always `sqlite`.
- `org`: default `doublechaintech`.
- `_module_key`: always `root`.

Example shape:

```xml
<root alias_model_name="pet_hospital_management"
      cfg_mask_china_mobile="false"
      chinese_name="宠物医院管理"
      english_name="Pet Hospital Management"
      data_service="sqlite"
      name="pet-hospital-service"
      org="doublechaintech"
      _module_key="root">
</root>
```

## Structure

- Only one `<root>`.
- All objects must be direct children of `<root>`.
- No object nesting except `<_value>` entries inside constant objects.
- Each element type must be unique.
- Object names use lowercase snake_case.
- Dates use ISO format such as `2024-01-15`.

## Object Rules

- Elements are objects.
- Attributes are fields.
- References to business objects use `object_name()` directly, such as
  `pet()`, `owner()`, `veterinarian()`.
- References to constant objects use `constant_object_name()` directly, such as
  `appointment_status()` or `gender()`.
- Do not use `_id` suffixes for object references.

Every object must include:

- `_name`.
- `_module`.
- `_module_key`.

## Module Design

`_module` and `_module_key` define the first-level menu structure. Objects
sharing the same `_module` become second-level menus under that module.

### `_module`

- Purpose: first-level menu display name.
- Format: local language or English Title Case with spaces.
- Examples: `Basic Data`, `Surgery Management`, `Inventory Management`.

### `_module_key`

- Purpose: first-level menu system identifier.
- Format: lowercase English kebab-case.
- Examples: `basic-data`, `surgery-management`, `inventory-management`.
- Always use hyphens. Never use spaces.

Wrong:

```xml
<child _module="Child Management" _module_key="child management"/>
```

Correct:

```xml
<child _module="Child Management" _module_key="child-management"/>
```

### Module Grouping

- Business objects go in the functional module where they belong.
- Constant objects usually go in `Basic Data`, unless a process-specific module
  is clearer.
- Prefer functional or process groupings.
- Avoid menu clutter.
- Avoid single-object modules.

## Business Objects

Business objects must not include:

- `id="id()"`.
- `version`.
- `_constant="true"`.
- `_identifier`.
- `<_value>` children.

Business objects must include:

- `_name`.
- `_module`.
- `_module_key`.
- `merchant="merchant(context)"` for tenant-owned business objects.
- Concrete values for real-world fields.

Baseline objects for generated TeaQL services should include:

- `platform`.
- `merchant`.
- `employee`.

`platform` and `merchant` may be global baseline objects without
`merchant="merchant(context)"`. Tenant-owned business objects should include
`merchant="merchant(context)"`.

## Constant Objects

Constant objects must include:

- `id="id()"`.
- `name="string()"`.
- `code="string()"`.
- `_constant="true"`.
- `_identifier="code"`.
- `<_value>` entries.

Constant objects must not include:

- `merchant="merchant(context)"`.
- Concrete example values for `name` or `code`.

### Value Entries

Each `<_value>` must include an `id` attribute starting from `1001`.

IDs increment sequentially:

```xml
<_value id="1001" name="Pending" code="PENDING"/>
<_value id="1002" name="Confirmed" code="CONFIRMED"/>
<_value id="1003" name="Completed" code="COMPLETED"/>
```

Attribute order is:

1. `id`.
2. `name`.
3. `code`.

Code values must use uppercase with underscores:

- `PENDING`.
- `IN_PROGRESS`.
- `QUALITY_CONTROL`.

Never use lowercase or camelCase for constant `code` values.

## Field Value Rules

Use concrete typical values for real-world fields. Do not use generic type
functions for normal business values.

Wrong:

```xml
<pet species="string()" breed="string()" color="string()"/>
<employee name="string()" phone="string()" email="string()" hire_date="date()"/>
```

Correct:

```xml
<pet species="dog" breed="golden retriever" color="golden"/>
<employee name="John Smith"
          phone="13800138000"
          email="john.smith@example.com"
          hire_date="2024-01-15"/>
```

## Status and Type Fields

Fields that represent a finite set must reference constant objects.

Use constant objects for:

- status.
- type.
- category.
- gender.
- priority.
- urgency level.
- boolean-like states such as active/inactive.

Wrong:

```xml
<appointment status="string()"/>
<pet gender="string()"/>
```

Correct:

```xml
<appointment_status _name="Appointment Status"
                    _module="Basic Data"
                    _module_key="basic-data"
                    id="id()" name="string()" code="string()"
                    _constant="true" _identifier="code">
  <_value id="1001" name="Pending" code="PENDING"/>
  <_value id="1002" name="Confirmed" code="CONFIRMED"/>
  <_value id="1003" name="Completed" code="COMPLETED"/>
  <_value id="1004" name="Cancelled" code="CANCELLED"/>
</appointment_status>

<appointment status="appointment_status()"/>
<pet gender="gender()"/>
```

Use `object_name()` directly. Do not write `object(object_name)`.

## Value Selection Table

| Scenario | Use |
| --- | --- |
| Name, title, description | Concrete typical value |
| Phone | Concrete typical phone number |
| Email | Concrete typical email |
| Address | Concrete typical address |
| Status, type, category | `constant_object()` |
| Gender | `gender()` or a domain-specific constant |
| Date fields | Concrete date such as `2024-01-15` |
| `create_time`, `update_time` | `createTime()`, `updateTime()` |
| Numeric IDs, counts, amounts | Concrete number |
| Reference to another object | `object_name()` |

## Built-In Functions

- `createTime()`.
- `updateTime()`.
- `currentUser()`.
- `remoteIp()`.
- `cityByIp()`.

## Output Rules

- Output XML only for pure model generation.
- No explanation.
- No markdown fences.
- No duplicate elements.
- No nested business objects.
- Root metadata must be dynamically generated from the requested domain.

## Quick Reference

| Rule | Constant Object | Business Object |
| --- | --- | --- |
| `id="id()"` | Required | Forbidden |
| `name="string()"` | Required | Forbidden for normal values |
| `code="string()"` | Required | Usually forbidden |
| `_constant="true"` | Required | Forbidden |
| `_identifier="code"` | Required | Forbidden |
| `<_value>` children | Required | Forbidden |
| `merchant="merchant(context)"` | Forbidden | Required for tenant-owned objects |
