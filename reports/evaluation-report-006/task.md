# 评估任务

## 任务描述

使用 TeaQL 代码生成器构建一个学校管理系统（School Service），包含以下实体：

- **Platform（平台）** — 域根实体，表示学校所属平台
- **SchoolType（学校类型）** — 常量实体，PRIMARY（小学）/ SECONDARY（中学）
- **School（学校）** — 业务对象，关联 Platform 和 SchoolType

要求完成：
1. 编写 KSML 模型（model.xml）
2. 使用 teaql eval 校验模型
3. 使用 teaql gen-lib 生成 Rust 代码
4. 编写 main.rs 实现完整的 CRUD 操作
5. 验证：创建数据、关联查询、过滤、搜索、聚合

## 任务流程

```
KSML 模型编写 → teaql eval 校验 → teaql gen-lib 生成代码
    → 编译 → 运行时验证 CRUD → SQL/审计追踪分析
```

## 交付物

- model.xml（3 实体）
- 生成的 Rust 代码（~24 文件）
- 可运行的主程序（main.rs）
- 运行时日志与 SQL 追踪

## 约束

- 不得手写 SQL 绕过 TeaQL 层
- 必须使用 Q/E facade API
- 必须遵循审计规则（.comment() / .purpose() / .audit_as()）
- 不得编辑生成代码
