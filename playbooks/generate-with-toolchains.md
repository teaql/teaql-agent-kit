# Generate With TeaQL Toolchains

Use this playbook after a valid KSML `model.xml` exists and the user wants Java,
Rust, or both TeaQL code generation tracks.

## Inputs

- Valid KSML model file or model directory.
- Target runtime: Java, Rust, or both.
- Target project directory or playground local trial directory.
- Optional Java workspace output when the user asks for a runnable Java
  workspace: service `java-workspace`.
- Optional Rust app output when the user asks for a runnable Rust app:
  generation target `rust-app-console`, which depends on the generated Rust
  library crate.
- TeaQL client tools installed from package registries. For Java, resolve TeaQL
  Maven plugin version `1.1.0` or newer from the TeaQL Nexus releases
  repository: `https://nexus.teaql.io/repository/maven-releases/`. Do not rely
  on Maven Central freshness, and invoke the plugin with fully qualified
  coordinates such as `io.teaql:teaql-maven-plugin:1.1.0:generate -Dservice=java-lib`, not Maven
  prefix resolution such as `mvn teaql:generate -Dservice=java-lib`. Ensure Maven settings or the
  project POM exposes that URL as both a repository and a plugin repository. For
  Rust, install `cargo-teaql` version `2.0.5` or newer from crates.io with
  `cargo install cargo-teaql`, then run `cargo-teaql install-links`.
- Optional server-side KSML evaluation target exposed by the installed client:
  `cargo teaql --input <model> evaluate` for the Rust/client path, or the fully
  qualified Maven plugin `eval` goal for the Java/Maven path.
- Optional TeaQL service URL, license file, output directory, and timeout.

## General Rules

- Do not generate from vague business text directly. Generate from the model.
- Before any TeaQL evaluation or generation command, refresh or verify the
  TeaQL client version. Previous successful use of an older local client is not
  evidence that it is valid for this repository. The repository-required
  versions are authoritative for every new run: Java
  `io.teaql:teaql-maven-plugin:1.1.0` or newer from the TeaQL Nexus releases
  repository, and Rust `cargo-teaql` `2.0.5` or newer from crates.io.
- For Rust, when network access is available, run
  `cargo install cargo-teaql --force`, then `cargo-teaql --version`, then
  `cargo-teaql install-links` before generation. If the available version is
  older than `2.0.5`, stop and report the blocker.
- For Java, never rely on a previously resolved plugin or Maven prefix
  resolution. Invoke the fully qualified plugin coordinate with version
  `1.0.0` or newer, such as
  `mvn io.teaql:teaql-maven-plugin:1.1.0:generate -Dservice=java-lib`. If Maven resolves an older
  plugin, or the required version cannot be resolved from the TeaQL Nexus
  releases repository, stop and report the blocker.
- Using `cargo-teaql < 2.0.5`, `teaql-maven-plugin < 1.1.0`, or `mvn teaql:*`
  is an evaluation failure unless the user explicitly asks to reproduce an
  old-version bug.
- Run server-side KSML evaluation before generation when the installed client
  exposes an `evaluate` target. Evaluation `errors` must be fixed before generation.
  Evaluation `warnings` and `suggestions` should be reported to the user but do
  not block generation by default.
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
- Use concrete paths in command-line examples and invocations. Do not pass
  Maven/POM expressions such as `${project.basedir}` or `${project.baseDir}` to
  `-Dteaql.input`, `-Dteaql.output`, `-Dteaql.workspaceDir`, or `--output`. Maven only interpolates project expressions in POM/plugin
  configuration contexts, not arbitrary CLI property values; use an actual path
  such as `/path/to/app-playground/generate-lib` or `app-playground/generate-lib`.
- For Java playgrounds that should be runnable as an application, generate the
  Java library first with the fully qualified Maven plugin coordinate and
  `-Dservice=java-lib`, then generate the workspace with
  `-Dservice=java-workspace` and write the workspace output to
  `app-playground/java-workspace` with `teaql.workspaceDir`. The workspace
  request generates a Spring Boot/Maven workspace from the model, including `AGENTS.md`,
  `pom.xml`, `.gitignore`, `src/main/resources/application.properties`, the
  Spring Boot application class, `CustomUserContext`, `EnsureModelController`,
  and `docs/teaql-java-crud-guide.md`. Do not recreate these files by hand when
  the goal is available.
- After generating the TeaQL library under `app-playground/generate-lib`, read
  `app-playground/generate-lib/AGENTS.md` before using, explaining, testing, or
  wiring the generated library APIs. If that library guide is missing after
  generation, stop and report it as a blocker. If the generated library is
  consumed from a package repository instead of a local generated directory,
  locate the unpacked dependency source first; for Cargo dependencies, use
  `cargo metadata` or `cargo vendor`, then read the crate root `AGENTS.md`
  before writing code against that crate.
- When working inside a generated Java workspace, read and follow its generated
  `AGENTS.md` in addition to this kit-level playbook before reading, editing,
  testing, running, or explaining workspace code. The generated workspace guide
  is created dynamically by the server for that domain and runtime, so read it
  again after every workspace regeneration. It is the local authority for Java
  business code written there; when it is more specific than this kit-level
  playbook, follow the workspace guide. If the workspace is expected to be
  generated but has no `AGENTS.md`, stop and report that missing guide as the
  blocker.
- Treat TeaQL service generated Java or Rust code as read-only. Do not edit
  generated files directly; fix the model, generator configuration, TeaQL
  generator, or runtime, then regenerate.
- For user-facing workflows, install TeaQL client tools from package registries
  and use those clients to request TeaQL service generation. For Java, use TeaQL
  Maven plugin version `1.1.0` or newer from the TeaQL Nexus releases
  repository: `https://nexus.teaql.io/repository/maven-releases/`. Do not rely
  on Maven Central freshness. Invoke Java goals with fully qualified Maven
  plugin coordinates, for example
  `mvn io.teaql:teaql-maven-plugin:1.1.0:generate -Dservice=java-lib`; do not use `mvn teaql:*`.
  For Rust, install `cargo-teaql` version `2.0.5` or newer from crates.io with
  `cargo install cargo-teaql`, then run `cargo-teaql install-links`.
- Do not clone, search for, or build local or remote TeaQL toolchain source
  repositories for normal generation work. If the Maven plugin, Maven plugin
  goal, TeaQL plugin/tool invocation, or crates.io crate cannot be installed,
  resolved, invoked, or executed, stop immediately and report the specific
  blocker. Do not continue by attempting a source checkout, local source build,
  hand-written generation, generated-code patch, or alternate generation path.
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
- When writing customer query code during AI Coding, start from the generated
  `Q` collection API for the target entity. For fixed business queries, use
  typed TeaQL Q/query helpers for filtering, ordering/sorting, pagination,
  facet/aggregation, and field selection/projection where the generated runtime
  exposes them. Keep query construction explicit and close to the page's
  visual/request order: begin with the entity Q collection, apply hard-coded
  business/security filters, apply dynamic search with `findByJson` /
  `findWithJsonExpr` or `find_with_json_expr` when runtime criteria exist,
  apply deterministic ordering, apply pagination such as `offset(0, 3)`, apply
  facet/aggregation declarations such as `facetByProductAs(...)` when the
  business view needs them, apply selected fields such as `selectName()`, then
  execute the query.
- When customer query code must accept dynamic fields, operators, selected
  fields, search terms, sort clauses, aggregation requests, or pagination
  options at runtime, use the high-level JSON query API or documented
  aggregation query surface instead of low-level filter mutation primitives. In
  Rust, use `find_with_json_expr`; in Java / Spring Boot, use the documented
  `findByJson` / `findWithJsonExpr` dynamic query surface. Do not assemble
  dynamic queries by calling Rust `add_filter` or Java `addFilter` directly.
  The official guide is
  <https://teaql.io/docs/working-with-teaql-and-springboot/find-by-json-dynamic-query>.
  Apply tenant scope, permission boundaries, page-size caps, and default
  ordering as fixed typed TeaQL request constraints around the dynamic JSON
  query.
- When customer code changes entity state, use the generated chainable
  `update<Field>(...)` methods where the runtime exposes them. Chain related
  field updates on the entity and persist with the normal TeaQL save surface.
  Do not update generated state by direct field mutation, raw SQL, generated
  service internals, or lower-level persistence bypasses.
- When writing Rust customer code, playground code, examples, or tests that
  create new entities, use the generated `Q` collection factory:
  `Q::<entities>().comment(...).new_entity(&ctx)`, such as
  `Q::products().comment("Initialize new product").new_entity(&ctx)`. Do not instantiate generated entity structs
  directly with struct literals, `Default`, or ad hoc builders.

## Rust Track

Use the Rust CLI when the target runtime is Rust or when the user asks for the
Cargo toolchain.

Rust generation in this Agent Kit has exactly two legal generation targets. Keep
their outputs separate:

| Output | Command | Directory | Purpose | Editable? |
| --- | --- | --- | --- | --- |
| Generated library crate | `rust-lib-core` | `app-playground/generate-lib` | TeaQL runtime/domain code generated from the model | No |
| Runnable app console | `rust-app-console` | `app-playground/rust-app-console` | Customer-owned Cargo app that depends on the generated crate | Yes |

Always generate the library first, then the app console. Do not send both
commands to the same output directory.

Do not use `rust-workspace`, `markdown-doc`, `frontend-model`, or other command
names as Rust generation targets in this repository. Every Rust TeaQL command
that reads or generates from a model must be invoked as
`cargo teaql --input <model> <command> ...`. The CLI may expose dynamic
commands, especially assist commands generated from a model input. For dynamic
commands, pass the current model with `--input` and read the current help/output
before using them.

1. Install `cargo-teaql` version `2.0.5` or newer from crates.io. If this
   command fails because the crate cannot be found, downloaded, installed,
   invoked, or executed, stop immediately and report the failure. Do not look
   for source code or try to build `cargo-teaql` from a local or remote
   repository.

   ```bash
   cargo install cargo-teaql
   ```

2. Install the local command links exposed by the CLI:

   ```bash
   cargo-teaql install-links
   ```

3. Evaluate the reviewed model when the installed client exposes `evaluate`.
   Evaluation errors block generation; warnings and suggestions should be
   reported:

   ```bash
   cargo teaql --input /path/to/app-playground/models/model.xml evaluate
   ```

4. Generate the read-only backend/domain library from the model. In playground
   mode, create or copy the reviewed model to
   `/path/to/app-playground/models/model.xml`, and use
   `/path/to/app-playground/generate-lib` as the output path:

   ```bash
   cargo teaql --input /path/to/app-playground/models/model.xml rust-lib-core \
     --output /path/to/app-playground/generate-lib \
     --cwd /path/to/app-playground
   ```

5. Generate the editable Rust app console after `rust-lib-core`. Write it to
   `/path/to/app-playground/rust-app-console`, not to `generate-lib`:

   ```bash
   cargo teaql --input /path/to/app-playground/models/model.xml rust-app-console \
     --output /path/to/app-playground/rust-app-console \
     --cwd /path/to/app-playground
   ```

   The generated app console depends on the generated runtime crate. It is also
   the project-specific handoff point for AI coding work: immediately read
   `/path/to/app-playground/rust-app-console/AGENTS.md` after generation. Follow
   that local guide before adding code, running checks, or explaining the app
   console. If the file is missing, stop and report the missing generated guide.

6. Run target-project Rust checks when a Cargo project is generated:

   ```bash
   cargo check
   cargo test
   ```

Put customer query functions, business helper functions, tests, runtime wiring,
and integration code inside `rust-app-console`. Keep `src/main.rs` as a thin
Tokio async smoke entrypoint. Do not add a web framework unless the user
explicitly asks for one.

Recommended playground shape:

```text
app-playground/
  models/
    model.xml           # semantic source of truth for generation
  generate-lib/         # generated Java or Rust TeaQL runtime code
  rust-app-console/     # editable Rust app from rust-app-console
    AGENTS.md
    Cargo.toml
    src/
      lib.rs             # customer functions and query helpers
      main.rs            # thin Tokio async smoke demo
    tests/
      inventory_queries.rs # scenario-oriented experiments
  TEAQL_QUICK_TRY_REPORT.md
```

Example:

```rust
// rust-app-console/src/lib.rs
use generated_domain_crate::Q;

pub fn stock_on_hand_query() {
    let _query = Q::stock_items()
        .comment("Load stock on hand")
        .select_product_with(Q::products().comment("Filter by SKU").which_skus_are("USB-C-001"))
        .select_warehouse_with(Q::warehouses().comment("Filter by warehouse code").which_codes_are("SHA-MAIN"))
        .which_quantities_greater_than(0)
        .page(1, 20);
}
```

```rust
// rust-app-console/tests/inventory_queries.rs
use generated_workspace_crate::stock_on_hand_query;

#[test]
fn builds_stock_on_hand_query() {
    stock_on_hand_query();
}
```

```rust
// rust-app-console/src/main.rs
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    generated_workspace_crate::stock_on_hand_query();
    println!("playground smoke check passed");
    Ok(())
}
```

Keep regenerated TeaQL code in `app-playground/generate-lib`. Do not mix
generated runtime files into `rust-app-console/src/` or `rust-app-console/tests/`.
Read `app-playground/generate-lib/lib/AGENTS.md` before using or explaining the
generated Rust library APIs. If the crate is consumed from a Cargo registry,
locate the unpacked dependency source with `cargo metadata` or materialize it
with `cargo vendor`, then read the crate root `AGENTS.md`. When working inside
`rust-app-console`, read its generated `AGENTS.md` first and read it again after
regeneration.

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
   - For Java `java-workspace` output, list the workspace path and call out the
     generated `AGENTS.md`, Maven files, Spring Boot application class,
     `CustomUserContext`, `EnsureModelController`, application properties, and
     CRUD guide.
   - For Rust `rust-app-console` output, list the app path and call out the
     generated `AGENTS.md`, `Cargo.toml`, Tokio async entrypoint, dependency on
     the generated library, and customer-owned source/test directories.
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

Before running Maven for a Java project, read
`playbooks/java-generation-known-pitfalls.md`.

1. Resolve TeaQL Maven plugin version `1.1.0` or newer from the TeaQL Nexus
   releases repository:
   `https://nexus.teaql.io/repository/maven-releases/`. Do not rely on Maven
   Central freshness. Invoke goals with fully qualified Maven plugin coordinates
   such as `io.teaql:teaql-maven-plugin:1.1.0:generate -Dservice=java-lib`; do not use Maven prefix
   resolution such as `mvn teaql:generate -Dservice=java-lib`, because Maven may resolve the prefix
   against Central or the wrong plugin group. Ensure Maven settings or the
   project POM exposes the TeaQL Nexus releases URL as both a repository and a
   plugin repository. If Maven cannot resolve the plugin from the TeaQL Nexus
   repository, if the plugin version is older than `1.0.0`, or if any TeaQL
   Maven plugin goal or TeaQL plugin/tool invocation fails, stop and report the
   failure immediately. Do not look for source code, try to build the plugin from
   a local or remote repository, hand-build generated output, or try an alternate
   generation path in normal generation mode.

2. Evaluate the reviewed model when the installed Maven plugin exposes `eval`.
   Use the fully qualified Maven plugin coordinate. Evaluation errors block
   generation; warnings and suggestions should be reported:

   ```bash
   mvn io.teaql:teaql-maven-plugin:1.1.0:eval \
     -Dteaql.input=/path/to/app-playground/models/model.xml
   ```

3. Generate backend/domain library code from the reviewed model. In playground
   mode, create or copy the reviewed model to
   `/path/to/app-playground/models/model.xml`, and use
   `/path/to/app-playground/generate-lib` as the output path:

   ```bash
   mvn io.teaql:teaql-maven-plugin:1.1.0:generate -Dservice=java-lib \
     -Dteaql.input=/path/to/app-playground/models/model.xml \
     -Dteaql.output=/path/to/app-playground/generate-lib
   ```

4. After `java-lib` generation succeeds, generate a runnable Java playground
   workspace when the user wants a local Spring Boot application. Use service
   `java-workspace` and
   write the workspace to
   `/path/to/app-playground/java-workspace`:

   ```bash
   mvn io.teaql:teaql-maven-plugin:1.1.0:generate -Dservice=java-workspace \
     -Dteaql.input=/path/to/app-playground/models/model.xml \
     -Dteaql.workspaceDir=/path/to/app-playground/java-workspace
   ```

   If the installed Maven plugin does not expose service `java-workspace`, or if
   that invocation fails, stop and report that plugin capability or
   invocation failure as the blocker. Do not hand-build the workspace or fall
   back to source checkouts in normal generation mode.

   The generated workspace includes its own domain-specific `AGENTS.md`,
   generated dynamically by the server. Read that file before inspecting,
   adding, editing, testing, running, or explaining controllers, services, jobs,
   query experiments, or integration code inside the workspace. If the workspace
   is regenerated, read the regenerated `AGENTS.md` again before continuing,
   because its rules may have changed. If the expected generated `AGENTS.md` is
   missing, stop and report that blocker. Generated TeaQL library classes remain
   read-only; workspace-owned Spring Boot code, controllers, tests, and
   configuration may be edited.

5. Run target-project Java checks when a Maven project is generated.
   For `java-workspace`, run checks from the generated workspace directory:

   ```bash
   mvn clean compile
   mvn test
   ```

For Java playground mode, always start from the reviewed model, run
fully qualified `generate -Dservice=java-lib`, and then run fully qualified
`generate -Dservice=java-workspace` when the expected result is a runnable directory. Keep the model under
`app-playground/models`, the generated library under `app-playground/generate-lib`,
and the generated workspace under `app-playground/java-workspace`. The workspace
is the application playground: keep user controllers, query experiments,
scenario code, and integration configuration there, while continuing to treat
generated TeaQL library classes as read-only. For library-only Java generation,
stop after fully qualified `generate -Dservice=java-lib` and wire any playground application to the
generated library locally.

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
   - Toolchain error: CLI/plugin config, service URL, license, evaluation, or
     network.
3. Fix model errors in `model.xml`, rerun `evaluate` when available, then
   regenerate.
4. Fix integration errors in the target project.
5. For generation client installation, resolution, invocation, or execution
   failures, including TeaQL Maven plugin goal failures and TeaQL plugin/tool
   invocation failures, stop immediately after reporting the blocker. Do not
   fall back to source checkout, source build, local toolchain repository usage,
   hand-written generation, generated-code patching, or alternate generation
   paths unless the user explicitly changes the task to debugging mode.
6. Do not patch generated TeaQL service code. If the user explicitly asks for a
   temporary investigation patch, mark it as temporary and do not present it as a
   deliverable project change.

## Done

The task is done when generation has run for the requested runtime, target
checks have passed or the remaining blocker is clearly reported, and the final
response lists the model path, evaluation result when available, generated
output path, playground path, report path, commands run, and any assumptions.
