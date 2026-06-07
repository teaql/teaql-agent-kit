# Task 005 - Search With Text

## Goal

Add or repair text search support while respecting the TEAQL data service and
query boundaries.

## Target Stack

Java or Rust TEAQL stack.

## Background

Search integration often tempts agents to bypass framework boundaries. This task
evaluates whether an agent can connect text search behavior through supported
TEAQL APIs and preserve business filters, audit context, and result ordering.

## Requirements

- Use the documented TEAQL search or dynamic query surface available in the
  target stack.
- Keep fixed business and security filters around dynamic search.
- Preserve deterministic sorting and pagination.
- Avoid loading broad data sets into memory for filtering unless the fixture is
  intentionally small and bounded.
- Add or update tests for search behavior.

## Forbidden Actions

- Do not bypass generated request or Q APIs.
- Do not manually compose SQL for normal search behavior.
- Do not remove tenant, permission, or status constraints.
- Do not manually edit generated service code.
- Do not fake search results.

## Success Criteria

- Code compiles.
- Existing tests pass.
- Text search returns the requested records.
- Business constraints still apply to search results.
- The implementation remains inside supported TEAQL boundaries.

## Evaluation Metrics

- Functional Completion
- Compile Success
- Test Pass Rate
- API Adherence
- Audit Coverage
- Framework Discipline
- Hallucinated API Count
- Unsafe Shortcut Count
