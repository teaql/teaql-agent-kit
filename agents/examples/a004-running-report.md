# A-004 School Management System — Running Report

**Date**: 2026-06-18 (Asia/Shanghai)
**TeaQL CLI**: cargo-teaql **2.0.7**
**TeaQL Core**: **4.0.5**
**Gen Scope**: `rust-app-console`
**Gen Server**: latest (20260618)

---

## Domain Model

| Concept | Type | Description |
|---------|------|-------------|
| Platform | Business Object | Domain root, manages schools |
| School Type | Constant Object | Primary (1001) / Secondary (1002) |
| School | Business Object | References platform + school_type |

## Generation

```bash
cargo install cargo-teaql --force       # v2.0.7
cargo-teaql install-links               # symlinks
cargo teaql --input model.xml evaluate          # 0 errors, 0 warnings, 15 solids
cargo teaql --input model.xml rust-lib-core     # → /tmp/teaql-build/lib
cargo teaql --input model.xml rust-app-console  # → /tmp/teaql-build/ (complete app console)
```

## Manual Fixes After Generation

| Component | Fix |
|-----------|-----|
| Cargo.toml | Rename `school-service-core-workspace` → `school-service-console` |
| Cargo.toml | Fix dep alias: `school_service` → `school_service_core` |
| src/lib.rs | Fix re-export: `school_service` → `school_service_core` |
| src/main.rs | Fix imports: `school_service::` → `school_service_core::` |

## Test Results (12 steps)

| Test | Description | Result |
|------|-------------|--------|
| Q1 | List all platforms | ✅ 1 platform found |
| Q2 | List school types | ✅ Primary + Secondary |
| Q3 | Create primary school | ✅ id=201 |
| Q4 | Create secondary school | ✅ id=202 |
| Q5 | List all schools | ✅ 202 (200 seed + 2 created) |
| Q6 | Filter by name (name_containing) | ✅ 1 match |
| Q7 | Filter by constant shortcut | ✅ 101 primary (100 seed + 1) |
| Q8 | Count all schools | ✅ 202 |
| Q9 | Load with relations (platform + type) | ✅ Platform & SchoolType loaded |
| E1 | E expression - get_name, get_id | ✅ Some("Sunshine Primary School") |
| E2 | E expression - relation traversal | ✅ platform name, type code, is_secondary |
| E3 | E expression - or_else default | ✅ "Sunshine Primary School" |
| Update | Rename school | ✅ Sunshine → Sunshine International |
| Delete | Soft-delete | ✅ 202 → 201 active |

## Key API Patterns (cargo-teaql v2.0.7 + core 4.0.5)

```rust
// Q: List with filters
Q::schools()
    .with_name_containing("Primary")
    .comment("Filter schools")
    .purpose("Demo name filter")
    .execute_for_list(&ctx)

// Q: Filter by constant
Q::schools()
    .with_school_type_is_primary()
    .execute_for_list(&ctx)

// Q: Relation loading
Q::schools()
    .select_platform()
    .select_school_type()
    .execute_for_one(&ctx)

// Q: Count
Q::schools()
    .execute_for_count(&ctx)

// Q: Minimal (safe for writes, avoids cascade conflicts)
Q::schools_minimal()
    .select_name()
    .execute_for_one(&ctx)

// Q: Create
let mut school = Q::schools().new_entity(&ctx);
school.update_name("Name");
school.update_platform_id(1);
school.update_school_type_to_primary();

// Save (must chain .audit_as() before .save())
school.audit_as("description").save(&ctx)

// E: Traversal
E::school(&school).get_platform().get_name().eval()

// Delete
school.mark_as_delete();
school.audit_as("soft delete").save(&ctx)
```

## Files

- `~/workspace/A-004/model.xml` — KSML semantic model
- `~/workspace/A-004/lib/` — Generated core library (`school-service-core`)
- `~/workspace/A-004/src/main.rs` — Q/E API test app
- `~/workspace/A-004/src/lib.rs` — Workspace re-exports
- `~/workspace/A-004/Cargo.toml` — Workspace manifest
- `~/workspace/A-004/RUNNING-REPORT.md` — This file
