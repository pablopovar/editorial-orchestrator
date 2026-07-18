---
name: Compress
description:
enabled: true
legacy_id: 12
object_type: step
step_type: transformer
---

This step does:
1. Analyze session_payload against criteria for filler, redundancy, and non-essential material.
2. Reduce content while preserving the conceptual spine and return it in StepResult.session_payload.
