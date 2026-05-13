# TeaQL Overview

TeaQL is a development system built around domain modeling, code generation,
and type-safe query APIs. Its goal is to let teams describe the domain once and
generate readable, strongly typed APIs for querying, relation traversal,
aggregation, graph persistence, and safe value access.

This repository is the entry point for the TeaQL project family. It explains the
overall direction and points readers to the core repositories.

## Main Tracks

TeaQL currently has two major tracks.

1. **Rust track**

   The Rust track splits TeaQL into a native runtime, SQL compiler, derive
   macros, database dialects, code generator support, and CLI tooling. The main
   repositories are `teaql-rs`, `teaql-code-gen`, and `teaql-cli`.

2. **Java / Spring Boot track**

   The Java track contains the earlier TeaQL runtime and service integration
   work. It remains important for existing generated services, Spring Boot
   integration, and the design history behind the TeaQL programming model.

## Core Repositories

| Repository | Purpose | Main technology | Remote |
| --- | --- | --- | --- |
| `teaql-rs` | Rust-native TeaQL runtime, including entity metadata, query AST, SQL compilation, repositories, graph save, checkers, events, and PostgreSQL/SQLite executors. | Rust / Cargo | <https://github.com/teaql/teaql-rs.git> |
| `teaql-code-gen` | Code generation service that turns a compact domain model into Java or Rust libraries. The Rust `rust-lib` target is now a first-class path. | Java / Gradle / Spring Boot / StringTemplate | <https://github.com/teaql/teaql-code-gen.git> |
| `teaql-cli` | Rust command-line tool for code generation, documentation generation, model generation, configuration, and local command aliases. | Rust / Cargo | <https://github.com/teaql/teaql-cli.git> |
| `teaql-spring-boot-starter` | Java / Spring Boot integration entry point for the existing TeaQL service stack. | Java / Gradle / Spring Boot | <https://github.com/teaql/teaql-spring-boot-starter.git> |

## Recommended Reading Order

For the Rust track:

1. `teaql-rs/README.md`: understand the runtime boundary, crate layout, and
   current capability list.
2. `teaql-code-gen/README.md`: understand how a domain model becomes a generated
   Rust service crate with `Q`, `E`, entities, behaviors, and runtime modules.
3. `teaql-cli/README.md`: understand how the generation workflow is exposed from
   the command line.
4. Generate a sample service crate, then return to `teaql-rs` to study
   executors, repositories, graph save, and relation enhancement.

For the Java / Spring Boot track:

1. `teaql-spring-boot-starter`
2. `teaql-code-gen`
3. Existing generated service projects that use the Java stack

## Query Style

TeaQL APIs are intended to read like typed domain language while still compiling
to structured query and repository operations.

```java
Q.families()
```

```java
Q.families().selectKidList()
```

```java
Q.families().hasKids(Q.kids().whosGenderIsBoy())
```

```java
Q.families().countKids("kidGirlsCount", Q.kids().whosGenderIsGirl())
```

The Rust generation path follows the same direction:

```rust
use crm_erp_service::Q;

let platforms = Q::platforms()
    .select_merchant_list_with(
        Q::merchants()
            .select_name()
            .which_names_contain("TeaQL"),
    )
    .execute_for_list(&ctx)
    .await?;
```

## Documentation Tasks

- Keep this repository as the short project-family entry point.
- Keep detailed runtime documentation in `teaql-rs`.
- Keep generator behavior, templates, and generated API documentation in
  `teaql-code-gen`.
- Keep CLI usage and local configuration details in `teaql-cli`.
- Add a Rust end-to-end flow document: model XML -> code generator -> generated
  service crate -> `teaql-rs` runtime -> database.
- Add a migration note that compares the Java and Rust tracks.
