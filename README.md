# TEAQL Agent Kit

**TEAQL Agent Kit** is an evaluation environment for coding agents and language models on auditable business software tasks.

It is designed to measure not only whether generated code works, but also whether an agent can preserve business semantics, follow framework boundaries, maintain auditability, recover from errors, and use tokens efficiently.

---

## What This Repository Is

This repository is focused on **evaluation**.

It provides tasks, prompts, guides, and reports for observing how coding agents behave when working with TEAQL-based business software.

The current goal is not ungated production automation.

The current goal is to answer a more basic question:

> How do coding agents actually behave when business rules, generated APIs, audit traces, and framework boundaries matter?

---

## Main Branch: Controlled Evaluation

The `main` branch is the primary entry point.

It is used for controlled and reproducible evaluation, with:

* Clear task definitions
* Explicit TEAQL API rules
* Agent-readable guides
* Optional human checkpoints
* Comparable evaluation reports

This branch asks:

> What can a coding agent do when the rules are clear and the evaluation is controlled?

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

For long-lived business software, these dimensions matter as much as whether the code compiles.

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

