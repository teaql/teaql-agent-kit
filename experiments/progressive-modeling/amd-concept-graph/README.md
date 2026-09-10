# AMD Concept Graph Line Protocol Probe

Date: 2026-09-10

This probe tests a minimal first-stage modeling contract. The model emits only
groups, concepts, coarse relations, and unresolved terms. A local parser
assigns stable IDs and projects accepted facts into CSV.

The prompt asks the model to avoid bare reserved words across Java, Rust,
TypeScript, Go, Swift, C#, Python, and SQL. The parser independently enforces a
compact cross-language denylist; later TeaQL evaluation remains the global
keyword oracle.

## Protocol

```text
group <group_key>
concept <term> <root|entity|ambiguous>
relation <from_term> <verb> <to_term>
unresolved <term>
```

Every line contains one fact. A `group` line opens the group used by following
concept lines. There are no headers, commas, quotes, indentation, Markdown
delimiters, or model-assigned IDs.

## Reproduce

```bash
AMD_API_TOKEN=... python3 run.py
```

The bearer credential is read from the process environment and is not written
to any retained artifact. `concept-graph.txt` preserves the latest model output;
`concepts.csv` and `relations.csv` are deterministic projections made by the
local parser.

## Result

Four prompt/protocol iterations were executed against `Qwen3.8-Flash-Next`.
Rejected outputs are retained because the purpose of this probe is to measure
contract adherence, not manufacture a green result.

| Attempt | Protocol/change | Raw groups | Raw concepts | Raw relations | Tokens | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 1 | Explicit group on every concept | 14 | 45 | 57 | 1,567 | One two-word relation verb |
| 2 | Explicit four-token relation reminder | 14 | 120 | 216 | 3,363 | Model expanded beyond both budgets and hit the output cap |
| 3 | Exact count budget | 9 | 44 | 53 | 1,455 | Model omitted the repeated group key and collapsed groups |
| 4 | Group-context protocol | 14 | 50 | 50 | 1,490 | Three deterministic findings |

The fourth attempt is the most useful protocol result. It reduced repetition,
stayed inside the concept and relation budgets, and cost `$0.00041518`. Its
remaining findings were:

- `references` was emitted as a relation verb even though it is in the SQL
  denylist;
- the group name `finance` was used as a relation endpoint twice, although no
  concept named `finance` exists.

Across all four prompt-development attempts the model consumed 7,875 tokens
(3,119 prompt and 4,756 completion) at a reported cost of approximately
`$0.00268013`.

## Interpretation

The line protocol is a better first-stage interchange than asking this worker
for CSV. It has no escaping or header failure mode, assigns no unstable IDs,
and lets the harness project accepted facts into CSV afterward. Making the
current group implicit also removes one repeated token from every concept.

Prompt instructions are not enforcement. Even with temperature zero and an
explicit denylist, the model used a reserved word and an undeclared endpoint.
It also varied substantially between calls. Therefore the accepted pipeline
must retain these deterministic gates:

1. line grammar and token arity;
2. unique, declared concepts and relation endpoints;
3. exactly one domain root;
4. group/concept/relation budgets;
5. a shared Java, Rust, TypeScript, Go, Swift, C#, Python, and SQL denylist;
6. exact correspondence between `ambiguous` and `unresolved` facts.

The next implementation step should be a bounded repair call containing only
the rejected facts plus the accepted concept vocabulary. A full regeneration
would discard good work and reintroduce the observed variance.
