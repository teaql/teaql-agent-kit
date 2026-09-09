# Controlled Generated-Source Fallback

Use this exception only after normal progressive Assist reported
`MISSING_ASSIST`, a compiler diagnostic identifies a generated-code problem,
and the user or orchestrator explicitly authorized generated source inspection.
Verification or confidence gathering is never sufficient reason. An agent
cannot authorize its own fallback.

Request authorization with:

```text
SOURCE_FALLBACK_REQUEST
language: <language>
entity: <KSML entity>
action: <assist action>
missing_operation: <operation absent from Assist>
compiler_error: <exact diagnostic, or not available>
requested_file: <one exact generated file>
requested_lines: <start>-<end, at most 80 lines>
reason: <why Assist and compiler diagnostics are insufficient>
```

Authorization applies only to the named file and line range. Do not search
recursively, read a complete generated file, inspect adjacent files, or infer
permission for a second request. Generated source remains read-only.

Record the request, authorization, inspected range, finding, and resulting
`MISSING_ASSIST` defect in the completion evidence.
