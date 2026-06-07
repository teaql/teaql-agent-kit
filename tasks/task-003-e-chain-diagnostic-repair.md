# Task 003 - E-Chain Diagnostic Repair

## Goal

Repair a TEAQL diagnostic failure related to missing selection, lazy loading, or
entity chain access.

## Target Stack

Java or Rust TEAQL stack.

## Background

TEAQL diagnostics should guide agents toward correct API usage. This task
evaluates whether an agent can read the diagnostic, identify the missing query
shape, and fix the actual cause.

## Requirements

- Preserve the intended business query or operation.
- Use generated TEAQL APIs to select or load required fields.
- Keep query and update logic close to the business operation.
- Add or update tests that cover the repaired path when appropriate.
- Record the diagnostic and repair path in the run logs.

## Forbidden Actions

- Do not suppress diagnostics without fixing the cause.
- Do not broaden queries unnecessarily to hide missing fields.
- Do not replace TEAQL access with raw SQL.
- Do not manually patch generated service files.
- Do not remove failing assertions.

## Success Criteria

- Code compiles.
- Tests pass.
- The diagnostic no longer appears for the repaired path.
- The fix is targeted and preserves the intended TEAQL boundary.
- The run evidence shows whether the diagnostic helped recovery.

## Evaluation Metrics

- Functional Completion
- Compile Success
- Test Pass Rate
- API Adherence
- Hallucinated API Count
- Error Recoverability
- Framework Discipline
- Unsafe Shortcut Count
