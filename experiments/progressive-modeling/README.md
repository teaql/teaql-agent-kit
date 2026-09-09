# Progressive Modeling Smoke Test

Date: 2026-09-10

This experiment checks whether a model can grow through independently valid
checkpoints without permitting generation from an incomplete planned domain.
It intentionally uses a tiny fixture; the next experiment should compare the
same large private domain with one-pass and progressive modeling.

## Reproduce

Use `cargo-teaql 2.0.14` and the current TeaQL evaluation service:

```bash
cargo teaql --input experiments/progressive-modeling/stage-1/model.xml evaluate
cargo teaql --input experiments/progressive-modeling/stage-2/model.xml evaluate
```

## Retained results

| Stage | Scope | Errors | Warnings | Suggestions | Solids |
| --- | --- | ---: | ---: | ---: | ---: |
| invalid root-only probe | domain root only | 1 | 0 | 0 | 7 |
| stage 1 | root + first business object | 0 | 1 | 0 | 9 |
| stage 2 | add a related business object | 0 | 0 | 0 | 11 |

The invalid probe was rejected by `KSML-BUSINESS-003`. This proves that a
progressive foundation must be a real vertical slice, not a placeholder root.
The stage-1 warning (`KSML-MODULE-003`) disappeared after the Operations module
gained its second related object in stage 2.

## Separate evaluator drift found

An intermediate probe added a constant with `display_order="integer()"` and a
domain-root relationship. The current `/latest/evaluate` response produced:

- `KSML-REFERENCE-003`, treating `integer` as a referenced object;
- `KSML-CONSTANT-002`, requesting a root field named after the root object;
- two `KSML-CONSTANT-008` findings requesting the relationship in each value.

Those findings conflict with the current Agent Kit guidance that uses
`integer()` for ordinal fields and omits the Fix/Context-managed root relation
from constant values. They are recorded as service/kit version drift and were
not hidden inside the successful progressive-modeling result.

## Next A/B test

Run the same 100+ object private-domain requirement twice:

1. one-pass model construction;
2. progressive construction using the ledger template.

Compare peak context, total input, evaluation rounds, cross-module reference
errors, late rewrites, wall time, final counts, and fresh-context resume rate.
