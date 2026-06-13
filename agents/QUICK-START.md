# TeaQL Quick Start for AI Agents (5-Minute Guide)

This guide provides the fastest path for an AI agent to build a TeaQL project from scratch. By following these 5 steps, you will construct a correctly structured model, validate it, generate the code, and use the APIs.

## Step 1: Read the Rules (2 mins)
**CRITICAL**: Read `agents/RULES.md` before writing any XML or Code. It defines exact naming conventions and required attributes.
- Entities MUST use `_id` and `_name` for primary properties.
- Roots require `_features="root"`.

## Step 2: Create the Model (`model.xml`)
Use `agents/TEMPLATES.md` to copy the exact XML blocks.
Follow `agents/DECISION-TREES.md` to pick the right root and tenancy strategy.

**Example Minimal Model:**
```xml
<teaql>
    <domain name="myapp" package="com.myapp">
        <entity name="tenant" _features="root" />
        <entity name="user" tenant="tenant()" />
    </domain>
</teaql>
```

## Step 3: Validate and Fix Errors
Run the validation tool:
```bash
cargo-teaql eval model.xml
```
*Tip: When errors occur, the CLI natively outputs a beautifully formatted Markdown report for easy reading and analysis.*
- **If errors occur**: Read the output or Markdown report, then go straight to `agents/ERROR-FIX.md` and use the copy-paste fixes provided there.
- **If 0 errors**: Proceed to generation.

## Step 4: Generate the Workspace
Generate the libraries and workspace code.
```bash
cargo-teaql gen-lib model.xml
cargo-teaql gen-workspace model.xml
```
*Note: Never manually edit files inside the generated folders (`generate-lib/` or `generate-workspace/` or `bizcore/`).*

## Step 5: Write the Code
After generating, reference the API pattern document for your target language to write correct queries and updates:
- **Java**: Read `reference/API-PATTERN-JAVA.md`
- **Rust**: Read `reference/API-PATTERN-RUST.md`

Make sure you always include `.purpose()` / `.comment()` for queries, and `.audit_as()` / `.auditAs()` for updates.

Read `generate-lib/AGENTS.md` for workspace-specific rules if generated.
Finally, run checks to ensure correctness:
```bash
cargo check && cargo test
```
