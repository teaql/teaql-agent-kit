# Evaluator Improvement Proposal: Actionable Error Messages for AI Agents

**Status:** Proposal  
**Priority:** High  
**Source:** evaluation-report-003 (183-object Moving Company Management System)  
**Date:** 2026-06-11

---

## Problem Statement

The current evaluator produces errors that require multiple iterations for AI agents to resolve. In evaluation-report-003, the agent required **5 rounds** of fix cycles to go from 96 errors to 0. Each round involved:

1. Running `cargo-teaql eval`
2. Parsing the error output
3. Understanding what the error means
4. Guessing the correct fix
5. Applying the fix
6. Re-running eval

**Target:** Reduce to **1-2 rounds** by making every error message self-contained and immediately actionable.

---

## Current State Analysis

### Error Category 1: Empty Attributes

**Current output:**
```
Attribute 'resolution_notes' of object 'damage_report' is empty at line 348.
Empty values are not allowed.
```

**Problem:** AI does not know whether to remove the attribute or provide a value.

**Proposed output:**
```
ERROR: Empty attribute 'resolution_notes' in 'damage_report' (line 348)
FIX: Remove the attribute entirely, or provide a concrete value.
EXAMPLE FIX: Change to resolution_notes="Repaired by team" or delete the attribute.
RULE: Business object attributes must have concrete values, not empty strings.
```

### Error Category 2: Constant Object Missing Root Reference

**Current output:**
```
Constant object 'merchant_status' must be associated with the root object.
For example, add platform="platform()" to the definition.
```

**Problem:** This is already close to actionable, but when 96 errors appear together, AI misses it.

**Proposed output:**
```
ERROR: Constant object 'merchant_status' has no reference to domain root 'platform' (line 245)
FIX: Add platform="platform()" to the <merchant_status> tag.
COPY-PASTE:
  <merchant_status _name="Merchant Status"
                   _module="Platform"
                   _module_key="platform"
                   platform="platform()"
                   id="id()" name="string()" code="string()"
                   _constant="true" _identifier="code">
```

**Additional improvement:** When multiple constants have the same error, batch them:
```
ERROR: 38 constant objects missing 'platform="platform()"' reference.
AFFECTED OBJECTS: merchant_status, merchant_type, move_status, move_type, ...
FIX: Add platform="platform()" to all constant objects.
AUTOFIX AVAILABLE: Run cargo-teaql fix --add-root-ref to auto-add the attribute.
```

### Error Category 3: Sensitive Field Masking (Truncated)

**Current output:**
```
The field 'password_hash' in entity 'user_account' contains highly sensitive keywords.
You MUST mask it.
Fix Example: Update your XML entity definition:
<user_account ... _audit_mask_fields="password_
```

**Problem:** Fix example is truncated. AI cannot see the complete fix.

**Proposed output:**
```
ERROR: Sensitive field 'password_hash' in 'user_account' requires audit masking (line 789)
FIX: Add _audit_mask_fields attribute to the entity tag:
  <user_account _audit_mask_fields="password_hash" ...>
RULE: Fields containing tokens, keys, passwords, secrets, or credentials must be masked.
COMPLETE LIST: Add all sensitive fields in one attribute:
  _audit_mask_fields="password_hash,token,secret_key"
```

### Error Category 4: Reference Chain Depth Exceeded

**Current output:**
```
find with OD: 'insurance_claim' reaches 20
```

**Problem:** Completely opaque to AI. No guidance on what to fix.

**Proposed output:**
```
ERROR: Entity 'insurance_claim' reference chain depth exceeds limit of 20
CHAIN: insurance_claim → move_order → customer → customer_type → platform
        insurance_claim → damage_report → inventory_item → move_order → ...
FIX: Remove one deep reference from 'insurance_claim':
  OPTION A: Remove damage_report="damage_report()" (depth 3 saved)
  OPTION B: Remove insurance_policy="insurance_policy()" (depth 2 saved)
  OPTION C: Replace object references with string fields:
    damage_reference="DR-2024-001" instead of damage_report="damage_report()"
SUGGESTATION: Prefer string fields for references that do not need relation loading.
```

### Error Category 5: Disconnected Entity Graph

**Current output:**
```
Multiple independent business objects found: platform, merchant, permission, api_endpoint.
The model may have disconnected graphs.
```

**Problem:** Warning only. No guidance on which entities are disconnected or how to connect them.

**Proposed output:**
```
WARNING: Disconnected entity graph detected
DISCONNECTED ENTITIES:
  - 'permission' (no outgoing reference to other business objects)
  - 'api_endpoint' (no outgoing reference to other business objects)
FIX: Add a reference to connect each entity to the main graph:
  permission: Add merchant="merchant(context)" or platform="platform()"
  api_endpoint: Add merchant="merchant(context)" or platform="platform()"
```

### Error Category 6: Finite Set Field Without Constant Reference

**Current output:**
```
Field 'status' in 'automation_template' represents a finite set
and should preferably reference a constant object.
```

**Problem:** "Should preferably" is too weak. AI ignores warnings.

**Proposed output:**
```
WARNING: Field 'status' in 'automation_template' (line 1234) is a plain string
but appears to represent a finite set (boolean-like, status-like, type-like).
CURRENT VALUE: status="active"
RECOMMENDATION: Create a constant object or use an existing one:
  OPTION A: Create <automation_template_status> with values ACTIVE/INACTIVE
  OPTION B: Reuse existing <service_status> if semantically appropriate
  OPTION C: Keep as string if values are truly free-form
```

---

## Output Format Improvement

### Current: Flat JSON list

```json
{"errors":[{"ruleId":"KSML-CONSTANT-002","message":"..."},{"ruleId":"KSML-CONSTANT-002","message":"..."}]}
```

96 errors in a flat list. AI processes them sequentially. No grouping. No priority.

### Proposed: Grouped by severity and type

```
=== EVALUATION RESULT ===
FATAL ERRORS (must fix before generation): 3
  [EMPTY-ATTRIBUTE] 12 instances
  [MISSING-ROOT-REF] 38 instances  
  [SENSITIVE-FIELD] 14 instances

WARNINGS (should fix, do not block generation): 66
  [DISCONNECTED-GRAPH] 4 entities
  [FINITE-SET-NO-CONSTANT] 3 fields

SUGGESTIONS (optional improvements): 179
  [UI-COLOR] 40 constants
  [LOG-MARKER] 5 entities

=== AUTOFIX AVAILABLE ===
Run: cargo-teaql fix --add-root-ref --remove-empty
This will fix 50 of 66 errors automatically.
```

### Key improvements:
1. **Group by rule ID** — AI can fix one pattern across all instances
2. **Count instances** — AI knows the scale of each fix
3. **Separate fatal from warning** — AI prioritizes correctly
4. **Offer autofix** — For mechanical fixes, let the tool fix them

---

## Error Message Template

Every error should follow this template:

```
ERROR: [RULE-ID] [Short description]
  Entity: [entity_name] (line [N])
  Field: [field_name]
  Problem: [What is wrong]
  Fix: [Exact change needed]
  Copy-paste: [Ready-to-use XML/code]
  Rule: [Why this rule exists]
```

Every warning should follow this template:

```
WARNING: [RULE-ID] [Short description]
  Entity: [entity_name] (line [N])
  Field: [field_name]
  Current: [Current state]
  Recommendation: [What to do]
  Options: [A/B/C choices]
```

---

## Priority Implementation

### Phase 1: Immediate (1-2 days)
- [ ] Truncate no more: show complete fix examples
- [ ] Batch identical errors: "38 constants missing root ref"
- [ ] Add copy-paste XML to every error
- [ ] Add autofix command for mechanical fixes

### Phase 2: Short-term (1 week)
- [ ] Group output by severity (fatal → warning → suggestion)
- [ ] Add entity line numbers to every message
- [ ] Show reference chain depth with full path
- [ ] Show disconnected graph components

### Phase 3: Medium-term (2 weeks)
- [ ] Add "Rule: [explanation]" to every error
- [ ] Add "Options: A/B/C" to every warning
- [ ] Implement `cargo-teaql fix` command for common patterns
- [ ] Add model diff view after each fix round

---

## Expected Impact

| Metric | Current | After Improvement |
|--------|---------|-------------------|
| Rounds to 0 errors | 5 | 1-2 |
| AI comprehension | Low (opaque messages) | High (self-contained fixes) |
| Human intervention | Sometimes needed | Never needed |
| First-model success rate | ~20% | ~80% |

---

## Evidence

This proposal is based on actual evaluation data from:
- **Report:** evaluation-report-003
- **Model:** 183 objects, 12 modules
- **Initial errors:** 96
- **Fix iterations:** 5
- **Raw data:** `reports/evaluation-report-003/raw/`

Every proposed improvement addresses a real error that caused a real iteration in the evaluation.
