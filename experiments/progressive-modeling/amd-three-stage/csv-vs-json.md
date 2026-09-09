# Direct CSV versus compact JSON

Date: 2026-09-10

Model and requirement were the same in both C0 requests. Thinking was disabled
and temperature was zero.

| Format | Prompt tokens | Completion tokens | Content characters | Time | Cost |
| --- | ---: | ---: | ---: | ---: | ---: |
| Compact JSON | 372 | 1,357 | 3,806 | 36.7 s | $0.00069 |
| Direct CSV bundle | 393 | 931 | 1,773 | 22.4 s | $0.00050 |
| Change | +5.6% | -31.4% | -53.4% | -39.1% | -28.4% |

The direct CSV response contained four sections: groups, concepts, relations,
and unresolved terms. It was complete and syntactically parseable. It returned
36 concepts and all six requested ambiguous terms.

It did not fully obey the contract: the request allowed at most 24 relations,
but the model returned 29. The output also remained a custom multi-section CSV
bundle rather than one standard CSV table.

## Decision

Use direct CSV for flat C0 vocabulary discovery when token and latency cost are
important. Parse and validate every section before accepting it. Use separate
files as persistent artifacts after parsing.

Keep JSON for C1 resolution and C2 object completion because lineage,
replacement operations, missing concepts, and questions are nested structures.
Encoding those structures into CSV would require custom conventions and weaken
validation clarity.
