# Scoring — Evaluation Report 003

## Run Metadata

- **Task ID:** TEAQL-AUTO-003
- **Task Title:** Build a Moving Company Management System with 183+ KSML Objects
- **Agent:** MiMo Code Agent (mimo-auto)
- **Model:** mimo/mimo-auto
- **Stack:** Rust (TeaQL Runtime v4.0.3 / SQLite)
- **Date:** 2026-06-11
- **Branch:** autonomous
- **Human Intervention Count:** 0

## Result Summary

- **Final Status:** Passed
- **One-Shot Success:** No (required multiple model fix iterations)
- **Compile Success:** Yes
- **Test Pass Rate:** 100% (15/15)
- **Total Token Usage:** Not measured

## Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Functional Completion | 5 | All 183 objects created, all modules covered |
| API Adherence | 5 | Correct Q/E API usage, audit_as pattern |
| Hallucinated API Count | 0 | Used only generated API names |
| Audit Coverage | 5 | Every query has .comment()/.purpose(), saves have .audit_as() |
| Framework Discipline | 5 | Did not edit generated files, followed AGENTS.md |
| Error Recoverability | 4 | Recovered from 96 eval errors to 0, but required multiple iterations |
| Repair Turns Required | 5 | 5 model fix iterations to reach 0 errors |
| Human Intervention Count | 0 | Fully autonomous |
| Unsafe Shortcut Count | 0 | No unsafe shortcuts observed |

## Score Calculation

**Weighted Score: 8.8 / 10**

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Project Understanding | 20% | 9.0 | 1.80 |
| TeaQL Convention Alignment | 25% | 9.0 | 2.25 |
| Code Correctness | 25% | 8.5 | 2.13 |
| Auditability / Traceability | 20% | 9.0 | 1.80 |
| Engineering Judgment | 10% | 8.5 | 0.85 |
| **Total** | **100%** | | **8.83** |

## Dimension Details

### Project Understanding (9.0/10)
- Accurately understood TeaQL modeling-first workflow
- Understood the scale requirement (183 objects)
- Correctly identified multi-tenant architecture needs
- Understood module organization requirements

### TeaQL Convention Alignment (9.0/10)
- Correctly used Q API for all queries
- Correctly used .comment() and .purpose() pattern
- Correctly used .audit_as() for saves
- Correctly used _audit_mask_fields for sensitive fields
- Did not bypass TeaQL APIs

### Code Correctness (8.5/10)
- 15/15 automated tests pass
- All query and expression examples build successfully
- Smoke test runs without errors
- Minor: E API examples commented out (require runtime instances)

### Auditability / Traceability (9.0/10)
- Every query includes .comment() and .purpose()
- Every save includes .audit_as()
- Complete evaluation trace preserved
- All raw data available in raw/ directory

### Engineering Judgment (8.5/10)
- Recovered from 96 evaluation errors through systematic fixes
- Used generated API names after compilation errors
- Fixed sensitive field issues following error messages
- Made reasonable trade-offs (removed circular references)

## Evidence

- **Prompt file:** raw/agent-prompt.md
- **Response file:** raw/agent-response.md
- **Build log:** raw/build-log.txt
- **Runtime log:** raw/runtime-log.txt
- **SQL trace:** raw/sql-trace.txt
- **Code diff:** raw/code-diff.patch

## Observations

### What the Agent Did Well
- Created a comprehensive 183-object model covering all required modules
- Systematically resolved evaluation errors through multiple iterations
- Used generated API names correctly after compilation errors
- Preserved complete audit trail throughout the process
- Followed all TeaQL conventions without bypassing

### What the Agent Misunderstood
- Initial model had 96 errors (empty attributes, missing references, sensitive fields)
- Some API names needed to be read from generated source code
- E API requires entity instances at runtime (not testable without database)

### TeaQL Boundaries Respected
- Did not write raw SQL
- Did not bypass TeaQL APIs
- Did not edit generated files
- Did not invent unsupported APIs
- Followed AGENTS.md rules

### Unsafe Shortcuts
- None observed

### TeaQL Diagnostics Help
- Evaluation errors were clear and actionable
- Error messages guided the fix process
- Generated API names were discoverable through source code

## Final Notes

This evaluation demonstrates that TeaQL's semantic guardrails work effectively even for large-scale models (183 objects). The agent was able to create a comprehensive moving company management system while maintaining TeaQL conventions. The evaluation process itself was transparent and auditable, with all raw data preserved for independent verification.
