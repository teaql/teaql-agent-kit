# Compact JSON versus direct CSV and Markdown

Date: 2026-09-10

Model and requirement were the same in all C0 requests. Thinking was disabled
and temperature was zero.

| Format | Prompt tokens | Completion tokens | Content characters | Time | Cost |
| --- | ---: | ---: | ---: | ---: | ---: |
| Compact JSON | 372 | 1,357 | 3,806 | 36.7 s | $0.00069 |
| Direct CSV bundle | 393 | 931 | 1,773 | 22.4 s | $0.00050 |
| Markdown tables | 399 | 1,028 | 2,244 | about 33.5 s | $0.00054 |

Relative to compact JSON, direct CSV used 31.4% fewer completion tokens and
Markdown used 24.2% fewer. Markdown required 10.4% more completion tokens than
CSV and produced 26.6% more content characters.

The direct CSV response contained four sections: groups, concepts, relations,
and unresolved terms. It was complete and syntactically parseable. It returned
36 concepts and all six requested ambiguous terms.

It did not fully obey the contract: the request allowed at most 24 relations,
but the model returned 29. The output also remained a custom multi-section CSV
bundle rather than one standard CSV table.

The Markdown response returned the same 9 groups, 36 concepts, 29 relations,
and 6 unresolved terms. It also violated the 24-relation limit. More
importantly, it omitted the mandatory Markdown separator row after every table
header, so the result is Markdown-like text rather than valid GitHub-flavored
Markdown tables. The retained artifact is the exact model output and preserves
this failure as evidence.

## Decision

Use direct CSV for flat C0 vocabulary discovery when token and latency cost are
important. Parse and validate every section before accepting it. Use separate
files as persistent artifacts after parsing.

Use Markdown only as a generated human-review projection after structured data
has passed validation. It is easier to inspect than JSON or CSV, but it adds
syntax overhead and, in this run, was less structurally reliable than either
machine-oriented format.

Keep JSON for C1 resolution and C2 object completion because lineage,
replacement operations, missing concepts, and questions are nested structures.
Encoding those structures into CSV would require custom conventions and weaken
validation clarity.
