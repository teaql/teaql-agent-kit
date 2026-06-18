# TEAQL Agent Kit - Autonomous Branch

This branch is for no-gate evaluation of coding agents and language models on
TEAQL-based business software tasks.

Agents attempt tasks fully automatically, without human intervention
checkpoints.

The goal is to observe agent behavior, measure autonomy, discover unsafe
shortcuts, and identify the guardrails needed before production use.

This branch is for benchmarking and stress-testing autonomous coding agents. It
is not a recommendation for ungated production deployment.

## Branch Purpose

The `autonomous` branch complements the controlled evaluation flow on `main`.

The main branch asks:

> What can a coding agent do when the rules are clear and the evaluation is
> controlled?

The autonomous branch asks:

> What does a coding agent actually do when no human gate is present?

This distinction matters because long-lived business software depends on more
than a successful compile. It also depends on business semantics, generated API
discipline, auditability, error recovery, framework boundaries, and
maintainability.

## Repository Structure

```text
README.md
AUTONOMOUS_DESIGN.md

tasks/
  task-001-faceted-query.md
  task-002-audit-safe-status-update.md
  task-003-e-chain-diagnostic-repair.md
  task-004-generated-api-regeneration.md
  task-005-search-with-text.md

runs/
  claude-code/
  cursor-agent/
  codex/
  aider/
  local-llm/

evaluation/
  scorecard-template.md
  metrics-schema.json
  report-template.md
```

Historical evaluation reports and long-form background material live in the
separate repository `/Users/Philip/githome/teaql-evaluation-reports`. This
repository is the current execution guide for AI coding agents.

## Evaluation Rules

- Start from a stable task file in `tasks/`.
- Give the agent only the planned initial context.
- Do not provide hints, API corrections, edited code, or new business knowledge
  after execution starts.
- If human intervention occurs, record it in the run scorecard.
- Preserve evidence in `runs/<agent>/<task-id>/<run-date>/`.
- Score the run with `evaluation/scorecard-template.md`.
- Publish evidence-first summaries in `/Users/Philip/githome/teaql-evaluation-reports`.

## Evaluation Focus

Autonomous runs are scored across dimensions such as:

- Functional completion
- Compile success
- Test pass rate
- API adherence
- Hallucinated API count
- Audit coverage
- Framework discipline
- Error recoverability
- Human intervention count
- Token usage
- Unsafe shortcut count

## Production Interpretation

No-gate evaluation is not a production promise. It is how this project discovers
what production guardrails must exist.

The long-term path is measured automation:

1. Evaluate agent behavior.
2. Identify safe and unsafe task classes.
3. Define gates and guardrails.
4. Introduce controlled automation.
5. Preserve auditability and human accountability.
