# 任务描述

## 评估目标
评估 TeaQL Agent Kit（autonomous 分支）的完整工作流，验证其作为 AI 驱动代码生成框架的可用性和可靠性。

## 评估范围

### 1. 建模阶段
- 使用 KSML（Knowledge Structure Modeling Language）定义领域模型
- 验证模型语法和语义正确性
- 测试服务端 eval 验证

### 2. 代码生成阶段
- 生成 Rust 库代码（实体、查询、表达式、校验器）
- 验证生成代码的编译正确性
- 检查类型安全和 API 完整性

### 3. 集成测试阶段
- 编写综合测试覆盖 Q/E/CRUD API
- 验证运行时行为正确性
- 测试边界情况和错误处理

## 测试领域

### 学校管理系统（School Management System）
**实体清单**:
- Platform（平台）
- SchoolType（学校类型：Primary/Secondary）
- SchoolStatus（学校状态：Active/Inactive/Pending/Closed）
- School（学校）
- Gender（性别）
- StudentStatus（学生状态）
- AttendanceStatus（出勤状态）
- Student（学生）
- Teacher（教师）
- Department（部门）
- Course（课程）
- ClassGroup（班级）
- GradeRecord（成绩记录）
- GradingRule（评分规则）
- Attendance（出勤记录）

**关系复杂度**: 14 个实体，多对多关系，常量引用

## 评估维度

| 维度 | 权重 | 说明 |
|------|------|------|
| 文档完整性 | 20% | API_GUIDE.md、TOOL_API.md、AGENTS.md 覆盖度 |
| 代码生成质量 | 20% | 生成代码的正确性、完整性、可读性 |
| 错误信息友好度 | 15% | 编译错误和运行时错误的可理解性 |
| AI 上手成本 | 20% | 学习曲线、文档发现成本、调试难度 |
| 运行时稳定性 | 15% | 测试通过率、运行时崩溃、数据一致性 |
| API 设计一致性 | 10% | 命名规范、模式一致性、可预测性 |

## 成功标准
- [x] 模型通过服务端验证（15/15 solid）
- [x] 代码生成零错误
- [x] 编译零错误
- [x] 所有测试通过（22/22）
- [x] 无运行时崩溃
- [x] 文档完整可读

## 交付物
- 评估报告（本目录）
- 运行时日志
- 构建日志
- 代码差异
- 测试报告
