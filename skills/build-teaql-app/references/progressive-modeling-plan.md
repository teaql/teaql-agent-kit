# Progressive Modeling Ledger

Keep this file under `models/.teaql/progressive-modeling.md`. Replace the
examples and remove unused rows. Keep entries factual and compact.

## Outcome

- Business outcome: `<one bounded outcome>`
- In scope: `<capabilities>`
- Out of scope: `<explicit exclusions>`
- Current checkpoint: `P0`
- Next bounded task: `<one module or relation batch>`

## Domain map

| Module | Responsibility | Objects | One-hop dependencies | Status |
| --- | --- | --- | --- | --- |
| `<module>` | `<one line>` | `<ksml names>` | `<module: reason>` | planned |

Status is one of `planned`, `active`, `evaluated`, or `frozen`.

## Cross-module relations

| From | Field | To | Owner | Status |
| --- | --- | --- | --- | --- |
| `<object>` | `<field>` | `<object>` | `<module>` | deferred |

Status is one of `deferred`, `implemented`, or `verified`.

## Decisions

| ID | Decision | Affected modules |
| --- | --- | --- |
| `D-001` | `<stable business/modeling decision>` | `<modules>` |

## Open questions

| ID | Question | Blocks |
| --- | --- | --- |
| `Q-001` | `<question requiring business judgment>` | `<checkpoint/module>` |

## Evaluation ledger

| Checkpoint | Input hash | Errors | Warnings | Suggestions | Solids | Result |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `P1` | `<sha256>` | 0 | 0 | 0 | 0 | foundation valid |

## Freeze record

- Complete plan: `no`
- Final input: `<absolute or repository-relative model directory>`
- Final model hash: `<sha256>`
- Final evaluation: `<counts>`
- Accepted warnings: `<IDs or none>`
- Generation targets: `<targets>`
