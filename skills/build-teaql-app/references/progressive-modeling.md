# Progressive Modeling Protocol

Use this protocol when the planned domain is too large to model reliably in
one context window or when the available model is small, private, slow, or
instruction-sensitive.

## Objective

Build one globally consistent KSML model through small, deterministic,
recoverable steps:

```text
business outcome
  -> concept discovery
  -> concept resolution
  -> object completion
  -> valid foundation
  -> module closures
  -> relation closure
  -> global governance
  -> frozen model
```

The protocol reduces context demand. It does not relax TeaQL evaluation or
allow code generation from an incomplete domain.

## Persistent artifacts

Keep these under the application's model directory:

```text
models/
  main.xml
  <module>.xml
  .teaql/
    progressive-modeling.md
    concepts.csv
    relations.csv
    object-completions/
```

`progressive-modeling.md` is application-owned planning state, not KSML and
not generator input. Copy the companion template and keep it compact. It must
record facts required to resume work without replaying the full conversation.

## Checkpoints

### C0 — Concept discovery

Extract compact language-neutral artifacts:

- vocabulary with stable temporary IDs;
- broad groups with stable IDs;
- coarse relation triples between concept IDs;
- ambiguous or overloaded source terms.

Do not use KSML rules, propose fields, or resolve ambiguous words here. Keep
the artifact compact: IDs, canonical candidates, groups, relation verbs, and
ambiguity flags. If it cannot fit the output budget, process one source module
batch at a time and merge through deterministic ID checks.

### C1 — Concept resolution

Process one ambiguity cluster at a time. Supply:

- the active terms and their local meanings;
- affected group IDs;
- neighboring concept IDs;
- the global `concept ID + canonical term` index, without full definitions.

Return split, rename, merge, reuse, or unresolved operations with lineage. A
proposed canonical term that already exists must reuse its existing concept
ID. Do not add fields or redesign unrelated concepts.

### C2 — Object completion

Complete exactly one canonical business object per request. Provide its ID,
definition, group, accepted neighboring concepts, and an explicit allowed
reference set. Field candidates remain language-neutral. They may contain a
semantic type, required/optional state, and allowed target concept ID.

References outside the allowed set are forbidden. The worker must return a
`missing_concepts` item rather than invent a target. Runtime-managed identity,
version, audit, timestamps, and tenant-root fields are not proposed here.

See [`concept-modeling.md`](concept-modeling.md) for the artifact contracts and
context packets.

### P1 — Valid foundation and deterministic assembly

Select a connected vertical slice from accepted concept and object-completion
artifacts. A deterministic assembler—not free-form model output—creates the
entry root, domain root, and smallest useful KSML slice. Every object written
must be complete enough to evaluate. Evaluate and repair to zero Errors before
expanding the model.

The foundation must include at least one real business object in addition to
the domain root and constants. A root-only skeleton is rejected by
`KSML-BUSINESS-003` and is not a valid checkpoint.

This is a valid partial domain, not a placeholder model. Record its evaluation
counts and completed object names in the ledger.

### P2 — Module closure

For each module, one at a time:

1. Load the module's ledger entry, its file, and only its one-hop dependency
   summaries.
2. Complete its objects, fields, constants, local relationships, audit masks,
   and connection to the domain graph.
3. Evaluate the complete current input directory.
4. Repair only reported locations and re-evaluate.
5. Mark the module complete only at zero Errors.

If a referenced future module is not present, either defer that relationship
in the ledger or introduce a complete minimal dependency object. Never add a
fake placeholder object merely to satisfy the evaluator.

### P3 — Relation closure

Process deferred cross-module references in bounded batches. For each batch:

- identify both owning modules;
- load both module files and the relation ledger entry;
- add the relationship and any required inverse/query semantics;
- check for cycles and root connectivity;
- evaluate and record the result.

### P4 — Global governance

Use the complete model for checks that cannot be proven module-locally:

- root uniqueness and graph connectivity;
- constant completeness and stable IDs;
- primary and secondary state ordering;
- privacy/audit masking;
- cross-language keyword and naming safety;
- circular reference depth;
- module ownership and duplicate concepts;
- unresolved ledger decisions.

No planned module, relation, or blocking question may remain open at freeze.

### P5 — Freeze and generate

Evaluate the complete model directory once more. Record:

- input path;
- model revision or commit;
- deterministic model hash;
- Errors, Warnings, Suggestions, and Solids;
- resolved or explicitly accepted Warnings;
- requested generation targets.

Only a complete plan plus zero Errors opens the generation gate. Generation,
Assist, compilation, and runtime verification follow the normal Skill.

## Context packet for a modeling turn

Give a constrained model only this packet:

```text
Outcome: <one sentence>
Checkpoint: <C0-C2 or P1-P5>
Current module: <name>
Current objects: <names and responsibilities>
One-hop dependencies: <names and relationship direction>
Accepted decisions: <only decisions affecting this edit>
Open findings: <current evaluator findings>
Task: <one bounded edit and its done condition>
Forbidden: do not redesign completed modules or invent placeholders
```

The full conversation, full rule catalog, completed modules outside the
dependency closure, and generated source are not part of this packet.

## Evidence and stop rules

For each evaluation retain the checkpoint, command, input hash, counts, and
changed files. Stop when:

- five repair rounds in one checkpoint are exhausted;
- a business decision changes module ownership or the domain boundary;
- resolving an error requires loading more than one-hop dependencies;
- the model plan and KSML disagree about what is complete;
- final evaluation has Errors or a blocking unresolved decision.

Report the exact condition. Do not hide it by advancing the checkpoint.

## Experiment metrics

When comparing this protocol with one-pass modeling, record:

- peak input context and total input tokens;
- objects completed per checkpoint;
- evaluation rounds and findings per module;
- cross-module reference errors;
- number of completed modules rewritten later;
- final global evaluation counts;
- elapsed time and resume success from a fresh context.

The experiment succeeds only if global quality remains equal or better while
peak context and late large rewrites decrease.
