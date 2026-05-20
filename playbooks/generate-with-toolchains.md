# Generate With TeaQL Toolchains

Use this playbook after a valid KSML `model.xml` exists and the user wants Java,
Rust, or both TeaQL code generation tracks.

## Inputs

- Valid KSML model file or model directory.
- Target runtime: Java, Rust, or both.
- Target project directory or playground local trial directory.
- TeaQL client tools installed from package registries. For Java, resolve the
  TeaQL Maven plugin from Maven Central or the configured Maven repository. For
  Rust, install the `cargo-teaql` CLI from crates.io with
  `cargo install cargo-teaql`.
- Optional TeaQL service URL, license file, output directory, and timeout.

## General Rules

- Do not generate from vague business text directly. Generate from the model.
- Before generation, run `playbooks/model-review-gate.md`. The model must be
  confirmed by the user, or autonomous playground assumptions must be explicitly
  listed and accepted by the user's request.
- Playground mode is the default mode for local trials. Do not require git
  repositories or artifact publishing.
- In playground mode, keep model input and generated runtime code inside
  `app-playground` for easy review: use `app-playground/models` for `model.xml`
  and related model inputs, and `app-playground/generate-lib` for generated
  TeaQL runtime code. Keep generated runtime code separate from the user's
  experiment source and test code. Use a local path dependency when the
  playground needs to call generated APIs.
- Treat TeaQL service generated Java or Rust code as read-only. Do not edit
  generated files directly; fix the model, generator configuration, TeaQL
  generator, or runtime, then regenerate.
- For user-facing workflows, install TeaQL client tools from package registries
  and use those clients to request TeaQL service generation. For Java, use the
  TeaQL Maven plugin from Maven Central or the configured Maven repository. For
  Rust, install the `cargo-teaql` CLI from crates.io with
  `cargo install cargo-teaql`.
- Do not clone, search for, or build local or remote TeaQL toolchain source
  repositories for normal generation work. If the Maven plugin or crates.io
  crate cannot be installed, resolved, invoked, or executed, stop immediately and
  report the specific blocker. Do not continue by attempting a source checkout,
  local source build, hand-written generation, generated-code patch, or alternate
  generation path.
- Local toolchain source repositories are only for explicitly requested TeaQL
  toolchain development or debugging, never as a fallback for generation:
  - Rust CLI source: `~/githome/teaql-cargo-cli`
  - Java Maven plugin source: `~/githome/teaql-maven-plugin`
- Debugging mode is only active when the user explicitly asks to debug TeaQL
  toolchains, generated output, or integration failures. State the mode switch
  before using source repositories or temporary investigation patches.
- Playground mode may run `ensure_schema()` automatically to create local demo
  tables and make the first run executable. Outside playground mode, schema
  creation and migration must be treated as explicit deployment decisions, not
  hidden runtime initialization side effects.
- Use the same model input for Java and Rust when the user requests both tracks.
- When writing customer query code that must accept dynamic fields, operators,
  sort clauses, or pagination options at runtime, use the high-level JSON query
  API instead of low-level filter mutation primitives. In Rust, use
  `find_with_json_expr`; in Java / Spring Boot, use the documented
  `findByJson` / `findWithJsonExpr` dynamic query surface. Do not assemble
  dynamic queries by calling Rust `add_filter` or Java `addFilter` directly.
  The official guide is
  <https://teaql.io/docs/working-with-teaql-and-springboot/find-by-json-dynamic-query>.
  Apply tenant scope, permission boundaries, page-size caps, and default
  ordering as fixed typed TeaQL request constraints around the dynamic JSON
  query.

## Rust Track

Use the Rust CLI when the target runtime is Rust or when the user asks for the
Cargo toolchain.

1. Install the TeaQL CLI from crates.io. If this command fails because the crate
   cannot be found, downloaded, installed, invoked, or executed, stop immediately
   and report the failure. Do not look for source code or try to build
   `cargo-teaql` from a local or remote repository.

   ```bash
   cargo install cargo-teaql
   ```

2. Generate backend/domain code from the model. In playground mode, create or
   copy the reviewed model to `/path/to/app-playground/models/model.xml`, and
   use `/path/to/app-playground/generate-lib` as the output path:

   ```bash
   cargo-teaql gen-code /path/to/app-playground/models/model.xml \
     --output /path/to/app-playground/generate-lib \
     --cwd /path/to/app-playground
   ```

3. Generate documentation or frontend model output when requested:

   ```bash
   cargo-teaql gen-doc /path/to/model.xml \
     --output /path/to/target/build \
     --cwd /path/to/target/project

   cargo-teaql gen-model /path/to/model.xml \
     --output /path/to/target/build \
     --cwd /path/to/target/project
   ```

4. Run target-project Rust checks when a Cargo project is generated:

   ```bash
   cargo check
   cargo test
   ```

For playground mode, create a Cargo playground crate, place the model under
`app-playground/models`, place generated runtime code under
`app-playground/generate-lib`, and depend on the generated runtime by local path.
The generated Rust crate is usually under the `lib` directory of the generator
output:

```bash
cargo init --bin --vcs none app-playground
```

```toml
[dependencies]
my_generated_runtime = { path = "generate-lib/lib" }
```

Put customer query functions and business helper functions in `src/lib.rs`.
Use `tests/` for scenario-oriented experiments. Keep `src/main.rs` as a thin
smoke demo only.

Recommended playground shape:

```text
app-playground/
  models/
    model.xml           # semantic source of truth for generation
  generate-lib/         # generated Java or Rust TeaQL runtime code
  src/
    lib.rs               # customer functions and query helpers
    main.rs              # thin smoke demo
  tests/
    inventory_queries.rs # scenario-oriented experiments
  TEAQL_QUICK_TRY_REPORT.md
```

Example:

```rust
// src/lib.rs
use my_generated_runtime::Q;

pub fn stock_on_hand_query() {
    let _query = Q::stock_items()
        .select_product_with(Q::products().which_skus_are("USB-C-001"))
        .select_warehouse_with(Q::warehouses().which_codes_are("SHA-MAIN"))
        .which_quantities_greater_than(0)
        .page(1, 20);
}
```

```rust
// tests/inventory_queries.rs
use app_playground::stock_on_hand_query;

#[test]
fn builds_stock_on_hand_query() {
    stock_on_hand_query();
}
```

```rust
// src/main.rs
fn main() {
    app_playground::stock_on_hand_query();
    println!("playground smoke check passed");
}
```

Keep regenerated TeaQL code in `app-playground/generate-lib`. Do not mix
generated runtime files into `src/` or `tests/`.

## Playground Report

For playground mode, always create a short report in the playground directory:

```text
app-playground/TEAQL_QUICK_TRY_REPORT.md
```

The report should help a customer understand what happened, which files matter,
and what TeaQL contributed beyond ordinary code generation.

Recommended sections:

1. `Goal`
   - State the natural-language business scenario being tried.
   - State the target runtime.

2. `Directory Layout`
   - List `app-playground/models`, `app-playground/generate-lib`, and the
     customer-owned playground source/test paths.
   - State explicitly that generated runtime code and customer experiment code
     are separate.

3. `Model Review`
   - State the review status: `confirmed`, `confirmed_with_assumptions`, or
     `needs_revision`.
   - State who or what confirmed it: user confirmation, or explicit autonomous
     assumptions for playground mode.
   - List the model path.
   - Summarize reviewed entities, important fields, relationships, constants,
     tenancy classification, tenant boundary if any, assumptions, and open
     questions.

4. `Model Summary`
   - List the main business objects, constants, tenancy classification, tenant
     boundary if any, and important relationships.
   - Explain that `model.xml` is the semantic source of truth.

5. `Generated Runtime`
   - List the generated crate path and the key generated APIs, such as `Q`,
     entity structs, request builders, relation loaders, aggregation helpers,
     runtime registration, and schema bootstrap helpers when present.
   - State that generated files should be regenerated from the model, not
     hand-edited.
   - If `ensure_schema()` is called automatically in playground mode, state that
     this is a local demo convenience. Outside playground mode, schema creation
     and migration must be executed through an explicit deployment, DBA, CI/CD,
     admin command, or migration workflow.

6. `Customer Playground`
   - List the customer-owned files in `src/lib.rs`, `src/main.rs`, and `tests/`.
   - Explain which queries or scenario functions were written and which
     generated APIs they use.

7. `Commands Run`
   - Include the exact generation and verification commands.
   - Include pass/fail results.

8. `TeaQL Value Demonstrated`
   - Explain the concrete guardrails demonstrated:
     - Natural language was converted to a semantic model first.
     - The model was reviewed before code generation.
     - Generated API names came from the model.
     - Query code used typed generated methods instead of ad-hoc SQL.
     - Generated code and customer code stayed separated.
     - Schema bootstrap stayed visible as a decision point: automatic in quick
       try only, explicit in project and production environments.
     - Checks can be rerun after every model change.
   - Include a short, readable code excerpt from the customer's playground and
     point out how the generated API reads in business terms.
   - Explain runtime customization points such as provider choice, runtime
     context assembly, behavior hooks, checker hooks, tenant/user context, and
     schema bootstrap.
   - Explain SQL observability. If SQL was captured during the run, include a
     short example. If not, state that the generated query can be executed with
     TeaQL SQL log options enabled as the next verification step.

For Rust playground mode, prefer adding one scenario test that initializes a local
runtime, enables select SQL logging on the runtime context, executes a generated
query, and asserts that SQL logs were captured. This makes the report concrete:
the customer sees readable query code and the SQL produced behind it.

The SQL log shown in the report should be customer-readable. Prefer showing:

- result summary, such as `0 x StockItem` or `3 x Product`;
- end time;
- elapsed time;
- formatted SQL with line breaks for `FROM`, `WHERE`, `ORDER BY`, `LIMIT`, and
  boolean clauses.

9. `Next Steps`
   - Suggest the smallest next model change or customer scenario to try.
   - Mention when to move from local path dependencies to a runtime repository
     or artifact repository.

## Java Track

Use the Maven plugin when the target runtime is Java or when the user asks for
the Maven toolchain.

1. Resolve the TeaQL Maven plugin from Maven Central or the configured Maven
   repository. If Maven cannot resolve or execute the plugin, stop and report the
   failure immediately. Do not look for source code or try to build the plugin
   from a local or remote repository.

2. Generate backend/domain code from the model. In playground mode, create or
   copy the reviewed model to `/path/to/app-playground/models/model.xml`, and
   use `/path/to/app-playground/generate-lib` as the output path:

   ```bash
   mvn teaql:gen-code \
     -Dteaql.input=/path/to/app-playground/models/model.xml \
     -Dteaql.output=/path/to/app-playground/generate-lib
   ```

3. Generate documentation or frontend model output when requested:

   ```bash
   mvn teaql:gen-doc \
     -Dteaql.input=/path/to/model.xml \
     -Dteaql.output=/path/to/target/build

   mvn teaql:gen-model \
     -Dteaql.input=/path/to/model.xml \
     -Dteaql.output=/path/to/target/build
   ```

4. Run target-project Java checks when a Maven project is generated:

   ```bash
   mvn test
   ```

For playground mode, keep the model under `app-playground/models` and the
generated runtime as a separate local Maven module or directory under
`app-playground/generate-lib`. Let the playground application depend on it
locally. If no artifact repository exists yet, install the generated runtime
into the local Maven cache or use a multi-module local workspace during the
trial. Keep user controllers, query experiments, and scenario code in the
playground module.

## Configuration

Both toolchains use the same configuration model:

1. CLI or Maven parameter.
2. Environment variable.
3. `~/.teaql/config.yml`.
4. Built-in default.

Common keys:

| Purpose | Rust CLI flag | Maven property | Environment variable |
| --- | --- | --- | --- |
| Service URL | `--service-url` | `teaql.serviceUrl` | `TEAQL_SERVICE_URL` |
| License file | `--license-file` | `teaql.licenseFile` | `TEAQL_LICENSE_FILE` |
| Output directory | `--output` | `teaql.output` | `TEAQL_BUILD_DIR` |
| Timeout seconds | `--timeout-seconds` | `teaql.timeoutSeconds` | `TEAQL_TIMEOUT_SECONDS` |

Recommended public generation endpoint:

```text
https://api.teaql.io/latest/generate
```

## Repair Loop

1. Read generator output and compiler errors.
2. Classify the failure:
   - Model error: invalid entity, field, relationship, constant, or lifecycle.
   - Integration error: missing dependency, project config, database provider, or
     runtime wiring.
   - Toolchain error: CLI/plugin config, service URL, license, or network.
3. Fix model errors in `model.xml` and regenerate.
4. Fix integration errors in the target project.
5. For generation client installation, resolution, invocation, or execution
   failures, stop immediately after reporting the blocker. Do not fall back to
   source checkout, source build, local toolchain repository usage, hand-written
   generation, generated-code patching, or alternate generation paths unless the
   user explicitly changes the task to debugging mode.
6. Do not patch generated TeaQL service code. If the user explicitly asks for a
   temporary investigation patch, mark it as temporary and do not present it as a
   deliverable project change.

## Done

The task is done when generation has run for the requested runtime, target
checks have passed or the remaining blocker is clearly reported, and the final
response lists the model path, generated output path, playground path, report
path, commands run, and any assumptions.
