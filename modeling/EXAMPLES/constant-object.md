# Constant Object Examples

This document provides complete, copy-paste examples of constant objects in KSML. 
Constant objects represent finite sets like status, category, kind, or priority.

## 1. Status Constant Object
*(Example assumes `clinic` is the actual domain root object.)*

```xml
<appointment_status _name="Appointment Status"
                    _module="Basic Data"
                    _module_key="basic-data"
                    id="id()" name="string()" code="string()"
                    clinic="clinic()"
                    _constant="true" _identifier="code">
  <_value id="1001" name="Pending" code="PENDING"/>
  <_value id="1002" name="Confirmed" code="CONFIRMED"/>
  <_value id="1003" name="Completed" code="COMPLETED"/>
  <_value id="1004" name="Cancelled" code="CANCELLED"/>
</appointment_status>
```

## 2. Category Constant Object

```xml
<course_category _name="Course Category"
                 _module="Course Management"
                 _module_key="course-management"
                 id="id()" name="string()" code="string()"
                 school="school()"
                 _constant="true" _identifier="code">
  <_value id="1001" name="Mathematics" code="MATHEMATICS"/>
  <_value id="1002" name="Science" code="SCIENCE"/>
  <_value id="1003" name="Literature" code="LITERATURE"/>
  <_value id="1004" name="Physical Education" code="PHYSICAL_EDUCATION"/>
</course_category>
```

## 3. Priority Constant Object
*(Example assumes `support_center` is the actual domain root object.)*

```xml
<ticket_priority _name="Ticket Priority"
                 _module="Basic Data"
                 _module_key="basic-data"
                 id="id()" name="string()" code="string()"
                 support_center="support_center()"
                 _constant="true" _identifier="code">
  <_value id="1001" name="Low" code="LOW"/>
  <_value id="1002" name="Medium" code="MEDIUM"/>
  <_value id="1003" name="High" code="HIGH"/>
  <_value id="1004" name="Critical" code="CRITICAL"/>
</ticket_priority>
```
