# B-001 School Management — Running Report

**Date**: 2026-06-18 (Asia/Shanghai)
**Tools**: cargo-teaql 2.0.7 / teaql-core 4.0.5 / rusqlite 0.32.1
**Gen Scope**: `rust-app-console`
**Gen Server**: latest

---

## Domain Model

```
Platform (root) ──< School
                  └──< School Type (constant: Primary / Secondary)
```

| Entity | Type | Module |
|--------|------|--------|
| Platform | Business Object | Platform Management |
| School Type | Constant Object | School Management |
| School | Business Object | School Management |

## Process (following QUICK-START.md)

| Step | Action | Result |
|------|--------|--------|
| 1 | Read KSML-RULES.md + RULES.md | Complete |
| 2a | Decision Tree: platform is root (single-tenant) | platform as root, no merchant |
| 2b | TEMPLATES.md: model.xml | Written |
| 3 | `cargo teaql --input model.xml evaluate` | 0 errors, 0 warnings, 15 solids |
| 4a | `cargo teaql --input model.xml rust-lib-core` | ✅ |
| 4b | `cargo teaql --input model.xml rust-app-console` | ✅ |
| 4c | Copy generated files + rename app package | ✅ |
| 5 | `cargo check` | ✅ |
| 5 | `cargo run` | ✅ All 12 tests pass |

## Fixes After Generation

| Item | Change |
|------|--------|
| Cargo.toml package | `school-service-core-workspace` → `school-service-console` |

Note: This generation fixed the dep alias — `Cargo.toml` now uses `school_service_core = { package = "school-service-core", path = "lib" }`, and `src/lib.rs`/`src/main.rs` use `school_service_core::` directly. No import fix needed.

## Test Results

| # | Test | Result |
|---|------|--------|
| Q1 | List platforms | ✅ 1 platform |
| Q2 | List school types | ✅ Primary + Secondary |
| Q3 | Create primary school | ✅ id=201 |
| Q4 | Create secondary school | ✅ id=202 |
| Q5 | List schools | ✅ 202 total |
| Q6 | Filter by name (containing) | ✅ 1 match |
| Q7 | Filter by constant shortcut | ✅ 101 primary |
| Q8 | Count | ✅ 202 |
| Q9 | Load with relations | ✅ platform + school_type |
| E1 | E: get scalar fields | ✅ Some("Sunshine...") |
| E2 | E: relation traversal | ✅ platform name, type code |
| E3 | E: or_else default | ✅ "Sunshine Primary School" |
| — | Update: rename | ✅ 201 → International |
| — | Delete: soft-delete | ✅ 202 → 201 active |

## Key Patterns

```rust
// Q: filter by constant shortcut
Q::schools()
    .with_school_type_is_primary()
    .comment("Filter to primary schools")
    .purpose("Demo constant shortcut filter")
    .execute_for_list(&ctx)

// Q: relation loading
Q::schools()
    .select_platform()
    .select_school_type()
    .with_name_is("...")
    .comment("...")
    .purpose("...")
    .execute_for_one(&ctx)

// Q: minimal for writes (avoids cascade)
Q::schools_minimal()
    .select_name()
    .execute_for_one(&ctx)

// E: chain traversal
E::school(&school).get_platform().get_name().eval()

// Save (must import AuditedSave trait)
school.audit_as("description").save(&ctx).await?

// Soft delete
school.mark_as_delete();
school.audit_as("soft delete").save(&ctx).await?;
```

## Files

| Path | Purpose |
|------|---------|
| `B-001/model.xml` | KSML semantic model |
| `B-001/lib/` | Generated core library |
| `B-001/src/main.rs` | Test app (Q + E APIs) |
| `B-001/src/lib.rs` | Workspace re-exports |
| `B-001/Cargo.toml` | Workspace manifest |
| `B-001/RUNNING-REPORT.md` | This file |
