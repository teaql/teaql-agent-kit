# Documentation Redesign Proposal: AI as the Primary User

**Status:** Proposal  
**Priority:** Critical  
**Source:** evaluation-report-003 (183-object Moving Company Management System)  
**Date:** 2026-06-11

---

## Problem Statement

Current TeaQL documentation is written for human developers. In evaluation-report-003, the AI agent successfully built a 183-object system by reading these documents. But the process revealed that documentation written for humans creates friction for AI agents:

1. AI reads everything sequentially — long documents waste tokens
2. AI needs structured rules, not narrative explanations
3. AI needs copy-paste examples, not conceptual descriptions
4. AI cannot ask clarifying questions — documentation must be unambiguous

**Goal:** Redesign documentation so AI can consume it faster, understand it more accurately, and produce better output with fewer iterations.

---

## Current Documentation Structure

```
AGENTS.md                    # Agent entry instructions
TECH-INTRODUCTION.md         # Framework overview (long)
prompts/modeling/
  system.md                  # Role prompt
  task-template.md           # Task frame
  ksml-rules.md              # Modeling rules (source of truth)
  checklist.md               # Validation checklist
playbooks/
  model-from-natural-language.md
  model-review-gate.md
  generate-with-toolchains.md
```

### What works:
- `ksml-rules.md` is well-structured with clear rules
- `checklist.md` provides validation points
- `AGENTS.md` sets clear boundaries

### What doesn't work:
- `TECH-INTRODUCTION.md` is too long — AI reads it all, wastes context
- Narrative explanations mixed with rules — AI can't separate them
- No copy-paste templates for common patterns
- No "if error X, do Y" lookup tables

---

## Proposed Documentation Principles

### Principle 1: Rules Before Narrative

**Current (narrative-first):**
```
TeaQL is a semantic development system built around domain modeling...
The core value is: Semantic Guardrails for AI Coding...
You describe the domain once: entities, fields, relationships...
```

**Proposed (rules-first):**
```
## RULES (read this first)

1. Every business object must have _name, _module, _module_key
2. Constant objects must have id="id()", name="string()", code="string()"
3. Never use id="id()" on business objects
4. References use object_name() directly, not object(object_name)
5. [20 more rules...]

## EXAMPLES (read after rules)

### Business object example
<employee _name="Employee" _module="..." .../>

### Constant object example  
<move_status _name="Move Status" _module="..." id="id()" name="string()" code="string()" _constant="true" _identifier="code">

## NARRATIVE (optional, for understanding context)
TeaQL is a semantic development system...
```

### Principle 2: Copy-Paste Templates

For every common pattern, provide a ready-to-use template:

```xml
<!-- TEMPLATE: Business Object -->
<{entity_name} _name="{Display Name}"
               _module="{Module Name}"
               _module_key="{module-key}"
               {field}="{value}"
               merchant="merchant(context)"
               create_time="createTime()"
               update_time="updateTime()"/>

<!-- TEMPLATE: Constant Object -->
<{constant_name} _name="{Display Name}"
                 _module="{Module Name}"
                 _module_key="{module-key}"
                 id="id()" name="string()" code="string()"
                 platform="platform()"
                 _constant="true" _identifier="code">
  <_value id="1001" name="{Value Name}" code="{VALUE_CODE}"/>
</{constant_name}>

<!-- TEMPLATE: Reference Field -->
{relation_name}="{relation_name}()"  <!-- business object reference -->
{status_field}="{constant_name}()"   <!-- constant reference -->
```

### Principle 3: Error → Fix Lookup Tables

```markdown
## ERROR REFERENCE

| Error | Meaning | Fix |
|-------|---------|-----|
| Empty attribute | Attribute has no value | Delete it or fill with concrete value |
| Missing root ref | Constant not linked to root | Add platform="platform()" |
| Depth exceeded | Too many nested references | Remove one reference or use string field |
| Sensitive field | Token/key/password detected | Add _audit_mask_fields="field_name" |
| Disconnected graph | Entity not connected to root | Add merchant="merchant(context)" |
```

### Principle 4: Decision Trees

Instead of explaining all options, give AI a decision path:

```markdown
## CHOOSING YOUR DOMAIN ROOT

Does the system have a platform/operator managing multiple organizations?
  YES → Use "platform" as root
  NO → Does it have a company/merchant/tenant?
    YES → Use that as root
    NO → Use the main business entity as root

## CHOOSING TENANCY MODEL

Is this a single-tenant system?
  YES → Do not add merchant="merchant(context)"
  NO → Is there a clear tenant owner (merchant, company, school)?
    YES → Add {tenant_owner}="merchant(context)" to tenant-owned objects
    NO → Ask the user to clarify
```

---

## Proposed Documentation Structure

```
agents/
  RULES.md                    # 50 hard rules, no narrative
  TEMPLATES.md                # Copy-paste XML templates
  ERROR-FIX.md                # Error → Fix lookup table
  DECISION-TREES.md           # Decision paths for common choices
  
modeling/
  KSML-RULES.md               # Current rules, restructured
  CHECKLIST.md                # Current checklist
  EXAMPLES/
    business-object.md        # 10 complete examples
    constant-object.md        # 10 complete examples
    relationship.md           # 10 relationship patterns
    module-layout.md          # Module organization examples

playbooks/
  QUICK-START.md              # 5-minute guide for AI
  MODEL-FROM-NL.md            # Current playbook, restructured
  MODEL-REVIEW.md             # Current review gate
  GENERATE.md                 # Current generation workflow

reference/
  API-PATTERN.md              # Q/E API patterns with examples
  AUDIT-PATTERN.md            # comment/purpose/audit_as patterns
  SENSITIVE-FIELDS.md         # Field masking rules
```

---

## Specific Improvements

### AGENTS.md: Make it machine-first

**Current opening:**
```markdown
# TeaQL Rust Workspace Instructions

> [!WARNING]
> **PARADIGM SHIFT WARNING: DO NOT GUESS METHOD NAMES**
> TeaQL was explicitly designed to PREVENT AI hallucinations...
```

**Proposed opening:**
```markdown
# AGENTS.md — Rules for AI Agents

## READ THIS BEFORE CODING

1. Never guess method names — read generated source code
2. Never edit files under generate-lib/
3. Every query needs .comment() and .purpose()
4. Every save needs .audit_as()
5. [5 more hard rules]

## IF YOU GET AN ERROR

| Error type | What to do |
|-----------|------------|
| `no method named update_xxx` | Read the entity source file for correct method name |
| `Missing .audit_as()` | Add .audit_as("description") before .save() |
| `Missing .purpose()` | Add .purpose("why") before .execute_for_list() |
```

### KSML-RULES.md: Separate rules from explanations

**Current (mixed):**
```markdown
### Explicit Tenancy Rule
KSML models must not assume multi-tenancy by default.
Tenancy is an explicit architectural choice. When modeling a domain, determine
whether the target system is single-tenant, multi-tenant, platform-managed
multi-tenant, or undecided. Do not add `merchant`, `tenant`, `platform`...
```

**Proposed (rules separated):**
```markdown
## TENANCY RULES (hard)

1. Do NOT add merchant/platform/tenant unless explicitly needed
2. Single-tenant: no tenant boundary fields
3. Multi-tenant: add {tenant_owner}="merchant(context)" to tenant-owned objects
4. Record tenancy assumption in model review

## TENANCY EXPLANATION (context)

KSML models must not assume multi-tenancy by default...
[existing explanation]
```

### QUICK-START.md: 5-minute AI guide

```markdown
# TeaQL Quick Start for AI Agents

## Step 1: Read rules
Read RULES.md (50 rules, 2 minutes)

## Step 2: Create model
Use TEMPLATES.md to create model.xml
Follow DECISION-TREES.md for root and tenancy choices

## Step 3: Validate
Run: cargo-teaql eval model.xml
If errors: look up in ERROR-FIX.md
If 0 errors: proceed

## Step 4: Generate
Run: cargo-teaql gen-lib model.xml
Run: cargo-teaql gen-workspace model.xml

## Step 5: Code
Read generate-lib/AGENTS.md
Write queries using API-PATTERN.md
Run: cargo check && cargo test
```

---

## Expected Impact

| Metric | Current | After Redesign |
|--------|---------|----------------|
| Time to first model | 30+ minutes | 5 minutes |
| Iterations to 0 errors | 5 | 1-2 |
| Token usage for documentation | ~50k | ~15k |
| AI comprehension accuracy | ~70% | ~95% |

---

## Proposed Tool: `teaql query` CLI

### Problem

Even with improved documentation, AI agents must still:
1. Read documentation to understand API patterns
2. Guess which methods exist on which entities
3. Try to compile, fail, read generated source, retry

This is the #1 cause of compilation errors (e.g., `vehicle_statuses` vs `vehicle_status`).

### Solution: Entity-Specific Code Generation CLI

```bash
teaql query <entity> <operation>
```

### Operations

| Operation | Description | Output |
|-----------|-------------|--------|
| `create` | Create new entity | `new_entity()` + field updates + `audit_as().save()` |
| `query` | Query entity list | `Q::<entities>()` + filters + `execute_for_list()` |
| `query-one` | Query single entity | `Q::<entities>()` + filter + `execute_for_one()` |
| `update` | Update entity fields | Load + `update_field()` + `audit_as().save()` |
| `delete` | Soft delete entity | Load + `mark_as_delete()` + `audit_as().save()` |
| `stats` | Aggregation query | `Q::<entities>()` + count/sum/group |
| `relations` | List all relations | Show all loaded and filtered relations |
| `fields` | List all fields | Show all fields with types and references |
| `constants` | List constant values | Show all `_value` entries for constant objects |

### Examples

```bash
# Create an employee
teaql query employee create
```

Output:
```rust
// Create new employee
use moving_company_service::{Q, E};

let mut employee = Q::employees()
    .purpose("Create new employee")
    .new_entity(&ctx);

employee.update_name("Wang Fang");
employee.update_employee_number("EMP-2024-001");
employee.update_phone("13900139001");
employee.update_email("wangfang@swiftmove.com");
employee.update_id_card_number("110108199005151234");
employee.update_hire_date("2024-01-15");
employee.update_address("Beijing Chaoyang District");
employee.update_emergency_contact("Li Ming");
employee.update_emergency_phone("13800138002");
employee.update_photo_url("/img/employees/emp-001.jpg");
// References (set one):
// employee.update_gender_to_male();
// employee.update_employment_status_to_active();
// employee.update_job_position_to_moving_specialist();
// employee.update_department(...);

employee.audit_as("Register new employee").save(&ctx).await?;
```

```bash
# Query employees with department
teaql query employee query
```

Output:
```rust
// Query employees with relations
use moving_company_service::{Q, E};

let employees = Q::employees()
    .select_self()
    .select_department_with(Q::departments().select_self())
    .select_gender_with(Q::genders().select_self())
    .select_employment_status_with(Q::employment_statuses().select_self())
    .select_job_position_with(Q::job_positions().select_self())
    .comment("Load employees with relations")
    .purpose("Employee directory")
    .execute_for_list(&ctx)
    .await?;
```

```bash
# Query employees filtered by status
teaql query employee query --filter status=active
```

Output:
```rust
// Query active employees
let employees = Q::employees()
    .select_self()
    .with_employment_status_is_active()
    .comment("Load active employees")
    .purpose("Active employee list")
    .execute_for_list(&ctx)
    .await?;
```

```bash
# Show all fields for employee
teaql query employee fields
```

Output:
```
Entity: employee
Table: employee_data
Fields:
  - name: String ("Wang Fang")
  - employee_number: String ("EMP-2024-001")
  - phone: String ("13900139001")
  - email: String ("wangfang@swiftmove.com")
  - id_card_number: String ("110108199005151234")
  - hire_date: Date ("2024-01-15")
  - address: String ("Beijing Chaoyang District")
  - emergency_contact: String ("Li Ming")
  - emergency_phone: String ("13800138002")
  - photo_url: String ("/img/employees/emp-001.jpg")
  - create_time: DateTime (createTime())
  - update_time: DateTime (updateTime())
References:
  - gender → gender()
  - employment_status → employment_status()
  - job_position → job_position()
  - department → department()
  - merchant → merchant(context)
```

```bash
# Show all relations for employee
teaql query employee relations
```

Output:
```
Entity: employee
Parent relations (N:1):
  - merchant → merchant
  - gender → gender
  - employment_status → employment_status
  - job_position → job_position
  - department → department

Child relations (1:N):
  - work_assignments → work_assignment[]
  - worked_hours → worked_hours[]
  - bonuses → bonus[]
  - leave_requests → leave_request[]
  - employee_certifications → employee_certification[]
  - employee_schedules → employee_schedule[]

Loaded via:
  .select_department_with(Q::departments().select_self())
  .select_gender_with(Q::genders().select_self())
  ...
```

### Benefits for AI Agents

1. **No documentation reading needed** — CLI outputs exact code
2. **No method guessing** — all field names from model
3. **No compilation errors** — code is generated from model
4. **Copy-paste ready** — output is valid Rust code
5. **Instant feedback** — change model, re-run CLI, get updated code

### Implementation

Add to `cargo-teaql`:

```bash
cargo teaql query <model.xml> <entity> <operation> [--filter field=value]
```

The CLI reads the model.xml, looks up the entity definition, and generates the exact TeaQL code pattern.

### Expected Impact

| Metric | Current | With `teaql query` |
|--------|---------|-------------------|
| Time to write query code | 10-15 minutes | 30 seconds |
| Compilation errors | 2-5 per query | 0 |
| Documentation dependency | High | None |
| AI agent autonomy | Medium | High |

---

## Implementation Plan

### Phase 1: Restructure existing content (1 week)
- [ ] Extract all rules from narrative documents into RULES.md
- [ ] Create copy-paste templates from existing examples
- [ ] Build error → fix lookup table from evaluation data
- [ ] Write decision trees for root, tenancy, module choices

### Phase 2: Create AI-first documents (1 week)
- [ ] Write QUICK-START.md for AI agents
- [ ] Restructure AGENTS.md with rules first
- [ ] Create API-PATTERN.md with complete examples
- [ ] Add copy-paste examples to every rule

### Phase 3: Validate with AI (1 week)
- [ ] Run AI agent on new documentation
- [ ] Measure iterations to 0 errors
- [ ] Collect feedback on comprehension
- [ ] Refine based on failure patterns

---

## Evidence

This proposal is based on actual AI agent behavior from:
- **Report:** evaluation-report-003
- **Model:** 183 objects, 12 modules
- **Documentation read:** AGENTS.md, TECH-INTRODUCTION.md, ksml-rules.md, checklist.md, playbooks
- **Iterations to success:** 5 rounds
- **Raw data:** `reports/evaluation-report-003/raw/`

The AI agent succeeded by reading human-oriented documentation. It would succeed faster and more reliably with AI-oriented documentation.
