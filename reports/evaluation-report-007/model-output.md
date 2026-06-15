# Model Output

## KSML Model

```xml
<root alias_model_name="school_management" chinese_name="学校管理"
      english_name="School Management" name="school-service"
      data_service="sqlite" org="doublechaintech">
  <platform _name="Platform" _module="Platform Management"
            name="Standard Education Platform"
            description="Platform for managing schools"
            create_time="createTime()" update_time="updateTime()"/>
  <school_type _name="School Type" _module="School Management"
               id="id()" name="string()" code="string()"
               _constant="true" _identifier="code" platform="platform()">
    <_value id="1001" name="Primary" code="PRIMARY"/>
    <_value id="1002" name="Secondary" code="SECONDARY"/>
  </school_type>
  <school _name="School" _module="School Management"
          name="Sunshine Elementary" address="123 Education Street"
          principal="Dr. Sarah Chen" student_count="850"
          platform="platform()" school_type="school_type()"
          create_time="createTime()" update_time="updateTime()"
          _audit_mask_fields="address"/>
</root>
```

## Evaluation

- First eval: 0 errors, 4 warnings → fixed module mismatch + audit mask
- Second eval: **0 errors, 0 warnings, 15 solids** ✓

## Generated Code

24 Rust source files, ~3500 lines, 7 entity types:
- lib/src/ (lib.rs, e.rs, q.rs, runtime.rs, sample_data.rs, request_support.rs)
- lib/src/platform/ (entity, request, expressions, behavior, checker)
- lib/src/school/ (entity, request, expressions, behavior, checker)
- lib/src/school_type/ (entity, request, expressions, behavior, checker)
