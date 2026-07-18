---
name: PromptAuditFit
description:
enabled: true
legacy_id: 20
object_type: step
step_type: control
---

This step does:
1. Analyze session_payload for drift, overreach, vagueness, or mismatch with the extracted prompt intent and contract.
2. Populate StepResult.step_output with a prompt-fit audit report.
3. Return StepResult with an unchanged session_payload.
