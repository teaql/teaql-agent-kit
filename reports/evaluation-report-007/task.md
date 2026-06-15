# Task Specification

## Source Repository

https://github.com/teaql/teaql-agent-kit/tree/autonomous

## Task

Build a complete TeaQL School Management System from scratch:

1. Create a KSML model with 3 entities: Platform (domain root), SchoolType (constant), School (business object)
2. Evaluate the model with `cargo-teaql eval` — target 0 errors, 0 warnings
3. Generate code with `cargo-teaql gen-lib` and `cargo-teaql gen-workspace`
4. Read generated entity source for accurate API method names
5. Write a test `main.rs` exercising Q API and E API
6. Compile with zero warnings
7. Run and verify all steps pass

## Key Rules

From AGENTS.md:
1. Never guess method names — read generated entity source files
2. Never edit generated files
3. Every query: `.purpose("why").comment("what")`
4. Every save: `.audit_as("description")`
5. Refresh cargo-teaql before generation
