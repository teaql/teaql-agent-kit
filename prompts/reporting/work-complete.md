# TeaQL Agent Kit Work Complete Report

Load this template only after the requested result is complete.

Build an evidence chain from the user's original request to the model, generated
API contract, constrained business code, and working result. Use actual values
from the run and link concrete artifacts.

Never invent token savings or harness evidence. If telemetry is unavailable,
write `not reported`. Label estimates as `Estimated` and state their basis.
Redact secrets from the original prompt and code excerpts.

Report Review reduction concretely: say which mechanical checks were completed
before human review and what still needs business judgment. Do not claim that
Review was eliminated.

## Output Template

```text
TeaQL Agent Kit — Work Complete

Outcome: <what now works>
Model: <concrete model file or directory>
Outputs: <generated or runnable output paths>
Verification: <evaluation, compile, test, and runtime results>

Original Modeling Prompt
<the user's original business requirement, with secrets redacted>

Modeling Result
- Service: <root name>
- Domain root: <business root>
- Objects: <business count>; constants: <constant count>
- Modules: <module names>
- Contract: <important relationships, states, tenancy decision, and assumptions>
- KSML evidence: <model link and one representative excerpt>

API Constraint Harness Evidence
- Generated guide: <local generated AGENTS.md path, or missing>
- Assist commands used: <exact commands and entity/action targets>
- API facts used: <exact generated query/update/save surfaces>
- Query policy: <checked count>/<query count> execution paths include purpose and comment
- Write policy: <checked count>/<save/update count> write paths include audit_as or auditAs
- Generated files edited manually: <none, or explicit exception>
- Compile/test/runtime evidence: <commands and results>
- Code evidence: <links to actual query and write call sites>

Agent Kit Impact
- Token strategy: minimal prompt + golden example; detailed rules requested only by Rule ID
- Context: full rule catalog loaded <0|count> times; on-demand Rule ID lookups <count>
- Token usage: <actual usage, or "not reported">
- Estimated context avoided: <estimate and basis, or "not measured">
- Review automation: <model errors, API misuse, and repeated patterns fixed before human review>
- Human review focus: <remaining business decisions, accepted warnings, application effect, or "none">

Simple Next Use
1. Open <primary artifact or application URL>.
2. Run <one concrete command>.
3. Review <one concrete result>.

Execution Log
[request] <original requirement captured>
[model] <model path and result summary>
[check 1] <errors, warnings, suggestions>
[repair 1] <largest pattern fixed>
[contract] <generated guide and assist evidence collected>
[harness] <purpose/comment and audit policy checks>
[build/test/run] <result>
[ready] <artifact or application ready for review>
```

## Constraint Harness Pattern Examples

The report should quote actual code from the completed project. Use these only
to explain the enforced pattern; exact generated methods must come from local
`AGENTS.md` and assist output.

Rust query:

```rust
let merchants = Q::merchants()
    .which_names_contain("TeaQL")
    .purpose("Find merchants for search results")
    .comment("Search merchant names")
    .execute_for_list(&ctx)
    .await?;
```

Rust write:

```rust
merchant
    .audit_as("Update merchant details")
    .save(&ctx)
    .await?;
```

Java query:

```java
var merchants = Q.merchants()
    .filterByName("TeaQL")
    .purpose("Find merchants for search results")
    .comment("Search merchant names")
    .executeForList(userContext);
```

Java write:

```java
merchant
    .auditAs("Update merchant details")
    .save(userContext);
```

## Example Evidence Log

```text
[request] "Build merchant search and approval"
[model] models/main.xml: 8 business objects, 3 constants, root merchant_platform
[check 1] 3 errors, 1 warning, 0 suggestions
[repair 1] removed three deprecated root-name attributes
[check 2] 0 errors, 0 warnings, 0 suggestions
[contract] generated AGENTS.md read; current help and object-specific merchant query/save assist output captured
[harness] queries 4/4 purpose+comment; writes 2/2 audit_as; generated files untouched
[build/test/run] cargo check ✓; cargo test 12/12; console smoke test ✓
[ready] rust-app-console ready for parallel application-effect review
```
