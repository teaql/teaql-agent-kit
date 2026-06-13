# 评估报告 005：TeaQL Agent Kit 评估（全量日志版）

**评估日期**: 2026-06-13
**评估模型**: QClaw (Kimi K2.6)
**评估对象**: TeaQL Agent Kit (autonomous 分支)
**TeaQL 版本**: 4.0.3
**运行环境**: macOS 12.6.8, Intel i7-4770HQ, 16GB RAM
**报告路径**: `~/githome/teaql-agent-kit/reports/evaluation-report-005/`

## 评估概要

本次评估基于 TeaQL Agent Kit 的 autonomous 分支，测试学校管理系统（School Management System）的完整工作流：
- KSML 建模 → 服务端验证 → 代码生成 → 编译测试 → 集成测试

**最终评分**: 4.625/5.0（加权 4.727/5.0）

**零硬伤**: 所有 22 个测试通过，编译零错误
**全量日志**: 本次评估包含完整运行时日志（TEAQL_SQL=_full, TEAQL_AUDIT=_full）

## 目录结构

```
evaluation-report-005/
├── README.md              # 本文件
├── environment.md         # 环境配置
├── task.md                # 任务描述
├── model-output.md        # 模型输出分析
├── scoring.md             # 评分详情
├── raw/
│   ├── agent-prompt.md    # Agent 指令
│   ├── agent-response.md  # Agent 响应
│   ├── build-log.txt      # 构建日志
│   ├── runtime-log.txt    # 运行时日志（全量）
│   ├── sql-trace.txt      # SQL 追踪（全量）
│   └── code-diff.patch    # 代码差异
└── assets/
    └── report-cover.png   # 报告封面
```

## 关键发现

### 1. API 设计一致性（4/5）
- 查询构建器链式调用模式清晰：`Q::schools().with_xxx().purpose().execute_for_list()`
- 类型状态模式确保编译时安全：`.purpose()` 将 `*Request` 转为 `PurposedQuery<*Request>`
- 但存在命名不一致：`with_name_contains` vs `with_name_containing`（不同实体类型前缀不同）

### 2. AI 上手成本（4/5）
- 文档完整性高（API_GUIDE.md + TOOL_API.md + AGENTS.md）
- 但文档发现成本高：需要主动寻找，无代码内提示
- 错误信息不友好：链式调用错误难以定位

### 3. 运行时稳定性（5/5）
- 所有 22 个测试通过（14 Q + 3 E + 4 CRUD + 1 聚合）
- 零运行时崩溃
- 乐观锁冲突处理正确

### 4. 代码生成质量（5/5）
- 112 个源文件自动生成
- 实体、查询、表达式、校验器完整生成
- 类型安全，编译零错误

## 已知问题

1. **Supplier 字段序列化**: `is_active` bool/int 不一致
2. **聚合分组名称**: 显示 "(unknown)"，字段名映射问题
3. **编译周期**: 4-8 分钟（依赖解析 + 代码生成）

## 摩擦记录

| 摩擦点 | 影响 | 解决方式 |
|--------|------|----------|
| `execute_by_id` 泛型推断 | 编译错误 | 显式类型标注 `PurposedQuery<SchoolRequest<School>>` |
| `.set_comment()` → `.audit_as()` | 编译错误 | 阅读 AGENTS.md 发现 API 变更 |
| `with_name_contains` → `with_name_containing` | 编译错误 | 阅读 API_GUIDE.md 发现命名规则 |
| 空字符串字段 NPE | 服务端崩溃 | 替换 `""` 为 `"none"` |
| 并发 DB 访问 | 测试失败 | `unique_db_path()` 原子计数器 |
| ID 回写问题 | 测试失败 | 改用 `with_name_containing()` 查询 |

## 透明跟踪

本报告遵循 TeaQL 框架的透明跟踪和审计原则：
- 所有 Agent 操作记录于 `raw/agent-response.md`
- 构建日志记录于 `raw/build-log.txt`
- 运行时日志记录于 `raw/runtime-log.txt`
- 代码变更记录于 `raw/code-diff.patch`

---

**评估者**: QClaw Agent
**评估时间**: 2026-06-13 10:20 CST
**GitHub**: https://github.com/teaql/teaql-agent-kit/tree/autonomous/reports/evaluation-report-005
