---
name: model-teaql-from-datahub
description: "Create or evolve a complete TeaQL KSML model grounded in existing DataHub metadata, with traceability from each business object, field, relationship, and policy to source evidence or an explicit inference. Use when a user provides DataHub dataset URNs, asks to build from an existing data catalog or enterprise schema, wants DataHub context incorporated into TeaQL modeling, or needs a model change assessed against DataHub schema, tags, glossary terms, ownership, or lineage."
---

# Model TeaQL from DataHub

Use existing enterprise context before interpreting natural-language
requirements. Treat DataHub as the authority for captured source facts and the
user's request as the desired business outcome or delta. Do not present a
TeaQL projection as a lossless copy of DataHub.

## Mandatory Workflow

Follow this order:

1. Read the target repository's nearest `AGENTS.md` and record the requested
   outcome, model target, supplied DataHub locators, and existing local model.
2. Discover the available DataHub connector or MCP tools. Query the exact
   datasets and the metadata needed for the request.
3. Save the raw, sanitized DataHub responses before modeling. Record source
   URNs, environment, query arguments, retrieval time, and tool or server
   identity when available.
4. Read [`references/grounding-contract.md`](references/grounding-contract.md).
   Start the grounding ledger from the captured evidence.
5. Draft and save one complete KSML model. When a local model already exists,
   preserve it as the baseline and apply the requested delta instead of
   reconstructing the domain from scratch.
6. Complete the ledger and coverage checks. Label every material decision as
   `datahub-fact`, `agent-inference`, `teaql-framework`, or `unresolved`.
7. Continue with the repository's `build-teaql-app` skill, using the saved
   KSML as the first complete model target. Let that skill own client version
   checks, evaluation, repair, generation, implementation, and verification.

Never run a TeaQL evaluation or model-derived command before step 5. Do not
copy versioned TeaQL commands into this skill.

## Acquire Only Relevant Context

Prefer purpose-built DataHub tools over generic browsing. Inspect the tool
catalog instead of assuming a fixed MCP tool name. Retrieve only what can
affect the requested model:

- dataset identity, platform, environment, and schema fields;
- native types, nullability, descriptions, and structured classifications;
- tags, glossary terms, domains, owners, and structured policies;
- explicit foreign keys, documented joins, and relevant lineage;
- existing DataHub model or data-product identity and version metadata.

Expand from a supplied dataset only when the evidence points to another
dataset or the user request requires it. Record each additional locator and
why it was queried.

Sanitize credentials, private endpoints, personal data, and unrelated
enterprise metadata before saving evidence. Never place access tokens in the
model, ledger, logs, or report.

## Separate Facts from Modeling Judgment

Apply these boundaries:

- Map a schema field or structured classification as `datahub-fact` only when
  the saved response contains it and the ledger cites an exact locator.
- Mark renamed objects, type conversions, aggregates, bounded-context splits,
  and other semantic transformations explicitly; source grounding does not
  make the transformation itself a raw DataHub fact.
- Create a TeaQL relationship from an explicit foreign key or documented join
  when available. Do not treat lineage alone as proof of a domain reference,
  direction, or cardinality.
- Treat name similarity, descriptions, and cross-dataset guesses as
  `agent-inference`. State the assumption and its impact.
- Mark generated identifiers, versions, timestamps, and other TeaQL-required
  infrastructure as `teaql-framework` rather than DataHub business fields.
- Leave a decision `unresolved` when missing evidence could materially change
  the domain contract. Ask the user only when the target cannot be completed
  safely with an explicit conservative assumption.

Do not invent business fields to make the model appear complete. Do not drop a
selected source field silently; map it, exclude it with a reason, or mark it
unresolved in the ledger.

## Apply Governance with Evidence

Use structured metadata before prose:

1. field-level tags or classifications;
2. structured policies or glossary terms with defined semantics;
3. dataset-level tags or classifications;
4. descriptions and free text.

When free text causes a TeaQL policy decision, label the decision
`agent-inference`. Record the quoted concept in paraphrase and cite its source
locator. Never claim that metadata propagation proves runtime enforcement.
Runtime behavior is verified only by an actual application-level policy test.

## Save Portable Artifacts

Follow target-repository conventions when present. Otherwise save:

```text
models/
├── model.xml
└── datahub-grounding/
    ├── context.json
    └── ledger.md
```

Keep the raw context independent from the ledger: evidence can be refreshed
without erasing prior modeling judgments. When updating an existing model,
include a compact baseline-to-target model delta in the ledger.

Do not copy source descriptions or ownership details into KSML comments when
an evidence locator and a short paraphrase in the ledger are sufficient.

## Handoff and Report

Before continuing with `build-teaql-app`, report:

```text
DataHub Grounding Ready
- Model: <absolute KSML path>
- Context: <absolute sanitized context path>
- Ledger: <absolute ledger path>
- Decisions: <facts>, <inferences>, <framework>, <unresolved>
```

Continue without waiting when there are no contract-blocking unresolved
decisions. In the final result, distinguish:

- what DataHub directly established;
- what the agent inferred or transformed;
- what TeaQL added for framework semantics;
- what remains unresolved;
- what model, generated-code, policy, compile, test, and runtime evidence was
  actually verified.
