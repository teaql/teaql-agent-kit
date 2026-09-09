# AMD CSV-first Moving Company Modeling Probe

Date: 2026-09-10

This experiment asks `Qwen3.8-Flash-Next` to model the moving-company domain
through flat CSV artifacts. The model never writes KSML. A deterministic local
runner validates and assigns IDs, requests fields in bounded group packets,
and assembles a candidate KSML model.

The API credential is supplied only through `AMD_API_TOKEN`; it is never
written to this directory.

## Reproduce

```bash
AMD_API_TOKEN=... python3 run.py
cargo teaql --input output/ evaluate
```

Generated evidence is retained under `raw/` and `output/`. A run does not
overwrite accepted evidence silently: remove or archive the output explicitly
before starting another measurement.

## Final retained result

The final accepted pipeline used 30 model calls. One superseded batch
resolution call is retained separately and excluded from the accepted-path
totals.

| Measure | Result |
| --- | ---: |
| Source groups | 14 |
| Discovered concepts | 48 before local group repair |
| Catalog after minimum group repair | 55 |
| Ambiguities selected for bounded review | 8 |
| Catalog after accepted resolution | 61 |
| Accepted business fields | 344 |
| Missing concepts | 0 |
| Field validation errors | 0 |
| Accepted-path prompt tokens | 22,311 |
| Accepted-path completion tokens | 5,902 |
| Accepted-path total tokens | 28,213 |
| Accepted-path provider cost | $0.00574 |

The candidate KSML was assembled by local code, not by the model. The TeaQL
evaluation result was:

```text
Errors:       0
Warnings:    51
Suggestions:  8
Solids:      165
```

The remaining warnings identify the next modeling stages rather than a broken
artifact:

- 33 reference fields still carry an `_id`-style name;
- 14 finite-set strings should be promoted to constant objects;
- 4 privacy fields should be added to audit masks.

The eight suggestions consist of two append-only log candidates and six
additional privacy-mask candidates. They are retained for later review rather
than silently rewritten.

## Pipeline

```text
business requirement
  -> concept discovery CSV
  -> minimum group coverage validation and local repair
  -> ambiguity scan CSV
  -> one-concept-at-a-time resolution CSV
  -> per-group field CSV
  -> ID, type, reference, cardinality and uniqueness validation
  -> deterministic KSML assembly
  -> TeaQL evaluation
```

The model is never asked to emit XML or remember TeaQL grammar. Runtime-managed
fields, root ownership, reserved-word replacement, boolean naming, module-key
normalization, and mandatory secret masking are deterministic assembler
responsibilities.

## Prompt optimization findings

This probe required several real feedback cycles. Local runs archive rejected
outputs under ignored `raw-attempt-*` and `output-attempt-*` directories. The
accepted raw requests/responses are versioned; rejected behavior is summarized
below without permanently duplicating every provider envelope.

| Finding | Change to the harness |
| --- | --- |
| The first response left five platform groups with only 1-2 concepts. | Reject incomplete coverage and request only the missing group rows. |
| Small repair responses omitted CSV headers and once used an invalid enum. | Retain the violation, parse only known columns, and locally retry the failed slice. |
| Natural-language rationale made CSV more fragile. | Keep rationale out of generation tables; use it only in the ambiguity-review artifact. |
| Batch resolution recreated global concepts. | Resolve one ambiguous concept per request with a compact global term index. |
| Passing rationale caused 23 speculative splits and grew 56 concepts to 79. | Require distinct persisted identity, lifecycle, or ownership; cap a scan at eight candidates. |
| Discovery flags leaked into the dedicated ambiguity scan. | Reset candidate state before applying the scan result. |
| The model attempted to split the domain root and reused global terms. | Treat resolutions as candidates; deterministically reject root splits and name collisions. |
| One field was duplicated and several references lacked targets. | Locate the owning group and rerun only that field packet. |

Three formatting deviations remain in the final accepted path: a concept
header, ambiguity header, and resolution header were omitted. The parser could
recover them because those sections contain only fixed short columns. These
remain findings; recovery is not reported as contract compliance.

Across all prompt-development attempts, including rejected experiments, the
provider cost was approximately `$0.02468`. This is useful evidence that
prompt evolution can be driven by deterministic checks at low cost on this
hosted model.

## Interpretation

CSV works well for progressive model construction when each call emits one
flat relation and the harness owns IDs, validation, retry, and assembly. It is
not safe to accept CSV merely because it parses: the most important failures
in this experiment were semantic over-splitting, global-name reuse, missing
reference targets, and incomplete group coverage.

The prompt is therefore a versioned implementation component. Parser findings
and TeaQL evaluation rules form its regression suite. Prompt improvements may
change candidate quality, but deterministic gates prevent those changes from
silently weakening the accepted model.
