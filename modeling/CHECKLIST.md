# KSML Modeling Checklist

Use this checklist before evaluating or generating from a KSML model.
`modeling/KSML-RULES.md` remains authoritative.

## MUST — Validity Gate

### Root and Structure

- [ ] Exactly one outer `<root>` element.
- [ ] Root `name` is non-empty, lowercase kebab-case, and ends in `-service`.
- [ ] Root has no `alias_model_name`, `english_name`, or `chinese_name`.
- [ ] Every object is a direct child of `<root>`.
- [ ] Only constant objects contain children, and those children are `<_value>`.
- [ ] Object and attribute names use lowercase snake_case.
- [ ] Attribute names do not exactly match SQL2016 reserved keywords.
- [ ] No duplicate object elements.

### Business Objects and Connectivity

- [ ] Every business object has `_name`, `_module`, and `_module_key`.
- [ ] No business object has `id="id()"`, `_constant`, `_identifier`, or
  `<_value>` children.
- [ ] Exactly one business object is the domain root.
- [ ] The domain-root business object references no other business object.
- [ ] Every non-root business object has a business relationship path to the
  domain root; an isolated constant reference does not satisfy this rule.
- [ ] Normal business fields use representative literals, not scalar placeholder
  functions.

### Constants and References

- [ ] Every constant has complete object metadata.
- [ ] Every constant has `id="id()"`, `name="string()"`, `code="string()"`,
  `_constant="true"`, and `_identifier="code"`.
- [ ] Every constant has one or more `<_value>` entries.
- [ ] `<_value>` ids start at `1001` and increment sequentially.
- [ ] `<_value>` codes use `UPPERCASE_WITH_UNDERSCORES`.
- [ ] Constants do not contain tenant context.
- [ ] References use `object_name()` directly, not `object(object_name)`.
- [ ] Lifecycle states and finite classifications reference constants.
- [ ] Simple independent yes/no switches use Boolean literals.
- [ ] `_module_key` uses lowercase kebab-case.

## SHOULD — Modeling Decisions

- [ ] The domain root is the highest real owner inside the requested system
  boundary, not an object inferred only from the system title.
- [ ] Constant objects reference the domain root directly unless explicitly
  modeled as cross-system global data.
- [ ] Object and attribute names use complete, unambiguous domain words.
- [ ] Tenancy is classified as single-tenant, multi-tenant, platform-managed
  multi-tenant, or undecided.
- [ ] Tenant objects and context fields are not copied from templates by default.
- [ ] Multi-tenant ownership is applied only to data requiring isolation.
- [ ] `merchant="merchant(context)"` is used only when `merchant` is the actual
  tenant owner.
- [ ] An undecided tenancy assumption is recorded for parallel review without
  blocking autonomous modeling.
- [ ] Repository root metadata defaults are used unless the target overrides
  them: `data_service="sqlite"`, `org="example"`,
  `_module_key="root"`.

## MAY — Readability

- [ ] Related objects share coherent modules where useful.
- [ ] Single-object modules are avoided where practical.
- [ ] Attributes follow the preferred order: presentation metadata, identity
  values, classifications and relationships, tenant context, system fields,
  then constant mechanics.
