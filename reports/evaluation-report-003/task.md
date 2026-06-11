# Task — Evaluation Report 003

## Task ID
TEAQL-AUTO-003

## Task Title
Build a Moving Company Management System with 183+ KSML Objects

## Task Description

Build a comprehensive moving company management system using the TeaQL Rust stack. The system must include:

### Core Modules
- Operations & logistics: moves, routes, time slots, fulfillment events, addresses
- Employees & payroll: staff registry, job assignments, worked hours, payroll calculations, bonuses, leave tracking
- Customer management: private and corporate customers, linked contacts, billing info, customer history
- Products & services: moving, cleaning, box rentals, and additional services with configurations and pricing
- Marketing & sales: campaigns, discount codes, lead tracking, conversion metrics
- Finance & accounting: payments, invoices, expenses, VAT, financial summaries
- Asset management: vehicles, equipment, consumables, maintenance schedules
- Administration & compliance: contracts, insurance, document storage, audit logs

### Platform Modules
- User & role management: admin, manager, employee, customer access levels
- Authentication & permissions: support for magic links, role-based access control (RBAC)
- Activity logging & audit trail: full history of changes, edits, and user actions
- Versioning & soft deletes: data recovery and edit history tracking
- Notifications & automation hooks: triggers for operational or financial updates
- API-ready architecture: structured for integration with front-end and external services

### Requirements
- At least 180 objects
- Keep platform, merchant, and employee definitions
- Attributes _module and _module_key for module tagging, all in English
- Create semantic TeaQL model first, review it, then generate Rust TeaQL code
- Test some Q and E APIs
- Generate a running report

## Success Criteria

1. Valid KSML model with 180+ objects
2. Model passes cargo-teaql eval with 0 errors
3. Generated Rust library compiles
4. Generated workspace compiles
5. At least 10 automated tests pass
6. Q and E API examples build successfully
7. Complete audit trail preserved

## Evaluation Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Object Count | ≥180 | 183 |
| Eval Errors | 0 | 0 |
| Compile Success | Yes | Yes |
| Test Pass Rate | ≥80% | 100% (15/15) |
| Q API Examples | ≥5 | 15 |
| E API Examples | ≥1 | 2 (commented, require runtime) |
