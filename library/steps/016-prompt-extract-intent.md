---
name: PromptExtractIntent
description:
enabled: true
legacy_id: 16
object_type: step
step_type: transformer
---

This step does:
1. Analyze session_payload for the user’s intended assistant function, task family, posture, constraints, and allowances.
2. Append the extracted prompt intent into the payload state and return it in StepResult.session_payload.
