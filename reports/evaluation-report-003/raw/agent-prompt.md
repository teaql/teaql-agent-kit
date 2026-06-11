# Agent Prompt — Evaluation Report 003

## Initial Prompt

Follow the instructions from updated https://github.com/teaql/teaql-agent-kit/tree/autonomous

Use Rust to build a system to meeting the following requirement:

🔧 Core Modules
• Operations & logistics: moves, routes, time slots, fulfillment events, addresses
• Employees & payroll: staff registry, job assignments, worked hours, payroll calculations, bonuses, leave tracking
• Customer management: private and corporate customers, linked contacts, billing info, customer history
• Products & services: moving, cleaning, box rentals, and additional services with configurations and pricing
• Marketing & sales: campaigns, discount codes, lead tracking, conversion metrics
• Finance & accounting: payments, invoices, expenses, VAT, financial summaries
• Asset management: vehicles, equipment, consumables, maintenance schedules
• Administration & compliance: contracts, insurance, document storage, audit logs

🧩 Platform Modules
• User & role management: admin, manager, employee, customer access levels
• Authentication & permissions: support for magic links, role-based access control (RBAC)
• Activity logging & audit trail: full history of changes, edits, and user actions
• Versioning & soft deletes: data recovery and edit history tracking
• Notifications & automation hooks: triggers for operational or financial updates
• API-ready architecture: structured for integration with front-end and external services

至少180种对象：
保持platform和merchant和employee的定义。
属性_module和_module_key用于标记属于哪个工作台，全部用英文。

Create the semantic TeaQL model first, review it, then generate the Rust TeaQL code. test some of Q and E api and generate a running report

just put all generated folder and files under ~/workspace/A-004 folder

代码生成使用本地快速端点,设置环境变量TEAQL_ENDPOINT_PREFIX为http://t420.doublechaintech.cn:23380

## System Context

- AGENTS.md from teaql-agent-kit autonomous branch
- TECH-INTRODUCTION.md for TeaQL framework understanding
- prompts/modeling/ksml-rules.md for KSML modeling rules
- prompts/modeling/checklist.md for model validation
- playbooks/generate-with-toolchains.md for generation workflow
