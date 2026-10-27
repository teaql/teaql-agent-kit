# Capture actual Agent and model identity

Use the bundled Python 3.9+ helper after saving a complete model and before
**every** evaluate, generation or Assist call. Run discovery on the machine
hosting the Agent, not merely the machine hosting the generator. No Python
packages, network service, model API credential or global hook is required.

Set `SKILL_DIR` to the actual installed `build-teaql-app` directory:

```sh
python3 "$SKILL_DIR/scripts/model_provenance.py" stamp --input /path/to/model.xml
cargo-teaql --version  # Must satisfy the toolchain requirement.
cargo teaql --input /path/to/model.xml evaluate
```

For split models, pass the same directory used by TeaQL. The helper chooses
`main.xml`, or the unique top-level XML file whose root has a service name.
For any other layout, supply `--entry relative/path.xml` explicitly. Only the
entry root is modified; included module bytes remain untouched. A missing
UUID is generated once; an existing valid UUID survives model, Agent and LLM
changes. An invalid existing UUID fails rather than silently replacing a
lifecycle. Template copies intended as independent models still need their
own new UUID (do not copy the template's identity).

The helper updates only the opening root tag, preserves the rest of the file
byte for byte, uses an atomic replacement and preserves file permissions.
Repeated stamping with unchanged identity does not change the revision hash.
When identity changes, re-evaluate before generation. Missing current fields
become `unknown`; a previous Agent's known values are never carried forward.

## Codex: automatic current-session discovery

`CODEX_THREAD_ID` selects the exact active session under
`${CODEX_HOME:-~/.codex}/sessions`. The recorded `session_meta.id` must match.
The helper reads only these metadata fields into the exported result:

| KSML attribute | Runtime source |
| --- | --- |
| `agent` | `codex`, identified by the current thread environment |
| `agent_version` | Latest matching `session_meta.cli_version` |
| `llm_provider` | Latest `turn_context.model_provider`, or recorded session provider |
| `llm_model` | Latest complete `turn_context.model` |
| `skill_version` | This Skill checkout's commit (marked dirty if edited), or bundled VERSION |

If `CODEX_TURN_ID` is exposed, the context must match that turn as well.
Missing/unreadable/ambiguous session data becomes `unknown`. A latest turn
without a model never reuses the preceding model. No other session's metadata,
chat text, model-name inference, shell-installed CLI version, `OPENAI_MODEL`,
`ANTHROPIC_MODEL` or default config file is used as actual-run evidence.

The transcript schema is an observed, tested Codex compatibility adapter, not
a claim that a generic shell API exposes every host's effective model. Do not
upload transcript files. The helper emits only an allowlisted identity record;
no prompts, tool outputs, auth files or environment dumps are exported.
Codex also documents session/turn metadata in its
[official hook inputs](https://learn.chatgpt.com/docs/hooks). A host integration
can export the effective values through the generic contract below rather
than relying on transcript discovery.

## Other hosts: trusted runtime exports

A host adapter can obtain the effective provider/model from its current turn
API and export the **complete** bundle before invoking the helper:

```sh
export TEAQL_RUNTIME_SESSION_ID='<actual current session id>'
export TEAQL_RUNTIME_AGENT='<actual agent name>'
export TEAQL_RUNTIME_AGENT_VERSION='<actual running version or unknown>'
export TEAQL_RUNTIME_LLM_PROVIDER='<actual current provider or unknown>'
export TEAQL_RUNTIME_LLM_MODEL='<actual current model id or unknown>'
```

These are adapter-owned runtime values, not instructions to guess them from
examples or copy an old config. A complete explicit bundle takes precedence
over Codex discovery; partial bundles fail to avoid mixing different agents.
Native discovery for Claude/Pi/OpenCode and other hosts is not claimed by this
helper. Their adapters must supply the values above, or unavailable fields
remain `unknown`. Existing protected tools must retain their file-policy and
zero-error gates; this helper does not bypass those tools or auto-install hooks.

## Remote execution over SSH

Capture on the Agent host immediately before use:

```sh
umask 077
python3 "$SKILL_DIR/scripts/model_provenance.py" capture > /tmp/teaql-actor.json
# Transfer only this small allowlisted JSON to the execution host.
scp /tmp/teaql-actor.json host:/path/to/task/run/actor.json
# On the execution host, using its installed Skill:
python3 "$SKILL_DIR/scripts/model_provenance.py" stamp \
  --input /path/to/model.xml --context /path/to/task/run/actor.json
```

Context snapshots expire after five minutes. Capture again before another
operation or after a model/Agent change. An exposed current session ID must
match the snapshot. Do not copy a snapshot between unrelated Agent sessions;
do not use a server's unrelated Codex session to stamp a client's model.
Snapshots and root fields remain caller-declared provenance, not authenticated
provider attestation. `model_uuid` and event UUIDs identify different things;
neither can substitute for actual Agent/LLM metadata.
