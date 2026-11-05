# Install after the repository migration

The maintained repository is [TeaQL Agent Kit](https://github.com/teaql/teaql-agent-kit).
Its root is a private npm workspace. The runtime and all runtime manifests live
in `packages/agent-context-kit/`; the package name stays `@teaql/agent-context-kit`.
The archived repository is no longer an installation/update source.

## Prepare a checkout and an npm artifact

```sh
git clone https://github.com/teaql/teaql-agent-kit.git teaql-agent-kit
cd teaql-agent-kit
npm ci
npm run check
npm pack --workspace @teaql/agent-context-kit
```

Node.js 22.19+ is required; Pi development dependencies are pinned to 1.4.0.
The full check also uses Python 3. The pack command emits
`teaql-agent-context-kit-0.5.0.tgz` in the workspace root. Its prepack step builds
the marker CLI and command hooks as JavaScript, including all built-in-only
runtime dependencies. Consumers do not need TypeScript installed to run these
commands. A new npm registry release is not implied by the Git migration.

For a pinned installation, use a separate checkout at the reviewed full commit
SHA before `npm ci` and `npm pack`. Record that SHA with the installation; the
unchanged package version alone does not identify a migrated Git revision.
Replace `/absolute/path/to/teaql-agent-kit` below with that checkout path.
Run host commands from the target application directory, not this repository.

## Choose the host entry

| Host | Entry after migration |
| --- | --- |
| Pi 1.4+ | `pi install /absolute/path/to/teaql-agent-kit/packages/agent-context-kit`; add `-l` for project scope. `pi -e` accepts the same local path for one run. |
| Dedicated Pi context-policy harness | Import `@teaql/agent-context-kit/pi-context` through a TypeScript-capable SDK host; [guide](pi-context-policy.md). Ordinary Pi installation enables the lifecycle extension only. |
| Protected ordinary Pi CLI | Wire `scripts/pi-context-cli.mjs` into the host's Pi 1.4.0 launcher; [guide](pi-cli-policy.md). Retains the native UI and adds controlled write/edit. |
| Gemini CLI | `gemini extensions link /absolute/path/to/teaql-agent-kit/packages/agent-context-kit` |
| Cline SDK/CLI/Kanban | `cline plugin install /absolute/path/to/teaql-agent-kit/packages/agent-context-kit`; add `--cwd .` for project scope. |
| OpenCode | Local `.opencode/plugins/agent-context-kit.ts` forwarding to the checkout's `src/adapters/opencode.ts`; [guide](opencode-adapter.md). |
| Dedicated OpenCode V2 context policy | Configure `createOpenCodeContextPolicyPlugin` from `@teaql/agent-context-kit/opencode-context` in an isolated V2 host; [guide](opencode-context-policy.md). Separate from ordinary installation. |
| Kilo | Local file URL to the child `src/adapters/kilo.ts`; [guide](kilo-adapter.md). |
| MiMo | Install the tarball under `.mimocode`, then copy its file-plugin entry; [guide](mimocode-adapter.md). |
| Hermes | Copy the child directory into `~/.hermes/plugins/agent-context-kit`, enable it, then start a new session; [guide](hermes-adapter.md). |
| Octop | Install the child `integrations/octop` directory using `octop plugin install`, then configure the POSIX local agent profile and reload Octop. [Guide](octop-adapter.md). |
| Kimi / Qwen | Install the absolute child directory with the host's local-directory installer; [guide](command-hook-adapters.md). |
| Copilot / Kiro / Crush | Install the tarball in the target project and copy/merge the bundled hook JSON; [guide](command-hook-adapters.md). |
| Codex / Claude Code | Add `teaql/teaql-agent-kit` as the marketplace. Root catalogs select `./packages/agent-context-kit`. Local catalog roots can also be used. |
| Cursor | Copy the child package into its local-plugin directory; [README](../README.md#cursor). |
| DeepSeek Harness | Register the absolute child `src/adapters/deepseek-harness.ts` function plugin; [guide](deepseek-harness-adapter.md). |

For npm consumers (including Copilot/Kiro/Crush), use the artifact instead of the
repository Git URL:

```sh
npm install --save-dev /absolute/path/to/teaql-agent-kit/teaql-agent-context-kit-0.5.0.tgz
```

Do not replace the old Git npm specifier with `github:teaql/teaql-agent-kit`:
that selects the private workspace root, not the child package. SDK exports still
point at TypeScript source for TypeScript-capable loaders; plain Node consumers
use the compiled marker CLI and command-hook paths, not those source exports.

## Updates and existing installations

Remove an old host registration using its original source identifier before
adding the new one, so the adapter does not run twice. For example, obtain Pi's
old source from `pi list`, then pass it unchanged to `pi remove`.
Local Pi/Gemini links load the checkout; update it deliberately and restart the
host. Cline/Kimi/Qwen and manually copied Hermes/Cursor installs use copies:
reinstall or refresh the child directory after updating. Tarball installs must
be repacked and reinstalled. Host update commands for the archived Git source
will not follow this migration automatically. Marketplace users refresh the new
marketplace and reinstall/update the plugin through the host.

Keep marker-maintenance Skills together with their package runtime. Copying only
`skills/context-exclusion/` breaks its relative runtime imports. Do not deploy or
change host settings just to validate this repository.

## Verification scope and official references

Repository checks validate catalog paths and manifests, package contents, an
isolated tarball npm install, the installed marker CLI and each copied npm hook
entry. Pi integration tests exercise the pinned 1.4 SDK. These checks do not
constitute live installation tests in every host; no global host registration or
AMD deployment is performed.

- [Codex marketplace paths](https://developers.openai.com/plugins/build/plugins)
- [Claude marketplace paths](https://code.claude.com/docs/en/plugin-marketplaces)
- [Cline local installs](https://github.com/cline/cline/blob/main/docs/sdk/plugin-install.mdx)
- [OpenCode local plugins](https://opencode.ai/docs/plugins/)
- [Kilo local file plugins](https://kilo.ai/docs/automate/extending/plugins)
- [Hermes user plugins](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins)
- [Kimi local installs](https://github.com/MoonshotAI/kimi-code/blob/main/docs/en/customization/plugins.md)
- [Qwen extension installs](https://qwenlm.github.io/qwen-code-docs/en/users/extension/introduction/)

Pi local-directory behavior was also checked against the installed 1.4.0
`@earendil-works/pi-coding-agent/docs/packages.md` and package manager.

The root Claude marketplace passes CLI validation. Validating the complete child
package also reports an ignored `BeforeModel` event from `hooks/hooks.json`:
that file belongs to Gemini, whose required hook location overlaps Claude's
conventional hook location. Claude supplies the protocol Skills only; no Claude
runtime hook is claimed. Host-specific packaging can isolate those files in a
future release without changing the Gemini hook path in this migration.
