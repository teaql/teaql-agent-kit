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

- Java: `io.teaql:teaql-maven-plugin:1.1.0` or newer
- Rust: `cargo-teaql` `2.0.7` or newer

For Rust:

```bash
cargo install cargo-teaql --force
cargo-teaql --version
cargo-teaql install-links
```

For Java, always invoke the fully qualified plugin version, for example:

```bash
mvn io.teaql:teaql-maven-plugin:1.1.0:eval -Dteaql.input=model.xml
```

Run the validation tool:
```bash
cargo teaql --input model.xml evaluate
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

## Step 4: Generate Rust Outputs
For Rust generation in this Agent Kit, only two generation targets are valid:
`rust-lib-core` and `rust-app-console`.

Generate the read-only library first, then the runnable app console. Keep their
output directories separate. Do not use `rust-workspace`, `markdown-doc`,
`frontend-model`, or other command names as Rust generation targets in this
repository.

```bash
cargo teaql --input app-playground/models/model.xml rust-lib-core \
  --output app-playground/generate-lib \
  --cwd app-playground

cargo teaql --input app-playground/models/model.xml rust-app-console \
  --output app-playground/rust-app-console \
  --cwd app-playground
```

`rust-lib-core` writes generated TeaQL runtime/domain code to
`app-playground/generate-lib`; do not edit it. `rust-app-console` writes the
runnable customer-owned Cargo app to `app-playground/rust-app-console`; put
custom Rust code there. The app console depends on the generated library.

The `rust-app-console` output is a project-specific handoff point for the next
AI coding step. Immediately after it is generated, read
`app-playground/rust-app-console/AGENTS.md` and follow that local guide before
adding code, running checks, or explaining the app console.

*Note: The generated Rust library crate name will automatically append `-core` to the model name (e.g., `bookstore-service-core`), but the Rust module name remains unchanged (e.g., `bookstore_service`). Never manually edit files inside the generated folders (`generate-lib/` or `bizcore/`).*

Immediately after generation, locate and read the nearest generated `AGENTS.md`
before using any generated API. Common locations include
`app-playground/generate-lib/AGENTS.md`,
`app-playground/generate-lib/lib/AGENTS.md`,
`app-playground/rust-app-console/AGENTS.md`, and the generated application
workspace root. If generated code is present but its local `AGENTS.md` is
missing, stop and report the missing guide instead of guessing the API rules.

## Step 5: Write the Code
After generating, do not use generic API pattern documents as the source of
truth. Use the generated output for your target language:

- **Java**: Follow the generated workspace `AGENTS.md` and generated source
  files for the exact service, controller, query, and entity API shape.
- **Rust**: Run the object-specific assist command for the entity and action you
  are coding:

```bash
cargo teaql --input modeling/<your-model>.xml rust-assist-<action> <entity_name>
```

For Rust, the assist output is the source of truth for exact generated method
names and code shape. Dynamic Rust assist commands are generated from the input
model; before using one, pass the current model input with `--input` and read
its current help or output.

Make sure you always include `.purpose()` / `.comment()` for queries, and `.audit_as()` / `.auditAs()` for updates.
Finally, run checks to ensure correctness:
```bash
cargo check && cargo test
```
