# TeaQL Quick Start for AI Agents (5-Minute Guide)

This guide provides the fastest path for an AI agent to build a TeaQL project from scratch. By following these 5 steps, you will construct a correctly structured model, validate it, generate the code, and use the APIs.

## Step 1: Read the Rules (2 mins)
**CRITICAL**: Read `modeling/KSML-RULES.md` and `agents/RULES.md` before writing any XML or code. `modeling/KSML-RULES.md` is the canonical source for KSML XML.
- The document element MUST be `<root>`.
- All business and constant objects MUST be direct children of `<root>`.
- Business objects MUST NOT use `id="id()"`.
- Constant objects MUST use `id="id()"`, `name="string()"`, `code="string()"`, `_constant="true"`, and `_identifier="code"`.

## Step 2: Create the Model (`model.xml`)
Use `agents/TEMPLATES.md` to copy the exact XML blocks.
Follow `agents/DECISION-TREES.md` to pick the right root and tenancy strategy.

**Example Minimal Model:**
```xml
<root alias_model_name="bookstore_management"
      chinese_name="书店管理"
      english_name="Bookstore Management"
      name="bookstore-service"
      cfg_mask_china_mobile="false"
      data_service="sqlite"
      org="doublechaintech"
      _module_key="root">
  <bookstore _name="Bookstore"
             _module="Store"
             _module_key="store"
             name="TeaQL Books"
             create_time="createTime()"
             update_time="updateTime()"/>
  <book_status _name="Book Status"
               _module="Basic Data"
               _module_key="basic-data"
               id="id()" name="string()" code="string()"
               _constant="true" _identifier="code">
    <_value id="1001" name="Available" code="AVAILABLE"/>
    <_value id="1002" name="Archived" code="ARCHIVED"/>
  </book_status>
  <book _name="Book"
        _module="Catalog"
        _module_key="catalog"
        title="Domain Modeling with TeaQL"
        bookstore="bookstore()"
        status="book_status()"
        create_time="createTime()"
        update_time="updateTime()"/>
</root>
```

## Step 3: Validate and Fix Errors
Before validation, refresh and verify the TeaQL client version. Do not reuse an
older local client from a previous run.

Required versions:

- Java: `io.teaql:teaql-maven-plugin:1.0.1` or newer
- Rust: `cargo-teaql` `1.0.0` or newer

For Rust:

```bash
cargo install cargo-teaql --force
cargo-teaql --version
cargo-teaql install-links
```

For Java, always invoke the fully qualified plugin version, for example:

```bash
mvn io.teaql:teaql-maven-plugin:1.0.1:eval -Dteaql.input=model.xml
```

Run the validation tool:
```bash
cargo-teaql eval model.xml
```
*Tip: When errors occur, the CLI natively outputs a beautifully formatted Markdown report for easy reading and analysis.*
- **Prefer evaluate over rereading docs**: Evaluation is cheap and gives the
  current model's exact errors. After each KSML fix, rerun evaluation
  immediately.
- **If errors occur**: Read the output or Markdown report first, then go
  straight to `agents/ERROR-FIX.md` and use the copy-paste fixes provided
  there. Consult long-form rules only for the specific rule named by the
  report.
- **If 0 errors**: Proceed to generation.

## Step 4: Generate the Workspace
Generate the libraries and workspace code.
```bash
cargo-teaql gen-lib model.xml
cargo-teaql gen-workspace model.xml
```
*Note: Never manually edit files inside the generated folders (`generate-lib/` or `generate-workspace/` or `bizcore/`).*

## Step 5: Write the Code
After generating, reference the API pattern document for your target language to write correct queries and updates:
- **Java**: Read `reference/API-PATTERN-JAVA.md`
- **Rust**: Read `reference/API-PATTERN-RUST.md`

Make sure you always include `.purpose()` / `.comment()` for queries, and `.audit_as()` / `.auditAs()` for updates.

Read the nearest generated `AGENTS.md` before using generated APIs. In the
default playground layout this is usually `app-playground/generate-lib/lib/AGENTS.md`.
Finally, run checks to ensure correctness:
```bash
cargo check && cargo test
```
