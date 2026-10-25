# Cross-language runtime feature snapshot

This page preserves the runtime evidence recorded for the 2026-08-12 snapshot;
it was reorganized on 2026-10-25, not reverified against new releases.
For the repository entry point, see the [README](../README.md#supported-languages-and-runtime-evidence).

TeaQL natively supports seven language families. While the core philosophy remains identical, the implementation maturity of specific features varies by ecosystem.

**Legend:**
- 🟢 **Supported:** Feature is implemented and working.
- 🟡 **Partial / WIP:** Feature is partially implemented or under active development.
- ⚪ **Not Supported:** Feature is not yet implemented or not applicable for this language tier.

## Verified Runtime Snapshot — 2026-08-12

This snapshot records generated-code and real-runtime evidence, not only the
presence of an adapter or a code template. A green database entry means the
generated API chain compiled and ran against that database with real
persistence. Some results are on validated development branches, so merge and
release availability can lag behind this engineering snapshot.

| Language runtime | Latest verified runtime evidence | Verified databases | Qualification |
| :--- | :--- | :--- | :--- |
| [Java](https://github.com/teaql/teaql-java) | Full database matrix: `9 tests / 0 failures / 0 errors / 0 skipped` | PostgreSQL, MySQL, SQLite, Oracle, DB2, DM8, SAP HANA, SQL Server, DuckDB | Broadest enterprise database coverage; Android remains SQLite-only |
| [Rust](https://github.com/teaql/teaql-rs) | Generated API chain and runtime suite passed; runtime branch coverage reached 95.5% | PostgreSQL, MySQL, SQLite | SQL Server is intentionally out of scope |
| [Go](https://github.com/teaql/teaql-golang) | Runtime suite and generated SQL matrix passed; statement coverage reached 94.9% | PostgreSQL, MySQL, SQLite | Includes generated-query `WithComment` compatibility |
| [Swift](https://github.com/teaql/teaql-swift) | Generated Swift package and runtime suite pass on the current conformance baseline | SQLite | Local-first runtime for iOS/macOS plus a TFP federation client; no federation server |
| [Python](https://github.com/teaql/teaql-python) | `73` runtime tests passed plus generated real-SQL integration | PostgreSQL, MySQL, SQLite | Uses real async SQL providers; no longer counted as JSON/fake persistence |
| [C# / .NET](https://github.com/teaql/teaql-dotnet) | `124` runtime tests passed plus generated database integration | PostgreSQL, MySQL, SQLite, SQL Server | SQL Server support is specific to Java and .NET |
| [TypeScript](https://github.com/teaql/teaql-ts) | `6` runtime tests plus `4 tests / 0 failures / 0 errors / 0 skipped` generated matrix | PostgreSQL, MySQL, SQLite | Canonical Node SQL runtime; the browser/TFP entry installs and loads no database driver |

| Feature Area | Java | Rust | Go | Swift | Python | C# (.NET) | TypeScript |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Core Runtime** | | | | | | | |
| AST Parsing & Query Execution | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| Audited Graph Persistence | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| UserContext & Identity | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| Triple-Intent Policy | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| **Data Providers** | | | | | | | |
| SQLite | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| MySQL | 🟢 | 🟢 | 🟢 | ⚪ | 🟢 | 🟢 | 🟢 |
| PostgreSQL | 🟢 | 🟢 | 🟢 | ⚪ | 🟢 | 🟢 | 🟢 |
| MS SQL Server | 🟢 | ⚪ | ⚪ | ⚪ | ⚪ | 🟢 | ⚪ |
| Oracle | 🟢 | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ |
| DB2 | 🟢 | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ |
| SAP HANA | 🟢 | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ |
| DuckDB | 🟢 | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ |
| DM8 (Dameng) | 🟢 | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ |
| Snowflake | 🟡 | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ |
| **Advanced Integrations** | | | | | | | |
| Federation Protocol (TFP) Server | 🟢 | 🟢 | 🟢 | ⚪ | ⚪ | 🟢 | ⚪ |
| TFP HTTP Provider (Client) | ⚪ | ⚪ | ⚪ | 🟢 | 🟢 | ⚪ | 🟢 |
| Web Framework Integration | 🟢 | 🟢 | 🟢 | ⚪ | 🟢 | 🟢 | ⚪ |
| Redis Cache | 🟢 | 🟢 | 🟢 | ⚪ | 🟢 | 🟢 | ⚪ |
| **Cloud Native (Microservices)** | | | | | | | |
| Nacos Integration | 🟢 | 🟢 | 🟢 | ⚪ | ⚪ | ⚪ | ⚪ |
| Consul Integration | 🟢 | 🟢 | 🟢 | ⚪ | ⚪ | ⚪ | ⚪ |
| Health Actuator & Metrics | 🟢 | 🟢 | 🟢 | ⚪ | ⚪ | ⚪ | ⚪ |
| **Tooling & Code Generation** | | | | | | | |
| Typed DSL Generation | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| Dynamic String Interpreter | 🟢 | ⚪ | ⚪ | ⚪ | ⚪ | ⚪ | 🟢 |

> **💡 Note on Java Database Support:**
> The Java ecosystem has highly adaptable data provider support depending on its execution environment:
> - **Server / Backend (Spring Boot, Quarkus, etc.):** The latest full-chain matrix verifies **PostgreSQL, MySQL, SQLite, Oracle, DB2, DM8, SAP HANA, SQL Server, and DuckDB**. Snowflake is not counted as verified because no official locally runnable Snowflake database service image was found.
> - **Android / Mobile (`teaql-android`):** When running natively on mobile, database support is strictly constrained to **SQLite** to ensure local compatibility, zero-configuration, and memory efficiency without pulling in heavy JDBC drivers.

> **💡 Note on TypeScript Profiles:**
> The green SQL entries apply to the explicit Node.js profiles
> `teaql-ts/sql/postgres`, `teaql-ts/sql/mysql`, and
> `teaql-ts/sql/sqlite`. The default `teaql-ts` browser/TFP entry has no SQL
> import and does not install or load `pg`, `mysql2`, or `better-sqlite3`.
