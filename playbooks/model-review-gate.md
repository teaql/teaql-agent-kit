# Model Ready Signal and Parallel Review

Use this playbook after modeling and KSML evaluation are complete. The
historical filename is retained for compatibility, but this is not a blocking
gate.

## Required Signal

When evaluation has zero errors, immediately notify the user with two facts:

- **Model path** — the concrete path to the single model file or complete
  multi-file model directory.
- **Evaluation result** — whether evaluation passed, plus the error, warning,
  and suggestion counts.

Use this compact format:

```text
Model Ready
- Model: /absolute/path/to/models/model.xml
- Evaluation: passed — 0 errors, 2 warnings, 1 suggestion
```

For a multi-file model, point to the complete model directory and optionally
name its authoritative `main.xml` entrypoint:

```text
Model Ready
- Model: /absolute/path/to/models
- Entrypoint: /absolute/path/to/models/main.xml
- Evaluation: passed — 0 errors, 0 warnings, 3 suggestions
```

Use a path the user can open directly. Do not replace it with a long entity or
relationship summary: the signal exists so the user can inspect the model
itself.

## Continue Without Waiting

The signal is a milestone notification, not a confirmation request. After
sending it, continue with generation, implementation, testing, and repair.

Human review happens in parallel. If asynchronous feedback changes the domain
contract, update the model, evaluate it again, send an updated Model Ready
signal, regenerate affected outputs, and continue. Never patch generated files
to imitate a model change.

Evaluation errors still block generation. Fix them and rerun evaluation before
sending the Model Ready signal. Warnings and suggestions do not block
generation, but their counts must be visible in the signal.

Pause only for a genuine blocker that cannot be resolved safely, such as
missing business information that would materially change the system or a new
action requiring user authority.

## Report Requirement

Project or playground reports should record:

- The exact Model Ready signal.
- When it was sent.
- Asynchronous feedback received.
- Model revisions and subsequent evaluation results.

The report must not imply that generation waited for user confirmation.
