# Evaluation Report #001 — Environment

---

## Purpose

The evaluation was conducted on a commodity developer laptop rather than a high-end workstation or cloud GPU environment. Goal: observe whether the TeaQL workflow, generated code, audit trail, and runtime behavior remain practical on ordinary engineering hardware.

## Hardware Environment

- **Device:** MacBook Pro (Retina, Mid 2015)
- **CPU:** Intel Core i7-4770HQ @ 2.20GHz (x86_64)
- **Memory:** 16 GB RAM
- **Storage:** Local SSD
- **Dedicated GPU:** Not used
- **Cloud acceleration:** Not used

## System Environment

- **Operating System:** macOS (Darwin)
- **Shell:** zsh
- **Rust toolchain:** rustc 1.94.1 (e408947bf 2026-03-25)
- **Cargo:** 1.94.1
- **SQLite:** System default (via sqlx 0.8)
- **Git:** System default

## Evaluation Software

| Component | Version | Source |
|-----------|---------|--------|
| `cargo-teaql` CLI | 0.2.0 | `cargo-teaql --version` |
| teaql-core | 3.2.2 | Cargo.lock |
| teaql-runtime | 3.2.2 | Cargo.lock |
| teaql-sql | 3.2.2 | Cargo.lock |
| teaql-macros | 3.2.2 | Cargo.lock |
| teaql-data-service | 3.2.2 | Cargo.lock |
| teaql-provider-sqlx-sqlite | 3.2.2 | Cargo.lock |
| teaql-tool-core | 1.0.0 | Cargo.lock |

## Code Generation Endpoint

- **Primary:** `https://api.teaql.io/latest/generate` (default, used for code generation)
- **Custom:** `http://t420.doublechaintech.cn:23380` (returned HTTP 500 during evaluation)

## Agent Information

- **Agent:** WorkBuddy (CodeBuddy AI Assistant)
- **Model:** mimo-v2.5-pro
- **Evaluation date:** 2026-06-08 to 2026-06-09

## Raw Evaluation Records

Raw evaluation logs, prompts, code changes, build and runtime logs, and SQL/audit traces are available at:

[GitHub Raw Data](https://github.com/teaql/teaql-agent-kit/tree/autonomous/reports/evaluation-report-001/raw/)
