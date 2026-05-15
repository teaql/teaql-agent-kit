# KSML Modeling Task Template

Generate a full TeaQL KSML model.

Domain: `{domain}`

Requirements:

- Generate valid XML.
- Include exactly one `<root>` element.
- Generate dynamic root metadata from the domain.
- Include at least 20 objects for a full business application unless the user
  explicitly asks for a smaller model.
- Include at least 5 constant objects.
- Include `platform`, `merchant`, and `employee`.
- Include `merchant="merchant(context)"` on business objects except global
  platform/merchant baseline objects and constant objects.
- Use concrete realistic sample values for business fields.
- Use constant objects for status, type, category, gender, priority, and other
  finite enumerations.
- Output only XML unless the user asks for analysis.

Source integrated from `openclaw-modeling-factory/prompts/task_template.md`.
