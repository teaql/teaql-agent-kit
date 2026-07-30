# TeaQL KSML Modeling Task

## Business Requirement

```text
{{business_requirement}}
```

## Model Target

Save the complete model at:

```text
{{model_path}}
```

The target may be one XML file or a directory containing `main.xml` and its
included model files.

## Quality Feedback

Use this command after saving the model and after every repair round:

```bash
{{evaluation_command}}
```

The evaluation command must submit the complete model target. For Rust clients,
use:

```bash
cargo teaql --input {{model_path}} evaluate
```

For a multi-file model, `{{model_path}}` must be the complete directory, not
only `main.xml`.

Follow the system prompt and supplied `golden-example.xml`. Evaluation must
report zero errors before generation, but the requested business result is the
completion target.

At completion, load `prompts/reporting/work-complete.md`. Include concrete
verification results, honest token/context metrics, the reduction in mechanical
Review work, the original modeling prompt, modeling-result summary, generated
API and assist evidence, purpose/comment and audit policy counts, one simple
next-use command, and a short execution log.
