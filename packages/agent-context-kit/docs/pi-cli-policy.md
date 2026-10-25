# Directory protection in the ordinary Pi command

`scripts/pi-context-cli.mjs` runs native Pi **1.4.0** with the shared marker policy,
retaining the TUI, model/auth configuration and print/JSON/RPC modes. It is separate
from ordinary lifecycle installation and must be wired into the host's `pi` launcher.

```sh
node --experimental-strip-types /absolute/package/scripts/pi-context-cli.mjs
```

Use an extracted package outside `node_modules` with Node 22.19+ and a resolvable
matching Pi SDK. The server deployment links its `node_modules` to managed Pi
1.4.0 and checks that version in the shell launcher. Keep the launcher/package
host-owned. Guarded writes deny `.pi` and this installed package when in scope.
The existing lifecycle package can remain registered: native extension discovery
is disabled and lifecycle handling is loaded inline, avoiding duplicate adapters.

## Behavior

- Start with `cd project; pi`. The policy root is the startup directory. Use a fresh
  session when adopting markers; previously exposed transcript content is not erased.
  Restart Pi to change directory scope.
- `read`, `grep`, `find`, `ls` use shared policy tools; excluded subtrees are pruned
  before enumeration. Markers are checked afresh.
- `write`/`edit` retain native input schemas and permit application-source changes.
  Excluded directories/files and control files are protected. Parent directories
  must exist. Edits require unique exact non-overlapping matches applied together.
  No source previews/diffs are returned. Symlink mutations remain prohibited.
- Arbitrary Shell, user `!` commands, MCP, codemode, delegation and external tools
  are disabled. Fixed host capabilities can be explicitly registered as described
  below; arbitrary command execution is never enabled by a project or marker.
- Native context-file, Skill/template/theme and extension discovery are disabled
  before loading. Root guidance is reloaded through the checked bounded loader as
  project data before each provider request. Explicit CLI `@files`, resource paths
  and system-prompt overrides are rejected to prevent alternate-loader bypasses.
  Use guarded reads for project documents, Skills and images.
- Package/auth/configuration subcommands remain native host operations. The old
  `pi-context` command can remain available, but ordinary `pi` no longer needs it.

This controls model-context entry points, not OS access. Direct native binaries,
other processes/host APIs, races, hard links, content copies and pre-read user
messages remain outside the v1 guarantee. Do not re-enable arbitrary extensions
or Shell and continue claiming the same boundary.

## Tests

### Optional host capabilities

`<agentDir>/context-kit-host-tools.json` may explicitly list absolute module paths
in `modules`, with `version: 1`. Modules must reside under the protected agent
directory and export `createTools({projectRoot, agentDir})`. Their tool definitions
are added to the controlled catalog. They cannot replace file tools or register
`bash`/`shell`/`powershell`. This is trusted host code, never project discovery.
Missing configuration adds no capabilities; malformed configuration blocks startup.

The optional [TeaQL Rust module](../../../integrations/pi-teaql/README.md) provides
evaluation, progressive Assist, gated library generation and fixed build/test
targets. It lives outside the generic independently publishable package. Only
projects explicitly approved in its host configuration receive these tools.

Direct `excluded`/`outOfScope` file-tool results preserve their status and include
`blocked: true`, `retryable: false`, `code: "CONTEXT_ACCESS_DENIED"` and host-authored
English feedback. A Pi `tool_result` hook sets the actual `isError` flag; returning
an `isError` property from an executor alone is not the supported Pi mechanism.
Marker guidance stays separately identified as project data and is retained on
the first denial. Later attempts within the same canonical directory (including
aliases and different tools) include `previouslyBlocked` and a scope counter, omit
repeated guidance and instruct the model to use permitted alternatives.

A bounded request-local host-policy reminder records denied scopes. It is never
an authorization cache: every tool call rechecks markers, and reminders are removed
when the host policy allows the scope. Broad searches which skip excluded subtrees
remain successful and do not count as direct retries. Returned file text cannot
create denial controls. This feedback reduces ambiguous retries but cannot guarantee
that every model will never attempt another call; all such calls remain blocked.
The task is not automatically terminated after two denials.

The same supported Pi error flag now applies to ordinary file-operation failures,
not only directory exclusions. A bounded metadata/header inspection distinguishes
`UNSUPPORTED_BINARY`, `FILE_TOO_LARGE`, `FILE_NOT_FOUND`, `UNSUPPORTED_FILE_TYPE`
and `READ_ACCESS_DENIED`. It keeps images supported, does not load oversized bodies,
and never returns binary header bytes. Other read/invalid-input errors also have
`retryable: false`. These reminders are scoped to the file/request, not its whole
directory, and are cleared when the file changes or a corrected request succeeds.
Use the registered build/test tools for diagnostics instead of reading executables.

The integration test runs native Pi `main` in a separate process with a real local
faux provider, using the same flags and inline policy extension. It verifies denied
generated reads, pruned searches, permitted writes/edits, disabled Shell and absent
native SYSTEM/APPEND_SYSTEM context. Root `npm ci` and `npm run check` include this
test and the existing Pi/OpenCode regressions. No paid provider is required.

## Completion verification after mutations

When the host registers both `app_build` and `app_test`, successful controlled
`write`/`edit` calls invalidate previous verification. Before a completed run
settles, the host invokes any missing fixed checks and appends their actual
policy-filtered results as a visible `agent-context-kit-completion-report-v1`
message. Pi then continues automatically so the model can report results or
make a localized repair. A promise in assistant text never counts as a check.
Calls already attempted for the current revision are not repeated; failures
remain failures and may be reported as concrete blockers. Zero executed tests
do not establish coverage. A later edit invalidates both checks again.

The host allows at most three automatic verification rounds per submitted user
request. At the limit it displays `VERIFICATION_INCOMPLETE`, including the
missing checks, rather than continuing forever or claiming success. User
cancellation and provider errors do not trigger automatic verification.
Read-only work and failed mutations do not create verification obligations.
State is stored in host custom session entries and restored from the active
branch. These checks use only registered capabilities; no shell is enabled.

## Recover an old conversation that repeats without tools

The protected native Pi entry point detects three similar action-promise replies
without an intervening tool call/result in a bounded recent window. Factual
repeated answers and explicit blocker codes do not qualify. This is a heuristic
for the observed reply loop, not semantic detection of every ignored task.

When resuming such a session, it appends a visible `CONTEXT_RECOVERED` host message
before the next provider request. A loop detected at turn end can also continue
automatically. The outgoing view preserves all system/tool instructions, current
active lifecycle/policy messages, all user instructions preceding the marker,
and the marker plus all subsequent messages and tool results. Project files are
still freshly policy-checked. Old assistant promises and stale tool diagnostics
before the marker are omitted from this view; the on-disk transcript is unchanged
apart from appended entries. The anchor is restored from the selected session
branch, so restarting does not require `/new` or reintroduce the omitted loop.

There is at most one automatic recovery per submitted user request. A renewed
promise-only stop with no tool attempt after recovery emits
`STALLED_NO_TOOL_PROGRESS` rather than silently retrying. User cancellation,
provider errors and a completion guard's existing continuation do not trigger
another recovery. No tool, write root or read permission is added by recovery.
Already running Pi processes must load the updated extension before using this
behavior; updating files does not hot-replace imported code.
