# Java API Patterns (Q/E API Examples)

This document provides complete patterns for querying (Q), expressions (E), and persistence (save/update) using TeaQL generated Java APIs.

### Q: Simple Query
```java
var merchants = Q.merchants()
    .selectSelf()
    .page(1, 20)
    .comment("Load merchants for homepage")
    .purpose("List active merchants")
    .executeForList(userContext);
```

### Q: Filtering
```java
var merchants = Q.merchants()
    .filterByPlatformWith(Q.platforms()
        .comment("Load platform")
        .filterByName("Shopify")
        .selectSelf())
    .filterByName("TeaQL")
    .comment("Search merchants by name and platform")
    .purpose("Filter merchants")
    .executeForList(userContext);
```

### Q: Multi-Level Loading
```java
var merchants = Q.merchants()
    .selectPlatformWith(Q.platforms()
        .comment("Load platform details")
        .selectSelf())
    .selectEmployeeListWith(Q.employees()
        .comment("Load employee details")
        .selectSelf())
    .comment("Load merchants with relations")
    .purpose("Export merchant data")
    .executeForList(userContext);
```

### Q: Dynamic JSON Query
When an application needs runtime-defined query criteria (e.g., chosen by a user), use the `findWithJsonExpr` dynamic query surface rather than building low-level `addFilter` calls.

### E: Safe Expressions
```java
var platformName = E.merchant(merchant)
    .getPlatform()
    .getName()
    .eval();
```

### Updates and Persistence (DDD Typed Behavior)
```java
// Define a domain type
class OperableMerchant extends Merchant {
    OperableMerchant openStore() {
        updateStatus(MerchantStatus.ACTIVE);
        return this;
    }
}

// Load typed entity
var merchant = Q.merchants()
    .returnType(OperableMerchant.class)
    .filterByName("TeaQL Store")
    .comment("Load merchant to open store")
    .purpose("Open store")
    .executeForOne(userContext)
    .orElseThrow();

// Act and persist
merchant.openStore()
    .updateDisplayName("TeaQL Store") // chainable updates
    .auditAs("Open store for the first time")
    .save(userContext);
```
