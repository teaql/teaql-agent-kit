# Evaluation Report #001 — Scoring

---

## Overall Score

**Composite: 7.9 / 10**

---

## Scoring Dimensions

| Dimension | Score | Weight | Key Evidence |
|-----------|------:|--------|--------------|
| Semantic Modeling | 9.0 | 15% | 28 lines define full domain; eval diagnostics accurate (0 errors, 0 warnings) |
| Type Safety | 8.5 | 15% | 291 methods/entity; Audited<T> enforces audit at compile time |
| Code Generation | 8.0 | 15% | select_*_with exists; 1 doc-code inconsistency (execute_for_exists) |
| API Design | 8.5 | 15% | Q/E facade + constant shortcuts + comment chain |
| Runtime | 7.0 | 10% | Full-featured (auto-migration, graph save, checkers); heavy deps with sqlx |
| Documentation | 7.5 | 10% | API_GUIDE.md mostly accurate; 1 execute_for_exists claim wrong |
| Ecosystem | 7.0 | 10% | ~20 Rust crates + 3 Java + open source forge; low community stars |
| Extensibility | 7.0 | 10% | Behavior/Checker hooks; 5 database providers |

---

## Detailed Scoring

### 1. Semantic Modeling — 9.0

**Strengths:**
- 28 lines of KSML XML define the complete domain graph with 3 entities, 2 constant values, and all relationships
- `cargo-teaql eval` provides structured JSON diagnostics (solids/warnings/suggestions/errors)
- Constant objects (`_constant="true"`) automatically generate enum-like shortcuts across query, mutation, and check dimensions
- Model-as-documentation: the KSML file itself serves as the domain specification
- Module assignment (`_module_key`) groups related objects logically

**Weaknesses:**
- XML format feels dated in 2026
- Validation requires the eval endpoint (but teaql-forge-rs provides local offline deployment)

### 2. Type Safety — 8.5

**Strengths:**
- 291 public methods on SchoolRequest, covering every field with exhaustive filter operators
- `PurposedQuery<T>` wrapper ensures `.purpose()` must precede `execute_*()` calls
- `Audited<T>` wrapper enforces audit comment at compile time (empty comment panics, teaql-core entity.rs line 101)
- E expression chains check relation paths at compile time
- `SmartList<T>` carries pagination metadata without breaking type safety

**Weaknesses:**
- `execute_for_exists` only on raw SchoolRequest, not PurposedQuery — inconsistent with other execute methods
- All IDs are `u64` — no newtype wrappers to prevent ID type confusion

### 3. Code Generation — 8.0

**Strengths:**
- 28 lines XML → 8,165 lines Rust (290:1 expansion)
- `select_school_type_with()` supports custom sub-queries (school/request.rs line 1963)
- Checker framework provides validation hooks (required_text, min/max_string_length)
- sample_data.rs auto-generates test data seeding code
- AGENTS.md, API_GUIDE.md, TOOL_API.md generated alongside code

**Weaknesses:**
- request.rs files are very large (2,114 lines for a 5-field entity)
- One doc-code inconsistency: execute_for_exists documented on PurposedQuery but only on SchoolRequest

### 4. API Design — 8.5

**Strengths:**
- Q/E dual facade is a genuine innovation
- Constant shortcuts cover query (with_school_type_is_primary), mutation (update_school_type_to_primary), and check (school_type_is_primary) dimensions
- `.comment()` and `.purpose()` chain annotations through to SQL trace logs
- Graph save: one `.save()` persists entity + all attached children
- Relation loading with both default (select_school_type) and custom (select_school_type_with) variants

**Weaknesses:**
- execute_for_exists location inconsistency

### 5. Runtime — 7.0

**Strengths:**
- One-line startup: `service_runtime_from_env()` connects and runs schema migration
- Auto schema migration: `ensure_schema()` creates tables and adds columns, never drops
- Graph save with full audit pipeline: audit_as → checkers → diff → SQL → audit log → events
- Environment variable control: TEAQL_AUDIT, TEAQL_SCHEMA, TEAQL_SQL_LOG
- Multiple database providers: SQLite (sqlx/rusqlite), PostgreSQL, MySQL, Meilisearch, Redis

**Weaknesses:**
- 261 total dependencies when using sqlx-sqlite (mainly from sqlx transitive deps)
- Code generator defaults to sqlx-sqlite for SQLite; rusqlite would be lighter
- Debug binary: 15MB

### 6. Documentation — 7.5

**Strengths:**
- API_GUIDE.md covers all query patterns, filter operators, relation methods, constant shortcuts, mutation patterns, expression facade, and aggregation
- TOOL_API.md documents UserContext, SmartList, WebResponse, AuditConfig, Schema Management, Save Pipeline
- AGENTS.md provides AI agent-specific instructions and safety guardrails
- All docs generated alongside code — stays synchronized with API

**Weaknesses:**
- One verified inaccuracy: execute_for_exists listed on PurposedQuery but only on SchoolRequest

### 7. Ecosystem — 7.0

**Strengths:**
- 10 public repositories in the teaql GitHub organization
- ~20 Rust crates covering core, 4 database providers, search, cache, web, and tools
- 3 Java packages (Spring Boot, Maven plugin, Java client)
- teaql-forge-rs: open source local code generation server (Apache-2.0, ~3MB Docker image)
- Multi-database: SQLite, PostgreSQL, MySQL, Meilisearch, Redis

**Weaknesses:**
- Community engagement is low (teaql-agent-kit has 2,774 stars; core repos have 3-8 stars each)
- teaql-rust-utils has 39 commits but 0 published releases

### 8. Extensibility — 7.0

**Strengths:**
- Checker hooks: custom validation logic via SchoolCheckerLogic trait (school/checker.rs)
- Behavior hooks: RepositoryBehavior trait for lifecycle events (school/behavior.rs)
- 5 database providers: sqlx-sqlite, sqlx-postgres, sqlx-mysql, rusqlite, meilisearch
- Cache integration: teaql-cache-integration-redis
- Web integration: teaql-web-integration-axum
- T:: utility facade: teaql-tool with std/extra feature flags

**Weaknesses:**
- Custom providers require implementing the full DataServiceExecutor trait
- No plugin system for extending the code generator itself

---

## Dependency Analysis

### Total: 261 crates (with sqlx-sqlite)

| Category | Count | Source |
|----------|------:|--------|
| TeaQL crates | 7 | core, runtime, sql, macros, data-service, provider, tool-core |
| SQLx + TLS | 16 | sqlx, sqlx-core/macros, rustls, ring, webpki |
| Windows compat | 27 | windows-sys/targets (unused on macOS/Linux) |
| ICU / Unicode | 24 | String normalization |
| Other | 187 | tokio, serde, chrono, rand, regex, etc. |

### Key Insight

Dependency weight is primarily a sqlx problem, not a TeaQL problem. TeaQL itself introduces 7 crates. Using `teaql-provider-rusqlite` instead of `teaql-provider-sqlx-sqlite` would eliminate ~50-60 transitive dependencies.

---

## Evidence Chain

- **Website:** [TeaQL](https://teaql.io)
- **Open-Source Project:** [TeaQL Agent Kit](https://github.com/teaql/teaql-agent-kit)
- **Code Generation Server:** [teaql-forge-rs](https://github.com/teaql/teaql-forge-rs) (Apache-2.0)
- **Raw Data:** [GitHub Raw Data](https://github.com/teaql/teaql-agent-kit/tree/autonomous/reports/evaluation-report-001/raw/)
- **Runtime Artifacts:** build logs, code diffs, SQL traces, test output
