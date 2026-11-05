# Octop context plugin

Install the Python hook from the Context Kit package. It applies to opted-in
Octop agents using a POSIX local `filesystem` backend mounted at the workspace.
It uses the Octop plugin loader and the `octop-harness` middleware API.

```sh
octop plugin install ./packages/agent-context-kit/integrations/octop
```

Run the command from the repository root, or pass the installed npm package's
`integrations/octop` directory. The plugin uses Octop's Python environment.

For each agent, use a canonical local workspace path for `workspace_dir` and
mount that same directory as the backend root with `virtual_mode: true`.

```json
{
  "workspace_dir": "/srv/octop/project",
  "backend": {
    "type": "filesystem",
    "root_dir": "/srv/octop/project",
    "virtual_mode": true
  }
}
```

Use the agent's actual ID as the key in `policy.json` under the installed plugin
directory (`~/.octop/plugins/teaql-agent-context-kit/` by default).

```json
{
  "agents": {
    "your-agent-id": {
      "workspace_root": "/srv/octop/project",
      "context_file": "project-context.md"
    }
  }
}
```

Place `project-context.md` beside `policy.json` before enabling the policy.
Both files belong to the server administrator and should be outside the
agent's workspace and writable tools. `context_file` is optional. Without it,
the agent still gets consume-once messages and the file read guard. Agents
absent from `policy.json` use Octop's usual behavior. The configured root must
match the agent's backend root. Docker, remote storage, composite backends and
other mount layouts are outside this profile.

Reload via **Admin → Plugins → Reload** or restart Octop after installing or
changing `policy.json`. Start a new thread to verify the profile. As a smoke
check, read a permitted text file and a file under a marked directory. The
second call should return the marker guidance. After a plugin update, verify
that the installed policy and context file are present and reload again.

## Lifecycle

Define blocks in the configured Markdown file using the exact V1 tag lines.

```markdown
<!--BLOCK_ID:modeling-->
Use the public Assist guide while modeling.
<!--/BLOCK_ID:modeling-->
```

Add a line `<!--DISCARD_BLOCK:modeling-->` to that same file when the block
should be retired. The file is checked before each model call. The first valid
definition in a thread remains authoritative. A discard applies separately in
each configured agent thread when it next makes a request, and stays applied
after restart when the thread uses a persistent checkpointer. Removing the
directive lets new threads activate the block. Chat messages, assistant output,
and tool results cannot define or discard blocks.

A message or tool result with an exact `<!--ephemeral-->` line is sent until
a later assistant message exists. Subsequent ordinary model requests contain a
short placeholder with the original byte count. The original message and its
tool call ID remain in the checkpoint. Active blocks are added to the outgoing
system message. The plugin logs activations, discards and projected ephemeral
messages at `INFO` with the request sequence and scope.

## File reads and scope

Put `.agent-no-read.md` in a directory to exclude reads of its descendants.
For example, a marker in `generated/` can tell the agent to use `docs/api.md`
or the TeaQL Assist workflow. The guard checks both the requested and resolved
paths before running native `read_file`. It returns bounded marker guidance as
workspace data. Missing files, paths outside the workspace, and unresolved
paths are denied. Relative `read_file` paths and paths beginning with `/` both
address the configured workspace. For example, `docs/api.md` and `/docs/api.md`
both refer to the same file in the workspace. The native tool receives the
checked workspace path.

The profile hides and rejects the native `ls`, `glob`, and `grep` tools so
they cannot enumerate or search excluded files. It also rejects direct
`read_image` and `read_video` tool calls if those names are available.
The plugin's scope is the main agent's ordinary model requests and the listed
read tools. Use Octop's tool settings to restrict other file access routes as
needed. Automatic context and attachment loading, other tools including edits,
MCP, ACP, nested agents, compaction and memory each have their own access path.
The read guard is a context policy. OS isolation and filesystem permissions
provide the host security boundary.

## Verify

The workspace's `npm run check` includes the POSIX read-policy tests. To run
the plugin through a real Harness graph, install the pinned Harness in a Python
3.12 environment and run the Octop tests from the repository root.

```sh
python -m pip install 'octop-harness==1.0.7' 'deepagents==0.7.16' \
  'langchain==1.4.2' 'langchain-core==1.6.3' 'langgraph==1.2.11'
python -B -m unittest discover -s packages/agent-context-kit/test -p 'octop*_test.py' -v
```

The graph test uses a deterministic recording model and native file tools, so
it runs without provider credentials. It exercises the installed plugin loader,
allowed and denied reads, tool result pairing, trusted discard, checkpoint
reopen, and thread isolation.

See Octop's [plugin packaging guide](https://github.com/TencentCloud/Octop/blob/4811eb45996169e86006db1b6451264ff4758223/docs/plugin-package.md)
and the [V1 lifecycle protocol](protocol-v1.md).
