# TeaQL KSML Model Generation Rules

This document is the canonical KSML modeling contract for this repository.

Source lineage:
`openclaw-modeling-factory/skills/domain-modeling/SKILL.md`,
`agents/RULES.md`, and validated TeaQL generation behavior.

## Rule Strength

Every rule has one of three strengths:

- **MUST**: A structural, generation, or repository contract. Violating it makes
  the model invalid for this workflow and must be fixed before generation.
- **SHOULD**: The normal modeling decision. Follow it unless the user requirement
  or a documented architecture decision gives a concrete reason not to.
- **MAY**: A readability or organization recommendation. Apply it when useful;
  it must never override a MUST or an explicit business requirement.

When rules appear to conflict, use this order:

1. Explicit user business requirements.
2. MUST rules in this document.
3. Documented architecture assumptions.
4. SHOULD rules.
5. MAY rules.

An explicit requirement may select among valid designs, but it does not make
invalid KSML syntax valid. Record important assumptions; do not turn them into a
confirmation gate before autonomous modeling.

## MUST — Valid KSML Contract

### Document Shape

- The document MUST contain exactly one outermost `<root>` element.
- The root MUST have a non-empty `name`.
- `name` MUST be the only model-name attribute. Do not add
  `alias_model_name`, `english_name`, or `chinese_name`.
- Root `name` MUST use lowercase `kebab-case` and end with `-service`.
- Every business object and constant object MUST be a direct child of `<root>`.
- Business objects MUST NOT be nested inside other business objects.
- XML fields MUST be represented as attributes, not child elements.
- Only constant objects MAY contain child elements, and those children MUST be
  `<_value>` entries.
- Object names and attribute names MUST use lowercase `snake_case`.
- Attribute names MUST NOT exactly match SQL2016 reserved keywords.
- The model MUST NOT contain duplicate object elements.

Minimal valid shape:

```xml
<root name="pet-hospital-service"
      cfg_mask_china_mobile="false"
      data_service="sqlite"
      org="example"
      _module_key="root">
  <hospital _name="Hospital"
            _module="Organization"
            _module_key="organization"
            name="Harmony Pet Hospital"/>
</root>
```

### Business Objects

Every business object MUST include:

- `_name`.
- `_module`.
- `_module_key`.

Business objects MUST NOT include:

- `id="id()"`.
- `version`.
- `_constant="true"`.
- `_identifier`.
- `<_value>` children.

Normal business fields MUST use representative concrete values:

```xml
<pet _name="Pet"
     _module="Clinical"
     _module_key="clinical"
     hospital="hospital()"
     name="Mochi"
     species="dog"
     birth_date="2020-05-10"/>
```

Do not use scalar type functions as placeholders for ordinary values:

```xml
<!-- Invalid -->
<pet name="string()" species="string()" birth_date="date()"/>
```

Only fields with special generated semantics MAY use the special functions
listed later in this document.

### Constant Objects

Every constant object MUST include:

- `_name`.
- `_module`.
- `_module_key`.
- `id="id()"`.
- `name="string()"`.
- `code="string()"`.
- `_constant="true"`.
- `_identifier="code"`.
- One or more `<_value>` entries.

Constant objects MUST NOT include:

- Tenant context such as `merchant="merchant(context)"`.
- Concrete example values in the object-level `name` or `code` attributes.

Every `<_value>` MUST:

- Have an `id`, starting at `1001` and incrementing sequentially.
- Have a concrete `name`.
- Have an uppercase underscore-separated `code`.

```xml
<appointment_status _name="Appointment Status"
                    _module="Clinical"
                    _module_key="clinical"
                    hospital="hospital()"
                    id="id()"
                    name="string()"
                    code="string()"
                    _constant="true"
                    _identifier="code">
  <_value id="1001" name="Pending" code="PENDING"/>
  <_value id="1002" name="Confirmed" code="CONFIRMED"/>
  <_value id="1003" name="Completed" code="COMPLETED"/>
</appointment_status>
```

Only constant objects use `string()` for `name` and `code`. A business object
may have `name` or `code`, but their values MUST be representative literals:

```xml
<service _name="Service"
         _module="Clinical"
         _module_key="clinical"
         hospital="hospital()"
         name="Annual Wellness Exam"
         code="WELLNESS-ANNUAL"/>
```

### Relationships and Model Connectivity

- Object references MUST use `object_name()` directly:
  `hospital="hospital()"`.
- Do not use `object(object_name)`.
- The model MUST contain exactly one domain-root business object.
- The domain-root business object MUST NOT reference another business object.
- Every non-root business object MUST have a relationship path to the
  domain-root business object.
- A reference to an isolated constant does not satisfy the connectivity rule.
- Constant references do not replace the business relationship path to the
  domain root.

Correct:

```xml
<hospital _name="Hospital"
          _module="Organization"
          _module_key="organization"
          name="Harmony Pet Hospital"/>
<department _name="Department"
            _module="Organization"
            _module_key="organization"
            hospital="hospital()"
            name="Clinical Services"/>
<appointment _name="Appointment"
             _module="Clinical"
             _module_key="clinical"
             department="department()"
             status="appointment_status()"
             appointment_time="2025-05-01T09:00:00"/>
```

### Finite Sets and Boolean Fields

Fields representing business states or reusable finite classifications MUST
reference constant objects. Examples include:

- Lifecycle status.
- Category, kind, classification, gender, priority, and urgency level.
- A binary state when each state has business meaning, transitions, labels, or
  future extensibility.

A simple independent yes/no capability or switch MAY use a Boolean literal:

```xml
<service _name="Service"
         _module="Clinical"
         _module_key="clinical"
         hospital="hospital()"
         name="Annual Wellness Exam"
         requires_fasting="true"/>
```

A lifecycle state MUST use a constant:

```xml
<appointment _name="Appointment"
             _module="Clinical"
             _module_key="clinical"
             hospital="hospital()"
             status="appointment_status()"
             appointment_time="2025-05-01T09:00:00"/>
```

### Module Keys and Reserved Names

- `_module_key` MUST use lowercase `kebab-case`, with no spaces.
- Reserved keywords MUST be replaced with complete domain names.

Examples:

| Avoid | Use |
| --- | --- |
| `type` | `item_kind`, `service_type` |
| `order` | `purchase_order`, `display_order` |
| `group` | `customer_group` |
| `user` | `system_user`, `customer_account` |
| `rank` | `priority_rank` |

## SHOULD — Default Modeling Decisions

### Choose the Domain Root from the System Boundary

Choose the highest real business owner inside the requested system boundary.

1. If an operator, organization, company, group, or platform owns operating
   units, it SHOULD be the domain root.
2. An operating unit such as a school, store, or hospital SHOULD be the root
   only when no higher-level owner is inside the modeled boundary.
3. Do not create a generic `platform` merely to satisfy this rule.

The domain root is a business object, distinct from the outer XML `<root>`.

### Scope Constant Objects

Constant objects SHOULD reference the domain-root business object directly:

```xml
<service_category _name="Service Category"
                  _module="Clinical"
                  _module_key="clinical"
                  hospital="hospital()"
                  id="id()"
                  name="string()"
                  code="string()"
                  _constant="true"
                  _identifier="code">
  <_value id="1001" name="Preventive Care" code="PREVENTIVE_CARE"/>
</service_category>
```

A constant MAY remain global only when the requirement explicitly describes it
as cross-system global reference data. The exception and its scope SHOULD be
recorded as a modeling assumption.

### Make Tenancy Explicit

KSML models SHOULD NOT assume multi-tenancy.

Classify the system as single-tenant, multi-tenant, platform-managed
multi-tenant, or undecided:

- Single-tenant models SHOULD NOT add tenant objects or tenant context fields
  unless they are real business concepts.
- Multi-tenant models SHOULD identify the tenant owner and add tenant ownership
  only to data that requires isolation.
- `merchant="merchant(context)"` SHOULD be used only when `merchant` is the
  actual tenant owner.
- Platform-level data and tenant-level data SHOULD have explicit boundaries.
- When tenancy is undecided, autonomous modeling SHOULD proceed with the safest
  reasonable assumption and record it for review.

Tenancy review happens alongside Agent work; it is not a mandatory waiting or
confirmation node.

### Use Representative Values

Choose values that make inferred types unambiguous:

| Intended type | Representative value |
| --- | --- |
| String | `name="Harmony Pet Hospital"` |
| Boolean | `enabled="true"` |
| Integer | `quantity="1"` |
| Long | `external_id="1000000000000000000l"` |
| Decimal | `price="99.99"` |
| Date | `birth_date="2020-05-10"` |
| DateTime | `appointment_time="2025-05-01T09:00:00"` |
| Time | `opening_time="09:00:00"` |
| Reference | `hospital="hospital()"` |
| Context reference | `merchant="merchant(context)"` |

Use the smallest correct type:

- Use `long` only when the value may exceed the integer range.
- Use decimal values for money and measured quantities.
- Do not use a fake string for a finite business set.
- Do not use a zero-like placeholder when a realistic value communicates the
  type more clearly.

### Use Complete Domain Names

Object and field names SHOULD use complete domain words:

- `diagnostic_report`, not `diag_report`.
- `insurance_claim`, not `ins_claim`.
- `prescription_item`, not `rx_item`.
- `vaccination_record`, not `vax_record`.

Widely understood domain terms such as `api`, `url`, `sku`, and `id` MAY remain
abbreviated when their meaning is unambiguous.

### Root Metadata Defaults

Unless the target environment or user requirement says otherwise, use:

```xml
<root name="{domain}-service"
      cfg_mask_china_mobile="false"
      data_service="sqlite"
      org="example"
      _module_key="root">
</root>
```

These are repository playground defaults, not universal KSML invariants:

- `cfg_mask_china_mobile`: default `false`.
- `data_service`: default `sqlite`.
- `org`: default `example`.
- `_module_key`: default `root`.

## MAY — Readability and Organization

### Attribute Order

For readable diffs, attributes MAY use this order:

1. Presentation metadata: `_name`, `_module`, `_module_key`.
2. Identity and descriptive values: `name`, `number`, `code`.
3. Classification and relationships.
4. Tenant context, when applicable.
5. System fields: `create_time`, `update_time`.
6. Constant mechanics: `id`, `_constant`, `_identifier`.

For `<_value>`, use `id`, `name`, then `code`.

### Module Design

`_module` and `_module_key` define first-level menu grouping.

- Closely related objects MAY share one module.
- Operational objects and their local constants MAY share a module.
- Prefer a small number of coherent modules.
- Avoid creating a new module for every object.

Example:

```xml
<department _module="Organization" _module_key="organization" .../>
<employee _module="Organization" _module_key="organization" .../>
<appointment _module="Clinical" _module_key="clinical" .../>
<appointment_status _module="Clinical" _module_key="clinical" .../>
```

## Special Generated Functions

Use these only when the field requires their generated semantics:

- `text()`.
- `jsonMe()`.
- `password()`.
- `createTime()`.
- `updateTime()`.
- `currentUser()`.
- `remoteIp()`.
- `cityByIp()`.

Do not use them as substitutes for representative business values.

## Generator Output Contract

For a task that asks for pure model generation, the response MUST:

- Contain XML only.
- Omit markdown fences and narrative explanation.
- Use a root `name` generated from the requested domain.

This output contract governs the generated model response. It does not prohibit
the Agent from separately reporting the saved model path, evaluation result,
warnings, and assumptions after modeling and evaluation finish.

## Final Checklist

Before evaluation, verify:

- [ ] Exactly one outer `<root>` with a non-empty kebab-case `name`.
- [ ] No obsolete model-name attributes.
- [ ] Exactly one domain-root business object.
- [ ] Every non-root business object has a path to the domain root.
- [ ] Every object is a direct child of `<root>`.
- [ ] Every object has `_name`, `_module`, and kebab-case `_module_key`.
- [ ] Business objects have no constant mechanics.
- [ ] Constants have the complete constant contract and sequential values.
- [ ] Finite business states reference constants; simple switches use Booleans.
- [ ] Normal fields use representative literals.
- [ ] References use `object_name()` directly.
- [ ] Tenancy is explicit or its assumption is recorded.
- [ ] Names are complete, snake_case, and not reserved keywords.
