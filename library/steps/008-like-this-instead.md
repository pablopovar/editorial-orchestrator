---
name: LikeThisInstead
description:
enabled: true
legacy_id: 8
object_type: step
step_type: transformer
---

Adhere to `contextual_data`, `instructions_definition`, and `goals_success_definition` as the governing frame.
Select one or more elements of session_payload —such as the title, length, pace, flow, content, or specific parts of it— and:
Say "This can be improved" and elaborate:
Say "This can be omitted" and elaborate:
Populate and return full, modified state in StepResult.session_payload.
