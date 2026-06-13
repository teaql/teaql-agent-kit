# Evaluation Report #006

**Project:** School Service — TeaQL Rust 学校管理系统  
**报告类型:** AI Agent 实用工程评估  
**日期:** 2026-06-13  
**报告系列:** #006  
**评估目标:** 评估 AI Agent (QClaw / DeepSeek) 在 TeaQL Rust 项目上的工程能力

---

## 目录结构

```
evaluation-report-006/
├── README.md                 # 本文件：报告概要
├── environment.md            # 评估环境详情
├── task.md                   # 评估任务描述
├── model-output.md           # KSML 模型与生成代码输出
├── scoring.md                # 评分详情
├── raw/
│   ├── agent-prompt.md       # 完整的 Agent Prompt 记录
│   ├── agent-response.md     # 完整的 Agent 响应记录
│   ├── build-log.txt         # 编译日志
│   ├── runtime-log.txt       # 运行时日志
│   ├── sql-trace.txt         # SQL 跟踪日志
│   └── code-diff.patch       # 代码变更差异
└── assets/                   # 报告相关素材
```

## 关键发现

1. **文档驱动开发的陷阱** — Agent 遵循了旧版 AGENTS.md 的手动初始化路径，绕过了 `service_runtime_from_env()` 标准入口，导致一连串错误修复
2. **3 次修复 = 3 次弯路** — 删 initial_graph、加 teaql-runtime 依赖、加 AuditedSave import 均因未使用框架标准入口
3. **上游已修复** — 重新运行 `teaql gen-lib` 后发现最新 AGENTS.md 已首推 `service_runtime_from_env()`
4. **TeaQL 安全审计验证** — save() 为 pub(crate)、FK 必须用关联方法、外部写入强制 comment 参数

## 评分概要

| 维度 | 得分 | 
|------|:----:|
| 项目理解 | 8.0 |
| TeaQL 规范对齐 | 6.5 |
| 代码正确性 | 7.5 |
| 审计与追踪 | 8.5 |
| 工程判断 | 7.0 |
| **综合** | **7.5** |
