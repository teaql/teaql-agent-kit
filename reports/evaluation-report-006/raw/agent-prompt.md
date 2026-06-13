# Agent Prompt 记录

## 初始 Prompt

> 使用 TeaQL 生成一个学校管理系统。项目名为 school-service，包含 3 个实体：
> - Platform（域根）：name
> - SchoolType（常量）：name, code — 小学/中学
> - School（业务对象）：name, description — 关联 Platform 和 SchoolType
> 
> 关键约束：
> 1. 遵循 teaql-agent-kit AGENTS.md 的编码规范
> 2. 使用 Q/E facade API
> 3. 不要手写 SQL
> 4. 使用 .comment() / .purpose() / .audit_as() 审计链
> 5. 生成的代码不可手动编辑

## 后续纠错 Prompt

（多次迭代纠正编译和运行时错误，核心 Prompt 包括：）

> "修复 UNIQUE constraint 冲突"
> "main.rs 编译错误：GraphNode 类型未识别"
> "API 名称不匹配：with_name_contains 未找到"
> "value type 转换错误：id() 返回 Option<&Value>"
> "运行时退出码 1：缺少环境变量 SCHOOL_SERVICE_DATABASE_URL"
> "重新运行 teaql gen-lib 检查文档是否更新"
> "安全审计：验证外部 crate 能否绕过 save()"

## 最终汇总 Prompt

> 给 teaql 技术一个评测

## 风格要求

> 报告全部中文
> 需要记录原始对话，如何修正错误的
> 不管是因为 teaql 的文档，工具还是你自己的出错，都要记录下来
> 这个框架的特色是透明的跟踪和审计
> 读取文档，输出运行日志，分析日志，增加审计分析页
> 如果影响最终评分请更新
