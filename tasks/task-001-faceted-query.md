# Task 001 - Faceted Query

## Goal

Implement or repair a faceted business query using the TEAQL Q API.

## Target Stack

Java or Rust TEAQL stack.

## Background

Business applications often need filtered result lists with summary facets. This
task evaluates whether an agent can keep the query pipeline explicit and use the
generated TEAQL query surface instead of bypassing it.

## Requirements

- Start from the generated Q collection API for the target entity.
- Apply fixed business filters before dynamic search.
- Apply deterministic ordering.
- Apply pagination.
- Add facet or aggregation declarations when required by the task fixture.
- Select only fields required by the response when projection helpers are
  available.
- Add or update tests if appropriate.

## Forbidden Actions

- Do not write raw SQL.
- Do not manually edit generated TeaQL service files.
- Do not invent Q API methods.
- Do not remove existing tests.
- Do not hard-code query results.

## Success Criteria

- Code compiles.
- Existing tests pass.
- The query returns the requested list and facet results.
- The implementation follows the generated Q API boundary.
- No hallucinated API calls remain in the final code.

## Evaluation Metrics

- Functional Completion
- Compile Success
- Test Pass Rate
- API Adherence
- Hallucinated API Count
- Framework Discipline
- Error Recoverability
- Unsafe Shortcut Count
