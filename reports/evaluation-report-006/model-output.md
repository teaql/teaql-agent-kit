# KSML 模型与生成代码输出

## KSML 模型（model.xml）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root xmlns="https://www.teaql.io/schema/ksml/v1"
      name="school-service"
      data_service="sqlite"
      alias_model_name="school_service"
      english_name="School Service"
      org="teaql">

    <Platform
        name="平台名称"
        create_time="createTime()"
        last_update_time="updateTime()"
        _module_key="domain"
    />

    <SchoolType
        name="类型名称"
        code="类型代码"
        _module_key="constant"
    />

    <School
        name="学校名称"
        description="描述"
        platform="Platform()"
        school_type="SchoolType()"
        create_time="createTime()"
        last_update_time="updateTime()"
        _module_key="business"
    />
</root>
```

## teaql eval 校验结果

- **Errors**: 0
- **Warnings**: 8（实体命名规范、缺失 display metadata、域根连接）
- **Suggestions**: 3（隐私掩码建议）
- **Solids**: 6（XML 解析、引用解析、模型结构）

## 生成代码统计

| 项目 | 数量 |
|------|------|
| Rust 源文件 | 24 文件 |
| 实体类型 | 3（Platform / SchoolType / School）|
| 生成的 query facade 方法 | 每个实体约 15-20 个 |
| 生成的 E expression facade | 3 组 |

## 生成的关键 API

### Q facade（查询入口）
```rust
Q::platforms().with_name_contains("...").purpose("...").execute_for_list(&ctx)
Q::schools().select_platform().select_school_type().purpose("...").execute_for_list(&ctx)
Q::school_types().with_name_is("小学").purpose("...").execute_for_first(&ctx)
Q::schools().with_school_type_matching(Q::school_types().with_name_is("小学"))
```

### E facade（安全表达式）
```rust
E::school(&rec).get_name().eval()  // 返回 Option<String>
```

### 实体 API（CRUD）
```rust
entity.update_name("...")
entity.update_platform_id(id)
entity.audit_as("comment").save(&ctx)  // 返回 GraphNode
```
