# Pi: recover the actual old session without tools

On 2026-10-25 (Asia/Shanghai), the target Pi session `01a16ecb-97a2-771e-b335-b7aca163bc36` repeatedly promised
to check old compiler errors, even after the user requested business scenarios
from an expanded model. Recent replies made no tool calls and the model server
was idle. Restarting a process while resuming that history did not remove the
loop. The existing completion guard covered successful edits, not this case.

## Implemented recovery

The protected native CLI now detects three similar action-promise replies with
no intervening tool call/result in a bounded recent window. It handles English
and Chinese, including short replies such as "Let me check the file." Factual
repeated answers and explicit blocker codes are excluded. This is a heuristic;
it does not semantically classify every ignored task.

A visible `CONTEXT_RECOVERED` host marker starts a request-local recovery view:

- retain system and tool instructions and active lifecycle/policy context;
- retain **all user instructions**, including older constraints;
- retain the recovery marker and all subsequent messages and tool results;
- omit earlier assistant narratives and tool results from the model request;
- leave the original transcript and session ID intact, appending audit/control
  records rather than deleting history.

The host restores the anchor from the selected native session branch. Pasted
user text or tool output cannot impersonate a host recovery marker. Project
files remain freshly checked; recovery adds no tools or access permissions.
There is one automatic recovery per user request. A renewed promise-only stop
without a tool attempt after recovery yields `STALLED_NO_TOOL_PROGRESS`.
Cancellation, provider errors and an existing completion continuation do not
start another recovery.

## Actual old-session validation

The deployment backed up the original session, confirmed the model server was
idle, and gracefully stopped the idle old Pi process before resuming the same
session file through the updated ordinary `pi` command. No `/new` was used.
The original file is:

```text
~/.pi/agent/sessions/--home-ai-t003--/
  2026-10-24T16-43-18-818Z_01a16ecb-97a2-771e-b335-b7aca163bc36.jsonl
```

The first recovery retained the original 97 records byte-for-byte, emitted one
recovery marker, read `models/school-service.xml` and the application guide, and
finished analysis in approximately 48 seconds. A new Pi process then continued
the same session and answered a distinct follow-up question without another
recovery or a manual continuation prompt.

During review the implementation was tightened to preserve all prior user
instructions instead of only recent turns. Native session branching replayed
the original stalled position to verify that behavior. Existing validation
branches and all previous records stayed in the same append-only file. The final
release was replayed from that original position as well. It emitted one recovery
marker on the active branch, made four successful permitted reads, completed
analysis in **34 seconds**, and exited 0 from one initial task prompt with no
manual continuation. The transcript then contained 135 records across the
preserved branches, with the original 97-record byte prefix intact. Source/model
hashes were unchanged. Its native event stream, branch metadata, exit status and
preservation checks are stored below.

The current model has eleven objects, including grade, class, teacher, course,
enrollment and enrollment status. The recovered agent read current files and
produced scenario analysis instead of repeating obsolete compiler errors. This
verifies restored tool use and conversation progress, not correctness of every
business inference. One analysis response's introductory entity count disagreed
with its table; the output is not treated as a validated business specification.
No model evaluation, application generation, compilation or database runtime
verification was requested by this read-only recovery task.

## Tests and evidence

The repository check passed **154 tests**: 118 package unit tests, 21 integration
tests, 8 root contract tests and 7 Python tests. New coverage includes:

- Chinese/English and short promise loops, normal factual answers and blockers;
- real tool progress resetting the detector;
- retention of old user constraints, system/policy context and new tool results;
- rejection of fake user-authored recovery anchors;
- bounded recovery, cancellation and completion-guard coexistence;
- the native Pi CLI resuming a persisted stuck session through its actual SDK
  and deterministic provider, while preserving its transcript and read policy.

Host evidence:

```text
~/.pi/agent/integrations/pi-teaql/evidence/
  old-session-recovery-20261025T101131Z/
    before-stop-session.jsonl
    resume-input.jsonl
    events.jsonl
    follow-up-events.jsonl
    final-all-user-instructions/
    deployed-final-replay/
    summary.json
```

The deployed package archive SHA-256 is:

```text
e89cb1000e5491235c7015c334fe084423f5ea6aed75c256ac037055c15b7b78
```

The backups and event streams remain host-private. No token savings are claimed.
The previously running process was replaced for this deployment; the validation
loaded the original session in the updated CLI, rather than hot-patching code
inside an already running process. Future resumes of that session retain the
recovery boundary. OpenCode's profile does not include this Pi-specific guard.
