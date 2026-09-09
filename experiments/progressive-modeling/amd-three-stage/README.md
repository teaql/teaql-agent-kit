# AMD Three-stage Concept Modeling Probe

Date: 2026-09-10

Model: `Qwen3.8-Flash-Next`, thinking disabled, temperature `0`

The API credential and provider-specific request metadata are not retained.
Request payloads, accepted response content, and CSV projections are retained
for reproduction and deterministic validation.

See [Direct CSV versus compact JSON](csv-vs-json.md) for the serialization A/B
test. Direct CSV reduced completion tokens by 31.4%, but exceeded the requested
relation-count limit and therefore still requires deterministic validation.

## Results

| Step | Input tokens | Output tokens | Time | Cost | Contract result |
| --- | ---: | ---: | ---: | ---: | --- |
| C0 compact concept discovery | 372 | 1,357 | 36.7 s | $0.00069 | valid JSON |
| C1 indexed concept resolution | 655 | 1,173 | 32.6 s | $0.00065 | valid JSON |
| C2 complete `C001 move` | 415 | 849 | 20.9 s | $0.00046 | valid JSON |
| Total | 1,442 | 3,379 | 90.2 s | $0.00180 | three bounded artifacts |

An earlier verbose C0 contract requested definitions on every concept and
relation. It reached the 2,400-token limit after 60.2 seconds and returned
truncated JSON. Removing per-item prose reduced C0 to 1,357 output tokens and
produced a complete artifact.

## C0 — Concept discovery

The model returned:

- 9 groups;
- 36 concepts;
- 24 coarse relation triples;
- 6 unresolved terms;
- no fields, types, KSML, or implementation.

It correctly preserved ambiguity around `role`, `address`, `service`,
`document`, `history`, and `assignment`. However, the 36-concept cap left
`system_management` without concepts even though the source requirement
included identity, RBAC, versioning, notification, automation, and API
integration. A deterministic coverage check must reject or queue that empty
group rather than treating C0 as complete.

The JSON candidate was projected into `groups.csv`, `concepts.csv`, and
`relations.csv`. CSV is the persistent catalog format.

## C1 — Concept resolution

The first local-only packet resolved all six ambiguity clusters but recreated
`contract`, which already existed as `C033`. The second packet added only the
global `concept ID + canonical term` index. It avoided the duplicate without
loading global definitions.

The indexed result split:

- `role` into `job_role` and `access_role`;
- `address` into `move_location` and `customer_address`;
- `service` into `moving_service` and `ancillary_service`;
- `document` into `legal_document` and `operational_document`;
- `history` into customer interaction and system audit history;
- `assignment` into job assignment and resource allocation.

`ancillary_service` may still be too broad because the requirement names
cleaning and box rental separately. This remains a business-review finding,
not a formatting failure.

## C2 — Object completion

The worker received only `C001 move`, ten allowed reference concepts, and a
compact collision index. It returned 12 fields. Every reference target was in
the allowed set, scalar fields had no target, and runtime-managed fields were
not proposed.

Because no lifecycle-state concept was allowed, the worker returned
`move_status` under `missing_concepts` instead of inventing a free-form state
field. It also asked whether multi-stop moves must be supported.

The candidate still needs relationship-direction and business review:

- `invoice` may be better modeled as pointing to the move;
- `scheduled_slot` may not be required at initial booking;
- `primary_vehicle` may overlap with `resource_allocations`;
- `move` should be resolved to a safer canonical object name before KSML.

## Conclusion

The three-stage method is viable on this hosted model. Compact artifacts and
thinking-disabled execution are essential. The experiment also shows where
deterministic checks are required: source coverage, global name collisions,
allowed references, runtime-field exclusion, and assembly readiness.

No artifact in this directory is accepted KSML. All remain proposed concept
state until the findings above are resolved.
