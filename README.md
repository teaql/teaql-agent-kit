# TeaQL Vibe Kit

TeaQL Vibe Kit is the agent-native entry point for the TeaQL ecosystem. It is
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

## Quick Start

Use this mode when you only want to try TeaQL. It should not modify your
existing project repository.

```bash
git clone https://github.com/teaql/teaql-vibe-kit.git
cd teaql-vibe-kit
```

Then open the folder in Codex, Claude Code, or another coding agent and ask:

```text
I only want to try TeaQL.
Use this repository as the TeaQL vibe coding kit.
Follow AGENTS.md.
Create a runnable demo project outside this repository.
Use the merchant sample model unless I provide another domain.
Model the domain from natural language, generate the TeaQL project, run checks,
fix any issues, and report the generated project path.
```

For a real project, initialize TeaQL support inside your own repository instead
of treating this kit as a disposable demo:

```text
This is a real project.
Use TeaQL Vibe Kit as the external workflow reference.
Initialize minimal TeaQL project configuration in this repository, pin the kit
version, model the first domain from natural language, generate code, run
checks, and document the commands used.
```

The intended split is simple:

| Mode | Where TeaQL Vibe Kit lives | Best for |
| --- | --- | --- |
| Quick try | A separate cloned repository | Demo, evaluation, proof of concept |
| Project mode | Your project keeps lightweight TeaQL config and references a pinned kit version | Real products, team development, long-term iteration |

## Natural-Language Modeling

TeaQL Vibe Kit includes a KSML modeling prompt pack adapted from the
`openclaw-modeling-factory` modeling workflow. Use it when the first task is
"turn this business description into a TeaQL model".

The key files are:

| File | Purpose |
| --- | --- |
| `AGENTS.md` | Agent entry instructions for Codex, Claude Code, and similar tools. |
| `playbooks/model-from-natural-language.md` | Step-by-step workflow for natural-language to KSML modeling. |
| `prompts/modeling/system.md` | Modeling role prompt. |
| `prompts/modeling/task-template.md` | Reusable task frame for a requested domain. |
| `prompts/modeling/ksml-rules.md` | Source-of-truth KSML modeling rules. |
| `prompts/modeling/checklist.md` | Validation checklist before code generation. |

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
`entity.save(userContext)` graph persistence. Exact method names are generated
from the model, so your API will vary with entity names, field names,
relationships, constants, and aggregate fields.

### Q: Simple Query

```java
import com.doublechaintech.crmerpservice.Q;

var merchants = Q.merchants()
    .selectSelf()
    .page(1, 20)
    .executeForList(userContext);
```

The `Q` entry point gives the agent a typed way to start from a business entity
instead of manually assembling SQL or repository calls.

### Q: Filtering

```java
var merchants = Q.merchants()
    .filterByPlatformWith(Q.platforms()
        .filterByName("Shopify")
        .selectSelf())
    .filterByName("TeaQL")
    .executeForList(userContext);
```

Filters are generated from the model, so the agent is guided toward valid fields
and valid value types. For scalar fields, the Java generator emits
`filterBy<Field>(...)` and readable helpers such as `whichNamesContain(...)`
when the model supports them.

### Q: Multi-Level Loading

```java
var merchants = Q.merchants()
    .selectPlatformWith(Q.platforms().selectSelf())
    .selectEmployeeListWith(Q.employees().selectSelf())
    .executeForList(userContext);
```

The agent can request relation loading explicitly without scattering lazy-load
logic through application code.

### Q: Multi-Level Loading With Filtering

```java
// Repeated subqueries can be wrapped in project-level helper methods, for
// example: platformNamed("Shopify") or employeesNamed("Ada").
var merchants = Q.merchants()
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
    .selectSelf()
    .countEmployeesAs("employeeCount")
    .statsFromEmployeesAs("employeeStats",
        Q.employees()
            .selectSelf()
            .count())
    .executeForList(userContext);
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

### DDD Transaction Scenario: Readable Write

```java
new Merchant()
    .updateName("TeaQL Store")
    .updatePlatform(platform)
    .addEmployee(employee)
    .save(userContext);
```

DDD-style application services should read like business operations, but the
generated TeaQL layer currently gives them stable entity APIs, relation methods,
and graph persistence through `entity.save(userContext)`. Business verbs such as
`openStore`, `approveRequest`, or `recordPayment` should live in application
code and use the generated model as the persistence boundary.

## Rust API Examples

The Rust examples use the same merchant sample style, generated as a Rust
service crate. The method shapes are aligned with the current Rust generator:
`Q::<entity_plural>()`, `select_<field>()`, `select_<relation>_with(...)`,
`filter_by_<field>(...)`, readable filters such as `which_names_contain(...)`,
relation filters such as `have_employees_with(...)`, generated `E::<entity>()`
expressions, and `entity.save(&ctx).await` graph persistence. Exact method names
are generated from the model, so your API will vary with entity names, field
names, relationships, constants, and aggregate fields.

### Q: Simple Query

```rust
use crm_erp_service::Q;

let merchants = Q::merchants()
    .select_self()
    .page(1, 20)
    .execute_for_list(&ctx)
    .await?;
```

### Q: Filtering

```rust
let merchants = Q::merchants()
    .which_names_contain("TeaQL")
    .filter_by_platform_with(Q::platforms()
        .which_names_are("Shopify")
        .select_self())
    .execute_for_list(&ctx)
    .await?;
```

### Q: Multi-Level Loading

```rust
let merchants = Q::merchants()
    .select_platform_with(Q::platforms().select_self())
    .select_employee_list_with(Q::employees().select_self())
    .execute_for_list(&ctx)
    .await?;
```

### Q: Multi-Level Loading With Filtering

```rust
// Repeated subqueries can be wrapped in project-level helper functions, for
// example: platform_named("Shopify") or employees_named("Ada").
let merchants = Q::merchants()
    .filter_by_platform_with(platform_named("Shopify"))
    .have_employees_with(employees_named("Ada"))
    .select_employee_list_with(employees_named("Ada"))
    .execute_for_list(&ctx)
    .await?;
```

### Q: Statistics and Aggregation

```rust
let merchants = Q::merchants()
    .select_self()
    .count_employees_as("employee_count")
    .stats_from_employees_as(
        "employee_stats",
        Q::employees()
            .select_self()
            .aggregate_count("count"),
    )
    .execute_for_list(&ctx)
    .await?;
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

### DDD Transaction Scenario: Readable Write

```rust
let mut merchant = Q::merchants()
    .new_entity(&ctx);

merchant
    .update_name("TeaQL Store")
    .update_platform_id(platform.id());

merchant.save(&ctx).await?;
```

In Rust, the same DDD goal applies: application code should expose the business
operation clearly, while generated TeaQL entities, update methods, relation
helpers, and `save(&ctx).await` keep persistence inside the generated runtime
surface.

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
| `teaql-vibe-kit` | Agent-native quick start, workflow guidance, examples, and ecosystem entry point. | Markdown / agent workflows | <https://github.com/teaql/teaql-vibe-kit> |
| `teaql-code-gen` | Code generation service that turns a compact domain model into Java or Rust libraries. | Java / Gradle / Spring Boot / StringTemplate | <https://github.com/teaql/teaql-code-gen> |
| `teaql-rs` | Rust-native TeaQL runtime, SQL compiler, query APIs, repositories, graph save, and executors. | Rust / Cargo | <https://github.com/teaql/teaql-rs> |
| `teaql-cli` | Command-line workflow for code generation, documentation, model generation, config, and local aliases. | Rust / Cargo | <https://github.com/teaql/teaql-cli> |
| `teaql-spring-boot-starter` | Java / Spring Boot runtime integration for the TeaQL service stack. | Java / Gradle / Spring Boot | <https://github.com/teaql/teaql-spring-boot-starter> |

## Suggested Agent Workflow

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

TeaQL Vibe Kit is the lightweight entry repository for the broader TeaQL
ecosystem. The Java and Rust tracks are both usable, and the vibe-coding
workflow will continue to evolve around real examples, agent playbooks, and
repeatable project initialization.
