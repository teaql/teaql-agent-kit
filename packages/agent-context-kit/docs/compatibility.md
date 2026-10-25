# Agent compatibility

This table is capability-based. “Plugin exists” and “the host can enforce V1”
are deliberately separate claims.

| Agent | Packaging documented | Request-local history rewrite | Project status |
| --- | --- | --- | --- |
| Pi | Extension package | Yes, `context` transform | Full V1 adapter |
| OpenCode | V2 package plugin; V1 compatibility entry | Yes, request-local `context` hook in V2 and message transform in V1 | Full V1 lifecycle adapter; read guard throws before tool execution |
| Kilo Code | Package server plugin | Yes, experimental message/system transforms | Full V1 adapter on an experimental host hook; OpenCode-compatible read guard |
| Cline | Git/npm package plugin | Yes, provider-bound `registerMessageBuilder` | Full V1 adapter for SDK, CLI, and Kanban; `beforeTool` read guard |
| MiMo Code | Project file plugin under `.mimocode/plugins/` | Yes, experimental message/system transforms | Source-verified experimental adapter; read guard uses the typed cancellation result |
| DeepSeek Harness | Cordis function plugin | Yes, durable message projections plus prompt sections | V1 adapter; trusted source must remain available when resuming |
| Gemini CLI | Extension with `hooks/hooks.json` | Text-only `BeforeModel` request view | Supported for text messages; non-text tool payloads are outside the stable hook API |
| Hermes Agent | Native `plugin.yaml` plus Python `register(ctx)` plugin | Request-local `pre_llm_call` context injection; no arbitrary history replacement | Persistent workspace blocks, trusted session discard, and protected-read blocking; consume-once transcript rewriting not claimed |
| Kimi Code | Native `kimi.plugin.json` | Current-request context only | Active blocks, subagent context, and protected-read blocking; no consume-once history rewrite |
| Qwen Code | Native `qwen-extension.json` and command hooks | Current-request context only | Active blocks, subagent context, and protected-read blocking; no consume-once history rewrite |
| Kiro CLI | Standalone `.kiro/hooks/*.json` | Current-request and `SubagentStart` context only | Active blocks, delegated-agent context, and protected-read blocking; no arbitrary history rewrite |
| GitHub Copilot CLI | Repository or installed-plugin hook JSON | No | Protected-read blocking only |
| Crush | Project `crush.json` command hook | No | Top-level protected-read blocking only; subagent calls are not intercepted |
| Codex | Agent Plugin | No; `UserPromptSubmit` only adds context | Installable protocol skill; runtime enforcement not claimed |
| Claude Code | Plugin | No arbitrary pre-model history replacement | Installable protocol skill; runtime enforcement not claimed |
| Cursor | Plugin | No arbitrary pre-model history replacement | Installable protocol skill; runtime enforcement not claimed |
| Antigravity | Skills, rules, workflows | No documented per-model request rewrite hook found | Skipped |
| WorkBuddy | Skills, experts, connectors | No documented per-model request rewrite hook found | Skipped |
| Aider | Configuration and read-only convention files | No documented plugin interception API | Skipped |
| Continue | Context providers and MCP | No documented full-request plus pre-tool interception API | Skipped |
| Roo Code | Rules and MCP | No documented stable plugin lifecycle interception API | Skipped |

## Runtime limits and skipped hosts

OpenCode also has an opt-in [V2 context-policy plugin](opencode-context-policy.md)
with marker-aware controlled reads/search/list, independent host-approved writes,
prompt admission controls and fixed diagnostic tasks. This is separate from the
ordinary adapter above; V1 strict mode is unsupported. Verification includes SDK
2.1.4 type compatibility and its real Promise/Effect bridge. A separate
[installed CLI 2.1.4 run](https://github.com/teaql/teaql-agent-kit/blob/main/docs/opencode-t003-verification.md) verifies
the t003 profile with a real local model: read/write boundaries and fixed Rust
build/test tasks, with zero test cases executed. TeaQL capabilities and Pi
automatic completion recovery are not composed here. The guide details its trust
and loading limits.

- OpenCode V2 documents a per-session `context` hook that mutates messages and
  system instructions only for the outgoing model request. Its tool hook can
  reject a protected read before execution. V1 compatibility uses the older
  message/system transform hooks and requires OpenCode 1.18.29 or later for the
  package object entry point. See [OpenCode V2 plugins](https://dev.opencode.ai/v2/docs/build/plugins/)
  and [the V1 migration table](https://dev.opencode.ai/v2/docs/build/plugins/migrate-v1).
- MiMo Code's maintained `@mimo-ai/plugin` source types expose message/system
  transforms and a cancellable `tool.execute.before` result. The project file
  loader scans `.mimocode/plugins/`, but the public plugin guide still contains
  inherited `.opencode` paths. Support is marked experimental until the
  documentation and API stability catch up. See the
  [plugin type source](https://github.com/XiaomiMiMo/MiMo-Code/blob/main/packages/plugin/src/index.ts),
  [current config reference](https://github.com/XiaomiMiMo/MiMo-Code/blob/main/packages/opencode/src/skill/builtin/.bundle/mimocode-docs/reference/config.md),
  and [path documentation issue](https://github.com/XiaomiMiMo/MiMo-Code/issues/1151).
- Hermes Agent documents native plugins that run in CLI and gateway sessions.
  Its `pre_llm_call` result is appended only to the current request and is not
  persisted, while `pre_tool_call` can veto a tool and return feedback to the
  model. This is enough for active block injection, `/context-discard`, and the
  read guard, but not for rewriting an arbitrary earlier ephemeral message.
  See [Hermes plugins](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins)
  and [event hooks](https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks).
- Kilo Code documents the same plugin behavior as OpenCode, including
  `experimental.chat.messages.transform`, `experimental.chat.system.transform`,
  and `tool.execute.before`. The first two hooks make full V1 possible, but the
  experimental label remains part of this project's support claim. See
  [Kilo Code plugins](https://kilo.ai/docs/automate/extending/plugins).
- Cline's `registerMessageBuilder` rewrites provider-bound messages and
  `beforeTool` can block a call before execution. Cline currently documents
  plugin installation for its SDK, CLI, and Kanban surfaces, so IDE-extension
  support is not claimed. See [Cline plugins](https://github.com/cline/cline/blob/main/docs/customization/plugins.mdx)
  and [plugin examples](https://github.com/cline/cline/blob/main/sdk/examples/plugins/README.md).
- Kimi Code plugins can bundle command hooks. `UserPromptSubmit` and
  `SubagentStart` add current-request context, while `PreToolUse` can deny a
  protected read. The hook API cannot replace arbitrary prior history. See
  [Kimi Code plugins](https://github.com/MoonshotAI/kimi-code/blob/main/docs/en/customization/plugins.md)
  and [hooks](https://github.com/MoonshotAI/kimi-cli/blob/main/docs/en/customization/hooks.md).
- Qwen Code native extensions can ship hook configuration. Its
  `UserPromptSubmit`, `SubagentStart`, and `PreToolUse` events cover current
  context and read guards, but no documented hook replaces arbitrary prior
  history. See [Qwen Code extensions](https://qwenlm.github.io/qwen-code-docs/en/users/extension/introduction/)
  and [hooks](https://qwenlm.github.io/qwen-code-docs/en/users/features/hooks/).
- Kiro CLI V3 standalone hooks add successful command output to agent context,
  expose `SubagentStart`, and block `PreToolUse` on nonzero exit. This supports
  active blocks, delegated-agent context, and read guards, not full-history
  rewriting. See [Kiro V3 hooks](https://kiro.dev/docs/cli/v3/hooks-migration/)
  and [hook actions](https://kiro.dev/docs/hooks/actions/).
- GitHub Copilot CLI's `PreToolUse` hook can deny a call with feedback, but
  command hooks do not expose arbitrary request-history replacement. The
  integration is therefore read-guard only. See
  [Copilot hooks](https://docs.github.com/en/copilot/reference/hooks-reference).
- Crush currently documents only `PreToolUse`, and explicitly excludes
  subagent-internal calls from interception. Its adapter protects top-level
  reads only. See [Crush hooks](https://github.com/charmbracelet/crush/blob/main/docs/hooks/README.md).

- Codex documents Agent Plugin packaging and lifecycle hooks, but
  `UserPromptSubmit` adds context rather than replacing the prompt or history,
  and its current post-tool hook does not expose a general updated tool-output
  field. The included Codex plugin therefore provides protocol guidance only.
  See [Codex plugins](https://developers.openai.com/plugins/concepts/plugins)
  and [Codex hooks](https://learn.chatgpt.com/docs/hooks).
- Claude Code documents plugins and lets `PostToolUse` replace the current tool
  output, but `UserPromptSubmit` cannot replace the prompt and there is no
  documented `BeforeModel` equivalent for rewriting arbitrary earlier history.
  The `.claude-plugin` manifest therefore packages the same protocol skill but
  no lifecycle hook.
  See [Claude Code plugins](https://code.claude.com/docs/en/plugins) and
  [hooks](https://code.claude.com/docs/en/hooks).
- Cursor documents hooks and Agent Plugin packaging. Its prompt hook is a
  continue/block gate, while post-tool replacement is limited to the current
  MCP output; neither is a full-history request transform. The `.cursor-plugin`
  manifest therefore packages the same protocol skill but no lifecycle hook. See
  [Cursor hooks](https://prod.cursor.com/docs/hooks) and
  [plugins](https://prod.cursor.com/docs/reference/plugins).
- Antigravity's public material documents `.agents/skills`, rules, and
  workflows, not a hook that receives and replaces every outgoing model
  request. See Google's [Antigravity skills guide](https://codelabs.developers.google.com/antigravity/how-to-create-agent-skills-for-antigravity-cli).
- WorkBuddy documents skills, experts, connectors, and Buddy Apps, but no
  equivalent request-history interception API. See
  [WorkBuddy skills](https://open.workbuddy.cn/en/docs/skill),
  [experts](https://open.workbuddy.cn/en/docs/expert), and
  [connectors](https://open.workbuddy.cn/en/docs/connector).
- Aider documents loading convention files as read-only context, but not a
  request transform or tool-call veto API. See
  [Aider conventions](https://aider.chat/docs/usage/conventions.html).
- Continue documents custom context providers and recommends MCP for new
  integrations, but does not document the paired request-history and pre-tool
  interception boundary needed here. See
  [Continue custom context providers](https://docs.continue.dev/customize/deep-dives/custom-providers).
- Roo Code documents rules and MCP usage, but no stable plugin hook that can
  rewrite outgoing history or deterministically veto built-in reads. See
  [Roo Code MCP usage](https://github.com/RooCodeInc/Roo-Code-Docs/blob/main/docs/features/mcp/using-mcp-in-roo.mdx).

This is a current documented-capability decision, not a permanent rejection.
A skipped host can be added when its official API exposes a deterministic
request-local transform with enough provenance to enforce the trust boundary.
