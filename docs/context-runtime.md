# Context runtime workspace

This repository contains TeaQL workflow Skills and an independent generic runtime.
The workspace root is private; the runtime package retains its existing identity.

| Path | Responsibility |
| --- | --- |
| `skills/build-teaql-app/` | TeaQL model/evaluate/generate/Assist/application workflow |
| `tools/teaql_workspace.py` | Existing seven-language runtime-source verification |
| `packages/agent-context-kit/` | Generic lifecycle, exclusion policy, host adapters, controlled diagnostics and marker maintenance |
| `tests/context-runtime/` | Cross-boundary contracts using the actual TeaQL Skill |

## Develop

Node.js 22.19+ and Python 3 are needed for the full development check. Pi development
dependencies are pinned to 1.4.0 in the child package. OpenCode SDK contract and
bridge tests pin `@opencode/plugin` to 2.1.4 as a development dependency. These do not become
requirements for users who only install the ordinary TeaQL Skill.

```sh
npm ci
npm run check
npm run example:context-markers
```

`npm run check` runs the package typecheck and Node tests, the root Skill/parser
contract, Python runtime-source tests, and Python Hermes adapter tests. No TeaQL
network service, remote model credentials or AMD deployment is involved. The root
`package-lock.json` is authoritative; the imported child lockfile was consolidated
into it without changing the imported dependency versions.

For focused work:

```sh
npm run check:context
npm run test:contracts
npm run test:python
```

## Install and publish the child package

The package remains `@teaql/agent-context-kit` at version 0.5.0 with its existing
public exports, CLI name, package-local host manifests, examples and tests.
The migration is published in this Git repository; no new npm registry version
has been released.

To create the child tarball from the workspace root:

```sh
npm pack --workspace @teaql/agent-context-kit
```

The child prepack builds the dependency-free JavaScript marker CLI and command
hook runtimes. The
root workspace is private and is not the publishable package. Publish explicitly
from the child package only when a release is authorized; this migration performs
no publish operation.

For a local Pi extension installation, point Pi at the absolute child directory:

```sh
pi install /absolute/path/to/teaql-agent-kit/packages/agent-context-kit
```

This enables the ordinary lifecycle adapter. The dedicated read-policy harness is
a separate SDK entry point; see the child
[Pi context-policy guide](../packages/agent-context-kit/docs/pi-context-policy.md).
Other host manifests are also rooted in the child directory. Do not substitute the
repository root for their package root. See the [installation guide](../packages/agent-context-kit/docs/installation.md)
for checkout/tarball installs, host-specific entry points and update behavior.
The root Codex and Claude marketplaces select `./packages/agent-context-kit`;
their package-local catalogs select `./`. Package exports keep their names.

The existing Skill command remains:

```sh
npx skills add teaql/teaql-agent-kit --skill build-teaql-app
```

The generic package Skills remain with their package runtime. Do not copy only the
context-exclusion Skill folder and lose its relative runtime imports. Use the
packaged marker CLI or a trusted fixed build wrapper; see
[marker maintenance](../packages/agent-context-kit/docs/context-marker-maintenance.md).

## Licensing and import provenance

The repository root keeps its existing MIT license. The complete imported package
keeps its Apache-2.0 LICENSE and all bundled asset license files. The workspace
does not relabel those files under the root license.

The import includes 121 source working-tree files from `teaql/agent-context-kit`,
including the uncommitted phase-1–4 implementation. Source HEAD at import was
`1ad889a2b986bee7250e5373fd12c9912046a87a`. The original repository is now
archived with a migration notice; its Git history has not been rewritten or
imported into this repository. The source child lockfile is represented by the
root workspace lock. Copied file bytes were preserved at import; package metadata,
installation guides and entry points are maintained here after migration. Root
changes include workspace configuration/documentation, plugin catalogs and four
lifecycle-comment spellings in the TeaQL Skill.

## Integration boundary and next steps

The runtime now includes a shared default-deny write policy and controlled file
mutations, the protected native Pi CLI bootstrap, and an opt-in OpenCode V2 plugin.
See the [Pi CLI guide](../packages/agent-context-kit/docs/pi-cli-policy.md),
[file policy](../packages/agent-context-kit/docs/file-policy.md) and
[OpenCode guide](../packages/agent-context-kit/docs/opencode-context-policy.md).
Tests include the real published SDK bridge, not an installed OpenCode CLI/model
end-to-end run. The full TeaQL workflow limitations below still apply.

The Skill phase comments now match the strict V1 grammar, enforced by a root
contract test. This does not automatically load the Skill into a protected harness,
recognize phase-complete text as a trusted event, or activate lifecycle discard.

The dedicated Pi SDK policy session remains read-only with optional fixed build/test
commands. Native Pi adds checked write/edit and completion verification when both
host-approved `app_build` and `app_test` tools are registered. OpenCode strict mode
adds explicit write roots and controlled mutations, without the Pi completion hook.
These entry points disable automatic external Skill loading and arbitrary shell.

The optional [Pi TeaQL Rust integration](../integrations/pi-teaql/README.md) now
provides version-checked evaluation, progressive Assist, zero-error-gated library
regeneration, marker restoration and policy-filtered Rust diagnostics. It handles
saved single-file models and existing application workspaces. The generic package
does not automatically install these host-owned capabilities or implement a full
seven-language TeaQL workflow. Trusted Skill phase transitions, multi-file model
fingerprints and additional language diagnostic integrations remain separate work.

See the [feature activation matrix](agent-feature-activation.md) and
[actual t003 business repair](t003-business-repair-verification.md) for current
boundaries and recorded evidence. The real-model t003 run compiled and ran the
test command autonomously, but executed zero test cases and did not exercise a
database runtime. Token/context savings remain unmeasured. OpenCode has pinned
SDK/bridge evidence; an installed-server/model run is still unverified.
