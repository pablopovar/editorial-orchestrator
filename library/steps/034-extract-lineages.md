---
name: ExtractLineages
description:
enabled: true
legacy_id: 34
object_type: step
step_type: transformer
---

This step does:
1. Analyze session_payload for relational concept descent, branch splits, and parent-child hierarchies.
2. Append this lineage mapping to the document state and return it in StepResult.session_payload.
