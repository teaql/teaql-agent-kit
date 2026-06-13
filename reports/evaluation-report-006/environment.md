# 评估环境

## 评估目的
本次评估在普通开发者笔记本电脑上进行，非高端工作站或云端 GPU 环境。目的：观察 Agent 工作流、生成代码、审计追踪在常规工程硬件上是否实用。

## 硬件环境

| 项目 | 规格 |
|------|------|
| 设备 | MacBook Pro (MacBookPro16,2) |
| CPU | Intel Core i5 (x86_64) |
| 内存 | 16 GB RAM |
| 存储 | 本地 SSD |
| 专用 GPU | 未使用 |
| 云端加速 | 未使用 |

## 系统环境

| 项目 | 版本 |
|------|------|
| 操作系统 | macOS 12.7.6 (Monterey) |
| Shell | zsh |
| Rust 工具链 | rustc 1.94.1 (Homebrew) |
| Cargo | 1.94.1 (Homebrew) |
| SQLite | 3.51.3 |
| Git | 2.37.1 (Apple Git-137.1) |

## 评估软件

| 项目 | 版本 |
|------|------|
| TeaQL CLI | 1.0.0 |
| TeaQL Rust Runtime | 4.0.3 |
| TeaQL Agent Kit | autonomous 分支 (reports/evaluation-report-006) |
| Agent | OpenClaw (QClaw) |
| 模型 | DeepSeek V4 (qclaw/pool-deepseek-v4-flash) |
| 评估日期 | 2026-06-13 |

## 原始评估记录
原始评估日志、Prompt、代码变更、编译与运行时日志、SQL/审计追踪均在 GitHub:
[Raw Data](https://github.com/teaql/teaql-agent-kit/tree/autonomous/reports/evaluation-report-006/raw/)
