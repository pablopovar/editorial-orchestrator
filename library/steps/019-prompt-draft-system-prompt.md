---
name: PromptDraftSystemPrompt
description:
enabled: true
legacy_id: 19
object_type: step
step_type: transformer
---

This step does:
1. Analyze session_payload for the prompt contract.
2. Draft a system prompt from that contract, append it to the payload state, and return it in StepResult.session_payload.
