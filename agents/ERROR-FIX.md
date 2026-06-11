# ERROR REFERENCE

## Validation Errors (`cargo-teaql eval`)

| Error | Meaning | Fix |
|-------|---------|-----|
| Empty attribute | Attribute has no value | Delete it or fill with a concrete value. |
| Missing root ref | Constant not linked to root | Add reference to root entity (e.g. `platform="platform()"`). |
| Depth exceeded | Too many nested references | Remove one reference or use string field. |
| Sensitive field | Token/key/password detected | Add `_audit_mask_fields="field_name"`. |
| Disconnected graph | Entity not connected to root | Connect to its natural parent or the root (e.g., add `merchant="merchant(context)"`). |
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
<entity name="order" />

<!-- After: Fix (Add root reference) -->
<entity name="order" platform="platform()" />
```

### Fix: Sensitive field
```xml
<!-- Before: Error (password detected as plain text) -->
<entity name="user" password="" />

<!-- After: Fix (Mask field) -->
<entity name="user" password="" _audit_mask_fields="password" />
```

### Fix: Disconnected graph
```xml
<!-- Before: Error -->
<entity name="order_item" />

<!-- After: Fix (Connect to parent) -->
<entity name="order_item" order="order(context)" />
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
