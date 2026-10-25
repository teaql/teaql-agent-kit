# Dedicated OpenCode V2 context policy

This opt-in entry point is separate from ordinary lifecycle/ReadGuard installation.
It is the second host integration of the marker-aware controlled filesystem after
Pi, adding host-approved file writes through the shared [file policy](file-policy.md).
It targets the published OpenCode V2 plugin SDK **2.1.4**. V1 strict mode explicitly
fails; the ordinary V1 lifecycle adapter remains unchanged.

## Install

Use a fresh OpenCode V2 session in an isolated profile with this as its only plugin.
Existing history can already contain excluded content. Other plugins/host APIs are
trusted: later transforms/hooks can change tools or context. Do not combine this
plugin with the ordinary lifecycle plugin.

Create a host-owned `.opencode/plugins/agent-context-policy/index.ts`:

```ts
import { createOpenCodeContextPolicyPlugin } from "/absolute/path/to/teaql-agent-kit/packages/agent-context-kit/src/adapters/opencode-context.ts";

export default createOpenCodeContextPolicyPlugin({
  projectRoot: "/absolute/path/to/project",
  writeRoots: ["models", "app/src", "app/tests"],
  readOnlyPaths: ["generated", "policy/context-markers.json"],
  contextPaths: ["docs/api.md"],
  // Optional explicitly trusted lifecycle source; agent tools cannot modify it:
  lifecycleFile: ".agent-context-kit.md",
  commands: {
    build: { executable: "node", args: ["tools/build-with-diagnostics.mjs"] },
    test: { executable: "node", args: ["tools/test-with-diagnostics.mjs"] },
  },
});
```

TypeScript-capable installed loaders may import `@teaql/agent-context-kit/opencode-context`.
Install/pack the child package, never the private workspace root. The ordinary
default plugin does not enable strict mode. Create markers through authorized
[marker maintenance](context-marker-maintenance.md). Keep editable application code
and required guides outside exclusions. Trusted external generation may update
read-only generated directories; no generic generator/Shell is exposed here.
Full TeaQL evaluate/generate/Assist integration remains separate work.

When using the `plugins` configuration array instead of auto-discovery, point it
at the plugin directory, not at the TypeScript file. OpenCode V2 2.1.4 skips
configured file paths with a warning. Check that the strict plugin is active
before sending a task. Host-managed deployments should reject startup on plugin
load errors and deny native tool permissions as a fallback.

## Controlled surface

- Controlled tools explicitly set `options.codemode = false` so they remain
  directly visible after the native Code Mode executor is removed.
- A tool transform removes all native/MCP/delegation/codemode tools and registers
  only `context_read`, `context_grep`, `context_find`, `context_list`, `context_create`,
  `context_overwrite`, `context_edit`, `context_delete`, `context_move`, plus configured
  `context_build`/`context_test`. Transforms replay on catalog refresh. A pre-tool
  hook denies other tool IDs, including direct invocations.
- Read/search/list reuse `ContextFiles`, pruning excluded subtrees before enumeration
  and suppressing excluded descendant names, contents and counts. Reads return bounded
  UTF-8 text with one-based `offset`/`limit`; images/binary files are unsupported.
- Writes use `WorkspaceFiles`, validating inputs even for direct executor calls and
  returning no automatic previews/diffs. Parent directories must exist. Directory
  creation/recursive mutation is unsupported.
- Prompt admission clears native file attachments, selected Skills and agent mentions
  before resolution. Use checked `contextPaths` or tools for documents. Pasted/typed
  user text remains user data.
- Every `context`, `compaction`, `generate` and `title` request replaces the native
  assembled system prompt with a host prompt and reloads permitted project context
  as request-local user data. This deliberately replaces the native assistant prompt;
  any custom `systemPrompt` must come from trusted host configuration. The shared
  loader checks the root guide and explicit documentation afresh with Pi's size bounds.
- Optional trusted lifecycle context is checked before loading; unavailable/excluded
  lifecycle context blocks the request. State is isolated by session ID. Marker data
  and ordinary messages cannot discard blocks. The host transcript is unchanged.
- A shell creation hook rejects arbitrary shell outside tool selection too. Fixed
  tasks suppress raw stdout/stderr through the [controlled-task module](controlled-tasks.md).

Unlike Pi's loader, this adapter does not prevent internal host discovery from
reading native resources; it replaces outgoing automatic system context and prevents
native prompt attachment resolution. Host-side synthetic messages, direct provider
APIs, other plugins and previously populated sessions are outside this surface.
This is not an OS sandbox; races, hard links and external content copies are outside
the guarantee. Use an OS filesystem boundary when one is required.

## Verification

Root `npm ci` and `npm run check` cover policy/filesystem contracts, adapter tests
and type compatibility against pinned `@opencode/plugin@2.1.4` (development only).
An integration test runs registration, controlled IO and denial through that SDK's
real Promise/Effect bridge and checks native provider-message shape. The remaining
host registry in that test is a fixture, not the OpenCode application server.
Separate [OpenCode CLI 2.1.4 real-model t003 evidence](https://github.com/teaql/teaql-agent-kit/blob/main/docs/opencode-t003-verification.md)
now covers denied reads/writes, an allowed comment edit and fixed Rust build/test
commands. The suite executed zero cases. Full TeaQL capability composition, Pi
automatic completion recovery and token savings are not claimed.

References: [V2 API](https://dev.opencode.ai/v2/docs/build/plugins/),
[published SDK](https://www.npmjs.com/package/@opencode/plugin/v/2.1.4).
