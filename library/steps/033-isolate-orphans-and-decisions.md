---
name: IsolateOrphansAndDecisions
description:
enabled: true
legacy_id: 33
object_type: step
step_type: transformer
---

This step does:
1. Analyze session_payload for orphaned topics, unmade decisions, and under-integrated concepts.
2. Append these isolated elements as a distinct pass layer and return the updated state in StepResult.session_payload.
