---
name: ImproveTranslationFidelity
description:
enabled: true
legacy_id: 26
object_type: step
step_type: transformer
---

This step does:
1. Analyze translated session_payload for semantic weakness, collapsed distinctions, or structural drift.
2. Correct the content to restore original qualifiers and logical relationships, and return the modified state in StepResult.session_payload.
