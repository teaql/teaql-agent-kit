# Agent feature activation

**Repository snapshot: 2026-10-25 (Asia/Shanghai).** These are capabilities implemented in this
package, not a claim that every host has been installed or tested live. A plugin
installation activates only its selected entry point. **ReadGuard** means configured
path/tool blocking; **marker policy** additionally controls directory traversal and
checked automatic context. The two are not interchangeable.

| Agent / entry point | Context lifetime controls | Read boundary | Controlled writes | Activation and evidence |
| --- | --- | --- | --- | --- |
| **Pi native CLI bootstrap** | Inline lifecycle handler; explicit trusted phase-source integration remains separate | Marker policy, fresh checked project context, non-retryable denial feedback | Checked native `write` / `edit` | Host wires the bootstrap behind ordinary `pi`; native CLI tests, real-model failure recovery, completion verification and t003 business repair; see the evidence below |
| **Pi dedicated SDK harness** | No lifecycle adapter composed by default | Marker policy, fresh checked project context, non-retryable denial feedback | Disabled | `createContextPolicyPiSession`; real Pi 1.4.0 with local deterministic provider tests |
| **Pi ordinary lifecycle plugin** | Named blocks, trusted discard, consume-once messages | Optional configured ReadGuard | No write-policy integration | `pi install <child-package-path>`; installing alone does not activate marker enforcement |
| **OpenCode V2 strict plugin** | Optional trusted `lifecycleFile`; request-local text-message lifetimes | Marker policy, checked project context and controlled tool catalog | Explicit write roots; create/overwrite/edit/delete/move | Opt-in `createOpenCodeContextPolicyPlugin`; pinned SDK/bridge tests and OpenCode CLI 2.1.4 real-model t003 read/write and fixed build/test verification |
| **OpenCode ordinary V2 / V1 adapter** | Named blocks, trusted discard, consume-once adapter | Optional configured ReadGuard | No write-policy integration | Local plugin entry; V1 package-object entry requires 1.18.29+; separate from strict V2 |
| **Cline SDK / CLI / Kanban** | Named blocks, trusted discard, consume-once adapter | Optional configured ReadGuard | No write-policy integration | Cline plugin registration; adapter tests, no IDE-extension claim |
| **Kilo Code** | Named blocks, trusted discard, consume-once adapter | Optional configured ReadGuard | No write-policy integration | Server plugin; experimental host transforms, adapter tests |
| **MiMo Code** | Named blocks, trusted discard, consume-once adapter | Optional configured ReadGuard | No write-policy integration | Project plugin; experimental source-verified hooks, adapter tests |
| **DeepSeek Harness** | Named blocks, trusted discard, durable ephemeral projections | No read guard wired in this adapter | No write-policy integration | Harness overlay; lifecycle adapter tests |
| **Gemini CLI** | Named blocks, trusted discard, text-only consume-once | No read guard wired in this extension | No write-policy integration | `BeforeModel` extension; non-text tool payloads outside its stable view |
| **Hermes Agent** | Active blocks and trusted session discard; no consume-once rewriting | Configured ReadGuard | No write-policy integration | Native Python plugin; Python adapter tests |
| **Kimi Code / Qwen Code / Kiro CLI** | Current-request and delegated context; no consume-once rewriting | Configured ReadGuard | No write-policy integration | Host command hooks; contract tests; no full marker-aware harness |
| **GitHub Copilot CLI** | No lifecycle rewriting | Configured ReadGuard | No write-policy integration | `PreToolUse` hooks; command-hook tests |
| **Crush** | No lifecycle rewriting | Top-level configured ReadGuard | No write-policy integration | Command hook; subagent tool calls are outside its interception |
| **Codex / Claude Code / Cursor** | Protocol guidance Skill only in this package | No runtime enforcement claimed | No write-policy integration | Installable guidance; packaging does not imply enforcement |
| **Other coding agents shown above** | TeaQL Skill instructions where supported | No Context Kit enforcement claimed | No write-policy integration | The ability to read a Skill is separate from a runtime adapter |

## Activate the protected Pi entry point

The [native CLI bootstrap](../packages/agent-context-kit/docs/pi-cli-policy.md) runs
Pi 1.4.0's native UI with controlled file tools. When the host has wired it into
the normal launcher, start a fresh session with `cd <project>; pi`; a separate
`pi-context` command is not required. Existing running sessions keep their old code
until restarted. Merely installing the ordinary lifecycle extension is insufficient.

Protected Pi/OpenCode modes disable arbitrary Shell, unguarded MCP/delegation and
automatic external resource loading. Pi can load explicitly approved capability
modules from its protected agent directory. The optional
[TeaQL Rust integration](../integrations/pi-teaql/README.md) supplies evaluation,
progressive Assist, zero-error-gated library regeneration and fixed build/test
targets. This is project-specific host configuration, not an unrestricted terminal
or a complete seven-language workflow integration.

## Activate OpenCode V2 strict mode

Create a host-owned `.opencode/plugins/agent-context-policy/index.ts` in an isolated
OpenCode V2 profile, replacing the checkout and project paths:

```ts
import { createOpenCodeContextPolicyPlugin } from "/absolute/teaql-agent-kit/packages/agent-context-kit/src/adapters/opencode-context.ts";

export default createOpenCodeContextPolicyPlugin({
  projectRoot: "/absolute/project",
  writeRoots: ["models", "app/src", "app/tests"],
  readOnlyPaths: ["generated"],
  contextPaths: ["docs/api.md"],
  // Optional, explicitly trusted lifecycle declarations:
  lifecycleFile: ".agent-context-kit.md",
});
```

Use a fresh session and create markers in the generated directories. Do not load
the ordinary lifecycle plugin alongside this strict plugin. Strict mode requires
V2 and rejects V1. See the [OpenCode policy guide](../packages/agent-context-kit/docs/opencode-context-policy.md)
for attachment handling, trusted-host assumptions and automatic-context limits.
OpenCode CLI 2.1.4 now has [real-model t003 verification](opencode-t003-verification.md)
for read/write boundaries and fixed Rust build/test tasks. The run executed zero
test cases; Pi completion recovery and TeaQL-specific capability tools are not
composed into this OpenCode profile.

See the full [compatibility guide](../packages/agent-context-kit/docs/compatibility.md)
and [host installation guide](../packages/agent-context-kit/docs/installation.md).

## Pi completion and real-model evidence

The native bootstrap enables automatic completion checks when the host registers
both `app_build` and `app_test`. Successful edits invalidate prior verification.
On a premature model stop, the host runs missing checks and returns their actual
results for continuation. Cancellation is respected; automatic verification is
bounded to three rounds per user request. The dedicated read-only harness and
OpenCode plugin do not include this Pi completion integration.

The [TeaQL Rust integration](../integrations/pi-teaql/README.md) adds version-checked
evaluation, progressive Assist, gated library regeneration and Rust diagnostics.
The [actual t003 repair record](t003-business-repair-verification.md) distinguishes
a failed initial attempt from the successful real-model run and its zero-test
limitation. These capabilities require trusted host configuration; installing
the lifecycle plugin alone does not activate them.

Protected Pi also includes [old-session reply-loop recovery](pi-old-session-recovery-verification.md).
It preserves all user instructions and the on-disk transcript while rebuilding
the outgoing view after repeated no-tool promises. This guard is independent of
registered build/test capabilities and is not ported to OpenCode.
