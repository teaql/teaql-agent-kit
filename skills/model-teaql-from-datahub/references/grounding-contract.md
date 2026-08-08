# DataHub Grounding Contract

Use this contract after saving the sanitized DataHub responses and before
finalizing the first complete KSML model.

## Evidence Rules

Apply the narrowest claim supported by the saved evidence.

| Evidence | Supports | Does not establish by itself |
| --- | --- | --- |
| Dataset URN, platform, environment | Source identity | TeaQL bounded context or object name |
| Schema field and native type | Source field existence and source type | Exact TeaQL type semantics |
| Nullability | Source nullability | Business-required optionality in every workflow |
| Field tag or classification | Structured field classification | Runtime enforcement |
| Glossary term | Defined business vocabulary when its definition is captured | A relationship or cardinality |
| Foreign key or documented join | A source-level join | Aggregate ownership or lifecycle |
| Lineage | Data flow and impact | Domain reference direction or cardinality |
| Description | Authored prose | A structured policy or verified relationship |
| Ownership | Data stewardship | Application authorization policy |

Use this relationship evidence order:

1. explicit foreign key or documented join;
2. captured structured relationship metadata;
3. glossary or lineage as supporting context only;
4. names and descriptions as an explicit agent inference.

Do not describe an empty query result as proof that a relationship or policy
does not exist. Record only that it was not present in the captured response.

## Decision Classes

- `datahub-fact`: Directly represented from saved DataHub evidence. Cite an
  exact URN plus JSON pointer, response item, or equivalent locator.
- `agent-inference`: Renaming, semantic conversion, relationship hypothesis,
  policy interpretation, or other judgment not directly established by the
  evidence.
- `teaql-framework`: Model content required for TeaQL infrastructure or
  generation rather than sourced business metadata.
- `unresolved`: Missing or conflicting evidence whose resolution could change
  the domain contract.

## Ledger Template

Create one row for every TeaQL business object, property, relationship, state,
and policy. Also create a row for every selected DataHub field that is
intentionally excluded.

```markdown
# DataHub Grounding Ledger

## Snapshot

- Requirement: <original request or delta>
- Baseline model: <path, revision, or none>
- Target model: <absolute path>
- DataHub sources: <URNs and environments>
- Context artifact: <absolute path and optional SHA-256>
- Retrieval: <time, query arguments, tool/server identity when available>

## Decisions

| ID | TeaQL element | Decision class | DataHub evidence | Mapping or rationale | Status |
| --- | --- | --- | --- | --- | --- |
| D-001 | `payment_transaction.currency_code` | `datahub-fact` | `<URN>#/schemaMetadata/fields/1` | `VARCHAR` represented by a KSML string sample | accepted |
| D-002 | `payment_transaction.payment_account -> user_account` | `agent-inference` | `<URN>#/schemaMetadata/fields/0` | Name suggests an account reference; no captured FK proves it | review |
| D-003 | `payment_transaction.create_time` | `teaql-framework` | N/A | TeaQL lifecycle timestamp | accepted |
| D-004 | `payment_transaction.some_field` | `unresolved` | `<URN>#/...` | Conflicting type evidence | blocked |

## Selected Source Coverage

| DataHub source element | Outcome | Decision ID |
| --- | --- | --- |
| `<URN>#/schemaMetadata/fields/1` | mapped | D-001 |
| `<URN>#/schemaMetadata/fields/4` | intentionally excluded: <reason> | D-005 |

## Model Delta

- Added: <objects, fields, relationships, policies>
- Changed: <before -> after>
- Preserved: <important baseline areas intentionally unchanged>
- Removed: <items and evidence or requirement supporting removal>

## Unresolved Decisions

- <decision, impact, conservative fallback, required evidence or user choice>
```

Use `N/A` rather than inventing a DataHub locator for framework additions.
Avoid copying sensitive descriptions into the ledger when a paraphrase and
locator are sufficient.

## Coverage Gate

Before handoff, verify all of the following:

- Every modeled business object has a DataHub source or an explicit inference.
- Every business property has a source locator, inference, or framework label.
- Every relationship records its supporting evidence and assumed direction or
  cardinality.
- Every policy records whether it came from structured metadata or free text.
- Every selected source field is mapped, intentionally excluded, or unresolved.
- Existing-model work records the baseline and the requested model delta.
- Raw context, ledger, and KSML paths exist and contain no credentials.
- Contract-blocking unresolved decisions are reported before TeaQL evaluation.

Counts summarize the ledger but never replace its decision-level evidence.
