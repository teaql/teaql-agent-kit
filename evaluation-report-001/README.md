# Evaluation Report #001

**Project:** TeaQL School Management System
**Report Type:** Practical Coding Agent Evaluation
**Date:** 2026-06-09
**Report Series:** #001

---

## Overview

This report evaluates the TeaQL framework through a practical implementation exercise: building a school management system with Platform, School, and SchoolType domain entities using Rust and the TeaQL code generation framework.

## Report Contents

| File | Description |
|------|-------------|
| `README.md` | This file — report overview and navigation |
| `environment.md` | Hardware, software, and evaluation environment |
| `task.md` | Task specification and execution methodology |
| `model-output.md` | Semantic model, generated code, and API analysis |
| `scoring.md` | Scoring dimensions, results, and evidence |
| `assets/report-cover.html` | Printable report cover page |
| `raw/` | Raw evaluation data (logs, traces, prompts) |

## Key Findings

- **Composite Score:** 7.9 / 10
- **Semantic Modeling:** 9.0 — 28 lines of KSML XML define the complete domain
- **API Design:** 8.5 — Q/E dual facade with constant shortcuts
- **Code Generation:** 8.0 — 8,165 lines from 28 lines; 1 doc-code inconsistency found
- **Runtime:** 7.0 — Full-featured but heavy dependencies with sqlx

## Evidence Chain

- **Website:** [TeaQL](https://teaql.io)
- **Open-Source Project:** [TeaQL Agent Kit](https://github.com/teaql/teaql-agent-kit)
- **Raw Data:** [GitHub Raw Data](https://github.com/teaql/teaql-agent-kit/tree/autonomous/reports/evaluation-report-001/raw/)
- **Code Generation Server:** [teaql-forge-rs](https://github.com/teaql/teaql-forge-rs) (Apache-2.0)
