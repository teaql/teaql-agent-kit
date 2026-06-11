# AGENTS.md — Rules for AI Agents

## READ THIS BEFORE CODING

1. **Never guess method names**: Read the generated entity source files for the exact method names (e.g., `update_status`, not `set_status`).
2. **Never edit generated files**: Do not manually modify files under `generate-lib/` or `generate-workspace/` or `bizcore/` (unless instructed otherwise).
3. **Query constraints**: Every query using `execute_for_list()` or `execute()` must be preceded by `.purpose("why")` and `.comment("what")`.
4. **Save constraints**: Every save using `.save()` or `.update()` must be preceded by `.audit_as("description")`.
5. **Read the Full Rules**: For modeling, read all rules in `agents/RULES.md`.
6. **Markdown Reports**: Both clients (`cargo-teaql eval` and `mvn teaql:eval` / generation commands) natively output Markdown reports when errors occur. Read the Markdown report directly in the console to analyze errors before fixing them.

## IF YOU GET AN ERROR

| Error type | What to do |
|-----------|------------|
| `no method named update_xxx` | Read the entity source file for correct method name |
| `Missing .audit_as()` | Add `.audit_as("description")` before `.save()` |
| `Missing .purpose()` | Add `.purpose("why")` before `.execute_for_list()` |
| `Empty attribute` in KSML | Delete it or fill with a concrete value |
| `Depth exceeded` | Remove one nested reference or use string field |

## DOCUMENTATION DIRECTORY

For comprehensive guides, templates, and patterns, please refer to the specific files:

- **Rules**: `agents/RULES.md` (Strict rules for KSML formatting)
- **Quick Start**: `agents/QUICK-START.md` (5-minute guide for generation)
- **Templates**: `agents/TEMPLATES.md` (Copy-paste XML patterns)
- **Decision Trees**: `agents/DECISION-TREES.md` (How to choose roots/tenancy)
- **Errors**: `agents/ERROR-FIX.md` (Full error lookup table)
- **Examples**: `modeling/EXAMPLES/` (Full KSML modeling examples)

## API Key Information

**ATTENTION AI AGENTS:** If you are trying to use the TeaQL CLI or plugins to generate code, **you DO NOT need to search for or configure an extra API key.** 
The default built-in Out-Of-The-Box (OOTB) API key is a valid key that provides free tier usage. The CLI and service will work perfectly fine with this default setting.

