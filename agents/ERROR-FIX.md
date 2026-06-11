# ERROR REFERENCE

| Error | Meaning | Fix |
|-------|---------|-----|
| Empty attribute | Attribute has no value | Delete it or fill with a concrete value. |
| Missing root ref | Constant not linked to root | Add reference to root entity (e.g. `platform="platform()"`). |
| Depth exceeded | Too many nested references | Remove one reference or use string field. |
| Sensitive field | Token/key/password detected | Add `_audit_mask_fields="field_name"`. |
| Disconnected graph | Entity not connected to root | Connect to its natural parent or the root (e.g., add `merchant="merchant(context)"`). |
| `no method named update_xxx` | Guessing method names | Read the entity source file for the exact correct method name. |
| `Missing .audit_as()` | Unaudited save/update | Add `.audit_as("description")` before `.save()` or `.update()`. |
| `Missing .purpose()` | Unjustified query | Add `.purpose("why")` and `.comment("what")` before `.execute_for_list()`. |
| Reserved keyword | Using a language keyword | Rename attribute (e.g., `type` -> `item_kind`, `user` -> `user_account`). |
