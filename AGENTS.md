# TeaQL Vibe Kit Agent Instructions

This repository is the agent-native entry point for TeaQL vibe coding.

## Core Rule

Use TeaQL as Semantic Guardrails for AI Coding. Do not jump directly from vague
business requirements to arbitrary application code. First create a semantic
domain model, then generate Java or Rust TeaQL code from that model.

## Modeling Workflow

When the user asks to model a business domain:

1. Read `playbooks/model-from-natural-language.md`.
2. Use `prompts/modeling/system.md` as the modeling role.
3. Use `prompts/modeling/ksml-rules.md` as the source of truth for KSML XML.
4. Use `prompts/modeling/task-template.md` to frame the user's domain.
5. Produce a `model.xml` candidate.
6. Validate the model against `prompts/modeling/checklist.md`.
7. If the TeaQL client toolchain exposes model evaluation, run server-side KSML
   evaluation before generation:
   - Rust/client path: `cargo-teaql eval <model-file-or-directory>`.
   - Java/Maven path:
     `mvn io.teaql:teaql-maven-plugin:0.1.9:eval -Dteaql.input=<model-file-or-directory>`.
   Fix all evaluation `errors` before generation. Bring `warnings` and
   `suggestions` into the model review instead of treating them as automatic
   blockers.
8. If generating Java or Rust TeaQL code, run the model review gate in
   `playbooks/model-review-gate.md` and get confirmation before generation.
9. If generating a TeaQL project, run the appropriate code generation and checks
   after the model is created.

## Code Generation Workflow

When the user asks to generate Java or Rust TeaQL code:

1. Complete the modeling workflow first.
2. Complete the model review gate in `playbooks/model-review-gate.md`. Do not
   generate TeaQL service code until the model is confirmed or the user has
   explicitly accepted listed assumptions for autonomous playground work.
3. Read `playbooks/generate-with-toolchains.md`.
4. For Java generation, read `playbooks/java-generation-known-pitfalls.md`
   before running Maven.
5. Run the toolchain's model evaluation target before generation when available.
   For Rust, use `cargo-teaql eval <model-file-or-directory>`. For Java, use the
   fully qualified Maven plugin `eval` goal. Fix evaluation `errors` before
   generation; report `warnings` and `suggestions` in the model review or final
   delivery notes.
6. Choose the Java Maven plugin path, the Rust Cargo CLI path, or both based on
   the user's target runtime. For Java, use TeaQL Maven plugin version `0.1.9`
   or newer from the TeaQL Nexus releases repository:
   `https://nexus.teaql.io/repository/maven-releases/`. Do not rely on Maven
   Central freshness, and do not invoke the plugin through Maven prefix
   resolution such as `mvn teaql:gen-lib` or `mvn teaql:gen-workspace`; use the
   fully qualified plugin coordinates, for example
   `mvn io.teaql:teaql-maven-plugin:0.1.9:gen-lib`. For Rust, use
   `cargo-teaql` version `0.1.9` or newer from crates.io, and run
   `cargo-teaql install-links` after installation. For a runnable Rust
   playground, generate the library first with `cargo-teaql gen-lib`, then
   generate the editable workspace with `cargo-teaql gen-workspace`; the
   workspace depends on the generated crate by local path. Do not clone, search
   for, or build local or remote toolchain source code for normal generation
   work. If the generation client, TeaQL Maven plugin goal, or TeaQL plugin/tool
   invocation cannot be installed, resolved, invoked, or executed, stop
   immediately and report the blocker instead of trying source builds or
   alternate generation paths.
   When invoking TeaQL tools from the command line, pass concrete absolute or
   project-relative paths. Do not pass Maven/POM expressions such as
   `${project.basedir}` or `${project.baseDir}` as `-D` values; CLI properties
   are not POM interpolation sites, and `${project.baseDir}` is not a valid
   Maven project property name.
7. Keep generated output in the target project or demo project, not in this kit
   repository.
8. Run generation, compile checks, and tests where the target project provides
   them.
9. Treat TeaQL service generated code as read-only. If generation or compilation
   fails because the model is wrong, update `model.xml` and regenerate instead
   of hand-editing generated code.

## Generated Code Rule

TeaQL service generated Java or Rust code must not be modified directly.

If generated code is wrong, fix the semantic model, generator configuration,
TeaQL generator, or TeaQL runtime, then regenerate. Customer code, playground
code, query functions, tests, runtime wiring, and integration configuration may
be edited, but generated TeaQL service code is not a maintenance surface.

The only acceptable exception is an explicitly requested temporary investigation
patch. Such a patch must be reported as temporary and must not be presented as a
deliverable project change.

## Generated Workspace AGENTS.md Rule

Generated TeaQL libraries and workspaces may contain their own `AGENTS.md`.
Those files are generated dynamically by the server for the specific domain,
runtime, and generated surface, and may contain rules that are newer or more
specific than this kit-level file.

Before any AI coding agent reads, edits, tests, runs, or explains code inside a
generated library or generated workspace, it must first locate and read the
nearest generated `AGENTS.md`. For playground layouts, read
`app-playground/generate-lib/AGENTS.md` before using the generated TeaQL library
APIs, then read the generated workspace `AGENTS.md` before working inside
`java-workspace` or `rust-workspace`. If a generated library is consumed from a
package repository instead of a local generated directory, locate the unpacked
dependency source first. For Cargo dependencies, use `cargo metadata` to find
the package source or `cargo vendor` to materialize it locally, then read the
crate root `AGENTS.md` before using that crate's APIs. If the library or
workspace is regenerated or the dependency version changes, read the generated
`AGENTS.md` again before continuing, because its contents may have changed.
Treat the generated library/workspace `AGENTS.md` as the local authority for
work inside that generated surface; combine it with this kit-level file, and let
the more specific generated rule win when the two differ.

If no `AGENTS.md` exists in a directory that is expected to be a generated
library or generated workspace, stop and report that blocker instead of
guessing the generated-surface rules.

## Q and Query API Rule

When writing TeaQL customer code, playground code, query functions, examples, or
tests, start from the generated `Q` collection API for the target entity. Use
the high-level Q/query surfaces for normal application queries instead of
manually composing SQL, bypassing generated request types, or mutating generated
service internals.

For AI Coding tasks that write fixed business queries, use the typed TeaQL Q API
for filtering, ordering/sorting, pagination, facet/aggregation, and
selecting/projecting fields when those typed helpers are available. Keep the
query pipeline explicit and close to the page's visual/request order:

1. Start with the entity Q collection.
2. Apply hard-coded business and security filters.
3. Apply dynamic search from JSON when the UI or API accepts runtime criteria.
4. Apply deterministic ordering/sorting.
5. Apply pagination with the generated paging helper, such as `offset(0, 3)`.
6. Apply facet/aggregation declarations when the business view needs them.
7. Apply field selection/projection when the view only needs selected fields.
8. Execute the query.

For example, when the business view needs finished tasks, dynamic search,
latest-first ordering, first-page pagination, product/task-type facets, and a
small field projection, prefer a Q chain shaped like:

```java
Q.tasks()
    .whichAreFinished()
    .findByJson(json)
    .orderByCreateTimeDescending()
    .offset(0, 3)
    .facetByProductAs("productFacet", Q.products().countTasks())
    .facetByTaskTypeAs("taskTypeFacet", Q.taskType().countTasks())
    .selectName()
    .selectXXX()
    .executeForList(ctx);
```

When a task needs dynamic query construction, such as user-selected fields,
runtime-selected operators, or other filters that are not known at compile time,
use the high-level TeaQL JSON query APIs:

- Rust: use `find_with_json_expr`.
- Java / Spring Boot: use the documented `findByJson` /
  `findWithJsonExpr` dynamic query surface.

Reference:
<https://teaql.io/docs/working-with-teaql-and-springboot/find-by-json-dynamic-query>

These dynamic query APIs support field filters, chain-field filters, sorting,
offset/limit, page/page-size, dynamic search, and field selection where the
runtime supports them. Use the documented aggregation query surface for dynamic
grouping and aggregate calculations; do not emulate aggregation by loading broad
result sets into application memory unless the data set is intentionally small
and bounded. Do not build dynamic application queries by calling lower-level
filter primitives such as Rust `add_filter` or Java `addFilter` directly. Keep
fixed business and security constraints, such as tenant scope and permission
boundaries, in typed TeaQL request code around the dynamic JSON query.

## Chainable Update Rule

TeaQL updates can also be expressed through generated chainable update methods.
When customer code, playground code, examples, or tests need to change entity
state, prefer generated `update<Field>(...)` methods over direct field mutation,
manual SQL, or generated service internals. Chain multiple updates on the entity
when the business transition changes more than one field, then persist through
the normal TeaQL save surface:

```java
merchant
    .updateStatus(MerchantStatus.ACTIVE)
    .updateDisplayName("TeaQL Store")
    .save(userContext);
```

Keep the chain focused on the domain state transition. If the update exposes a
modeling error, fix the model and regenerate instead of patching generated
service code.

## Rust Entity Creation Rule

When Rust customer code, playground code, examples, or tests need to create a
new TeaQL entity instance, use the generated `Q` collection factory:

```rust
let entity = Q::<entities>().new_entity(&ctx);
```

For example, use `Q::products().new_entity(&ctx)` for a `product` entity. Do not
construct generated entity structs directly with struct literals, `Default`, or
ad hoc builders in customer code. The `Q` factory is the semantic creation
surface that keeps context-aware defaults, generated conventions, and future
runtime hooks in one place.

## Output Discipline

- For pure modeling tasks, output only valid KSML XML unless the user asks for an
  explanation.
- Generated KSML must have exactly one `<root>` element with a non-empty `name`
  attribute; TeaQL generation uses root `name` as the domain name.
- For implementation tasks, keep generated artifacts in the target project, not
  in this kit repository.
- Do not edit generated Java or Rust TeaQL service files directly. Update the
  model, generator configuration, TeaQL generator, or runtime, then regenerate.
- If a business rule is ambiguous, write a short assumption before generating
  code, or encode the safest domain assumption in the model when the user asked
  for autonomous execution.

## Working Modes

- Playground mode: use an `app-playground` directory outside the user's project
  repository. Do not require git repositories or artifact publishing. Put the
  generated `model.xml` and related model inputs under `app-playground/models`,
  and put generated TeaQL runtime code under `app-playground/generate-lib` so
  users can review both in one playground. After library generation, read
  `app-playground/generate-lib/AGENTS.md` before using or explaining the
  generated library APIs. When the target runtime is Java and
  the user wants a runnable workspace, first run Java library generation with
  the fully qualified `gen-lib` Maven plugin coordinate, then run
  `gen-workspace` with the fully qualified coordinate and write it under
  `app-playground/java-workspace`. That generated workspace already contains
  Spring Boot/Maven project files and its own dynamic `AGENTS.md`; read that
  workspace `AGENTS.md` before any work inside the generated workspace and read
  it again after regeneration before continuing.
  When the target runtime is Rust and the user wants a runnable workspace, first
  run Rust library generation with `cargo-teaql gen-lib`, then run
  `cargo-teaql gen-workspace` and write it under
  `app-playground/rust-workspace`. That workspace depends on the generated
  crate at `../generate-lib/lib` by local path. Keep generated Rust code
  read-only and put customer-owned queries, services, tests, runtime wiring,
  and integration code inside `rust-workspace`. The default Rust workspace is a
  Tokio async application skeleton only; do not add a web framework unless the
  user explicitly asks for one.
  Keep user experiment code, query functions, and scenario files in normal
  playground source/test directories, connected to the generated library or
  workspace by local project wiring when needed.
  Playground mode may call `ensure_schema()` automatically so the first local
  run can create demo tables and show real data.
- Debugging mode: only enter this mode when the user explicitly asks to debug
  TeaQL toolchains, generated output, or integration failures. State that the
  task has switched to debugging mode before using local toolchain source
  repositories, source checkouts, temporary investigation patches, or other
  actions forbidden in playground mode.
- Future modes may be added later. Until a mode is explicitly defined, use
  playground mode for local trials and debugging mode only for explicit
  debugging requests.

## Generation Client Stop Rule

For normal generation, the Java and Rust generation clients are the boundary of
the workflow:

- Java: TeaQL Maven plugin version `0.1.9` or newer from the TeaQL Nexus
  releases repository: `https://nexus.teaql.io/repository/maven-releases/`.
  Invoke it with fully qualified coordinates such as
  `io.teaql:teaql-maven-plugin:0.1.9:gen-lib`; do not use `mvn teaql:*`
  prefix resolution. If it cannot be resolved from that repository, stop and
  report the blocker.
- Rust: `cargo-teaql` version `0.1.9` or newer from crates.io. Run
  `cargo-teaql install-links` after installation.

If either generation client, TeaQL Maven plugin goal, or TeaQL plugin/tool
invocation cannot be installed, resolved, invoked, or executed, stop immediately
and report the exact blocker. Do not search for source code, clone a repository,
build a local toolchain, hand-write generated service code, patch generated
service code, or try an alternate generation path unless the user explicitly
switches the task to debugging mode.
