# TeaQL Quick Start for AI Agents

## Step 1: Read rules
Read `agents/RULES.md` (50 rules, 2 minutes).

## Step 2: Create model
Use `agents/TEMPLATES.md` to create `model.xml`.
Follow `agents/DECISION-TREES.md` for root and tenancy choices.

## Step 3: Validate
Run: `cargo-teaql eval model.xml`
If errors: look up in `agents/ERROR-FIX.md`.
If 0 errors: proceed.

## Step 4: Generate
Run: `cargo-teaql gen-lib model.xml`
Run: `cargo-teaql gen-workspace model.xml`

## Step 5: Code
Read `generate-lib/AGENTS.md`.
Write queries using `reference/API-PATTERN.md`.
Run: `cargo check && cargo test`
