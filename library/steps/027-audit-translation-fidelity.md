---
name: AuditTranslationFidelity
description:
enabled: true
legacy_id: 27
object_type: step
step_type: control
step_inputs: payload, contextual_data, instructions_definition, goals_success_definition, session_payload
---

This step does:
1. Compare translated session_payload against immutable payload and the governing translation constraints.
2. Analyze translation equivalence, untranslated residue, omitted qualifiers, meaning drift, structural distortion, and localization creep.
3. Populate StepResult.step_output with a translation fidelity audit report.
4. Return StepResult with an unchanged session_payload.
