# Evaluation Environment

## Hardware

| Component | Detail |
|-----------|--------|
| Device | MacBook Pro (Mid 2015) |
| Model | MacBookPro11,4 |
| CPU | Intel Core i7 (Quad-Core) |
| Memory | 16 GB RAM |
| Storage | Local SSD |
| GPU | Intel integrated (not used) |
| Cloud | Not used |

## Software

| Component | Version |
|-----------|---------|
| OS | macOS 12.7.6 (Monterey) |
| Shell | zsh |
| Rust | rustc 1.94.1 (2026-03-25, Homebrew) |
| Cargo | 1.94.1 (Homebrew) |
| SQLite | 3.51.3 (bundled via libsqlite3-sys) |
| Git | 2.37.1 (Apple Git-137.1) |

## TeaQL Stack

| Component | Version |
|-----------|---------|
| cargo-teaql | 1.0.0 (from crates.io) |
| teaql-core | 4.0.3 |
| teaql-macros | 4.0.3 |
| teaql-runtime | 4.0.3 |
| teaql-sql | 4.0.3 |
| teaql-data-service | 4.0.3 |
| teaql-tool-core | 1.0.0 |
| teaql-provider-sqlite | 4.0.3 (rusqlite 0.32.1, bundled) |
| tokio | 1.52.3 |

## Agent

| Component | Detail |
|-----------|--------|
| Agent | QClaw (OpenClaw) with lossless-claw context management |
| Model | Pooled DeepSeek V4 Flash |
| Evaluation mode | Autonomous (no-gate) |
| Evaluation date | 2026-06-15 |
