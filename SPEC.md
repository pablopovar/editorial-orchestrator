# EdOr Web beta specification

## Purpose

The beta is a thin Python orchestrator. It handles the start of a run, ordered Step handoffs, loops, and the end of a run.

It does not redesign or complete the full EdOr protocol.

## Library

Roles, Modes, and Steps are independent Markdown files in their corresponding buckets:

```text
library/roles/
library/modes/
library/steps/
```

Adding a valid file makes the object available. The UI reads and edits the same files.

## Structured Input

The UI builds these stable fields:

- `contextual_data`
- `instructions_definition`
- `goals_success_definition`
- `payload`

The selected Role, Mode, ordered Steps, and loop count are included in `session_directives`.

## Execution

1. Resolve the selected Role, Mode, and ordered Steps.
2. Preserve the submitted `payload` unchanged.
3. Initialize `session_payload = payload`.
4. For each loop, execute each selected Step in order.
5. Make one independent model call per Step.
6. Present the complete Structured Input to every model call.
7. Add the selected Role definition, Mode definition, current Step execution logic, and current `session_payload`.
8. Receive the complete next `session_payload`.
9. Pass that value to the next Step.
10. After the last Step of the last loop, return the final `session_payload`.

No chat history is carried between model calls.

## Excluded from the initial beta

- UserStep
- TurnTurnover
- pause/resume
- StepContext
- declared Step inputs
- control/transformer enforcement
- dependency preflight
- history policies
- payload schema validation
- HALT/FAIL protocol machinery
