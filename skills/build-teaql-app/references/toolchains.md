# TeaQL Toolchains

Load this reference only after the first complete model has been written and
saved. Use the client requirements before evaluation; use the generation
sections only after evaluation reaches zero errors.

## Required Clients

- Rust: `cargo-teaql` exactly `2.0.12` from crates.io.
- Java: `io.teaql:teaql-maven-plugin:1.1.1` or newer from
  `https://nexus.teaql.io/repository/maven-releases/`.

Verify or refresh before every new generation run:

```bash
cargo install cargo-teaql --version 2.0.12 --force
cargo-teaql --version
cargo-teaql install-links
```

Stop if the resolved version is wrong or a client cannot be installed or
invoked. Do not clone toolchain source, hand-build generated outputs, or use an
older cached client as a fallback. The built-in Generation Service credential
supports normal use; do not search for an additional API key.

## Supported language targets

TeaQL supports seven language families. Ask the Generation Service for its
current target list and use only a returned target name. The currently
supported core and editable application targets include:

| Language | Core library | Editable application |
| --- | --- | --- |
| Java | `java-lib-core` | `java-web-spring-boot` |
| Rust | `rust-lib-core` | `rust-app-console` |
| Go | `golang-lib-core` | `golang-app-console`, `golang-web-gin` |
| Swift | `swift-lib-core` | — (embed the generated package in an iOS/macOS application) |
| Python | `python-lib-core` | `python-web-fastapi` |
| C#/.NET | `dotnet-lib-core` | `dotnet-web-aspnet` |
| TypeScript | `typescript-lib-core` | `typescript-web-hono` |

Kotlin/JVM applications use `java-lib-core` and the TeaQL Java runtime. Kotlin
is a supported application language through JVM interoperability, but there is
no separate `kotlin-*` generation target. Compile and test it with the target
Gradle or Maven build. The
[Compose Desktop vending-machine example](https://github.com/teaql/teaql-java-app-examples/tree/main/002-vending-machine-compose-desktop)
is the reference shape.

## Swift

Swift is a current generation target. Its verified scope is:

- generated Swift entities, requests, expressions, and user context from the
  same KSML model used by the server;
- a local-first SQLite runtime for iOS and macOS applications;
- a TFP federation client, but no Swift federation server;
- language-native purpose/comment, audited writes, optimistic locking, hard
  limits, transactions, and verification guidance;
- interoperability with TeaQL servers implemented in any of the other supported
  backend languages, while trusted identity, tenant, permission, and purpose
  policy remain server-controlled.

Generate the package with the exact advertised target:

```bash
cargo teaql --input /path/to/models/model.xml swift-lib-core \
  --output /path/to/app-playground/swift-lib-core \
  --cwd /path/to/app-playground
```

Read the generated package guide and current `swift-assist-*` output before
writing application code. Verify the generated package and application
integration with `swift build` and `swift test`. Do not claim a Swift TFP
server or a separate generated editable application workspace.

C++, Dart, Ruby, and other unlisted smaller language ecosystems are not
supported targets. Do not interpret the seven-language list or Kotlin/JVM
interoperability as universal language support.

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
mvn io.teaql:teaql-maven-plugin:1.1.1:eval \
  -Dteaql.input=/path/to/models/model.xml
```

Generate the domain library:

```bash
mvn io.teaql:teaql-maven-plugin:1.1.1:generate -Dservice=java-lib-core \
  -Dteaql.input=/path/to/models/model.xml \
  -Dteaql.output=/path/to/app-playground/java-lib-core
```

For a runnable Spring Boot result, generate the editable workspace second:

```bash
mvn io.teaql:teaql-maven-plugin:1.1.1:generate \
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

## Go, Python, C#/.NET, and TypeScript

Use the Generation Service client available in the target repository, passing
the saved model and one exact target from the table above. Before adding
business logic, read the generated workspace `AGENTS.md`, its README, and the
current object/action assist. The generated API—not a translated Java or Rust
example—is authoritative.

Run the native verification appropriate to the generated workspace:

```text
Go:         go test ./...
Python:     python -m pytest
C#/.NET:    dotnet build -p:UseSharedCompilation=false; dotnet test -p:UseSharedCompilation=false
TypeScript: use Node.js 22, install from the lockfile, then run the generated package's test and build scripts
```

Do not silently skip a missing compiler, runtime, database driver, test script,
or generated assist surface. Report it as a concrete verification gap.
