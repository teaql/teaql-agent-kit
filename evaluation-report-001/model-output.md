# Evaluation Report #001 — Model Output & API Analysis

---

## 1. Semantic Model (KSML)

The complete domain is defined in 28 lines of XML:

```xml
<root alias_model_name="school_management"
      chinese_name="学校管理"
      english_name="School Management"
      data_service="sqlite"
      name="school-management-service"
      org="doublechaintech"
      _module_key="root">

  <school_type _name="School Type"
               _module="School Management"
               _module_key="school-management"
               id="id()" name="string()" code="string()"
               _constant="true" _identifier="code"
               platform="platform()">
    <_value id="1001" name="Primary" code="PRIMARY"/>
    <_value id="1002" name="Secondary" code="SECONDARY"/>
  </school_type>

  <platform _name="Platform"
            _module="Platform Management"
            _module_key="platform-management"
            name="Sunrise Education Group"
            create_time="createTime()"
            update_time="updateTime()"/>

  <school _name="School"
          _module="School Management"
          _module_key="school-management"
          name="Green Valley Primary School"
          school_type="school_type()"
          platform="platform()"
          create_time="createTime()"
          update_time="updateTime()"/>

</root>
```

### Model Validation Result

`cargo-teaql eval` returned 0 errors, 0 warnings. 12 solid checks passed:

- KSML-UPLOAD-001: Model upload non-empty
- KSML-UPLOAD-005: Valid entrypoint found
- KSML-XML-002: XML well-formed
- KSML-ROOT-003: Standard root name
- KSML-OBJECT-001: Display metadata exists (3 objects)
- KSML-CONSTANT-001: Constant properties valid
- KSML-CONSTANT-002: Constant linked to root
- KSML-CONSTANT-004: Constant values present (2 values)
- KSML-REFERENCE-003: Reference targets exist (3 references)
- KSML-MODULE-004: Local constant module key matches
- KSML-DOMAIN-ROOT-003: One domain root found

---

## 2. Generated Code Structure

| File | Lines | Purpose |
|------|------:|---------|
| `school/request.rs` | 2,114 | 291 public methods: filters, ordering, pagination, relations, aggregation |
| `school/entity.rs` | 312 | Entity struct with get/update/changed/eval per field |
| `school/expression.rs` | 149 | E expression chain with NotLoaded panic guidance |
| `school/checker.rs` | 127 | Validation hooks |
| `school/behavior.rs` | 6 | Lifecycle behavior hook |
| `school/mod.rs` | 6 | Module re-exports |
| `platform/request.rs` | 2,011 | Platform query builder |
| `platform/entity.rs` | 246 | Platform entity |
| `platform/expression.rs` | 120 | Platform expressions |
| `school_type/request.rs` | 1,911 | SchoolType query builder |
| `school_type/entity.rs` | 245 | SchoolType entity |
| `school_type/expression.rs` | 119 | SchoolType expressions |
| `runtime.rs` | 336 | SQLite connection, schema migration, module registration |
| `sample_data.rs` | 255 | Auto-generated test data seeding |
| `request_support.rs` | 841 | Shared types: QueryOptions, RelationFilter, etc. |
| `q.rs` | 72 | Q entry point and PurposedQuery wrapper |
| `e.rs` | 127 | E expression facade |
| `lib.rs` | 31 | Module declarations and re-exports |
| **Total** | **8,165** | **26 files** |

---

## 3. Verified API Surface

### Q API — Query Building

Entry points (from q.rs):
- `Q::platforms()` / `Q::platforms_minimal()` / `Q::platforms_with_children()`
- `Q::schools()` / `Q::schools_minimal()` / `Q::schools_with_children()`
- `Q::school_types()` / `Q::school_types_minimal()` / `Q::school_types_with_children()`

Execution methods on PurposedQuery (school/request.rs lines 2055-2114):
- `.execute_for_list(&ctx)` → `SmartList<Entity>`
- `.execute_for_first(&ctx)` → `Option<Entity>`
- `.execute_for_one(&ctx)` → `Option<Entity>`
- `.execute_for_count(&ctx)` → `u64`
- `.execute_for_records(&ctx)` → `SmartList<Record>`
- `.execute_for_record(&ctx)` → `Option<Record>`

Execution methods on raw SchoolRequest (line 185):
- `.execute_for_exists(&ctx)` → `bool`

### Relation Loading (school/request.rs)

- `.select_school_type()` (line 1958) — default sub-select, 0 args
- `.select_school_type_with(Q::school_types()...)` (line 1963) — custom sub-query
- `.select_platform()` (line 1989) — default sub-select
- `.select_platform_with(Q::platforms()...)` (line 1994) — custom sub-query
- `.with_school_type_matching(Q::school_types()...)` (line 1698) — EXISTS filter
- `.with_platform_matching(Q::platforms()...)` (line 1823) — EXISTS filter
- `.have_school_type()` (line 1741) — has any children
- `.have_no_school_type()` (line 1746) — has no children

### Constant Shortcuts (school/request.rs)

- `.with_school_type_is_primary()` (line 1928)
- `.with_school_type_is_not_primary()` (line 1934)
- `.with_school_type_is_secondary()` (line 1944)
- `.with_school_type_is_not_secondary()` (line 1950)

### Entity Methods (school/entity.rs)

- `.update_school_type_to_primary()` (line 245)
- `.school_type_is_primary()` (line 249)
- `.update_school_type_to_secondary()` (line 252)
- `.school_type_is_secondary()` (line 256)
- `.school_type()` (line 259) — `Option<&SchoolType>`
- `.platform()` (line 274) — `Option<&Platform>`

### E API — Expression Access (school/expression.rs)

- `E::school(&entity).get_name().eval()` → `Option<String>`
- `E::school(&entity).get_school_type()` → `SchoolTypeExpression`
- `E::school(&entity).get_school_type().get_name().eval()` → `Option<String>`
- `E::school(&entity).get_platform()` → `PlatformExpression`
- `E::school(&entity).get_platform().get_name().eval()` → `Option<String>`

---

## 4. Test Results

18/18 tests passed (100% pass rate).

| # | Test | API | Result |
|---|------|-----|--------|
| 1 | List all platforms | `Q::platforms().execute_for_list()` | PASS |
| 2 | List all school types | `Q::school_types().execute_for_list()` | PASS |
| 3 | Create platform | `new_entity().audit_as().save()` | PASS |
| 4 | Create Primary school | `update_school_type_to_primary()` | PASS |
| 5 | Create Secondary school | `update_school_type_to_secondary()` | PASS |
| 6 | Paginated list | `.page(1, 10).execute_for_list()` | PASS |
| 7 | Filter by name | `.with_name_containing("Primary")` | PASS |
| 8 | Filter by type | `.with_school_type_is_primary()` | PASS |
| 9 | Load with relation | `.select_school_type()` | PASS |
| 10 | Load with children | `.select_school_list()` | PASS |
| 11 | Count | `.execute_for_count()` | PASS |
| 12 | Find by ID with relations | `.with_id_is(1).select_school_type().select_platform()` | PASS |
| 13 | E expression chain | `E::school().get_school_type().get_name()` | PASS |
| 14 | E constant expression | `E::school_type().get_name().get_code()` | PASS |
| 15 | Update entity | `update_name().audit_as().save()` | PASS |
| 16 | Constant check | `school_type_is_primary()` | PASS |
| 17 | Ordering | `.order_by_name_asc()` | PASS |
| 18 | Exists check | `.execute_for_exists()` | PASS |

---

## 5. Verified Doc-Code Inconsistency

**Location:** API_GUIDE.md line 49 vs school/request.rs line 185

**Claim:** `execute_for_exists` is listed as "available on PurposedQuery" in the API_GUIDE.md execution methods table.

**Reality:** `execute_for_exists` is defined on raw `SchoolRequest<R>` (line 185), not on `PurposedQuery<SchoolRequest<R>>` (lines 2055-2114). The other 6 execute methods are correctly on PurposedQuery.

**Impact:** Low — the method works, but developers following the documentation will get a compile error if they chain `.purpose()` before `.execute_for_exists()`.
