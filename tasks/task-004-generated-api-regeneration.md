# Task 004 - Generated API Regeneration

## Goal

Update the semantic model, regenerate TEAQL code, and adapt customer-owned code
without manually editing generated service files.

## Target Stack

Java or Rust TEAQL stack.

## Background

Generated-code discipline is central to TEAQL. This task evaluates whether an
agent fixes model-level problems at the model or generator boundary instead of
patching generated output.

## Requirements

- Identify the model change needed for the requested business behavior.
- Update `model.xml` or the task fixture's semantic model input.
- Run the appropriate TeaQL generation command for the target stack.
- Read generated workspace instructions before editing or explaining generated
  surfaces.
- Adapt only customer-owned code, tests, or runtime wiring as needed.
- Run compile checks and tests provided by the target project.

## Forbidden Actions

- Do not manually edit generated TeaQL service files.
- Do not clone or build generator source code during normal generation.
- Do not hand-write generated API surfaces.
- Do not use alternate generation paths if the required generation client fails.
- Do not remove tests to make regeneration appear successful.

## Success Criteria

- The model change is clear and semantically justified.
- Generation completes through the approved TeaQL client.
- Code compiles.
- Existing and relevant new tests pass.
- Generated files remain treated as read-only deliverables.

## Evaluation Metrics

- Functional Completion
- Compile Success
- Test Pass Rate
- API Adherence
- Framework Discipline
- Error Recoverability
- Human Intervention Count
- Unsafe Shortcut Count
