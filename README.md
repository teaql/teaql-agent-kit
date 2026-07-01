# TEAQL Agent Kit

> **AI agents:** this README is for human readers. Do not use it as execution
> guidance. For modeling, generation, debugging, or implementation work, read
> `AGENTS.md` and the focused files under `agents/`, `modeling/`, and
> `playbooks/` instead.

**TEAQL Agent Kit** is an evaluation environment for coding agents and language
models working on auditable business software tasks.

It tracks two kinds of engineering effort:

* **Software engineering discipline**: preserving business semantics, following
  generated API contracts, respecting framework boundaries, keeping audit traces,
  and recovering from errors without unsafe shortcuts.
* **Token efficiency discipline**: giving agents compact rules, generated local
  guides, object-specific assist output, and evaluation reports so they spend
  fewer tokens guessing, rereading, or exploring irrelevant source.

---

## What This Repository Is

This repository is focused on **evaluation**.

It provides tasks, prompts, guides, and reports for observing how coding agents behave when working with TEAQL-based business software.

The current goal is not ungated production automation.

The current goal is to answer two practical questions:

> How do coding agents behave when business rules, generated APIs, audit traces,
> and framework boundaries matter?

> How much context can be saved when the repository gives agents the right
> generated contracts, focused guides, and machine-readable feedback at the right
> time?

---

## Main Branch: Controlled Evaluation

The `main` branch is the primary entry point.

It is used for controlled and reproducible evaluation, with:

* Clear task definitions
* Explicit TEAQL API rules
* Agent-readable guides
* Generated local contracts and object-specific assist commands
* Markdown evaluation reports for targeted error repair
* Optional human checkpoints
* Comparable evaluation reports

This branch asks:

> What can a coding agent do when software engineering rules are clear,
> generated contracts are available, and context is spent deliberately?

---

## Autonomous Branch: No-Gate Evaluation

The `autonomous` branch is for experimental no-gate evaluation.

It is used to observe how far coding agents can go without human intervention checkpoints.

This branch focuses on:

* Fully automatic task attempts
* Self-repair behavior
* Unsafe shortcuts
* Framework boundary violations
* Token usage
* Guardrails that may be needed before production use

The autonomous branch is for benchmarking and stress-testing.
It is not a recommendation for ungated production deployment.

This branch asks:

> What does a coding agent actually do when no human gate is present?

---

## Evaluation Focus

TEAQL Agent Kit evaluates agents across dimensions such as:

* Functional completion
* API adherence
* Hallucinated API count
* Audit coverage
* Framework discipline
* Error recoverability
* Human intervention count
* Token efficiency

For long-lived business software, these dimensions matter as much as whether the
code compiles.

The token-efficiency work is part of the same evaluation, not a separate
optimization. Agents should use short execution guides, generated `AGENTS.md`
files, assist commands, and Markdown reports before falling back to broad source
reading. A good run should leave evidence that the agent used the smallest
reliable context needed to make the change.

---

## Reports

Evaluation reports will be published in this repository.

Reports may include controlled and autonomous runs across different coding agents, language models, and TEAQL stacks.

---

## Evaluation Across Stacks

TEAQL Agent Kit may evaluate equivalent business software tasks across different TEAQL implementations, including:

- TEAQL Java stack
- TEAQL Rust stack

The purpose is not to rank programming languages.

The purpose is to understand how coding agents preserve semantics, auditability, and framework boundaries across different implementation stacks.

---

## Long-Term Direction

Today, TEAQL Agent Kit evaluates coding agents.

Long term, the same evidence may help define which AI coding tasks can be safely automated, which require human gates, and which should never bypass review.

The goal is measured automation, not blind automation.
