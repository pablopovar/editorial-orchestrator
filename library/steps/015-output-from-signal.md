---
name: OutputFromSignal
description:
enabled: true
legacy_id: 15
object_type: step
step_type: transformer
---

This step does:
1. Analyze session_payload for extracted signals.
2. Generate output candidates from those signals prioritizing conceptual precision and structural fit.
3. Append the generated candidates to the payload state and return it in StepResult.session_payload.
