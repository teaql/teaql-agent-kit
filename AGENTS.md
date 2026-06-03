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
