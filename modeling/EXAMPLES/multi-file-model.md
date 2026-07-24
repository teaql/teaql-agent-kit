# Multi-File KSML Model

Use this structure when a model contains more than 20 domain objects, counting
business objects and constant objects together. Split those objects by business
subdomain. Models with 20 or fewer objects may continue to use one `model.xml`.
If a subdomain still has more than 20 objects, split it again by a smaller
cohesive business process and use nested includes.

## Directory Layout

```text
models/
  main.xml
  organization/
    organization.xml
  operations/
    operations.xml
  finance/
    finance.xml
```

`main.xml` is mandatory as the entrypoint for every multi-file model.

## Entrypoint

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root alias_model_name="moving_company_management"
      cfg_mask_china_mobile="false"
      chinese_name="搬家公司管理"
      english_name="Moving Company Management"
      data_service="sqlite"
      name="moving-company-service"
      org="doublechaintech"
      _module_key="root">
  <platform _name="Platform"
            _module="Platform Administration"
            _module_key="platform-administration"
            name="Moving Services Platform"
            create_time="createTime()"
            update_time="updateTime()"/>

  <_include file="./organization/organization.xml"/>
  <_include file="./operations/operations.xml"/>
  <_include file="./finance/finance.xml"/>
</root>
```

## Included Domain File

```xml
<root>
  <move_order_status _name="Move Order Status"
                     _module="Operations"
                     _module_key="operations"
                     id="id()"
                     name="string()"
                     code="string()"
                     _constant="true"
                     _identifier="code"
                     platform="platform()">
    <_value id="1001" name="Draft" code="DRAFT"/>
    <_value id="1002" name="Confirmed" code="CONFIRMED"/>
  </move_order_status>

  <move_order _name="Move Order"
              _module="Operations"
              _module_key="operations"
              order_number="MOVE-2026-0001"
              status="move_order_status()"
              platform="platform()"
              create_time="createTime()"
              update_time="updateTime()"/>
</root>
```

Included files may contain nested includes. Their paths are relative to the
file containing the declaration:

```xml
<root>
  <_include file="./quotes.xml"/>
  <_include file="./dispatch.xml"/>
</root>
```

The expanded model is still one logical KSML model. Object names must be unique
across all files, references may cross files, and the include graph must not
contain cycles. Keep include order explicit: foundational and referenced
objects come before the files whose objects reference them.

Always pass the directory so TeaQL uploads the complete include closure and
resolves `main.xml`:

```bash
cargo teaql --input /path/to/models evaluate
cargo teaql --input /path/to/models rust-lib-core --output /path/to/rust-lib-core
```

Do not pass only `/path/to/models/main.xml`; remote evaluation and generation
would not receive the other XML files.
