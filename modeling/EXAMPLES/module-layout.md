# Module Layout Examples

This document demonstrates how to organize objects across modules using `_module` and `_module_key`.

## 1. Grouping by Functional Area

Group related business objects into functional modules (e.g., HR, Payroll, Recruiting).

```xml
<!-- HR Management Module -->
<employee _name="Employee"
          _module="HR Management"
          _module_key="hr-management" .../>

<department _name="Department"
            _module="HR Management"
            _module_key="hr-management" .../>

<!-- Payroll Management Module -->
<salary_slip _name="Salary Slip"
             _module="Payroll Management"
             _module_key="payroll-management" .../>

<tax_deduction _name="Tax Deduction"
               _module="Payroll Management"
               _module_key="payroll-management" .../>
```

## 2. Placing Constants

If a constant is shared across modules, put it in `Basic Data`.
If it is strictly used within one module, keep it in that specific module.

```xml
<!-- Shared Status: Put in Basic Data -->
<system_status _name="System Status"
               _module="Basic Data"
               _module_key="basic-data" ...>
  <_value id="1001" name="Active" code="ACTIVE"/>
  <_value id="1002" name="Inactive" code="INACTIVE"/>
</system_status>

<!-- Local Status: Keep in the Specific Module -->
<surgery_status _name="Surgery Status"
                _module="Surgery Management"
                _module_key="surgery-management" ...>
  <_value id="1001" name="Scheduled" code="SCHEDULED"/>
  <_value id="1002" name="In Progress" code="IN_PROGRESS"/>
  <_value id="1003" name="Completed" code="COMPLETED"/>
</surgery_status>

<surgery_record _name="Surgery Record"
                _module="Surgery Management"
                _module_key="surgery-management"
                status="surgery_status()" .../>
```
