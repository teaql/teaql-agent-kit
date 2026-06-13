# Design Document: `teaql assistant` CLI

**Status:** Design  
**Priority:** High  
**Source:** evaluation-report-003  
**Date:** 2026-06-11

---

## 1. Problem

AI agents building TeaQL projects waste tokens grepping generated source code to find:
- Q entry point names (e.g., `book_categories` vs `book_categorys`)
- Filter method names (e.g., `with_title_is` vs `with_name_contains`)
- Relation select methods (e.g., `select_category_with`)
- Field names and types
- Constant values

This costs 50-100k tokens per project and causes compilation errors.

## 2. Solution: `teaql assistant` CLI

A dedicated CLI tool for AI agents to query model information without grepping.

### 2.1 Command Structure

```
teaql assistant                          # List all entities
teaql assistant <entity>                 # List all operations for entity
teaql assistant <entity> <operation>     # Execute specific operation
teaql assistant --search <keyword>       # Global search across all entities
```

### 2.2 Operations

| Operation | Description | Output |
|-----------|-------------|--------|
| `Q` | Query methods | Q entry points, filters, relation selects |
| `E` | Expression methods | E expression chains |
| `create` | Create code | new_entity + update fields + audit_as |
| `query` | Query code | Q chain with filters and relations |
| `update` | Update code | Load + update fields + audit_as |
| `delete` | Delete code | Load + mark_as_delete + audit_as |
| `fields` | Field list | All fields with types and examples |
| `relations` | Relation list | Parent/child relations |
| `constants` | Constant values | All _value entries |
| `stats` | Aggregation | count, sum, group_by methods |

### 2.3 Examples

```bash
# List all entities
> teaql assistant
Available entities:
  book, book_category, book_status, library_branch, loan, loan_status

# List operations for book
> teaql assistant book
Available operations:
  Q, E, create, query, update, delete, fields, relations, constants, stats

# Get Q methods for book
> teaql assistant book Q
Returns markdown table with:
  - Q entry points
  - Filter methods
  - Relation select methods
  - Status shortcuts

# Get fields for book
> teaql assistant book fields
Returns markdown table with:
  - Field name
  - Type
  - Example value
  - Whether it's a relation

# Search for isbn across all entities
> teaql assistant --search isbn
Returns:
  - book.isbn (String) - "978-7-111-42781-2"

# Generate create code for book
> teaql assistant book create
Returns complete Rust code:
  - Q::books().purpose("...").new_entity(&ctx)
  - All field updates
  - audit_as().save()
```

### 2.4 Output Format

All output is markdown. Example for `teaql assistant book Q`:

```markdown
# Entity: book — Q Methods

## Entry Points

| Method | Return Type |
|--------|-------------|
| `Q::books()` | BookRequest |
| `Q::books_minimal()` | BookRequest |
| `Q::books_with_children()` | BookRequest |

## Filters

| Method | SQL Equivalent |
|--------|----------------|
| `.with_title_is(v)` | `title = v` |
| `.with_title_contains(v)` | `title LIKE '%v%'` |
| `.with_author_is(v)` | `author = v` |
| `.with_isbn_is(v)` | `isbn = v` |
| `.with_total_copies_greater_than(v)` | `total_copies > v` |

## Relation Select

| Method | Target |
|--------|--------|
| `.select_library_branch_with(Q::library_branches()...)` | library_branch |
| `.select_category_with(Q::book_categories()...)` | book_category |
| `.select_status_with(Q::book_statuses()...)` | book_status |
| `.select_loan_list_with(Q::loans()...)` | loan[] |

## Status Shortcuts

| Method | Value |
|--------|-------|
| `.with_status_is_available()` | AVAILABLE |
| `.with_status_is_on_loan()` | ON_LOAN |
| `.with_status_is_reserved()` | RESERVED |
| `.with_status_is_damaged()` | DAMAGED |
| `.with_status_is_retired()` | RETIRED |
```

### 2.5 Search Mode

```bash
# Global search
> teaql assistant --search isbn

Found "isbn" in:
  - **book.isbn** (String) — "978-7-111-42781-2"
  - Module: Collection
  - Q: Q::books().with_isbn_is("...")

# Search by type
> teaql assistant --search --type String

All String fields:
  - book.isbn
  - book.title
  - book.author
  - book.publisher
  - loan.loan_number
  - loan.borrower_name
  - loan.borrower_card

# Search by relation
> teaql assistant --search --relation

All relation fields:
  - book.library_branch → library_branch
  - book.category → book_category (constant)
  - book.status → book_status (constant)
  - loan.book → book
  - loan.status → loan_status (constant)
```

## 3. Integration with AI Agents

### 3.1 Workflow

```
1. teaql assistant                    → See all entities
2. teaql assistant book               → See all operations
3. teaql assistant book fields        → Get field list
4. teaql assistant book Q             → Get query methods
5. Copy-paste into code               → No grep needed
6. cargo check                        → Compile
```

### 3.2 AGENTS.md Integration

```markdown
## Before Writing Code

1. Run `teaql assistant <entity> fields` to get field list
2. Run `teaql assistant <entity> Q` to get query methods
3. Copy-paste from the output directly into your code
4. Do NOT grep generated source files
```

### 3.3 Token Savings

| Before | After |
|--------|-------|
| grep q.rs → 200 lines | teaql assistant book Q → 30 lines |
| grep request.rs → 150 lines | teaql assistant book fields → 20 lines |
| Total: 350 lines × 5 entities = 1750 lines | 50 lines × 5 entities = 250 lines |
| **Savings: 85%** | |

## 4. Implementation

### 4.1 Source Data

The CLI reads:
- `generate-lib/lib/src/q.rs` — Q entry points
- `generate-lib/lib/src/<entity>/request.rs` — Filter and relation methods
- `generate-lib/lib/src/<entity>/struct.rs` — Entity fields
- `generate-lib/lib/src/<entity>/expression.rs` — E expressions

### 4.2 Command Implementation

```rust
// teaql assistant book Q
fn entity_q_methods(entity: &str, model: &Model) -> String {
    let mut output = String::new();
    output.push_str(&format!("# Entity: {} — Q Methods\n\n", entity));
    
    // Q entry points
    output.push_str("## Entry Points\n\n");
    output.push_str("| Method | Return Type |\n");
    output.push_str("|--------|-------------|\n");
    for entry in model.q_entries(entity) {
        output.push_str(&format!("| `Q::{}()` | {} |\n", entry.plural, entry.request_type));
    }
    
    // Filters
    output.push_str("\n## Filters\n\n");
    output.push_str("| Method | SQL Equivalent |\n");
    output.push_str("|--------|----------------|\n");
    for field in model.entity_fields(entity) {
        output.push_str(&format!("| `.with_{}_is(v)` | `{} = v` |\n", field.name, field.name));
    }
    
    output
}
```

### 4.3 Output Format

All commands output markdown. The CLI:
1. Reads model.xml or generated code
2. Extracts entity information
3. Formats as markdown tables
4. Prints to stdout

### 4.4 Configuration

```bash
# With model.xml
teaql assistant --model path/to/model.xml book Q

# With generated code
teaql assistant --generate-lib path/to/generate-lib book Q

# Auto-detect (search current directory)
teaql assistant book Q
```

## 5. Future Extensions

### 5.1 Explain Command

```bash
teaql assistant book explain
```

Output:
```markdown
# Entity: book

## Purpose
Represents a book in the library collection.

## Key Relationships
- Belongs to one library_branch
- Has one category (constant)
- Has one status (constant)
- Has many loans (child)

## Common Patterns
- Create: Add new book to collection
- Query: List books by category or status
- Update: Change availability count
- Delete: Retire damaged books
```

### 5.2 Diff Command

```bash
teaql assistant diff model1.xml model2.xml
```

Output:
```markdown
# Model Diff

## Added Entities
- loan

## Removed Entities
- reservation

## Changed Fields
- book.total_copies: i32 → i64
- book.status: added RETIRED value
```

### 5.3 Generate Command

```bash
teaql assistant book generate create
```

Output:
```rust
// Create new book
let mut book = Q::books()
    .purpose("Add new book to collection")
    .new_entity(&ctx);

book.update_isbn("978-7-111-42781-2");
book.update_title("Rust Programming");
book.update_author("Steve Klabnik");
book.update_publisher("O'Reilly");
book.update_total_copies(10);
book.update_available_copies(10);

book.audit_as("Add new book to collection").save(&ctx).await?;
```

## 6. Expected Impact

| Metric | Before | After |
|--------|--------|-------|
| Time to find method | 30 seconds (grep) | 1 second (CLI) |
| Token usage | 50k+ per project | 5k per project |
| Compilation errors | 5-10 | 0-1 |
| AI agent autonomy | Medium | High |

---

*This design document is based on actual AI agent behavior observed during evaluation-report-003.*
