# 代理提示词

## 初始提示词

```
清除记忆
Follow the instructions from updated https://github.com/teaql/teaql-agent-kit/tree/autonomous

Use Rust to build a school management system with these domain concepts:

- Platform
- School
- School Type, with values Primary and Secondary

Create the semantic TeaQL model first, review it, then generate the Rust TeaQL code. test some of Q and E api and generate a running report

just put all generatted folder and files under ~/workspace/A-003 folder
```

## 后续提示词

```
报告全部中文

这个是风格指南
http://t420.doublechaintech.cn:2080/upload/TeaQL_Website_Visual_and_Metaphor_Design_Guide.md

这个是报告的封面，要形成一个可打印版，
http://t420.doublechaintech.cn:2080/upload/gemini-code-1780971090102.html

报告在远程的访问路径是
https://github.com/teaql/teaql-agent-kit/tree/autonomous/reports

这个是每页内容规划
http://t420.doublechaintech.cn:2080/upload/Evaluation_Report_001_Template.md

保存报告的位置 ~/githome/teaql-agent-kit/reports/[report-id]

github用户名 emilyguo, access token: [REDACTED]

本次为evaluation-report-002

我们这个框架的特色是透明的跟踪和审计，你读取文档，输出运行日志，分析日志，增加一页，如果这个影响你最终评分，请更新

https://github.com/teaql/teaql-agent-kit/tree/autonomous

每个报告的目录结构
evaluation-report-002/
├── README.md
├── environment.md
├── task.md
├── model-output.md
├── scoring.md
├── raw/
│ ├── agent-prompt.md
│ ├── agent-response.md
│ ├── build-log.txt
│ ├── runtime-log.txt
│ ├── sql-trace.txt
│ └── code-diff.patch
└── assets/
└── report-cover.png
```
