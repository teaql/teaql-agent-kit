# Model Notification and Parallel Review

Use this playbook after a valid single-file model or multi-file model directory
exists. The historical filename is retained for compatibility, but this is not
a blocking gate.

## Purpose

Make the semantic model visible without stopping agent execution. Natural
language still becomes an explicit model before generated Java or Rust service
code, but user confirmation is not required before generation.

After evaluation succeeds, send a model-ready notification and continue with
generation, implementation, and verification. The user may review the model or
running application in parallel and provide asynchronous feedback.

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
- Open questions or risks that would benefit from review.

Keep the summary concise enough for a business user to review asynchronously.
Do not paste the entire XML unless the user asks for it.

## Non-blocking Notification

After successful evaluation, record one of these states:

- `model_ready_notified`: the model summary was sent and agent execution
  continued.
- `review_in_progress`: the user is reviewing while the agent continues.
- `feedback_received`: asynchronous feedback arrived and is being assessed.
- `revised`: feedback changed the model; evaluation and generation were rerun.

Do not ask for confirmation merely because the model is ready. The notification
is a milestone update, not a permission request or waiting node.

If server-side KSML evaluation reports `errors`, do not generate code. Fix the
model and run evaluation again. `warnings` and `suggestions` do not block
generation by default, but disclose them in the notification when present.

Pause only for a genuine blocker that cannot be resolved safely, such as
missing business information that would materially change the system or a new
action requiring user authority.

## What To Check

Make these points available for parallel review:

- Are the business objects correct?
- Are key fields missing or wrongly named?
- Are relationships and ownership directions correct?
- Are statuses, types, categories, and other constants complete enough?
- Is this system single-tenant or multi-tenant?
- If multi-tenant, is the tenant boundary correct?
- Are any generated names likely to conflict with the user's domain language?

Feedback may arrive while generation or implementation is already running. If
it invalidates the current contract, update the model, evaluate it again,
regenerate affected outputs, and continue. Do not manually patch generated
files.

## Report Requirement

Playground reports must include a `Model Review` section with:

- Notification/review state.
- Notification time or milestone.
- The model path.
- The summarized entities, relationships, constants, and assumptions.
- Asynchronous feedback received and any resulting revisions.

The report should show that the model was made visible before generation. It
must not imply that generation waited for confirmation.
