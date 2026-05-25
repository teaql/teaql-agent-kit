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

### Explicit Tenancy Rule

KSML models must not assume multi-tenancy by default.

Tenancy is an explicit architectural choice. When modeling a domain, determine
whether the target system is single-tenant, multi-tenant, platform-managed
multi-tenant, or undecided. Do not add `merchant`, `tenant`, `platform`, or
`merchant="merchant(context)"` only because an example or historical template
used them.

Single-tenant models:

- Do not create `merchant`, `tenant`, or `platform` as baseline objects unless
  they are real business concepts in the user's domain.
- Do not add `merchant="merchant(context)"` automatically.
- Model organization, company, store, department, warehouse, school, hospital,
  or similar objects only when they are part of the business language.

Multi-tenant models:

- Identify the tenant owner object explicitly, such as `merchant`, `company`,
  `organization`, `school`, `hospital`, or `store_group`.
- Add tenant ownership only to objects that must be isolated by that boundary.
- Use `merchant="merchant(context)"` only when the confirmed tenant owner is
  `merchant`.
- State the tenant boundary in the model review summary.

Platform-managed multi-tenant models:

- Model platform/operator concepts only if they matter to the business.
- Model tenant organizations separately from platform/operator data.
- Make platform-level and tenant-level data boundaries explicit.

Undecided tenancy:

- Ask a short clarification when possible.
- For autonomous playground work, record the assumption before generation, such
  as "Assumption: single-tenant playground; no tenant boundary was modeled."

### Attribute Order

Use this order for business object attributes:

1. Identity attributes: `name`, `number`, `code`, domain-specific classification
   names such as `category`, `kind`, or `classification`.
2. Relationship references: `status`, `provider`, `region`, parent objects.
3. Tenant boundary reference, if tenancy was explicitly confirmed.
4. System fields: `create_time`, `update_time`.

This reads as: who you are, who you belong to, then system records.

### Reserved Keyword Naming

To keep model names stable and consistent across generated code, SQL, JSON,
frontend clients, and agent-written application code, model names and attribute
names must not exactly match programming-language or database reserved keywords.

The prohibited keyword sets are:

- Java.
- SQL2016.
- JavaScript.
- Dart.
- Rust.
- Go.
- Python.

Do not use bare names such as `type`, `class`, `enum`, `interface`, `package`,
`module`, `match`, `async`, `await`, `yield`, `select`, `from`, `where`, `order`,
`group`, `user`, or `table` as the full object name or full attribute name.
Compound domain names such as `school_type`, `request_type`, `item_kind`, and
`sort_order` are valid because the full name is not a reserved keyword.

Use domain-specific alternatives instead:

- `request_type` instead of `type`.
- `item_kind` instead of `type`.
- `user_account` instead of `user`.
- `sort_order` instead of `order`.

## Root Definition

The model must contain exactly one `<root>` element. The root must include a
non-empty `name` attribute; TeaQL generation uses it as the domain name.

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
- Object names and attribute names must not exactly match reserved keywords in
  Java, SQL2016, JavaScript, Dart, Rust, Go, or Python.
- Dates use ISO format such as `2024-01-15`.

## Object Rules

- Elements are objects.
- Attributes are fields.
- References to business objects use `object_name()` directly, such as
  `pet()`, `owner()`, `veterinarian()`.
- References to constant objects use `constant_object_name()` directly, such as
  `appointment_status()` or `gender()`.
- Do not use `_id` suffixes for object references.

### Domain Root Business Object

Every system must have exactly one domain root business object. This object
represents the largest business scope covered by the system. Choose it from the
user's stated system boundary and ownership hierarchy, not from examples or
from the system title. Do not infer that `school` is the root merely because the
domain name contains "school management". If the model includes both `platform`
and `school`, and the platform manages, hosts, registers, or contains schools,
then `platform` is the root and `school` must reference `platform`.

The domain root business object:

- Is a business object, not the XML `<root>` metadata element.
- Must not reference any other business object or constant object.
- Should be named from the user's domain language, not from a generic template.
- Must be the object that other top-level business objects belong to. If the
  user says the root is `platform`, `group`, `organization`, `company`,
  `school`, or another named object, use that object as the domain root.
- Must not be replaced by a lower-level example object or by an object guessed
  from the system name.

Use these precedence rules when several root candidates appear:

1. If the user explicitly identifies the root or largest layer, use that object.
2. If a platform/operator/group/organization/company contains or manages
   schools, stores, hospitals, departments, or other operating units, the
   platform/operator/group/organization/company is the root.
3. Use `school` as the root only when the described system scope is one school
   and no higher-level platform, operator, group, organization, company, or
   owner object manages that school.

All other objects must be connected to the model through relationships:

- Every non-root business object must reference at least one other business
  object or constant object.
- Prefer connecting operational data to its natural parent, such as
  `student school="school()"`, `course school="school()"`, or
  `enrollment student="student()" course="course()"`.
- Do not leave standalone business objects that are not associated with the
  domain root graph.

Wrong when the user's system boundary is an education platform:

```xml
<school _name="School" .../>
<platform _name="Platform" school="school()" .../>
<school_type _name="School Type" school="school()" .../>
```

Correct:

```xml
<platform _name="Platform" .../>
<school _name="School" platform="platform()" .../>
<school_type _name="School Type" platform="platform()" .../>
```

Finite-set objects are special:

- Status, category, kind, priority, gender, and similar finite-set objects are
  constant objects.
- Every constant object must reference the domain root business object directly,
  such as `school_type platform="platform()"` when `platform` is the root, or
  `course_category school="school()"` when `school` is the root.
- Do not model finite-set objects as global standalone constants unless the user
  explicitly states they are cross-system global platform data.

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
- Tenant ownership only when tenancy is explicitly confirmed.
- Concrete values for real-world fields.

Baseline objects for generated TeaQL services are optional and domain-driven.
Include these only when they are real business concepts or confirmed
architecture assumptions:

- `platform`.
- `merchant`.
- `employee`.

When `merchant` is the confirmed tenant owner, tenant-owned business objects may
include `merchant="merchant(context)"`. `platform` and `merchant` may be global
baseline objects without `merchant="merchant(context)"`.

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

## Status and Classification Fields

Fields that represent a finite set must reference constant objects.

Use constant objects for:

- status.
- category.
- kind.
- classification.
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
| Status, category, kind, classification | `constant_object()` |
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
| Tenant boundary, such as `merchant="merchant(context)"` | Forbidden | Optional; only when explicitly confirmed |
