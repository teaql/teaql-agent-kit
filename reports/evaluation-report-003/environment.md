# Evaluation Environment — Report 003

## Hardware

- **Device:** Linux Developer Machine
- **CPU:** x86_64
- **Memory:** Standard configuration
- **Storage:** Local SSD
- **Dedicated GPU:** Not used
- **Cloud acceleration:** Not used

## System

- **Operating System:** Ubuntu (Linux 6.8.0-106-generic)
- **Shell:** bash
- **Rust toolchain:** rustc 1.94.0 (4a4ef493e 2026-03-02)
- **Cargo:** 1.94.0 (85eff7c80 2026-01-15)
- **SQLite:** Embedded (rusqlite v0.32.1)
- **Git:** 2.43.0

## Evaluation Software

- **TeaQL Rust version:** v4.0.3 (teaql-core, teaql-runtime, teaql-sql)
- **cargo-teaql version:** v0.2.3
- **Agent:** MiMo Code Agent (mimo-auto)
- **Model provider:** Xiaomi MiMo Team
- **Model version:** mimo/mimo-auto
- **Evaluation date:** 2026-06-11

## TeaQL Endpoint

- **Code generation endpoint:** http://t420.doublechaintech.cn:23380
- **Environment variable:** TEAQL_ENDPOINT_PREFIX

## Project Structure

```
~/workspace/A-004/app-playground/
  models/
    model.xml                    # 183 objects, 2635 lines
  generate-lib/
    lib/                         # 189 source files
    AGENTS.md
    API_GUIDE.md
    TOOL_API.md
  rust-workspace/
    src/
      lib.rs                     # 15 test functions
      main.rs                    # Smoke test
    AGENTS.md
    Cargo.toml
```
