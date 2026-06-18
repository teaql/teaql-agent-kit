# Model Review Gate

Use this gate after a valid `model.xml` candidate exists and before TeaQL code
generation starts.

## Purpose

The model review gate makes the semantic model visible to the user. Natural
language must not jump directly to generated Java or Rust service code. The user
should first confirm that the entities, fields, relationships, constants, and
assumptions match the business domain.

## Review Summary

Provide a short model review summary in business language. Include:

- Model name and target runtime.
- Server-side KSML evaluation result, when `evaluate` was available:
  - error count
  - warning count
  - suggestion count
  - any remaining warnings or suggestions that need user judgment
- Main entities.
- Important fields per entity.
- Relationships and ownership boundaries.
- Tenancy classification: single-tenant, multi-tenant, platform-managed
  multi-tenant, or undecided.
- Tenant boundary, only if multi-tenancy is confirmed or explicitly assumed.
- Constants and finite state/type/category objects.
- Assumptions made by the agent.
- Questions or risks that need user confirmation.

Keep the summary concise enough for a business user to review. Do not paste the
entire XML unless the user asks for it.

## Required Confirmation

Before generation, obtain one of these outcomes:

- `confirmed`: the user explicitly confirms the model is correct enough to
  generate code.
- `confirmed_with_assumptions`: the user accepts stated assumptions for
  playground or prototype generation.
- `needs_revision`: the user asks for model changes. Update `model.xml`,
  validate again, and repeat this gate.

For autonomous playground work, the agent may proceed only when assumptions are
explicitly listed in the report and the user has asked for autonomous execution.

If server-side KSML evaluation reports `errors`, do not generate code. Fix the
model and run evaluation again. `warnings` and `suggestions` do not block
generation by default, but they must be disclosed in the review summary when
present.

## What To Check

Ask the user to review:

- Are the business objects correct?
- Are key fields missing or wrongly named?
- Are relationships and ownership directions correct?
- Are statuses, types, categories, and other constants complete enough?
- Is this system single-tenant or multi-tenant?
- If multi-tenant, is the tenant boundary correct?
- Are any generated names likely to conflict with the user's domain language?

## Report Requirement

Playground reports must include a `Model Review` section with:

- Review status.
- Confirmation source, such as user confirmation or autonomous assumptions.
- The model path.
- The reviewed entities, relationships, constants, and assumptions.

Code generation results should appear after this section so the report shows
that the model was reviewed before TeaQL service code was generated.
