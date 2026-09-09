# Progressive Concept Modeling

The first progressive-modeling stages operate on language-neutral business
concepts. KSML is introduced only after vocabulary, ownership, relationships,
and object fields are accepted.

## C0 — Concept discovery

Persist the model output deterministically as two CSV files.

`concepts.csv`:

```csv
concept_id,term,group_id,ambiguity,status
C001,move_order,G001,none,proposed
```

`relations.csv`:

```csv
from_concept_id,verb,to_concept_id,status
C001,requested_by,C012,proposed
```

Required checks:

- concept, group, and relation IDs are unique and well formed;
- every group and relation endpoint exists;
- canonical candidates use lowercase snake_case;
- ambiguous source terms stay unresolved;
- this stage contains no fields, types, or KSML fragments.

For flat C0 discovery, direct CSV can materially reduce output tokens. Require
separate named sections or separate calls, parse every row deterministically,
and enforce count, ID, and reference limits before acceptance. Compact JSON is
the safer fallback when the provider frequently emits malformed CSV. CSV is
the persistent catalog; free-form prose is not retained as model state.

Do not generalize this optimization to nested artifacts automatically. C1
resolution lineage and C2 missing-concept/question structures remain clearer
and safer as strict JSON.

## C1 — Concept resolution

Send only one ambiguity cluster, its local neighbors, and a global name index:

```text
Active: role
Local meanings: employee responsibility; RBAC access grouping
Groups: G002 employees; G009 identity_access
Global names: C001 move_order; ...; C033 contract
```

The global index prevents a small local packet from recreating a concept that
already exists elsewhere. It contains only IDs and terms, so its cost remains
small even for a large model.

Accepted operations are `split`, `rename`, `merge`, `reuse`, and
`still_unresolved`. Every operation retains source IDs and rationale. Apply
operations deterministically and reject duplicate canonical terms.

## C2 — Object completion

One request completes one object:

```json
{
  "task": "complete_object",
  "concept": {
    "id": "C001",
    "term": "move_order",
    "definition": "One requested moving engagement"
  },
  "allowed_references": [
    {"id": "C012", "term": "customer_account"},
    {"id": "C005-A", "term": "move_location"}
  ],
  "global_names": ["C001 move_order", "C012 customer_account"],
  "limits": {"minimum_fields": 8, "maximum_fields": 14}
}
```

The result contains field name, meaning, semantic type, required state, and a
target concept ID for references. Scalar fields use no target. When a required
target is absent, the result must use `missing_concepts`; it must not invent a
reference or encode a state concept as a free-form string.

Reject an object completion when:

- a reference target is outside the allowed set;
- a scalar field contains a target ID;
- a reference lacks a target ID;
- runtime-managed fields are proposed;
- field names collide;
- field count exceeds the supplied budget;
- the response contains KSML or implementation code.

## Assembly boundary

Only accepted catalog rows and object completions enter deterministic KSML
assembly. The assembler applies TeaQL-specific naming, system fields, constant
rules, root association, module files, and XML syntax. TeaQL evaluation then
acts as the global oracle.

This boundary lets a constrained private model contribute local business
knowledge without needing to memorize TeaQL grammar or hold the entire domain
in one context window.
