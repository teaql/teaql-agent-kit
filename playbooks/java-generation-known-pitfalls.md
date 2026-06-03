# Java Generation Known Pitfalls

Read this playbook before starting any Java TeaQL project, runnable Java
workspace, or Spring Boot playground.

## Maven Plugin Resolution

Do not use Maven plugin prefix resolution for TeaQL generation.

Wrong:

```bash
mvn teaql:gen-lib
mvn teaql:gen-workspace
```

Maven may resolve the `teaql` prefix against Maven Central or the wrong plugin
group and fail with a message such as:

```text
Plugin org.apache.maven.plugins:teaql-maven-plugin not found in Maven Central
```

Use fully qualified Maven plugin coordinates and resolve TeaQL Maven plugin
version `0.1.10` or newer from:

```text
https://nexus.teaql.io/repository/maven-releases/
```

Maven must be able to use this URL for both dependency and plugin resolution.
Use the project's existing Maven settings or POM convention when one exists. If
the project has no convention, add the repository explicitly before generation,
for example:

```xml
<repositories>
  <repository>
    <id>teaql-releases</id>
    <url>https://nexus.teaql.io/repository/maven-releases/</url>
  </repository>
</repositories>

<pluginRepositories>
  <pluginRepository>
    <id>teaql-releases</id>
    <url>https://nexus.teaql.io/repository/maven-releases/</url>
  </pluginRepository>
</pluginRepositories>
```

Required command shape:

```bash
mvn io.teaql:teaql-maven-plugin:0.1.10:gen-lib \
  -Dteaql.input=app-playground/models/model.xml \
  -Dteaql.output=app-playground/generate-lib

mvn io.teaql:teaql-maven-plugin:0.1.10:gen-workspace \
  -Dteaql.input=app-playground/models/model.xml \
  -Dteaql.workspaceDir=app-playground/java-workspace
```

If Maven cannot resolve the plugin from the TeaQL Nexus releases repository, if
the plugin version is older than `0.1.10`, or if any TeaQL Maven plugin goal or
TeaQL plugin/tool invocation fails, stop immediately and report the exact
blocker. Do not try Maven Central freshness, local source builds, hand-built
workspace files, copied generated code, or alternate generation paths.

## Two-Step Java Workspace Generation

For a runnable Java/Spring Boot workspace, `gen-lib` and `gen-workspace` are both
required.

```text
model.xml -> gen-lib -> gen-workspace
  KSML      domain     Spring Boot workspace
```

`gen-lib` generates domain library code, including entity, `Q`, request, and
checker classes. `gen-workspace` generates the runnable Spring Boot project
skeleton, including project files, application properties, application entry
classes, `EnsureModelController`, and the generated workspace `AGENTS.md`.

When invoking Maven goals from the command line, use concrete paths for
`-Dteaql.input`, `-Dteaql.output`, and `-Dteaql.workspaceDir`. Do not pass
`${project.basedir}` or `${project.baseDir}` as a `-D` value. Those are POM
configuration expressions, not shell path variables; Maven will not reliably
interpolate them in user-supplied CLI properties, and `${project.baseDir}` is
not the valid Maven property spelling.

If the user asks for a Java project, runnable workspace, Spring Boot application,
or local Java playground, default to the full two-step pipeline. Only stop after
`gen-lib` when the user explicitly asks for library-only generation.

## Starter Version Consistency

The generated domain library and runnable workspace must use the same TeaQL
starter/runtime version.

Check both the domain library project and the generated workspace project for
the TeaQL version property, commonly:

```xml
<properties>
  <teaql.version>1.190-RELEASE</teaql.version>
</properties>
```

If `core/pom.xml`, `generate-lib` project files, or
`java-workspace/pom.xml`/workspace build files contain different TeaQL runtime
versions, align them before compiling or running. Prefer `1.190-RELEASE` or
newer for Spring Boot starter based workspaces.

If dependencies cannot be resolved, report the resolver failure and the missing
artifact/version. Do not hide the issue by editing generated service code.

## WebResponse Data Serialization

If an endpoint returns a correct record count but an empty `data` array, for
example:

```json
{"data":[],"recordCount":3}
```

check the TeaQL Spring Boot starter version first. TeaQL Spring Boot starter
versions before the `BaseEntitySerializer` fix can serialize `WebResponse.data`
incorrectly. Upgrade the starter/runtime version to `1.190-RELEASE` or newer and
keep the generated library and workspace versions consistent.

Verify with a real endpoint response after the application starts:

```bash
curl -s 'http://localhost:19987/school/list?page=1&size=20' | python3 -m json.tool
```

## Java Runtime Selection

Do not assume SDKMAN has been initialized in every shell or background process.
Before compiling or running a generated Java workspace, confirm Java is
available and is the expected version:

```bash
java -version
```

When SDKMAN is needed in an interactive shell:

```bash
source "$HOME/.sdkman/bin/sdkman-init.sh" && sdk use java 17.0.19-amzn
```

For background processes that do not inherit SDKMAN initialization, set
`JAVA_HOME` explicitly:

```bash
JAVA_HOME=/Users/openclaw-002/.sdkman/candidates/java/17.0.19-amzn \
  nohup mvn spring-boot:run > /tmp/teaql-app.log 2>&1 &
```

Use the actual local Java path for the machine. If Java cannot be selected or
executed, stop and report that blocker instead of continuing with an unknown
runtime.

## Port Conflicts

If the Spring Boot application fails with `Address already in use`, identify and
stop the process using the selected port, or choose a different port when that
is safer for the user's environment.

Common local playground command:

```bash
lsof -ti :19987 | xargs kill -9
```

Use destructive process termination carefully. If the port belongs to an
unrelated user process, report the conflict instead of killing it blindly.

## Curl JSON In Sandboxed Shells

Inline JSON can be intercepted or mangled by shell/sandbox parsing. Prefer a
temporary JSON file for POST/PUT requests:

```bash
printf '%s\n' '{"name":"Test","code":"TST","schoolTypeId":1001,"platformId":1}' > /tmp/teaql-request.json
curl -s -X POST http://localhost:19987/school/register \
  -H "Content-Type: application/json" \
  -d @/tmp/teaql-request.json | python3 -m json.tool
```

## TeaQL Count Results

TeaQL Java `count()` returns a request for numbers. Do not treat
`executeForList()` as an `int`.

Wrong:

```java
int count = request.count().executeForList();
```

Use `List<Number>` and inspect the first result when present:

```java
List<Number> counts = Q.schools().code().eq(code).count().executeForList(tql);
if (!counts.isEmpty() && counts.get(0).intValue() > 0) {
    // duplicate found
}
```

## Rebuild From A Clean Playground

If a previous playground directory has been removed, recreate the expected
layout and run the normal model-to-generation pipeline again:

```bash
mkdir -p app-playground/models app-playground/generate-lib app-playground/java-workspace
```

Then create or copy `model.xml`, run fully qualified `gen-lib`, run fully
qualified `gen-workspace` when a runnable app is needed, compile the workspace,
and add only customer-owned controllers, tests, or scenario code. Generated
TeaQL service code remains read-only.

## Quick Reference

| Category | Command |
| --- | --- |
| Generate Java library | `mvn io.teaql:teaql-maven-plugin:0.1.10:gen-lib -Dteaql.input=models/model.xml -Dteaql.output=generate-lib` |
| Generate Java workspace | `mvn io.teaql:teaql-maven-plugin:0.1.10:gen-workspace -Dteaql.input=models/model.xml -Dteaql.workspaceDir=java-workspace` |
| Install generated library | `cd core && mvn install -DskipTests` |
| Compile workspace | `cd java-workspace && mvn clean compile` |
| Run app | `mvn spring-boot:run -Dspring-boot.run.arguments="--server.port=19987"` |
| Test endpoint | `curl -d @/tmp/teaql-request.json http://localhost:19987/school/register` |
