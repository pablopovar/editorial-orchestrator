---
name: ConsolidatePasses
description:
enabled: true
legacy_id: 36
object_type: step
step_type: transformer
---

This step does:
1. Analyze session_payload elements (base document, addenda, classification layers, passes) and merge them into a unified, duplication-free document.
2. Preserve unresolved ambiguities cleanly and return the consolidated state in StepResult.session_payload.
