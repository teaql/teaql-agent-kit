# Enterprise Repository Topology

Use this playbook for larger TeaQL programs where one model serves multiple
applications, multiple runtimes, or multiple teams.

## Repository Split

Large projects should avoid treating the model as an incidental file inside one
application repository. Use separate repositories for semantic ownership and
runtime delivery.

| Repository | Owns | Typical output |
| --- | --- | --- |
| Model repository | KSML model, model changelog, review rules, compatibility policy, generation config. | Versioned model releases. |
| Runtime repository | Generated Java or Rust TeaQL code, runtime integration, database provider wiring, smoke tests. | Versioned runtime artifacts. |
| Application repository | Product-specific service, UI, workflow, deployment, and customization code. | Deployable application. |

There may be one runtime repository or multiple runtime repositories. For
example, an enterprise can maintain a Java runtime for Spring Boot business
services and a Rust runtime for high-throughput native services from the same
model.

## Model Repository

The model repository should be the source of truth for business semantics.

Recommended contents:

- `model.xml` or a structured model directory.
- Model ownership and review rules.
- Model changelog and release notes.
- Compatibility policy for field, relationship, constant, and lifecycle changes.
- CI jobs for XML validity, KSML checklist validation, and code generation dry
  runs.
- Optional generated documentation for business and engineering review.

Model changes should go through normal enterprise review. Treat removals,
renames, relationship changes, tenant-boundary changes, and constant-code changes
as compatibility-sensitive.

## Runtime Repositories

Runtime repositories turn the model into usable code for core application
scenarios.

Recommended responsibilities:

- Pin a model repository version or commit.
- Run TeaQL code generation for the selected target runtime.
- Wire generated code to the runtime stack, database provider, auth context,
  tenant context, observability, and deployment conventions.
- Run compile checks, schema checks, smoke tests, and scenario tests.
- Publish versioned artifacts for applications to consume.

Use separate runtime repositories when different application families need
different runtime stacks, release cadence, or infrastructure wiring.

## Application Repositories

Application repositories should consume the appropriate runtime artifact instead
of regenerating or hand-editing generated domain code by default.

Applications can still own:

- User-facing workflows.
- API endpoints and UI integration.
- Product-specific orchestration.
- Domain behavior extensions that belong to that application boundary.
- Deployment configuration and environment-specific integration.

When an application needs a model change, open the change in the model
repository, release the updated runtime artifact, then update the application
dependency.

## CI/CD Flow

Recommended enterprise flow:

1. Submit a pull request to the model repository.
2. Validate KSML structure and modeling checklist.
3. Generate Java and/or Rust runtime code in CI.
4. Run runtime compile checks and compatibility tests.
5. Publish model release metadata.
6. Trigger runtime repository builds.
7. Publish versioned runtime artifacts.
8. Let application repositories upgrade runtime versions through their normal
   dependency and deployment process.

## Done

The topology is ready when the model repository can validate and release model
changes independently, runtime repositories can regenerate and publish artifacts
from pinned model versions, and applications can choose the runtime artifact that
matches their core scenario.
