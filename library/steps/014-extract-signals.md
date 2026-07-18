---
name: ExtractSignals
description:
enabled: true
legacy_id: 14
object_type: step
step_type: transformer
---

This step does:
1. Analyze session_payload against contextual requirements for its top three strongest signals.
2. Append those extracted signals into a copy of the payload state and return it in StepResult.session_payload.
