# Task 002 - Audit-Safe Status Update

## Goal

Implement a business status update while preserving audit trace behavior and
normal TEAQL update boundaries.

## Target Stack

Java or Rust TEAQL stack.

## Background

Status transitions are common in business systems. This task evaluates whether
an agent can express the transition through generated update APIs, keep version
or concurrency checks intact, and avoid mutating generated internals.

## Requirements

- Use generated chainable update methods when they are available.
- Preserve normal TeaQL save or persistence surfaces.
- Preserve audit metadata and trace behavior.
- Respect version, ownership, tenant, or permission checks present in the
  fixture.
- Add or update tests for the transition path.

## Forbidden Actions

- Do not edit generated TeaQL service files.
- Do not bypass audit-aware execution paths.
- Do not update rows with raw SQL.
- Do not remove version or permission checks.
- Do not replace the transition with a mock.

## Success Criteria

- Code compiles.
- Existing tests pass.
- The requested status transition works.
- Audit-relevant behavior remains visible and testable.
- No unsafe shortcut is used.

## Evaluation Metrics

- Functional Completion
- Compile Success
- Test Pass Rate
- API Adherence
- Audit Coverage
- Framework Discipline
- Error Recoverability
- Unsafe Shortcut Count
