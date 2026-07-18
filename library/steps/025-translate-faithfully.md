---
name: TranslateFaithfully
description:
enabled: true
legacy_id: 25
object_type: step
step_type: transformer
---

This step does:
1. Analyze session_payload against variables and constraints before translating.
2. Translate content into the target language with maximum fidelity to original meaning, technical accuracy, and structural relationships.
3. Avoid unrequested localization or smoothing. Return the translation in StepResult.session_payload.
