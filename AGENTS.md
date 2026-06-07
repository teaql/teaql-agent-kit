# Agent Instructions

This project uses CodeGraph.

The CodeGraph index is generated in the parent directory of this project, not necessarily inside the project root.

Before analyzing, editing, or refactoring code, first check the parent directory for the CodeGraph index and prefer CodeGraph / MCP tools over broad grep or full-file scans.

Use CodeGraph especially for:

1. locating symbol definitions;
2. finding references and usages;
3. understanding call chains and dependencies;
4. checking impact scope before changes;
5. identifying related tests.

If CodeGraph tools are unavailable, fall back to normal file search.

## Autonomous Branch Rules

This branch is for no-gate evaluation of coding agents and language models on
TEAQL-based business software tasks.

When running an autonomous evaluation:

1. Start from a task file in `tasks/`.
2. Give the agent only the planned initial context.
3. Do not add hints, API corrections, code edits, or new business knowledge
   after execution starts.
4. If human intervention occurs, record it in the run scorecard.
5. Preserve evidence under `runs/<agent>/<task-id>/<run-date>/`.
6. Score the run with `evaluation/scorecard-template.md`.

Autonomous evaluation is a benchmark and stress-test workflow. It is not a
recommendation for ungated production deployment.

For TEAQL implementation work, preserve generated-code discipline: do not edit
generated TeaQL service code directly. If generated code is wrong, fix the model,
generator configuration, runtime, or toolchain and regenerate.
