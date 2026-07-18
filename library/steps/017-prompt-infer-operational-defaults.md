---
name: PromptInferOperationalDefaults
description:
enabled: true
legacy_id: 17
object_type: step
step_type: transformer
---

This step does:
1. Analyze session_payload for missing but necessary prompt constraints, boundaries, and allowances.
2. Infer minimal sensible prompt defaults, append them to the payload state, and return it in StepResult.session_payload.
