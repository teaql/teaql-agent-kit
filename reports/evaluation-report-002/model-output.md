# 模型输出

## KSML 语义模型

```xml
<root alias_model_name="school_management"
      cfg_mask_china_mobile="false"
      chinese_name="学校管理系统"
      english_name="School Management"
      data_service="sqlite"
      name="school-management-service"
      org="doublechaintech"
      _module_key="root">

  <platform _name="Platform"
            _module="Platform Management"
            _module_key="platform-management"
            platform_name="EduManage Platform"
            description="Central education management platform"
            contact_email="admin@edumanage.com"
            contact_phone="010-88886666"
            website="https://edumanage.com"
            create_time="createTime()"
            update_time="updateTime()"/>

  <school_type _name="School Type"
               _module="School Management"
               _module_key="school-management"
               platform="platform()"
               id="id()" name="string()" code="string()"
               _constant="true" _identifier="code">
    <_value id="1001" name="Primary" code="PRIMARY"/>
    <_value id="1002" name="Secondary" code="SECONDARY"/>
  </school_type>

  <school _name="School"
          _module="School Management"
          _module_key="school-management"
          school_name="Beijing No.1 Primary School"
          school_code="BJ-001"
          address="No.100 Chaoyang Road, Beijing"
          phone="010-66668888"
          email="contact@bj001.edu.cn"
          established_date="2005-09-01"
          principal_name="Zhang Wei"
          student_count="1200"
          school_type="school_type()"
          platform="platform()"
          create_time="createTime()"
          update_time="updateTime()"/>

</root>
```

## 模型评估结果

### 通过的规则 (15条)
- KSML-UPLOAD-001：模型上传非空
- KSML-UPLOAD-005：找到有效入口点
- KSML-XML-002：XML 格式正确
- KSML-ROOT-003：根名称格式正确
- KSML-OBJECT-001：所有对象定义了显示元数据
- KSML-CONSTANT-001：常量对象属性有效
- KSML-CONSTANT-002：常量对象正确关联到根对象
- KSML-CONSTANT-004：常量值存在
- KSML-REFERENCE-003：所有引用目标存在
- KSML-MODULE-004：本地常量模块键匹配
- KSML-DOMAIN-ROOT-003：恰好找到一个域根候选

### 警告 (5条)
- PII 数据掩码警告：contact_email, contact_phone, address, phone, email

### 建议 (5条)
- 添加稳定的 UI 排序
- 潜在个人数据建议：platform_name, name, school_name, principal_name

### 错误
- 无（首次评估有 1 个错误，已修复）
