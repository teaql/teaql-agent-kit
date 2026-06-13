# Relationship Examples

This document provides patterns for defining relationships in KSML.

## 1. Parent-Child Relationship (One-to-Many)
*(Example assumes `company` is the actual domain root object.)*

```xml
<department _name="Department"
            _module="HR Management"
            _module_key="hr-management"
            name="Engineering"
            company="company()"
            create_time="createTime()"
            update_time="updateTime()"/>

<employee _name="Employee"
          _module="HR Management"
          _module_key="hr-management"
          name="John Doe"
          department="department()"
          company="company()"
          create_time="createTime()"
          update_time="updateTime()"/>
```

## 2. Many-to-Many Relationship (Junction Object)

```xml
<student _name="Student"
         _module="School Management"
         _module_key="school-management"
         name="Alice Smith"
         school="school()"
         create_time="createTime()"
         update_time="updateTime()"/>

<course _name="Course"
        _module="School Management"
        _module_key="school-management"
        name="Mathematics 101"
        school="school()"
        create_time="createTime()"
        update_time="updateTime()"/>

<!-- Junction object resolving Many-to-Many -->
<course_enrollment _name="Course Enrollment"
                   _module="School Management"
                   _module_key="school-management"
                   enrollment_date="2024-01-15"
                   student="student()"
                   course="course()"
                   school="school()"
                   create_time="createTime()"
                   update_time="updateTime()"/>
```

## 3. Self-Referencing Relationship (Hierarchy)
*(Example assumes `company` is the actual domain root object.)*

```xml
<employee_category _name="Employee Category"
                   _module="HR Management"
                   _module_key="hr-management"
                   id="id()" name="string()" code="string()"
                   company="company()"
                   _constant="true" _identifier="code">
  <_value id="1001" name="Manager" code="MANAGER"/>
  <_value id="1002" name="Staff" code="STAFF"/>
</employee_category>

<!-- manager is a self-reference for hierarchy. -->
<employee _name="Employee"
          _module="HR Management"
          _module_key="hr-management"
          name="John Doe"
          category="employee_category()"
          manager="employee()"
          company="company()"
          create_time="createTime()"
          update_time="updateTime()"/>
```
