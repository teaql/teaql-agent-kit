# Business Object Examples

This document provides complete, copy-paste examples of business objects in KSML. 

## 1. Standard Business Object

```xml
<employee _name="Employee"
          _module="HR Management"
          _module_key="hr-management"
          name="John Doe"
          email="john.doe@example.com"
          phone="13800138000"
          hire_date="2024-01-15"
          department="department()"
          status="employment_status()"
          create_time="createTime()"
          update_time="updateTime()"/>
```

## 2. Multi-Tenant Business Object
*(Requires explicitly confirmed tenancy)*

```xml
<store_order _name="Store Order"
             _module="Order Management"
             _module_key="order-management"
             order_number="ORD-2024-001"
             total_amount="1500.00"
             order_status="order_status()"
             customer="customer()"
             merchant="merchant(context)"
             create_time="createTime()"
             update_time="updateTime()"/>
```

## 3. Platform-Level Business Object
*(Use this only when `platform` is the actual root object and the data is owned
by the platform operator.)*

```xml
<platform_configuration _name="Platform Configuration"
                        _module="System Administration"
                        _module_key="system-administration"
                        config_key="MAX_LOGIN_ATTEMPTS"
                        config_value="5"
                        is_active="true"
                        platform="platform()"
                        create_time="createTime()"
                        update_time="updateTime()"/>
```

## 4. Object with Masked Audit Fields

```xml
<user_account _name="User Account"
              _module="User Management"
              _module_key="user-management"
              username="johndoe123"
              password="hashed_password_string"
              _audit_mask_fields="password"
              status="account_status()"
              create_time="createTime()"
              update_time="updateTime()"/>
```
