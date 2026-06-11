# Model Output — Evaluation Report 003

## Model Summary

- **Model Name:** moving-company-service
- **Alias:** moving_company_management
- **English Name:** Moving Company Management
- **Total Objects:** 183 (143 business + 40 constant)
- **Modules:** 12

## Module Breakdown

| Module | Business Objects | Constants | Total |
|--------|-----------------|-----------|-------|
| Platform | 2 | 2 | 4 |
| Operations & Logistics | 11 | 14 | 25 |
| Employees & Payroll | 9 | 13 | 22 |
| Customer Management | 8 | 8 | 16 |
| Products & Services | 9 | 9 | 18 |
| Marketing & Sales | 7 | 10 | 17 |
| Finance & Accounting | 8 | 9 | 17 |
| Asset Management | 8 | 11 | 19 |
| Administration & Compliance | 6 | 10 | 16 |
| User & Role Management | 6 | 3 | 9 |
| Authentication & Permissions | 4 | 0 | 4 |
| Activity Logging & Audit | 2 | 3 | 5 |
| Versioning & Soft Deletes | 3 | 2 | 5 |
| Notifications & Automation | 3 | 0 | 3 |
| API Configuration | 3 | 0 | 3 |

## Key Entities

### Domain Root
- `platform` — No parent reference, manages merchants

### Tenant Owner
- `merchant` — References platform, all operational entities reference merchant(context)

### Core Business Objects
- `move_order` → customer, route, inventory_item, move_quote, damage_report
- `employee` → department, job_position, employment_status
- `customer` → customer_type, customer_status, gender
- `vehicle` → vehicle_type, vehicle_status
- `payment` → move_order, customer, payment_method, payment_status
- `invoice` → move_order, customer, invoice_line_item
- `campaign` → campaign_type, campaign_status, channel_type
- `contract` → contract_type, contract_status

## Evaluation Result

- **Solids:** 921
- **Warnings:** 66
- **Errors:** 0

## Model File

The complete KSML model is available at:  
`~/workspace/A-004/app-playground/models/model.xml`

The model contains 2635 lines of XML defining all 183 objects with their attributes, relationships, and constant values.
