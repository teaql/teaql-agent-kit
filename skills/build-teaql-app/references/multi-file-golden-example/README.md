# Multi-file KSML golden example

Use this structure when a model is split across files:

```text
models/
├── main.xml
├── organization.xml
└── operations.xml
```

- `main.xml` is the only entry file. Its `<root>` owns service-level settings
  and contains the `_include` elements.
- Every included file is a complete XML document with exactly one top-level
  `<root>` element.
- Included roots do not repeat `name`, `org`, `data_service`, or
  `_module_key`.
- All object definitions are direct children of the root in their own file.
- Evaluate and generate by passing the directory, not only `main.xml`:

```bash
cargo teaql --input models/ evaluate
```

The three XML files in this directory form one complete, connected example.
Copy the file structure and grammar, but replace the sample business concepts
with the user's actual domain.
