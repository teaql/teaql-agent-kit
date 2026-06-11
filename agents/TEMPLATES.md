# KSML Templates

For every common pattern, copy and paste the relevant template below, and replace the placeholder values.

<!-- TEMPLATE: Root Metadata -->
```xml
<root alias_model_name="{snake_case_domain_name}"
      chinese_name="{domain_translation}"
      english_name="{Title Case Domain Name}"
      name="{kebab-case-domain-name}-service"
      cfg_mask_china_mobile="false"
      data_service="sqlite"
      org="doublechaintech"
      _module_key="root">
  <!-- All objects go here -->
</root>
```

<!-- TEMPLATE: Business Object -->
```xml
<{entity_name} _name="{Display Name}"
               _module="{Module Name}"
               _module_key="{module-key}"
               {field}="{concrete_value}"
               merchant="merchant(context)"
               create_time="createTime()"
               update_time="updateTime()"/>
```
*(Remove `merchant="merchant(context)"` if not a multi-tenant system where merchant is the root).*

<!-- TEMPLATE: Constant Object -->
```xml
<{constant_name} _name="{Display Name}"
                 _module="{Module Name}"
                 _module_key="{module-key}"
                 id="id()" name="string()" code="string()"
                 platform="platform()"
                 _constant="true" _identifier="code">
  <_value id="1001" name="{Value Name 1}" code="{VALUE_CODE_1}"/>
  <_value id="1002" name="{Value Name 2}" code="{VALUE_CODE_2}"/>
</{constant_name}>
```

<!-- TEMPLATE: Reference Field -->
```xml
{relation_name}="{relation_name}()"  <!-- business object reference -->
{status_field}="{constant_name}()"   <!-- constant reference -->
```
