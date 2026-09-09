# Progressive Modeling Ledger

## Outcome

- Business outcome: manage service work orders and their operational notes
- In scope: organization ownership, work-order identity, operational notes
- Out of scope: assignment, scheduling, billing, and status constants
- Current checkpoint: `P2`
- Next bounded task: add scheduling as a separate module

## Domain map

| Module | Responsibility | Objects | One-hop dependencies | Status |
| --- | --- | --- | --- | --- |
| Organization | owns the service graph | business_organization | none | evaluated |
| Operations | records work and notes | service_work_order, work_order_note | Organization: ownership | evaluated |
| Scheduling | plans work execution | not modeled | Operations: scheduled work | planned |

## Cross-module relations

| From | Field | To | Owner | Status |
| --- | --- | --- | --- | --- |
| service_work_order | organization | business_organization | Operations | verified |
| scheduled_visit | service_order | service_work_order | Scheduling | deferred |

## Decisions

| ID | Decision | Affected modules |
| --- | --- | --- |
| D-001 | business_organization is the domain root | all |
| D-002 | operational notes are owned by a service work order | Operations |

## Open questions

| ID | Question | Blocks |
| --- | --- | --- |
| Q-001 | can one work order have multiple scheduled visits? | Scheduling |

## Evaluation ledger

| Checkpoint | Input | Errors | Warnings | Suggestions | Solids | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| P1 | stage-1/model.xml | 0 | 1 | 0 | 9 | valid vertical slice |
| P2 | stage-2/model.xml | 0 | 0 | 0 | 11 | Operations module closed |

## Freeze record

- Complete plan: `no`
- Final input: not ready
- Final model hash: not ready
- Final evaluation: not ready
- Accepted warnings: none
- Generation targets: none until P5
