# Agent 指令

## 任务
评估 TeaQL Agent Kit（autonomous 分支）的完整工作流，验证其作为 AI 驱动代码生成框架的可用性和可靠性。

## 输入
- TeaQL Agent Kit 仓库（GitHub: teaql/teaql-agent-kit, autonomous 分支）
- 工作目录: ~/workspace/A-002
- 端点: http://t420.doublechaintech.cn:23380

## 步骤
1. 读取 AGENTS.md、API_GUIDE.md、TOOL_API.md
2. 创建 KSML 模型（学校管理系统）
3. 执行服务端验证（cargo teaql eval）
4. 生成 Rust 库代码（cargo teaql generate）
5. 编写集成测试（main.rs）
6. 编译并运行测试
7. 记录摩擦点和评分

## 约束
- 必须使用 TeaQL 4.0.3 依赖（crates.io）
- 禁止猜测 API（必须阅读文档）
- 强制审计模式：.audit_as() → .save()
- 强制查询模式：.purpose() → execute

## 输出
- 评估报告（本目录）
- 运行时日志
- 构建日志
- 代码差异

## 评分维度
- 文档完整性（20%）
- 代码生成质量（20%）
- 错误信息友好度（15%）
- AI 上手成本（20%）
- 运行时稳定性（15%）
- API 设计一致性（10%）
