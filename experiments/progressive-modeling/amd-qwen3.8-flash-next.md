# AMD Qwen3.8 Flash Next — P0 Probe

Date: 2026-09-10

Service: AMD Radeon API, OpenAI-compatible Chat Completions

Model requested and used: `Qwen3.8-Flash-Next`

Credentials, request IDs, organization IDs, and provider log IDs are not
retained in this repository.

## Connectivity probe

| Result | Wall time | Prompt | Completion | Reasoning |
| --- | ---: | ---: | ---: | ---: |
| HTTP success, greeting returned | about 2.5 s | 53 | 29 | 18 |

## Progressive-modeling P0 probe

The bounded task asked for a strict JSON domain map for a moving-company
system. The response contract required a business outcome, domain root,
modules with no more than eight candidate objects, one-hop module
dependencies, a connected first vertical slice, and open questions.

### Default thinking

| Result | Wall time | Prompt | Completion | Reasoning | Cost |
| --- | ---: | ---: | ---: | ---: | ---: |
| failed: empty content, `finish_reason=length` | about 68.6 s | 315 | 2,200 | 2,200 | about $0.00208 |

The full completion budget was consumed by hidden reasoning. No candidate
artifact was produced.

### Thinking disabled

Request controls:

```json
{
  "reasoning_effort": "none",
  "chat_template_kwargs": {"enable_thinking": false}
}
```

| Result | Wall time | Prompt | Completion | Reasoning | Cost |
| --- | ---: | ---: | ---: | ---: | ---: |
| strict JSON candidate returned | about 38.6 s | 279 | 1,301 | 0 | about $0.00065 |

The output satisfied the requested JSON shape, snake-case identifiers,
candidate-object limit, and internal module-dependency references.

## Semantic findings

The candidate is useful but not ready to become KSML:

1. It selected `move` as the domain root. `move` is a plausible Aggregate
   Root, but the TeaQL service graph should be rooted at `moving_company`.
2. It proposed `role` in both Employees and Authentication, leaving ownership
   ambiguous. Separate concepts such as `job_role` and `access_role` are
   required.
3. It collapsed compliance, audit, notifications, versioning, and integration
   concerns into one `admin` module, losing explicit requested boundaries.
4. Some exclusion names did not match the candidate object vocabulary.

## Conclusion

This hosted model is suitable for bounded progressive-modeling candidate work
when thinking is explicitly disabled. It is not a source of truth. A
deterministic contract checker, TeaQL evaluation, and a repair checkpoint are
still required before the artifact may advance.

The next probe should request a compact patch for only the four findings above
instead of asking the model to regenerate the complete domain map.
