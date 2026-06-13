# ERROR REFERENCE

## Validation Errors (`cargo-teaql eval`)

| Error | Meaning | Fix |
|-------|---------|-----|
| Empty attribute | Attribute has no value | Delete it or fill with a concrete value. |
| Missing root ref | Constant not linked to root | Add reference to the actual domain root object (e.g. `bookstore="bookstore()"` when `bookstore` is the root). |
| Depth exceeded | Too many nested references | Remove one reference or use string field. |
| Sensitive field | Token/key/password detected | Add `_audit_mask_fields="field_name"`. |
| Disconnected graph | Entity not connected to root | Connect it to its natural parent or actual root object. Use a tenant context reference only when multi-tenancy is explicitly confirmed. |
| Reserved keyword | Using a language keyword | Rename attribute (e.g., `type` -> `item_kind`, `user` -> `user_account`). |

## Code Generation / Compilation Errors

| Error | Meaning | Fix |
|-------|---------|-----|
| `no method named update_xxx` | Guessing method names | Read the entity source file for the exact correct method name. |
| `Missing .audit_as()` | Unaudited save/update | Add `.audit_as("description")` before `.save()` or `.update()`. |
| `Missing .purpose()` | Unjustified query | Add `.purpose("why")` and `.comment("what")` before `.execute_for_list()`. |

---

## Copy-Paste Fix Snippets

### Fix: Missing root ref
```xml
<!-- Before: Error -->
<order_status _name="Order Status"
              _module="Basic Data"
              _module_key="basic-data"
              id="id()" name="string()" code="string()"
              _constant="true" _identifier="code">
  <_value id="1001" name="Created" code="CREATED"/>
</order_status>

<!-- After: Fix (Add the actual root object reference) -->
<order_status _name="Order Status"
              _module="Basic Data"
              _module_key="basic-data"
              bookstore="bookstore()"
              id="id()" name="string()" code="string()"
              _constant="true" _identifier="code">
  <_value id="1001" name="Created" code="CREATED"/>
</order_status>
```

### Fix: Sensitive field
```xml
<!-- Before: Error (password detected as plain text) -->
<user_account _name="User Account"
              _module="Identity"
              _module_key="identity"
              login_name="alice"
              password_hash="hash-example"
              bookstore="bookstore()"/>

<!-- After: Fix (Mask field) -->
<user_account _name="User Account"
              _module="Identity"
              _module_key="identity"
              login_name="alice"
              password_hash="hash-example"
              bookstore="bookstore()"
              _audit_mask_fields="password_hash"/>
```

### Fix: Disconnected graph
```xml
<!-- Before: Error -->
<order_item _name="Order Item"
            _module="Sales"
            _module_key="sales"
            item_name="Domain Modeling with TeaQL"/>

<!-- After: Fix (Connect to natural parent) -->
<order_item _name="Order Item"
            _module="Sales"
            _module_key="sales"
            item_name="Domain Modeling with TeaQL"
            order="order()"/>
```

### Fix: Missing .audit_as() / .purpose() (Java)
```java
// Before: Error
merchant.save(ctx);
Q.merchants().executeForList(ctx);

// After: Fix
merchant.auditAs("Updating merchant details").save(ctx);
Q.merchants().purpose("Load active merchants").comment("Home page").executeForList(ctx);
```

### Fix: Missing .audit_as() / .purpose() (Rust)
```rust
// Before: Error
merchant.save(&ctx).await?;
Q::merchants().execute_for_list(&ctx).await?;

// After: Fix
merchant.audit_as("Updating merchant details").save(&ctx).await?;
Q::merchants().purpose("Load active merchants").comment("Home page").execute_for_list(&ctx).await?;
```
