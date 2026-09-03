# Incremental application repair

Use this policy after an application-owned source file has been created and
compiled for the first time.

1. Read the exact compiler or test diagnostic and identify its file, symbol,
   and smallest affected block.
2. Patch only that block. Preserve code that already compiles, unrelated
   imports, formatting, functions, and tests.
3. Recompile and repeat with the next related diagnostic. Do not regenerate or
   rewrite the complete application file to repair a local failure.
4. If the proposed repair would replace more than 25% of an existing file,
   stop before editing and report:

```text
LARGE_REWRITE_REQUEST
file: <application-owned file>
diagnostic: <exact compiler or test diagnostic>
reason: <why a localized patch is insufficient>
estimated_scope: <lines or percentage>
```

This threshold does not prevent initial file creation, model-level repair and
regeneration, generated-file replacement by the generator, or a user-approved
architectural rewrite. It prevents an Agent from repeatedly replacing a
mostly-correct application file as an error-recovery strategy.

Before initially writing business code, keep the implementation inventory
short: list only the entities, fields, Q/E/mutation operations, and Assist
locations required by the task. A method is confirmed only when current Assist
provided it; do not use planning as permission to infer an API.
