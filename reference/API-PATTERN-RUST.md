# Rust API Patterns (Q/E API Examples)

This document provides complete patterns for querying (Q), expressions (E), and persistence (save/update) using TeaQL generated Rust APIs.

### Q: Simple Query
```rust
let merchants = Q::merchants()
    .select_self()
    .page(1, 20)
    .comment("Load merchants for homepage")
    .purpose("List active merchants")
    .execute_for_list(&ctx)
    .await?;
```

### Q: Filtering
```rust
let merchants = Q::merchants()
    .which_names_contain("TeaQL")
    .filter_by_platform_with(Q::platforms()
        .comment("Load platform")
        .which_names_are("Shopify")
        .select_self())
    .comment("Search merchants by name and platform")
    .purpose("Filter merchants")
    .execute_for_list(&ctx)
    .await?;
```

### Q: Multi-Level Loading
```rust
let merchants = Q::merchants()
    .select_platform_with(Q::platforms()
        .comment("Load platform details")
        .select_self())
    .select_employee_list_with(Q::employees()
        .comment("Load employee details")
        .select_self())
    .comment("Load merchants with relations")
    .purpose("Export merchant data")
    .execute_for_list(&ctx)
    .await?;
```

### Q: Dynamic JSON Query
When an application needs runtime-defined query criteria (e.g., chosen by a user), use the `find_with_json_expr` dynamic query surface rather than building low-level `add_filter` calls.

### E: Safe Expressions
```rust
let platform_name = E::merchant(merchant)
    .get_platform()
    .get_name()
    .eval();
```

### Updates and Persistence (DDD Typed Behavior)
```rust
// Define a domain type
struct OperableMerchant {
    inner: Merchant,
}

impl OperableMerchant {
    fn open_store(&mut self) -> &mut Self {
        self.inner.update_status_id(MerchantStatus::active_id());
        self
    }
}

// Load typed entity
let mut merchant = Q::merchants()
    .return_type::<OperableMerchant>()
    .which_names_are("TeaQL Store")
    .comment("Load merchant to open store")
    .purpose("Open store")
    .execute_for_one(&ctx)
    .await?
    .expect("merchant should exist");

// Act and persist
merchant.open_store();
merchant.inner.audit_as("Open store for the first time").save(&ctx).await?;
```
