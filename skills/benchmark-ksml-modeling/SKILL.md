---
name: benchmark-ksml-modeling
description: Run the fixed TeaQL modeling benchmark against a model and agent harness, retaining evidence from KSML evaluation and repair. Use for comparable modeling benchmark runs, not ordinary application development or code generation.
---

# Benchmark KSML Modeling

Tracking: [Agent Kit issue #43](https://github.com/teaql/teaql-agent-kit/issues/43)
and [conformance issue #10](https://github.com/teaql/teaql-conformance/issues/10).

Run benchmark `teaql-modeling-001` from the frozen
[moving-company requirement](references/requirement.md). The authoritative
protocol is in `teaql-conformance/benchmarks/modeling/001-moving-company/`;
use its `protocol.md` when available. Do not change the requirement, add a
target object count, or provide a reference model to the tested agent.
The requirement's SHA-256 is
`2af9a8e439363fc4bc7d18b0e82695d4911ef162cc9634961833a714f88f01bb`.
Check it before the run; report `FIXTURE_DRIFT` and stop if it differs.

This Skill stops at a complete, evaluated KSML model. Do not generate a
library or workspace, implement an application, compile code, or run runtime
tests as part of this benchmark.

## Run

1. Before modeling, record a run ID, tested model and agent/harness versions,
   TeaQL client and evaluation-service versions, resource limits, and the
   requirement file SHA-256. Use the same declared limits for compared runs.
   If a version or usage figure cannot be measured, mark it unknown.
2. Model the fixed requirement. A large model may use the progressive
   concept/module workflow described in
   [`../build-teaql-app/references/progressive-modeling.md`](../build-teaql-app/references/progressive-modeling.md).
   For KSML syntax, use its
   [golden example](../build-teaql-app/references/golden-example.xml) and
   [multi-file example](../build-teaql-app/references/multi-file-golden-example/README.md)
   only as grammar references, never as a business answer. Save a nonempty,
   well-formed model before the first evaluation.
3. Evaluate the saved model with the current TeaQL client. For multi-file
   models evaluate the **directory**, not just `main.xml`, so all includes
   participate. Record the exact command, raw report, model-file hashes, and
   counts. Fix reported defects in the model and repeat; do not hide failed
   rounds. For example: `cargo teaql --input models/ evaluate`.
4. Run a final global evaluation and map each of the requirement's 14 items
   to model objects/relations. Zero Errors alone does not prove coverage.
   Stop at zero Errors plus complete coverage, or at the declared resource
   limit. Disclose remaining Warnings, Suggestions, and partial coverage.

Retain a compact per-round ledger and final report with the fields specified
by the conformance protocol. Treat Solids and object count as descriptive
evidence, not points to maximize. Preserve source file and line number for
findings when the evaluator supplies them. Do not fabricate wall-clock,
token, context, or cost measurements. A timeout, unavailable service, or
partial model is a recorded non-pass result, never a green run.
