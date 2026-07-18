---
name: PromptDefineContract
description:
enabled: true
legacy_id: 18
object_type: step
step_type: transformer
---

This step does:
1. Analyze session_payload for extracted prompt intent, inferred defaults, and missing structure.
2. Convert them into a prompt contract covering scope, behavior, and posture, append to state, and return in StepResult.session_payload.
