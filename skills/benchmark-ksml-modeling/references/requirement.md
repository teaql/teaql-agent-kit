# Modeling Benchmark 001: Moving-company management

Benchmark ID: `teaql-modeling-001`

This is the frozen, public business requirement for version 1. Do not add a
target object count or silently narrow the scope for a particular model or
agent. The task is to produce a coherent KSML semantic model, not application
code.

Design a management system for a moving company. Its core business scope is:

1. Operations and logistics: moves, routes, time slots, fulfillment events,
   and service addresses.
2. Employees and payroll: staff registry, job assignments, worked hours,
   payroll calculations, bonuses, and leave.
3. Customer management: private and corporate customers, linked contacts,
   billing information, and customer history.
4. Products and services: moving, cleaning, box rentals, additional services,
   configurations, and pricing.
5. Marketing and sales: campaigns, discount codes, leads, and conversion
   metrics.
6. Finance and accounting: payments, invoices, expenses, VAT, and financial
   summaries.
7. Asset management: vehicles, equipment, consumables, and maintenance
   schedules.
8. Administration and compliance: contracts, insurance, document storage,
   and audit logs.

The platform scope is:

9. User and role management: administrator, manager, employee, and customer
   access levels.
10. Authentication and permissions: magic links and role-based access control.
11. Activity logging and audit trail: changes, edits, and user actions.
12. Versioning and soft deletes: recovery and edit history.
13. Notifications and automation hooks: operational and financial triggers.
14. API-ready architecture: structured integration with a front end and
    external services.

Model reasonable business distinctions and relationships. If a statement is
underspecified, record the assumption rather than inventing a hidden
requirement. Use synthetic examples only; no real customer data is needed.
