# Spring Boot Large Single Repo Reference

Use this playbook when a user wants a large TeaQL Spring Boot reference project
in one repository while preserving boundaries that could later become multiple
repositories.

This playbook is Spring Boot specific. Future Rust references should keep the
same model, custom context, app, shared, and AI-task boundary language where
practical, but should use a separate Rust-specific playbook.

## Purpose

The reference project demonstrates how to keep TeaQL semantic modeling,
generated code, custom context boundaries, application entrypoints, shared
libraries, and AI coding tasks separate in a single repository.

The single repository is for coordinated review and examples. Each top-level
`generated-*`, `custom-context-*`, `app-*`, and `shared-*` directory is
intentionally shaped as a future standalone repository boundary.

## Reference Name

Use this repository name for the Spring Boot reference:

```text
teaql-serviceops-spring-boot
```

Reserve the parallel name below for a future Rust reference:

```text
teaql-serviceops-rust
```

## Repository Shape

Recommended top-level layout:

```text
teaql-serviceops-spring-boot/
  README.md

  docs/
    design.md
    model-organization.md
    custom-context-boundaries.md
    data-scope.md
    ai-coding-guardrails.md
    clean-room-policy.md

  models/
    main.xml
    tenant/
    identity/
    customer/
    servicecatalog/
    operations/
    employee/
    finance/
    asset/
    compliance/
    audit/
    view/

  generated-serviceops-lib/
  generated-serviceops-workspace/

  custom-context-tenant/
  custom-context-customer/
  custom-context-assigned-admin/
  custom-context-platform-admin/
  custom-context-system/

  app-tenant-api/
  app-customer-portal-api/
  app-assigned-admin-console-api/
  app-platform-admin-api/
  app-system-jobs/

  shared-web-response/
  shared-common-util/
  shared-test-fixtures/

  docs-ai-tasks/
    01-create-service-order.md
    02-assign-route-and-time-slot.md
    03-record-fulfillment-event.md
    04-submit-worked-hours.md
    05-generate-invoice-after-fulfillment.md
    06-customer-view-own-order.md
    07-support-view-assigned-tenant-ticket.md
    08-platform-scan-overdue-invoices.md

  build.gradle
  settings.gradle
```

## Naming Rules

Use flat top-level directories so customers can see how the single repository
could split into multiple repositories later.

```text
generated-<artifact>
custom-context-<actor>
app-<entrypoint>
shared-<library>
```

Examples:

- `generated-serviceops-lib`: generated TeaQL library.
- `generated-serviceops-workspace`: generated runnable Spring Boot workspace.
- `custom-context-tenant`: custom tenant context, data scope, and default TeaQL
  constraints.
- `custom-context-customer`: custom customer context, customer data scope, and portal
  access constraints.
- `custom-context-assigned-admin`: custom delegated-admin context, delegated tenant
  scope, and assignment policy.
- `custom-context-platform-admin`: custom platform-admin context, cross-tenant
  permission checks, and audit policy.
- `custom-context-system`: custom system job context, job scope, and scheduled-task
  constraints.
- `app-tenant-api`: tenant-facing API.
- `app-customer-portal-api`: customer-facing API.
- `app-assigned-admin-console-api`: delegated support or admin console API.
- `app-platform-admin-api`: platform administrator API.
- `app-system-jobs`: scheduled and asynchronous system jobs.

## Model Directory

`models/` is the only semantic source of truth. Use KSML XML files, not Java
model classes, as the source for TeaQL generation.

`models/main.xml` is the only generation entrypoint. It owns the complete root
metadata, including `alias_model_name`, `english_name`, `chinese_name`, `name`,
`org`, `data_service`, and `_module_key`.

Split model files by stable business subdomain:

- `tenant/`: tenant organizations, tenant lifecycle, tenant plan, tenant
  ownership boundaries.
- `identity/`: accounts, roles, permissions, login identities, actor mappings.
- `customer/`: customer accounts, contacts, customer-owned assets.
- `servicecatalog/`: service products, service types, pricing catalog inputs.
- `operations/`: service orders, assignments, routes, time slots, fulfillment
  events.
- `employee/`: tenant employees, workers, dispatchers, supervisors.
- `finance/`: invoices, billing runs, payment status, charge lines.
- `asset/`: assets, devices, locations, maintenance targets.
- `compliance/`: checklists, inspection records, compliance states.
- `audit/`: audit event concepts that are part of the business model.
- `view/`: view-facing model concepts when the domain needs stable view objects.

Keep common constants in a clearly named basic or subdomain file. Cross-domain
constants may live under `models/basic/` if the project needs one. Process-local
constants should stay near their process domain.

Use `<_include file="..."/>` from `models/main.xml` to compose subdomain files.
Maintain include order explicitly: include referenced objects before objects
that reference them.

## Generated Code

TeaQL generation should distinguish generated service code from generated
editable scaffolding.

Generated TeaQL service code belongs under the generated service directories:

```text
generated-serviceops-lib/
generated-serviceops-workspace/
```

Treat generated TeaQL service code as read-only. If generated code is wrong,
fix `models/*.xml`, generator configuration, TeaQL generator behavior, or
custom context wiring, then regenerate. Do not present direct edits to
generated service files as deliverable project changes.

For Java generation, follow `playbooks/generate-with-toolchains.md`: use TeaQL
Maven plugin version `1.0.0` or newer from the TeaQL Nexus releases repository
and invoke the plugin with fully qualified coordinates, such as
`io.teaql:teaql-maven-plugin:1.0.0:gen-lib`.

Recommended Java generation targets for this reference:

| Target | Writes | Edit policy | Required guide |
| --- | --- | --- | --- |
| `java-lib` | `generated-serviceops-lib/` | Generated TeaQL service code is read-only. | Generated workspace or library guide when available. |
| `java-workspace` | `generated-serviceops-workspace/` | Generated workspace code follows its generated guide. | `generated-serviceops-workspace/AGENTS.md` |
| `java-custom-context` | `custom-context-*` modules | Editable custom context scaffolding. Regenerate carefully and preserve customer changes. | Each `custom-context-*` module must contain `AGENTS.md`. |
| `java-api-implementation` | `app-*` modules | Editable API/job scaffolding. Regenerate carefully and preserve customer changes. | Each `app-*` module must contain `AGENTS.md`. |

`java-custom-context` and `java-api-implementation` are not replacements for
the semantic model or generated TeaQL service code. They are scaffold targets
that create customer-owned implementation surfaces with local agent rules.
Agents must read the local `AGENTS.md` before editing any generated custom
context or API implementation module.

If a requested generation target is not available in the installed TeaQL Maven
plugin, stop and report that blocker. Do not hand-build a replacement generator
or invent generated service code unless the user explicitly switches to
debugging or generator-development work.

## Custom Context Boundaries

`custom-context-*` modules are the customization points for TeaQL context. They
adapt the generated TeaQL model to a specific actor or execution scenario by
defining custom context objects, data scopes, default query constraints,
permission checks, audit behavior, and Spring Boot wiring.

They are not general application service modules. Application modules must use
the appropriate custom context module; they must not create naked TeaQL
contexts or global queries directly.

| Custom context module | Actor | Data scope | Typical app | Cross tenant | Audit |
| --- | --- | --- | --- | --- | --- |
| `custom-context-tenant` | Tenant employee or tenant system | Current tenant | `app-tenant-api` | No | Business audit |
| `custom-context-customer` | End customer | Current customer account | `app-customer-portal-api` | No | Customer access audit |
| `custom-context-assigned-admin` | Assigned support/admin user | Authorized tenants, tickets, or assignments | `app-assigned-admin-console-api` | Limited | Strong audit |
| `custom-context-platform-admin` | Platform administrator | Platform permission scope | `app-platform-admin-api` | Yes | Strong audit |
| `custom-context-system` | Scheduled job or async worker | Explicit job scope | `app-system-jobs` | Controlled by job config | Job audit |

Recommended Spring Boot custom context classes:

```text
custom-context-tenant/
  AGENTS.md
  src/main/java/com/teaql/serviceops/context/tenant/
    TenantContextFactory.java
    TenantContext.java
    TenantDataScope.java
    TenantContextConfig.java

custom-context-customer/
  AGENTS.md
  src/main/java/com/teaql/serviceops/context/customer/
    CustomerContextFactory.java
    CustomerContext.java
    CustomerDataScope.java
    CustomerContextConfig.java

custom-context-assigned-admin/
  AGENTS.md
  src/main/java/com/teaql/serviceops/context/admin/
    AssignedAdminContextFactory.java
    AssignedAdminContext.java
    DelegatedTenantScope.java
    AdminAssignmentPolicy.java
    AssignedAdminContextConfig.java

custom-context-platform-admin/
  AGENTS.md
  src/main/java/com/teaql/serviceops/context/platform/
    PlatformAdminContextFactory.java
    PlatformAdminContext.java
    PlatformAdminAuditPolicy.java
    PlatformAdminContextConfig.java

custom-context-system/
  AGENTS.md
  src/main/java/com/teaql/serviceops/context/system/
    SystemContextFactory.java
    SystemContext.java
    SystemJobScope.java
    SystemContextConfig.java
```

Custom context modules should expose typed context and data scope objects.
Fixed business, tenant, customer, delegated-admin, platform, and job
constraints belong around TeaQL Q API queries as typed request constraints.

The most important responsibility of each `custom-context-*` module is to
provide a scenario-specific context surface. For example,
`custom-context-customer` should make it easy to obtain a `CustomerContext` and
`CustomerDataScope`, while making it hard for app code to accidentally run a
platform-wide query.

## Custom Context Implementation Pattern

The `java-custom-context` target should scaffold each `custom-context-*` module
with a local `AGENTS.md` and the same implementation pattern:

```text
<Actor>ContextFactory
<Actor>Context
<Actor>DataScope
<Actor>ContextConfig
```

Responsibilities:

- `<Actor>ContextFactory`: builds the custom context from request, auth,
  assignment, platform session, or job metadata.
- `<Actor>Context`: wraps the TeaQL user context and carries actor identity,
  data scope, audit metadata, and execution scenario.
- `<Actor>DataScope`: applies fixed visibility constraints to generated Q API
  queries. It does not execute queries.
- `<Actor>ContextConfig`: provides Spring Boot configuration, beans, limits,
  feature flags, and audit policy wiring.

Rules for generated `custom-context-*` scaffolding:

- Keep the module customer-editable, but keep its local `AGENTS.md` as the
  implementation authority.
- Do not put application use-case orchestration in `custom-context-*`.
- Do not let app code construct tenant, customer, delegated-admin, platform, or
  system scopes by hand.
- Apply fixed business and security constraints before dynamic JSON search.
- Keep custom context objects explicit enough that tests can prove the data
  scope.

## Application Boundaries

Application modules are entrypoints. Each app should depend only on the custom
context module that matches its actor and use case, plus generated code and
shared libraries.

Recommended app directories:

```text
app-tenant-api/
  AGENTS.md
  src/main/java/com/teaql/serviceops/app/tenant/
    controller/
    service/
    helper/
    domain/
    command/
    response/

app-customer-portal-api/
  AGENTS.md
  src/main/java/com/teaql/serviceops/app/customer/
    controller/
    service/
    helper/
    domain/
    command/
    response/

app-assigned-admin-console-api/
  AGENTS.md
  src/main/java/com/teaql/serviceops/app/admin/
    controller/
    service/
    helper/
    domain/
    command/
    response/

app-platform-admin-api/
  AGENTS.md
  src/main/java/com/teaql/serviceops/app/platform/
    controller/
    service/
    helper/
    domain/
    command/
    response/

app-system-jobs/
  AGENTS.md
  src/main/java/com/teaql/serviceops/app/system/
    job/
    service/
    helper/
    domain/
```

Hard rule:

> App modules must not directly create naked `UserContext` objects or naked
> TeaQL query contexts. Each entrypoint must select the appropriate custom
> context module and use that module's context and data scope for Q API queries
> and updates.

## API Implementation Pattern

The `java-api-implementation` target should scaffold each `app-*` module with a
local `AGENTS.md` and a consistent Spring Boot API pattern:

```text
controller/  HTTP endpoints, request parsing, response status.
service/     Use-case orchestration and Q API query/update pipeline.
command/     Input command and search DTOs.
response/    Output DTOs and page responses.
helper/      Small mapping or query helpers, with no hidden permission rules.
domain/      App-owned concepts only, not replacements for generated entities.
```

Required flow:

```text
Controller
  -> parse command or query request
  -> obtain custom context from the matching <Actor>ContextFactory
  -> call application service
  -> service starts from generated Q API
  -> apply custom context data scope
  -> apply dynamic query/search when needed
  -> order, page, select, execute
  -> map to response DTO
```

Rules for generated `app-*` scaffolding:

- Controllers must not construct TeaQL Q API queries directly.
- Controllers must not create naked `UserContext` or TeaQL query contexts.
- Services must not skip the selected custom context data scope.
- Services must not use `custom-context-platform-admin` for tenant or customer
  endpoints.
- Helpers must not hide permission filters or tenant/customer constraints.
- Response DTOs should expose intentional fields, not generated entities by
  default.
- Normal application queries should use the generated Q API, not raw SQL.

## Dependency Rules

Represent boundaries explicitly in `settings.gradle` and Gradle dependencies.

`settings.gradle` should include flat modules:

```gradle
include "generated-serviceops-lib"
include "generated-serviceops-workspace"

include "custom-context-tenant"
include "custom-context-customer"
include "custom-context-assigned-admin"
include "custom-context-platform-admin"
include "custom-context-system"

include "app-tenant-api"
include "app-customer-portal-api"
include "app-assigned-admin-console-api"
include "app-platform-admin-api"
include "app-system-jobs"

include "shared-web-response"
include "shared-common-util"
include "shared-test-fixtures"
```

Use these dependency directions:

```text
app-*       -> custom-context-* + shared-* + generated-serviceops-lib
custom-context-*   -> generated-serviceops-lib + shared-*
shared-*    -> no dependency on app-* or custom-context-*
models/     -> no code dependency; generation input only
generated-* -> generated service code is read-only
```

## Query And Update Rules

When writing customer code, playground code, examples, tests, controllers, or
services:

- Start normal reads from the generated `Q` collection API for the target
  entity.
- Apply the custom context module's data scope before dynamic search.
- Use `findByJson` or `findWithJsonExpr` for dynamic Java/Spring Boot query
  criteria.
- Apply deterministic ordering, pagination, facets or aggregation, and field
  selection explicitly.
- Do not use raw SQL for normal TeaQL application queries.
- Do not bypass generated request types or mutate generated service internals.
- Use generated chainable `update<Field>(...)` methods for state changes when
  available, then persist through the normal TeaQL save surface.

Expected query order:

1. Start with the entity Q collection.
2. Apply hard-coded business and security filters from the selected custom
   context module.
3. Apply dynamic search from JSON when accepted by the API.
4. Apply deterministic ordering.
5. Apply pagination.
6. Apply facet or aggregation declarations when needed.
7. Apply field selection or projection when needed.
8. Execute the query.

## AI Task Documents

Use `docs-ai-tasks/` for AI coding task contracts. These files are not generic
requirements. They tell an agent which custom context module, data scope,
model areas, and query shape must be used.

Every AI task should include:

- Task name.
- Target `app-*`.
- Required custom context module.
- Allowed model areas.
- Data scope rule.
- Forbidden actions.
- Expected Q API query or update shape.
- Acceptance checks.

Example:

```md
# Customer View Own Order

Target app: app-customer-portal-api
Required custom context module: custom-context-customer

Allowed model areas:
- customer
- operations
- finance

Data scope:
- Only orders belonging to the current customer account are visible.

Forbidden:
- Do not use custom-context-platform-admin.
- Do not query without CustomerDataScope.
- Do not use raw SQL.
- Do not edit generated-serviceops-lib.

Expected query shape:
- Start from Q.serviceOrders()
- Apply CustomerDataScope
- Apply dynamic JSON search if present
- Order by create time descending
- Apply pagination
- Select response fields

Acceptance checks:
- Customer A cannot see Customer B orders.
- The app compiles.
- Relevant service tests cover the data scope rule.
```

## Customer Prompt Contract

Teach customers to include the same boundary information in every AI request.
At minimum, a request should state:

```text
Business goal:
Target app:
Required custom context module:
Data scope:
Allowed model areas:
Forbidden actions:
Are model changes allowed:
Expected Q API shape:
```

### Prompt: Create A Project

```md
Please create a TeaQL large single repo Spring Boot project.

Reference mode:
- Project name: teaql-serviceops-spring-boot
- Use models/ as the only KSML semantic source.
- Use generated-* for TeaQL generated code. Generated service code is read-only.
- Use custom-context-* for actor/use-case custom TeaQL context boundaries.
- Use app-* for Spring Boot API and job entrypoints.
- Use shared-* for reusable libraries.
- Use docs-ai-tasks/ for AI coding task contracts.
- Use the java-custom-context generation target for custom-context-* scaffolding when
  the installed TeaQL generator supports it.
- Use the java-api-implementation generation target for app-* scaffolding when
  the installed TeaQL generator supports it.
- Ensure every generated custom-context-* and app-* module has a local AGENTS.md.

Business domain:
[Describe the business domain here.]

Before writing application code, complete:
1. Produce models/main.xml and a multi-directory model candidate.
2. Explain tenant, customer, assigned-admin, platform-admin, and system custom
   context boundaries.
3. Explain which app-* uses which custom-context-* module.
4. Run the model review gate before TeaQL generation.
5. Generate or scaffold custom context and API implementation modules only
   after the model and context boundaries are reviewed.

Do not directly write controller/service code before the model and custom
context boundaries are reviewed.
Do not hand-edit generated-* TeaQL service code.
Before editing a custom-context-* or app-* module, read its local AGENTS.md.
```

### Prompt: Implement A Feature

```md
Please implement this feature in the existing TeaQL large single repo Spring
Boot project:

Feature:
[Describe the feature here.]

Required boundaries:
- Target app: [app-*]
- Required custom context module: [custom-context-*]
- Data scope: [scope rule]
- Allowed model areas: [areas]

Forbidden:
- Do not use an unrelated custom context module.
- Do not query without the custom context module data scope.
- Do not use raw SQL for normal TeaQL queries.
- Do not edit generated-* TeaQL service code.

First check:
1. Whether models/ already has the required objects and relationships.
2. Whether the required custom context module has the needed Context and
   DataScope.
3. Whether the target app already has a similar controller/service pattern.
4. Whether the target custom-context-* and app-* modules have local AGENTS.md files,
   and follow them before editing.

If the model is missing fields or relationships, update models/*.xml first and
state that regeneration is required.
```

### Prompt: Create An AI Task

```md
Please convert the following requirement into a docs-ai-tasks AI coding task.
Do not implement code.

Requirement:
[Describe the requirement here.]

The task document must include:
- Task name
- Target app-*
- Required custom context module
- Allowed model areas
- Data scope rule
- Forbidden actions
- Expected Q API query/update shape
- Acceptance checks
```

## Documentation Requirements

The reference should include these docs:

- `docs/design.md`: business and architecture overview.
- `docs/model-organization.md`: KSML model directory rules and include order.
- `docs/custom-context-boundaries.md`: custom context actor, scope, and audit
  boundaries.
- `docs/data-scope.md`: tenant, customer, assigned-admin, platform, and system
  data-scope rules.
- `docs/ai-coding-guardrails.md`: rules for agent work in the repository.
- `docs/clean-room-policy.md`: generated-code read-only and regeneration
  policy.

## Done

The reference is ready when:

- `models/` is the only semantic source and has a clear `main.xml` entrypoint.
- Generated TeaQL code is isolated under `generated-*`.
- `java-custom-context` scaffolding, when generated, creates `custom-context-*`
  modules with local `AGENTS.md` guides.
- `java-api-implementation` scaffolding, when generated, creates `app-*`
  modules with local `AGENTS.md` guides.
- Every app entrypoint has a matching custom context module boundary.
- Every `custom-context-*` module follows the custom context implementation pattern.
- Every `app-*` module follows the API implementation pattern.
- Dependency directions are explicit.
- `docs-ai-tasks/` examples identify target app, custom context module, data
  scope, forbidden actions, and expected Q API shape.
- The README teaches customers to use the prompt contract before asking an AI
  coding agent to implement features.
