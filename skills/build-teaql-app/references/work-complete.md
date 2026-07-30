# TeaQL Agent Kit — Work Complete

Build an evidence chain from the original requirement through the model and
generated API contract to the working result. Link concrete artifacts.

Never invent token savings or harness evidence. If telemetry is unavailable,
write `not reported`. Label estimates as `Estimated` and explain their basis.
Redact secrets. State what mechanical Review work is complete and what still
needs human business judgment; do not claim that Review was eliminated.

```text
TeaQL Agent Kit — Work Complete

Outcome: <what now works>
Model: <model file or directory>
Outputs: <generated or runnable output paths>
Verification: <evaluation, compile, test, and runtime results>

Original Modeling Prompt
<original requirement, with secrets redacted>

Modeling Result
- Service: <root name>
- Domain root: <business root>
- Objects: <business count>; constants: <constant count>
- Modules: <module names>
- Contract: <important relationships, states, tenancy, and assumptions>
- KSML evidence: <model link and one representative excerpt>

API Constraint Harness Evidence
- Generated guide: <local generated AGENTS.md path, or missing>
- Assist commands used: <exact commands and entity/action targets>
- API facts used: <exact generated query/update/save surfaces>
- Query policy: <checked>/<total> executions include purpose and comment
- Write policy: <checked>/<total> writes include audit_as or auditAs
- Generated files edited manually: <none, or explicit exception>
- Compile/test/runtime evidence: <commands and results>
- Code evidence: <links to query and write call sites>

Agent Kit Impact
- Token strategy: minimal skill + golden example; dynamic guidance from Generation Service evaluation
- Context: full local rule catalogs loaded <count> times; evaluation rounds <count>
- Token usage: <actual usage, or "not reported">
- Estimated context avoided: <estimate and basis, or "not measured">
- Review automation: <mechanical checks completed before human review>
- Human review focus: <business decisions, accepted warnings, or app effect>

Simple Next Use
1. Open <primary artifact or application URL>.
2. Run <one concrete command>.
3. Review <one concrete result>.

Execution Log
[request] <requirement captured>
[model] <path and result summary>
[check 1] <errors, warnings, suggestions>
[repair 1] <largest pattern fixed>
[contract] <generated guide and assist evidence>
[harness] <purpose/comment and audit coverage>
[build/test/run] <result>
[ready] <artifact ready for parallel review>
```

Use actual code from the completed application as evidence. Exact generated
methods must come from the local generated guide and assist output.

Typical constrained shapes:

```rust
Q::merchants()
    .purpose("Find merchants for search results")
    .comment("Search merchant names")
    .execute_for_list(&ctx)
    .await?;

merchant
    .audit_as("Update merchant details")
    .save(&ctx)
    .await?;
```

```java
Q.merchants()
    .purpose("Find merchants for search results")
    .comment("Search merchant names")
    .executeForList(userContext);

merchant
    .auditAs("Update merchant details")
    .save(userContext);
```
