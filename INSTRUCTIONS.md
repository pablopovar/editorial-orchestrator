# Instructions

## What this file is for

This file explains how to use the SIS Editorial Orchestrator in practice.

The Orchestrator runs from **Structured Input**. That means you do not just paste a draft and say “improve this.” You provide a shaped input that tells the system:

- what the payload is
- what the job is
- what success looks like
- which stack should run
- how visible the run should be

That structure is what makes the system reusable and controllable.

---

## Operating model

The Orchestrator works from a small set of stable ideas:

- `payload` = source input
- `session_payload` = mutable working state
- Roles and Modes influence Steps
- Steps execute in Session order
- `session_payload` changes only when a Step returns payload
- Output follows `Session.output_settings`, or Quiet Output if unspecified

The app remains fixed. You change behavior by changing the selected stack.

---

## Recommended workflow

1. Load the app.
2. Let the assistant acknowledge load completion and enter **Structured Input** standby.
3. Prepare your Structured Input.
4. Select only the Role, Mode, and Steps needed for the task.
5. Run the stack.
6. Review the output.
7. Refine the Structured Input and rerun if needed.

Keep loops low unless another pass is likely to produce structural improvement rather than cosmetic churn.

---

## Structured Input Template

Use this template for every run.

```xml
STRUCTURED INPUT TEMPLATE

Structured Input template.
Recommended minimal: contextual_data, instructions_definition, goals_success_definition, payload.

<structured_input>
  <contextual_data>
  [Context, audience, domain, or relevant constraints.]
  </contextual_data>

  <instructions_definition>
  [What should be done to the payload.]
  </instructions_definition>

  <goals_success_definition>
  [Goals and success criteria.]
  </goals_success_definition>

  <payload>
  [Source input.]
  </payload>

  <session_directives>
    <role>
    [Select one Role from the Library.]
    </role>

    <mode>
    [Select one Mode from the Library.]
    </mode>

    <steps>
    [Provide the ordered list of Steps to execute.]
    </steps>

    <loops>
    [Provide the number of loop cycles to run.]
    </loops>

    <step_output>
    [quiet | minimal | full | double]
    </step_output>

    <loop_output>
    [quiet | full]
    </loop_output>

    <final_payload_output>
    [off | full | double]
    </final_payload_output>
  </session_directives>
</structured_input>
```

---
## Structured Input block breakdown

### `contextual_data`
Use this block for background and framing.

This is where you tell the system what kind of artifact it is dealing with, who it is for, what context it lives in, what surrounding conditions matter, and what broader situation should shape interpretation.

Typical contents:
- audience
- publication context
- site/page context
- surrounding ecosystem
- domain framing
- pressure state
- what kind of artifact this is

Ask:
**What does the system need to understand before touching the payload?**

---

### `instructions_definition`
Use this block for direct task instructions.

This is where you tell the system what to do to the payload.

Typical contents:
- rewrite
- compress
- improve
- audit
- title
- restructure
- reduce overlap
- preserve central distinctions
- remove filler
- shift audience fit

Ask:
**What is the job?**

---

### `goals_success_definition`
Use this block for outcome criteria.

This is where you define what a successful result must do, how it should function, and what “good” means for this run.

Typical contents:
- functional success criteria
- conversion/funnel criteria
- clarity requirements
- audience recognition requirements
- structural requirements
- quality thresholds

Ask:
**How will we know the run succeeded?**

---

### `payload`
Use this block for the source input.

This is the original content or object the run starts from.

Examples:
- article draft
- homepage draft
- outline
- titleless essay
- compressed notes
- raw copy
- source document to audit

The payload is not the instructions. It is the thing being worked on.

Ask:
**What is the source material for this run?**

### `session_directives`
Use this block to configure the run.

This is where you choose the working stack and execution behavior.

Session directives contain:

- `role` — one Role from the Library
- `mode` — one Mode from the Library
- `steps` — ordered Steps to execute
- `loops` — number of loop cycles
- `step_output` — per-step visibility [quiet | minimal | full | double]
- `loop_output` — per-loop visibility [quiet | full]
- `final_payload_output` — final output visibility [off | full | double]

Ask:
**How should this run behave?**
---

## How to think about the blocks

A good Structured Input usually has this shape:

- **Contextual data** explains the world around the artifact.
- **Instructions** explain what to do.
- **Goals and success conditions** explain what the result must accomplish.
- **Payload** supplies the source material.
- **Session directives** selects the method.

That is the simplest way to think about it.

---

## Example use cases

### Revision / corrective work
- `role`: `Writer`
- `mode`: `PackRanger`
- `steps`: `NotLikeThat`, `LikeThisInstead`, `Consolidate`

Use when the payload already exists and needs correction, tightening, or directional improvement.

### Exploratory generation from weak or unstable material
- `role`: `Seeder`
- `mode`: `Creative`
- `steps`: `ExplodeTheBasis`, `Orthogonalize`, `Consolidate`

Use when the starting material is rough, unstable, incomplete, or conceptually under-formed.

### Compression with verification
- `role`: `Writer`
- `mode`: `PackRanger`
- `steps`: `Compress`, `AuditCompress`, `Consolidate`

Use when the goal is to reduce length or density without losing key meaning or distinctions.

### Loop audit / drift check
- `role`: `Writer`
- `mode`: `PackRanger`
- `steps`: `NotLikeThat`, `LikeThisInstead`, `Consolidate`, `AuditLoop`

Use when you want a normal transformation stack followed by a loop-level check for drift, weak continuation, or diminishing returns.

### Signal extraction
- `role`: `Writer`
- `mode`: `PackRanger`
- `steps`: `ExtractSignals`

Use when the goal is to surface the strongest signals in the current payload without changing the working state.

### Title generation from extracted signals
- `role`: `Writer`
- `mode`: `Creative`
- `steps`: `ExtractSignals`, `TitleFromSignal`

Use when the goal is to derive title candidates from the strongest signals in the payload.

### Assistant / prompt design
- `role`: `Writer`
- `mode`: `PackRanger`
- `steps`: `ExtractAssistantIntent`, `InferOperationalDefaults`, `DefinePromptContract`, `DraftSystemPrompt`, `AuditPromptFit`

Use when the payload is a rough assistant concept, prompt idea, or behavioral description that needs to become a system prompt.