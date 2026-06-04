# TeaQL Agent Kit

TeaQL Agent Kit is the agent-native entry point for the TeaQL ecosystem. It is
designed for Codex, Claude Code, and similar coding agents that can read a
repository, follow instructions, generate or modify files, run commands, inspect
errors, and iterate until the project works.

TeaQL's core value is:

> Semantic Guardrails for AI Coding.

Instead of asking an AI coding agent to produce arbitrary application code from
free-form requirements, TeaQL gives the agent a semantic model, a typed query
language, generated domain APIs, and runtime conventions. The agent can still
work from natural language, but the generated code is constrained by domain
metadata, entity relationships, typed expressions, query builders, and tested
runtime behavior.

This repository is meant to become the GitHub-star entry point for TeaQL: start
here when you want to try TeaQL with vibe coding, understand what TeaQL gives to
AI-assisted development, and find the Java and Rust implementations.

## Quick Try

Copy one of these prompts into your coding agent. The agent should read
<https://github.com/teaql/teaql-agent-kit> directly and follow its instructions.

### Java Spring Boot

```text
Follow the instructions from https://github.com/teaql/teaql-agent-kit.

Use Java to build a school management system with these domain concepts:

- Platform
- School
- School Type, with values Primary and Secondary

Create the semantic TeaQL model first, review it, then generate the Java TeaQL
code. Generate both the Java library with gen-lib and the runnable Spring Boot
workspace with gen-workspace.

Build only:
- a query API for schools
- a registration API for schools

Use the generated Q/query APIs and generated update methods where applicable.
Do not hand-edit generated TeaQL service code.
```

### Rust Playground

```text
Follow the instructions from https://github.com/teaql/teaql-agent-kit.

Use Rust to build a school management system with these domain concepts:

- Platform
- School
- School Type, with values Primary and Secondary

Create the semantic TeaQL model first, review it, then generate the Rust TeaQL
code.

Build only:
- a query function/API for schools
- a registration function/API for schools

Use the generated Q/query APIs and generated update methods where applicable.
Do not hand-edit generated TeaQL service code.
```

The current workflow has two explicit modes. Additional modes can be added later
without changing the core modeling-first rule:

| Mode | Where TeaQL Agent Kit lives | Best for |
| --- | --- | --- |
| Playground mode | `app-playground` outside the user's project repository | Demo, evaluation, proof of concept |
| Debugging mode | Explicitly requested TeaQL toolchain, generated output, or integration debugging workspace | Debugging failures after the normal generation client path stops |

For larger projects, keep model change ownership separate from application
implementation. A recommended enterprise split is:

| Repository type | Purpose |
| --- | --- |
| Model repository | Owns KSML model changes, review history, compatibility policy, generated documentation, and CI validation. |
| Runtime repository | Generates Java or Rust TeaQL code from a pinned model version and publishes runtime artifacts for one or more core application scenarios. |
| Application repository | Consumes the appropriate runtime artifact and owns product-specific workflow, UI, API, deployment, and customization code. |

This keeps the semantic model trackable as its own asset. It also lets multiple
applications choose the runtime that fits their scenario, such as a Java/Spring
runtime for enterprise business services or a Rust runtime for native service
workloads.

In playground mode, keep the setup deliberately lighter. A user may only want a
single local playground that keeps reviewable artifacts together, for example:

```text
app-playground/
  models/        # model.xml and generation input
  generate-lib/  # generated Java or Rust TeaQL code
  java-workspace/# runnable Java Spring Boot workspace from gen-workspace
  rust-workspace/# editable Rust Tokio workspace from gen-workspace
  src/           # optional ad hoc user functions and query experiments
  tests/         # optional ad hoc scenario experiments
```

The playground should depend on the generated runtime by local path. It should
not copy generated source into the same directory as the user's own experiment
code. Keeping `models/` and `generate-lib/` under `app-playground` makes both
the semantic model and generated library easy for the user to review without
requiring a Maven/Cargo artifact repository before adoption.

For Java playgrounds that should run as a Spring Boot application, generate the
Java library first with the fully qualified `gen-lib` Maven plugin coordinate,
then use the fully qualified `gen-workspace` coordinate. The workspace goal
requests the generator's `java-workspace` output and extracts a runnable
Spring Boot/Maven workspace under `app-playground/java-workspace`, including
project files,
application properties, Java entry classes, a CRUD guide, and a domain-specific
`AGENTS.md` for coding inside that workspace. That workspace `AGENTS.md` is
generated dynamically by the server and may change whenever the workspace is
regenerated. AI coding agents must read it before reading, editing, testing,
running, or explaining code inside the generated workspace, and must read it
again after regeneration. If the expected generated `AGENTS.md` is missing, stop
and report the missing workspace guide instead of guessing the rules.

For Rust playgrounds that should run locally, generate the Rust library first
with `cargo-teaql gen-lib`, then run `cargo-teaql gen-workspace` and extract the
editable workspace under `app-playground/rust-workspace`. That workspace depends
on the generated crate at `../generate-lib/lib`, contains a thin Tokio async
entrypoint, and has its own generated `AGENTS.md`. Read that workspace guide
before coding inside the Rust workspace and again after regeneration. Do not add
a web framework unless the user explicitly asks for one.

Playground mode may automatically call `ensure_schema()` during runtime setup so
the first local run can create demo tables, seed sample data, and show a real
query result. That is a convenience for evaluation only.

Outside playground mode, schema creation and migration are explicit deployment
decisions. Do not hide schema mutation inside normal runtime initialization. Run
schema bootstrap, migration, validation, or DBA review through the project's
CI/CD, admin command, migration tool, or deployment workflow.

## Toolchain Workflow

TeaQL Agent Kit expects code generation to happen after a valid KSML model
exists. Users should install the TeaQL client tools from package registries. For
Java, resolve TeaQL Maven plugin version `0.1.10` or newer from the TeaQL Nexus
releases repository: `https://nexus.teaql.io/repository/maven-releases/`. Do not
rely on Maven Central freshness, and do not use Maven plugin prefix resolution
such as `mvn teaql:gen-lib`; Maven may search the wrong repositories. Invoke the
plugin with fully qualified coordinates, and ensure the user Maven settings or
project POM exposes the TeaQL Nexus releases repository as a repository and
plugin repository. For Rust, install CLI package `cargo-teaql` version `0.1.9`
or newer from crates.io, then run `cargo-teaql install-links`. Do not ask users
to download or build the client tool source code just to generate a service. If
a generation client, TeaQL Maven plugin goal, or TeaQL plugin/tool invocation
cannot be installed, resolved, invoked, or executed, stop immediately and report
the blocker instead of trying source builds or alternate generation paths.

| Target | User-installed client | Main command |
| --- | --- | --- |
| KSML evaluation, Rust/client path | `cargo install cargo-teaql` from crates.io, then `cargo-teaql install-links` | `cargo-teaql eval <model-file-or-directory>` |
| KSML evaluation, Java/Maven path | TeaQL Maven plugin with `eval` goal from `https://nexus.teaql.io/repository/maven-releases/` | `mvn io.teaql:teaql-maven-plugin:0.1.10:eval -Dteaql.input=<model-file-or-directory>` |
| Rust | `cargo install cargo-teaql` from crates.io, `cargo-teaql >= 0.1.9`, then `cargo-teaql install-links` | `cargo-teaql gen-lib <model.xml>` |
| Rust runnable workspace | `cargo install cargo-teaql` from crates.io, `cargo-teaql >= 0.1.9`, then `cargo-teaql install-links` | `cargo-teaql gen-workspace <model.xml> --workspace-dir <workspace-dir>` |
| Java | TeaQL Maven plugin `>= 0.1.10` from `https://nexus.teaql.io/repository/maven-releases/` | `mvn io.teaql:teaql-maven-plugin:0.1.10:gen-lib -Dteaql.input=<model.xml> -Dteaql.output=<output-dir>` |
| Java runnable workspace | TeaQL Maven plugin `>= 0.1.10` from `https://nexus.teaql.io/repository/maven-releases/` | `mvn io.teaql:teaql-maven-plugin:0.1.10:gen-workspace -Dteaql.input=<model.xml> -Dteaql.workspaceDir=<workspace-dir>` |

The Java runnable workspace path requires a Maven plugin/client version that can
run `gen-workspace`; use version `0.1.10` or newer from the TeaQL Nexus
releases repository. If the plugin cannot be resolved from that repository, if
the installed client does not provide that goal, or if any TeaQL plugin/tool
call fails, report that as the blocker and stop instead of hand-building the
workspace.

The Rust runnable workspace path follows the same model-first sequence:
generate the Rust library with `cargo-teaql gen-lib`, then generate the editable
workspace with `cargo-teaql gen-workspace`. In playground mode, write the model
to `app-playground/models`, generated runtime code to
`app-playground/generate-lib`, and the editable Rust workspace to
`app-playground/rust-workspace`. The workspace depends on the generated crate at
`../generate-lib/lib` by local path and starts as a Tokio async application
skeleton without a web framework.

The TeaQL client is only the request tool. Generated Java or Rust service code
still comes from the TeaQL service endpoint, for example
`https://api.teaql.io/latest/generate`.

Local source checkouts such as `~/githome/teaql-cargo-cli` and
`~/githome/teaql-maven-plugin` are for TeaQL toolchain development and
debugging, not for normal user installation.

Use `playbooks/generate-with-toolchains.md` when an agent needs to generate
Java, Rust, or both tracks from the same model. For Java projects, read
`playbooks/java-generation-known-pitfalls.md` before running Maven. The
high-level loop is:

1. Model the domain as KSML XML.
2. Validate the model with `prompts/modeling/checklist.md`.
3. Run server-side KSML evaluation with the client toolchain when the `eval`
   target is available. Fix evaluation `errors`; carry `warnings` and
   `suggestions` into review.
4. Run the model review gate and confirm the model before code generation.
5. Generate Java and/or Rust code with the selected toolchain.
6. Run target-project compile checks and tests.
7. Decide schema bootstrap or migration explicitly for project/production mode.
8. Fix model errors in `model.xml`, then regenerate.

Example agent request for both tracks:

```text
Use TeaQL Agent Kit.
Follow AGENTS.md.
Model the domain first, validate the KSML model, then generate both Java and
Rust TeaQL outputs.
Before generation, summarize the model for review and wait for confirmation.
Use the TeaQL client tools installed from package registries, including
`cargo-teaql` version `0.1.9` or newer from crates.io followed by
`cargo-teaql install-links`, to evaluate the KSML model and request TeaQL
service code generation.
Keep generated artifacts in the target project, run checks, and report the
commands and output paths.
```

## Natural-Language Modeling

TeaQL Agent Kit includes a KSML modeling prompt pack adapted from the
`openclaw-modeling-factory` modeling workflow. Use it when the first task is
"turn this business description into a TeaQL model".

The key files are:

| File | Purpose |
| --- | --- |
| `AGENTS.md` | Agent entry instructions for Codex, Claude Code, and similar tools. |
| `playbooks/model-from-natural-language.md` | Step-by-step workflow for natural-language to KSML modeling. |
| `playbooks/model-review-gate.md` | Required model confirmation gate before TeaQL code generation. |
| `prompts/modeling/system.md` | Modeling role prompt. |
| `prompts/modeling/task-template.md` | Reusable task frame for a requested domain. |
| `prompts/modeling/ksml-rules.md` | Source-of-truth KSML modeling rules. |
| `prompts/modeling/checklist.md` | Validation checklist before code generation. |
| `playbooks/generate-with-toolchains.md` | Java/Rust generation workflow after the model is valid. |
| `playbooks/enterprise-repository-topology.md` | Large-project repository split and CI/CD workflow guidance. |

Example agent request:

```text
Model a warehouse inventory management system.
Follow AGENTS.md and playbooks/model-from-natural-language.md.
Use prompts/modeling/ksml-rules.md.
Create a valid KSML model.xml first, then explain any assumptions.
```

## What TeaQL Is

TeaQL is a semantic development system built around domain modeling, generated
APIs, and runtime support for business applications.

You describe the domain once: entities, fields, relationships, lifecycle states,
queries, expressions, and transaction behavior. TeaQL then generates typed APIs
that make common application work readable and constrained:

- Query simple entity lists.
- Apply filters without hand-written SQL.
- Load multi-level object graphs.
- Load object graphs with nested filters.
- Compute counts, sums, and grouped aggregates.
- Use safe expressions instead of fragile string-based field access.
- Express DDD-style transaction scenarios in readable application code.

TeaQL is available in both Java and Rust:

- Java is the mature Spring Boot oriented runtime and service integration track.
- Rust is the native runtime track for generated Rust services, typed query APIs,
  SQL compilation, executors, graph persistence, and runtime customization.

The examples below follow the current generator's merchant sample model:
`Platform`, `Merchant`, and `Employee`. A customer can replace that model with
their own natural-language description, such as "inventory management with
warehouses and stock movements", "approval workflow for purchase requests", or
"membership system with subscriptions and invoices". The coding agent should
first turn that natural language into a TeaQL domain model, then generate Java
or Rust code from the model.

## Why Semantic Guardrails Matter

General vibe coding works well until the project needs consistency. Business
applications need stable names, relationships, authorization boundaries,
transaction rules, query behavior, and repeatable generated code. Without a
semantic layer, the agent has to rediscover the same rules every time it edits
the project.

TeaQL gives the agent a stronger operating surface:

- **Domain model as source of truth**: entities and relationships are explicit.
- **Generated APIs**: the agent uses typed methods instead of inventing access
  patterns.
- **Query DSL**: filtering, relation loading, and aggregation follow the same
  shape across the project.
- **Runtime context**: infrastructure concerns are centralized and customizable.
- **Repeatable checks**: code generation, compilation, and tests can be rerun by
  the agent after each change.

That is the practical meaning of Semantic Guardrails for AI Coding: natural
language can drive the work, but TeaQL keeps the generated system inside a
coherent domain and runtime model.

## Java API Examples

The Java examples use the generator's merchant sample style. They are
illustrative, but the method shapes are aligned with the current Java generator:
`Q.<entityPlural>()`, `select<Field>()`, `select<Relation>With(...)`,
`filterBy<Field>(...)`, `filterBy<Relation>With(...)`, relation counts such as
`countEmployeesAs(...)`, generated `E.<entity>(value)` expressions, and
`entity.auditAs(...).save(userContext)` graph persistence. Exact method names are generated
from the model, so your API will vary with entity names, field names,
relationships, constants, and aggregate fields.

### Ensure Schema

```java
import io.teaql.data.TQLContext;
import io.teaql.data.UserContext;
import io.teaql.data.meta.EntityMetaFactory;
import io.teaql.data.sql.SQLRepositorySchemaHelper;

@Controller
public class EnsureModelController {

    @Autowired
    private EntityMetaFactory factory;

    @GetMapping("/ensureSchema")
    @ResponseBody
    public Object ensureSchema(@TQLContext UserContext context) {
        new SQLRepositorySchemaHelper().ensureSchema(context, factory);
        return Map.of("ok", true);
    }
}
```

`ensureSchema(context, factory)` checks the generated TeaQL entity metadata
against the configured SQL repository and prepares the physical database schema.
It is typically used during setup, deployment, or controlled admin operations to
create or adjust tables before normal `Q` queries and graph saves run.

### Q: Simple Query

```java
import com.doublechaintech.crmerpservice.Q;

var merchants = Q.merchants()
    .comment("Load merchants for homepage")
    .purpose("List active merchants")
    .selectSelf()
    .page(1, 20)
    .executeForList(userContext);
```

The `Q` entry point gives the agent a typed way to start from a business entity
instead of manually assembling SQL or repository calls.

### Q: Filtering

```java
var merchants = Q.merchants()
    .comment("Search merchants by name and platform")
    .purpose("Filter merchants")
    .filterByPlatformWith(Q.platforms()
        .comment("Load platform")
        .purpose("Filtering")
        .filterByName("Shopify")
        .selectSelf())
    .filterByName("TeaQL")
    .executeForList(userContext);
```

Filters are generated from the model, so the agent is guided toward valid fields
and valid value types. For scalar fields, the Java generator emits
`filterBy<Field>(...)` and readable helpers such as `whichNamesContain(...)`
when the model supports them.

### Q: Dynamic JSON Query

When an application needs runtime-defined query criteria, such as fields,
operators, sorting, or pagination chosen by a user or external request, use the
Java / Spring Boot `findByJson` / `findWithJsonExpr` dynamic query surface. The
official guide is
<https://teaql.io/docs/working-with-teaql-and-springboot/find-by-json-dynamic-query>.
Do not build that dynamic surface by calling lower-level `addFilter` primitives
directly. Keep tenant scope, permission boundaries, page-size caps, and default
ordering in typed TeaQL request code around the dynamic JSON query.

### Q: Multi-Level Loading

```java
var merchants = Q.merchants()
    .comment("Load merchants with relations")
    .purpose("Export merchant data")
    .selectPlatformWith(Q.platforms()
        .comment("Load platform details")
        .purpose("Relations")
        .selectSelf())
    .selectEmployeeListWith(Q.employees()
        .comment("Load employee details")
        .purpose("Relations")
        .selectSelf())
    .executeForList(userContext);
```

The agent can request relation loading explicitly without scattering lazy-load
logic through application code.

### Q: Multi-Level Loading With Filtering

```java
// Repeated subqueries can be wrapped in project-level helper methods, for
// example: platformNamed("Shopify") or employeesNamed("Ada").
var merchants = Q.merchants()
    .comment("Load Shopify merchants with specific employees")
    .purpose("Filter merchants by related entities")
    .filterByPlatformWith(platformNamed("Shopify"))
    .haveEmployeesWith(employeesNamed("Ada"))
    .selectEmployeeListWith(employeesNamed("Ada"))
    .executeForList(userContext);
```

Nested filters let the generated API express "load the graph I need" without
turning the application layer into a string-query construction site.

### Q: Statistics and Aggregation

```java
var merchants = Q.merchants()
    .comment("Load merchants with stats")
    .purpose("Reporting")
    .selectSelf()
    // Adds a dynamic property named "employeeCount" to each returned merchant.
    .countEmployeesAs("employeeCount")
    // Adds a dynamic aggregate/refinement named "employeeStats"; use this for
    // richer per-merchant child statistics when the child request has
    // projections, counts, sums, groups, or other aggregate output.
    .statsFromEmployeesAs("employeeStats",
        Q.employees()
            .comment("Load employee profiles")
            .purpose("Build contact list")
            .selectSelf()
            .count())
    .executeForList(userContext);

for (Merchant merchant : merchants) {
    // Dynamic aggregate values are not generated fields. Read them by the alias
    // passed to countEmployeesAs/statsFromEmployeesAs.
    Long employeeCount = merchant.getDynamicProperty("employeeCount", 0L);
    Object employeeStats = merchant.getDynamicProperty("employeeStats");
}
```

Aggregates are attached to the domain query, keeping reporting logic close to
the entity relationships it depends on. The Java generator also emits scalar
aggregation helpers for numeric fields, such as `sumAmountAs(...)`, and relation
aggregation helpers such as `countEmployeesWith(...)` when those fields and
relations exist in the model.

### E: Safe Expressions

```java
import com.doublechaintech.crmerpservice.E;

var platformName = E.merchant(merchant)
    .getPlatform()
    .getName()
    .eval();
```

`E` expressions are meant to give agents and developers a safer alternative to
manual nested null checks and unchecked casts when reading through generated
entity chains.

### DDD Transaction Scenario: Typed Behavior

```java
class OperableMerchant extends Merchant {
    OperableMerchant openStore() {
        updateStatus(MerchantStatus.ACTIVE);
        return this;
    }
}

var merchant = Q.merchants()
    .comment("Load merchant to open store")
    .purpose("Open store")
    .returnType(OperableMerchant.class)
    .filterByName("TeaQL Store")
    .executeForOne(userContext)
    .orElseThrow();

merchant.openStore()
    .auditAs("Open store for the first time").save(userContext);
```

This is where TeaQL becomes especially useful for DDD. A project can define a
domain-specific subclass or behavior type, add readable business methods such as
`openStore`, `approveRequest`, or `recordPayment`, and ask the `Q` query to
return that type. After the query, application code calls the business method
directly instead of mapping raw records into a separate service object. Generated
entity APIs, relation methods, and graph persistence through
`entity.auditAs(...).save(userContext)` remain available at the application/service boundary.
As a best practice, keep domain behavior lightweight and easy to unit test:
mutate or validate domain state inside the method, and perform persistence
outside the domain method.

### Chainable Updates

Generated update methods are also part of the typed TeaQL surface. When a
business action changes entity state, prefer chainable `update<Field>(...)`
methods and persist through the normal save path instead of assigning fields
directly or writing update SQL:

```java
merchant
    .updateStatus(MerchantStatus.ACTIVE)
    .updateDisplayName("TeaQL Store")
    .auditAs("Update store display name").save(userContext);
```

Use the chain to express one domain transition clearly. If the generated update
surface is missing or awkward, fix the semantic model and regenerate rather than
patching generated service code.

## Rust API Examples

The Rust examples use the same merchant sample style, generated as a Rust
service crate. The method shapes are aligned with the current Rust generator:
`Q::<entity_plural>()`, `select_<field>()`, `select_<relation>_with(...)`,
`filter_by_<field>(...)`, readable filters such as `which_names_contain(...)`,
relation filters such as `have_employees_with(...)`, generated `E::<entity>()`
expressions, and `entity.audit_as(...).save(&ctx).await` graph persistence. Exact method names
are generated from the model, so your API will vary with entity names, field
names, relationships, constants, and aggregate fields.

### Ensure Schema

```rust
use teaql_provider_sqlx_postgres::{PgMutationExecutor, PostgresProviderExt};
use teaql_runtime::UserContext;

let mut ctx = UserContext::new()
    .with_module(crm_erp_service::module())
    .with_repository_registry(crm_erp_service::repository_registry());

ctx.use_postgres_provider(PgMutationExecutor::new(pg_pool));

// ensure_schema checks the generated TeaQL entity metadata against the
// registered database provider and prepares the physical schema. Provider
// implementations can create missing tables, add missing columns, and install
// provider-specific bootstrap objects needed by the runtime.
ctx.ensure_schema().await?;
```

After schema bootstrap, the same context can be used for generated `Q` queries,
graph save, safe expressions, and DDD behavior methods.

### Q: Simple Query

```rust
use crm_erp_service::Q;

let merchants = Q::merchants()
    .comment("Load merchants for homepage")
    .purpose("List active merchants")
    .select_self()
    .page(1, 20)
    .execute_for_list(&ctx)
    .await?;
```

### Q: Filtering

```rust
let merchants = Q::merchants()
    .comment("Search merchants by name and platform")
    .purpose("Filter merchants")
    .which_names_contain("TeaQL")
    .filter_by_platform_with(Q::platforms()
        .comment("Load platform")
        .purpose("Filtering")
        .which_names_are("Shopify")
        .select_self())
    .execute_for_list(&ctx)
    .await?;
```

### Q: Dynamic JSON Query

When an application needs runtime-defined query criteria, such as fields,
operators, sorting, or pagination chosen by a user or external request, use the
Rust `find_with_json_expr` API. It corresponds to the JSON dynamic query
capability documented in the Java / Spring Boot guide:
<https://teaql.io/docs/working-with-teaql-and-springboot/find-by-json-dynamic-query>.
Do not build that dynamic surface by calling lower-level `add_filter` primitives
directly. Keep tenant scope, permission boundaries, page-size caps, and default
ordering in typed TeaQL request code around the dynamic JSON query.

### Q: Multi-Level Loading

```rust
let merchants = Q::merchants()
    .comment("Load merchants with relations")
    .purpose("Export merchant data")
    .select_platform_with(Q::platforms()
        .comment("Load platform details")
        .purpose("Relations")
        .select_self())
    .select_employee_list_with(Q::employees()
        .comment("Load employee details")
        .purpose("Relations")
        .select_self())
    .execute_for_list(&ctx)
    .await?;
```

### Q: Multi-Level Loading With Filtering

```rust
// Repeated subqueries can be wrapped in project-level helper functions, for
// example: platform_named("Shopify") or employees_named("Ada").
let merchants = Q::merchants()
    .comment("Load Shopify merchants with specific employees")
    .purpose("Filter merchants by related entities")
    .filter_by_platform_with(platform_named("Shopify"))
    .have_employees_with(employees_named("Ada"))
    .select_employee_list_with(employees_named("Ada"))
    .execute_for_list(&ctx)
    .await?;
```

### Q: Statistics and Aggregation

```rust
use teaql_core::BaseEntity;

let merchants = Q::merchants()
    .comment("Load merchants with stats")
    .purpose("Reporting")
    .select_self()
    // Adds a dynamic property named "employee_count" to each returned merchant.
    .count_employees_as("employee_count")
    // Adds a dynamic aggregate/refinement named "employee_stats"; use this for
    // richer per-merchant child statistics when the child request has
    // projections, counts, sums, groups, or other aggregate output.
    .stats_from_employees_as(
        "employee_stats",
        Q::employees()
            .comment("Load employee profiles")
            .purpose("Build contact list")
            .which_roles_are("admin")
            .select_self()
            .aggregate_count("count"),
    )
    .execute_for_list(&ctx)
    .await?;

for merchant in merchants.iter() {
    // Dynamic aggregate values are not generated fields. Read them by the alias
    // passed to count_employees_as/stats_from_employees_as.
    let employee_count = merchant.dynamic_u64("employee_count").unwrap_or(0);
    let employee_stats = merchant.dynamic("employee_stats");
}
```

For scalar aggregation, the Rust generator emits helpers such as
`count_name_as(...)`, `sum_amount_as(...)`, `avg_amount_as(...)`, and
`group_by_name()` when the fields exist. For one-to-many relation aggregation,
it emits helpers such as `count_employees_as(...)`,
`stats_from_employees_as(...)`, and numeric relation helpers such as
`sum_amount_of_employees_as(...)` when the child relation has that numeric field.

### E: Safe Expressions

```rust
use crm_erp_service::E;

let platform_name = E::merchant(merchant)
    .get_platform()
    .get_name()
    .eval();
```

`E` gives the generated Rust code a structured expression surface that agents can
compose without falling back to nested `unwrap()` chains.

### DDD Transaction Scenario: Typed Behavior

```rust
struct OperableMerchant {
    inner: Merchant,
}

impl OperableMerchant {
    fn open_store(&mut self) -> &mut Self {
        self.inner.update_status_id(MerchantStatus::active_id());
        self
    }
}

let mut merchant = Q::merchants()
    .comment("Load merchant to open store")
    .purpose("Open store")
    .return_type::<OperableMerchant>()
    .which_names_are("TeaQL Store")
    .execute_for_one(&ctx)
    .await?
    .expect("merchant should exist");

merchant.open_store();
merchant.inner.audit_as("Open store for the first time").save(&ctx).await?;
```

Rust follows the same DDD shape. A project can define a runtime-compatible
domain type with extra behavior, set it as the query return type, and call the
method immediately after loading. Generated TeaQL entities, update methods,
relation helpers, and `audit_as(...).save(&ctx).await` still provide the persistence surface
at the application/service boundary. Keep behavior methods small and testable:
they should express domain state transitions, while persistence remains outside
the method.

Generated Rust update methods should be used the same way for state changes:
chain the generated update calls when the runtime exposes chainable setters,
then persist through `audit_as(...).save(&ctx).await`. Avoid direct generated-field mutation
and raw SQL for ordinary business updates.

## Runtime Context Customization

TeaQL does not assume that all projects share the same infrastructure. Both Java
and Rust tracks are designed around a runtime context that can be customized for
real applications.

### Java Runtime Context

In Java / Spring Boot projects, the runtime context is typically integrated with
the application's service layer and infrastructure beans.

Common customization points include:

- Current user, tenant, organization, locale, and request metadata.
- Permission checks and data visibility rules.
- Transaction boundaries.
- Event publishing and domain hooks.
- Repository and database integration.
- Audit fields, soft delete rules, and default filters.
- Application-specific services available to generated behaviors.

That allows a generated TeaQL service to fit into an existing Java application
instead of forcing the application to adopt a closed runtime.

### Rust Runtime Context

In Rust projects, the runtime context is the explicit execution environment
passed through generated query and behavior APIs.

Common customization points include:

- Database executors and connection pools.
- Tenant, user, locale, trace id, and request metadata.
- Permission and policy evaluators.
- SQL dialect behavior and repository wiring.
- Event sinks, validation hooks, and lifecycle checkers.
- Feature-specific services attached to the context.

The explicit `&ctx` style is useful for AI coding because the agent can see where
runtime capabilities come from and can pass the same context through generated
queries, graph loading, persistence, and transaction behavior.

## Repository Map

TeaQL is a family of repositories. This repository is the public starting point
for agent-based TeaQL adoption.

| Repository | Purpose | Main technology | Link |
| --- | --- | --- | --- |
| `teaql-agent-kit` | Agent-native quick start, workflow guidance, examples, and ecosystem entry point. | Markdown / agent workflows | <https://github.com/teaql/teaql-agent-kit> |
| `teaql-code-gen` | Code generation service that turns a compact domain model into Java or Rust libraries. | Java / Gradle / Spring Boot / StringTemplate | <https://github.com/teaql/teaql-code-gen> |
| `teaql-rs` | Rust-native TeaQL runtime, SQL compiler, query APIs, repositories, graph save, and executors. | Rust / Cargo | <https://github.com/teaql/teaql-rs> |
| `teaql-cli` | Command-line workflow for code generation, documentation, model generation, config, and local aliases. | Rust / Cargo | <https://github.com/teaql/teaql-cli> |
| `teaql-maven-plugin` | Maven workflow for TeaQL code generation, documentation, frontend model output, and effective config display. | Java / Maven | <https://github.com/teaql/teaql-maven-plugin> |
| `teaql-spring-boot-starter` | Java / Spring Boot runtime integration for the TeaQL service stack. | Java / Gradle / Spring Boot | <https://github.com/teaql/teaql-spring-boot-starter> |

## Suggested Agent Workflow

Initial tests suggest that capable AI coding agents generally perform better
when paired with stronger language models.

When using Codex or Claude Code, the workflow should be explicit and repeatable:

1. Read the user's natural-language business description.
2. Convert it into a TeaQL KSML domain model using `prompts/modeling/`.
3. Review entity boundaries, relationships, lifecycle states, permissions, and
   query needs.
4. Generate Java or Rust TeaQL code.
5. Run code generation, compile checks, and tests.
6. Inspect failures and repair the model or generated integration code.
7. Produce a short delivery report with commands, generated paths, and remaining
   assumptions.

The important rule is that the agent should not jump directly from a vague
requirement to arbitrary application code. It should first create the semantic
model, then let TeaQL generate and constrain the implementation surface.

## Status

TeaQL Agent Kit is the lightweight entry repository for the broader TeaQL
ecosystem. The Java and Rust tracks are both usable, and the agent-coding
workflow will continue to evolve around real examples, agent playbooks, and
repeatable project initialization.
