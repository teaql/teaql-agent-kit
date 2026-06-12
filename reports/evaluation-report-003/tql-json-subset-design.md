# Design Document: TeaQL Query Language (TQL) — JSON Subset Specification

**Status:** Design  
**Priority:** High  
**Source:** evaluation-report-003  
**Date:** 2026-06-11

---

## 1. Problem

AI agents and frontend developers need a compact, type-safe way to query TeaQL entities. Current options:

- **Q/E API**: Rust/Java method chains — backend only, not cross-platform
- **GraphQL**: Verbose syntax, incomplete type definitions, over-engineered
- **REST params**: Flat key-value pairs, no nested relations

We need a query language that:
1. Is pure JSON (no new syntax to learn)
2. Supports nested relations
3. Maps directly to Q/E, GraphQL, or REST
4. AI can construct without grep

## 2. Solution: TQL (TeaQL Query Language)

A JSON subset specification for querying TeaQL entities.

### 2.1 Basic Structure

```json
{
  "entity": "book",
  "fields": ["isbn", "title", "author"],
  "include": {
    "category": ["name", "code"],
    "status": ["name", "code"]
  },
  "where": {"title~": "Rust"},
  "sort": ["title"],
  "page": [1, 20],
  "comment": "Load Rust books",
  "purpose": "Book catalog"
}
```

### 2.2 Specification

```yaml
# TQL Query Language Specification v1.0

## Required Fields

entity: string
  # The entity to query (e.g., "book", "loan")

## Optional Fields

fields: string[]
  # Scalar fields to select
  # ["*"] means all scalar fields
  # ["isbn", "title"] means specific fields
  # Default: ["*"]

include: object
  # Relation fields to load
  # Key: relation name
  # Value: field list or nested object
  # Default: {} (no relations loaded)

where: object
  # Filter conditions
  # Key: field name with operator suffix
  # Value: filter value
  # Default: {} (no filters)

sort: string[]
  # Sort fields
  # Prefix "-" for descending
  # ["title"] means ASC
  # ["-total_copies", "title"] means DESC then ASC
  # Default: []

page: [number, number]
  # [page_number, page_size]
  # Page numbers are 1-based
  # Default: [1, 20]

comment: string
  # Business intent description
  # Maps to .comment() in Q/E
  # Required for audit trail

purpose: string
  # Query purpose description
  # Maps to .purpose() in Q/E
  # Required for audit trail
```

### 2.3 Where Syntax

The `where` clause uses a structured condition tree for complex filtering.

**Condition Object:**

```json
{
  "field": "title",
  "op": "~",
  "value": ["Rust"]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `field` | string | Field name to filter |
| `op` | string | Operator (see below) |
| `value` | array | Filter values (always array) |

**Operators:**

| Op | Meaning | SQL Equivalent |
|----|---------|----------------|
| `=` | equals | `field = value[0]` |
| `!=` | not equals | `field != value[0]` |
| `>` | greater than | `field > value[0]` |
| `<` | less than | `field < value[0]` |
| `>=` | greater or equal | `field >= value[0]` |
| `<=` | less or equal | `field <= value[0]` |
| `~` | contains | `field LIKE '%value[0]%'` |
| `^` | starts with | `field LIKE 'value[0]%'` |
| `$` | ends with | `field LIKE '%value[0]'` |
| `in` | in list | `field IN (value)` |
| `not_in` | not in list | `field NOT IN (value)` |
| `null` | is null | `field IS NULL` |
| `not_null` | is not null | `field IS NOT NULL` |
| `between` | between | `field BETWEEN value[0] AND value[1]` |

**Logic Combinators:**

```json
{
  "and": [condition, condition, ...],
  "or": [condition, condition, ...],
  "not": condition
}
```

**Examples:**

Simple AND:
```json
"where": {
  "and": [
    {"field": "title", "op": "~", "value": ["Rust"]},
    {"field": "status", "op": "=", "value": ["AVAILABLE"]},
    {"field": "total_copies", "op": ">=", "value": [5]}
  ]
}
```

Complex OR + AND:
```json
"where": {
  "or": [
    {"and": [
      {"field": "title", "op": "~", "value": ["Rust"]},
      {"field": "status", "op": "=", "value": ["AVAILABLE"]}
    ]},
    {"and": [
      {"field": "title", "op": "~", "value": ["Go"]},
      {"field": "available_copies", "op": ">", "value": [0]}
    ]}
  ]
}
```

NOT + IN:
```json
"where": {
  "and": [
    {"field": "status", "op": "in", "value": ["ACTIVE", "RESERVED"]},
    {"field": "status", "op": "not_in", "value": ["RETIRED"]},
    {"field": "return_date", "op": "null", "value": []}
  ]
}
```

BETWEEN:
```json
"where": {
  "and": [
    {"field": "total_copies", "op": "between", "value": [5, 20]},
    {"field": "loan_date", "op": "between", "value": ["2024-01-01", "2024-12-31"]}
  ]
}
```

### 2.4 Include Syntax

**Simple relation (select specific fields):**

```json
"include": {
  "category": ["name", "code"]
}
```

**Relation with filter:**

```json
"include": {
  "loan_list": {
    "fields": ["loan_number", "borrower_name"],
    "where": {"status": "ACTIVE"}
  }
}
```

**Nested relation (cascading load):**

```json
"include": {
  "category": {
    "fields": ["name", "code"],
    "include": {
      "library_branch": ["name", "address"]
    }
  }
}
```

**Relation with all options:**

```json
"include": {
  "loan_list": {
    "fields": ["loan_number", "borrower_name", "due_date"],
    "where": {"status!": "RETURNED"},
    "sort": ["-due_date"],
    "page": [1, 10],
    "include": {
      "status": ["name", "code"]
    }
  }
}
```

### 2.5 Complete Examples

**Example 1: Simple query**

```json
{
  "entity": "book",
  "fields": ["isbn", "title", "author"],
  "comment": "List all books",
  "purpose": "Book catalog"
}
```

**Example 2: Filtered query with relations**

```json
{
  "entity": "book",
  "fields": ["*"],
  "include": {
    "category": ["name", "code"],
    "status": ["name", "code"]
  },
  "where": {
    "title~": "Rust",
    "status": "AVAILABLE"
  },
  "sort": ["title"],
  "page": [1, 20],
  "comment": "Search available Rust books",
  "purpose": "Book search"
}
```

**Example 3: Complex nested query**

```json
{
  "entity": "book",
  "fields": ["isbn", "title", "total_copies", "available_copies"],
  "include": {
    "category": {
      "fields": ["name", "code"],
      "include": {
        "library_branch": ["name", "address"]
      }
    },
    "status": ["name", "code"],
    "loan_list": {
      "fields": ["loan_number", "borrower_name", "loan_date", "due_date"],
      "where": {"status": "ACTIVE"},
      "include": {
        "status": ["name", "code"]
      }
    }
  },
  "where": {
    "OR": [
      {"title~": "Rust"},
      {"title~": "Go"},
      {"title~": "Python"}
    ],
    "available_copies>": 0
  },
  "sort": ["-available_copies", "title"],
  "page": [1, 10],
  "comment": "Popular programming books with active loans",
  "purpose": "Featured books section"
}
```

## 3. Mapping to Q/E

### 3.1 TQL → Rust Q/E

| TQL | Rust Q/E |
|-----|----------|
| `"entity": "book"` | `Q::books()` |
| `"fields": ["isbn", "title"]` | `.select_isbn().select_title()` |
| `"fields": ["*"]` | `.select_self()` |
| `"include": {"category": [...]}` | `.select_category_with(...)` |
| `"where": {"title~": "Rust"}` | `.with_title_contains("Rust")` |
| `"where": {"status": "ACTIVE"}` | `.with_status_is_active()` |
| `"where": {"total_copies>": 5}` | `.with_total_copies_greater_than(5)` |
| `"sort": ["title"]` | `.order_by_title_asc()` |
| `"sort": ["-title"]` | `.order_by_title_desc()` |
| `"page": [1, 20]` | `.page(1, 20)` |
| `"comment": "..."` | `.comment("...")` |
| `"purpose": "..."` | `.purpose("...")` |

### 3.2 Example Conversion

**Input TQL:**

```json
{
  "entity": "book",
  "fields": ["*"],
  "include": {
    "category": ["name", "code"],
    "status": ["name", "code"]
  },
  "where": {"title~": "Rust"},
  "sort": ["title"],
  "page": [1, 20],
  "comment": "Search Rust books",
  "purpose": "Book search"
}
```

**Output Rust Q/E:**

```rust
Q::books()
    .select_self()
    .select_category_with(Q::book_categories()
        .select_name()
        .select_code()
    )
    .select_status_with(Q::book_statuses()
        .select_name()
        .select_code()
    )
    .with_title_contains("Rust")
    .order_by_title_asc()
    .page(1, 20)
    .comment("Search Rust books")
    .purpose("Book search")
    .execute_for_list(&ctx)
    .await?;
```

## 4. Mapping to GraphQL

### 4.1 TQL → GraphQL

```graphql
query BookSearch {
  books(
    filter: { title_contains: "Rust" }
    sort: { field: "title", order: "ASC" }
    page: { n: 1, size: 20 }
  ) {
    isbn
    title
    author
    category { name code }
    status { name code }
  }
}
```

### 4.2 GraphQL Schema Generation

```graphql
type Book {
  isbn: String
  title: String
  author: String
  publisher: String
  total_copies: Int
  available_copies: Int
  category: BookCategory
  status: BookStatus
  loan_list: [Loan]
}

input BookFilter {
  title: String
  title_contains: String
  author: String
  status: String
  total_copies_gt: Int
  total_copies_lt: Int
  OR: [BookFilter]
}

type Query {
  books(
    filter: BookFilter
    sort: SortInput
    page: PageInput
  ): [Book]
}
```

## 5. Implementation

### 5.1 TQL Parser (Rust)

```rust
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct TqlQuery {
    entity: String,
    #[serde(default = "default_fields")]
    fields: Vec<String>,
    #[serde(default)]
    include: serde_json::Value,
    #[serde(default)]
    where_clause: serde_json::Value,
    #[serde(default)]
    sort: Vec<String>,
    #[serde(default = "default_page")]
    page: [u32; 2],
    comment: String,
    purpose: String,
}

fn parse_tql(query: &TqlQuery) -> TeaQLQuery {
    // Convert TQL to Q/E chain
    match query.entity.as_str() {
        "book" => parse_book_query(query),
        "loan" => parse_loan_query(query),
        _ => panic!("Unknown entity: {}", query.entity),
    }
}
```

### 5.2 TQL HTTP Endpoint

```rust
#[post("/api/query")]
async fn query_endpoint(body: Json<TqlQuery>) -> Json<serde_json::Value> {
    let query = parse_tql(&body);
    let results = query.execute(&ctx).await?;
    Json(json!({"data": results}))
}
```

### 5.3 Frontend Client (TypeScript)

```typescript
import { TqlQuery, TqlResult } from 'teaql-client';

const result: TqlResult = await teaql.query({
  entity: "book",
  fields: ["isbn", "title", "author"],
  include: {
    category: ["name", "code"],
    status: ["name", "code"]
  },
  where: { "title~": "Rust" },
  sort: ["title"],
  page: [1, 20],
  comment: "Search Rust books",
  purpose: "Book search"
});

// result.data contains typed Book[]
```

## 6. Benefits

### 6.1 For AI Agents

- Pure JSON — no new syntax to learn
- Explicit fields — no guessing method names
- Structured — AI constructs valid queries by following schema
- Auditable — comment and purpose fields enforce traceability

### 6.2 For Frontend Developers

- Single query language for all entities
- Type-safe with generated TypeScript types
- No REST endpoint documentation needed
- Same query structure across all entities

### 6.3 For Backend Developers

- TQL maps directly to Q/E — no manual SQL
- Validation built into parser
- Audit trail automatic via comment/purpose
- Performance optimized by TeaQL runtime

## 7. Comparison

| Feature | TQL | GraphQL | REST Params |
|---------|-----|---------|-------------|
| Syntax | JSON | Custom | Key-value |
| Nested relations | ✅ | ✅ | ❌ |
| Type safety | ✅ | ✅ | ❌ |
| Audit trail | ✅ | ❌ | ❌ |
| Learning curve | Low | Medium | Low |
| Tooling | Simple | Complex | Simple |
| AI-friendly | ✅ | ⚠️ | ⚠️ |

## 8. Future Extensions

### 8.1 Aggregation

```json
{
  "entity": "book",
  "aggregate": {
    "total_copies": "sum",
    "available_copies": "avg",
    "_count": "count"
  },
  "group_by": "category",
  "comment": "Book statistics by category",
  "purpose": "Inventory report"
}
```

### 8.2 Mutations

```json
{
  "action": "create",
  "entity": "book",
  "data": {
    "isbn": "978-7-111-42781-2",
    "title": "Rust Programming",
    "author": "Steve Klabnik"
  },
  "comment": "Add new book",
  "purpose": "Expand collection"
}
```

### 8.3 Batch Operations

```json
{
  "action": "update",
  "entity": "book",
  "where": {"status": "DAMAGED"},
  "data": {"status": "RETIRED"},
  "comment": "Retire all damaged books",
  "purpose": "Inventory cleanup"
}
```

## 9. Expected Impact

| Metric | Before | After |
|--------|--------|-------|
| Frontend query construction | Manual REST calls | TQL JSON |
| API documentation | Separate docs needed | TQL schema is docs |
| Type safety | Runtime errors | Compile-time errors |
| AI agent token usage | 50k+ | 5k |
| Cross-platform consistency | Different per platform | Same TQL everywhere |

---

*This design document is based on TeaQL's Q/E API patterns and the need for a cross-platform query language.*
