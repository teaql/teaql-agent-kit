# Decision Trees

## CHOOSING YOUR DOMAIN ROOT

Does the system have a platform/operator managing multiple organizations?
  YES → Use `platform` as root
  NO → Does it have a company/merchant/tenant owner?
    YES → Use that as root (e.g., `company` or `merchant`)
    NO → Use the main business entity as root (e.g., `school` for a single-school system)

## CHOOSING TENANCY MODEL

Is this a single-tenant system?
  YES → Do not add `merchant="merchant(context)"` or any tenant boundary fields.
  NO → Is there a clear tenant owner (e.g. merchant, company, school)?
    YES → Add `{tenant_owner}="{tenant_owner}(context)"` to tenant-owned objects.
    NO → Ask the user to clarify before assuming tenancy.

## MODULE ASSIGNMENT

Does the object represent finite-set constant values (e.g. status, kind, category)?
  YES → Is the constant object only referenced by exactly one business object in a specific module?
    YES → Put it in the same module as the business object.
    NO → Put it in `Basic Data` (or `_module="Basic Data"`).
  NO → Is the object a core operational business entity?
    YES → Group it with related entities under a functional module (e.g., `Surgery Management`, `Inventory Management`).
