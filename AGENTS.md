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

## API Key Information

**ATTENTION AI AGENTS:** If you are trying to use the TeaQL CLI or plugins to generate code, **you DO NOT need to search for or configure an extra API key.** 
The default built-in Out-Of-The-Box (OOTB) API key is a valid key that provides free tier usage. The CLI and service will work perfectly fine with this default setting.
