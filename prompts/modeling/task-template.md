# KSML Modeling Task Template

Generate a full TeaQL KSML model.

Domain: `{domain}`

Requirements:

- Generate valid XML.
- Keep exactly one logical root and exactly one `<root>` container in each XML
  document.
- The authoritative `<root>` element must include a non-empty `name` attribute.
- The outermost XML tag must be `<root>`. Never use `<model>`, `<ksml>`,
  `<domain>`, or any other wrapper tag.
- Generate dynamic root metadata from the domain.
- Decide the domain root business object from the user's stated largest system
  boundary and ownership hierarchy. Do not infer it from the domain title alone.
  If `platform` manages schools, `platform` is the domain root and `school`
  references `platform`.
- Include at least 20 objects for a full business application unless the user
  explicitly asks for a smaller model.
- When the requested model contains more than 20 domain objects, counting
  business and constant objects together, prefer a multi-file model split by
  business subdomain with `<_include>`.
- If one subdomain still contains more than 20 objects, split it again by a
  smaller cohesive business process with nested includes.
- A multi-file model must use `main.xml` as its entrypoint. Put authoritative
  root metadata in `main.xml`, use `<root>` containers in included files, and
  submit the complete directory rather than `main.xml` alone.
- Include at least 5 constant objects.
- Do not assume multi-tenancy by default.
- Decide whether the model is single-tenant, multi-tenant, platform-managed
  multi-tenant, or undecided.
- Include `platform`, `merchant`, `tenant`, or `employee` only when they are
  real business concepts or explicitly confirmed architecture assumptions.
- Include tenant ownership fields only when a tenant boundary is confirmed.
- Use `merchant="merchant(context)"` only when `merchant` is the confirmed
  tenant owner.
- Use concrete realistic sample values for business fields.
- Use constant objects for status, category, kind, classification, gender,
  priority, and other finite enumerations.
- Do not use object or attribute names that exactly match reserved keywords in
  Java, JavaScript, Dart, Rust, Go, or Python.
- Do not use attribute names that exactly match SQL2016 reserved keywords.
- Output or write only the requested XML file set unless the user asks for
  analysis.

Source integrated from `openclaw-modeling-factory/prompts/task_template.md`.
