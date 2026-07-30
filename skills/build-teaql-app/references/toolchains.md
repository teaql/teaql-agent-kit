# TeaQL Toolchains

Load this reference only after the first complete model has been written and
saved. Use the client requirements before evaluation; use the generation
sections only after evaluation reaches zero errors.

## Required Clients

- Rust: `cargo-teaql` exactly `2.0.10` from crates.io.
- Java: `io.teaql:teaql-maven-plugin:1.1.0` or newer from
  `https://nexus.teaql.io/repository/maven-releases/`.

Verify or refresh before every new generation run:

```bash
cargo install cargo-teaql --version 2.0.10 --force
cargo-teaql --version
cargo-teaql install-links
```

Stop if the resolved version is wrong or a client cannot be installed or
invoked. Do not clone toolchain source, hand-build generated outputs, or use an
older cached client as a fallback. The built-in Generation Service credential
supports normal use; do not search for an additional API key.

## Rust

Every model-derived command, including dynamic assist, must use
`cargo teaql --input <model> ...`.

Generate the read-only library first:

```bash
cargo teaql --input /path/to/models/model.xml rust-lib-core \
  --output /path/to/app-playground/rust-lib-core \
  --cwd /path/to/app-playground
```

For a runnable result, generate the editable console application second:

```bash
cargo teaql --input /path/to/models/model.xml rust-app-console \
  --output /path/to/app-playground/rust-app-console \
  --cwd /path/to/app-playground
```

Read `rust-app-console/AGENTS.md`, then run current help and object-specific
`rust-assist-*` commands with the same `--input` model before writing business
code. The library may not contain `AGENTS.md`; generated source is an
assist-incomplete fallback only.

Verify from the editable application:

```bash
cargo check
cargo test
```

## Java

Never use Maven prefix commands such as `mvn teaql:generate`. Invoke the fully
qualified plugin and version. Ensure the TeaQL Nexus releases URL is available
as both a Maven repository and plugin repository.

Evaluate:

```bash
mvn io.teaql:teaql-maven-plugin:1.1.0:eval \
  -Dteaql.input=/path/to/models/model.xml
```

Generate the domain library:

```bash
mvn io.teaql:teaql-maven-plugin:1.1.0:generate -Dservice=java-lib-core \
  -Dteaql.input=/path/to/models/model.xml \
  -Dteaql.output=/path/to/app-playground/java-lib-core
```

For a runnable Spring Boot result, generate the editable workspace second:

```bash
mvn io.teaql:teaql-maven-plugin:1.1.0:generate \
  -Dservice=java-web-spring-boot \
  -Dteaql.input=/path/to/models/model.xml \
  -Dteaql.workspaceDir=/path/to/app-playground/java-web-spring-boot
```

Read the generated workspace `AGENTS.md` before business code. Generated
library classes remain read-only; workspace-owned controllers, services,
configuration, and tests are editable.

Verify from the generated workspace:

```bash
mvn clean compile
mvn test
```
