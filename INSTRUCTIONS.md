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
<context_definition>
[Place contextual information here.]
</context_definition>

<instructions_definition>
[Place direct instructions here.]
</instructions_definition>

<success_conditions_definition>
[Place success conditions here.]
</success_conditions_definition>

<other_definitions>
[Optional. Place exclusions, constraints, notes, or other supporting definitions here.]
</other_definitions>

<payload>
[Place the source input here.]
</payload>

<session>

<library_reference>
[Optional. Specify the active library if more than one library exists. If omitted, use the loaded default library.]
</library_reference>

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

<explicit_directives>
[Optional. Place run-specific directives here.]
</explicit_directives>

<output_settings>
step_output: [quiet | minimal | full]
loop_output: [quiet | full]
final_payload_output: [off | full]
</output_settings>

</session>
```

---

## Structured Input block breakdown

### `context_definition`
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

### `success_conditions_definition`
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

### `other_definitions`
Use this block for everything important that does not belong naturally in the first three blocks.

This is the pressure-release block. It keeps the main definitions clean while still allowing additional constraints.

Typical contents:
- tone constraints
- exclusions
- editorial pressure points
- caveats
- publication logic
- things to avoid
- removable or suspect sections
- special handling notes

Ask:
**What matters, but does not fit neatly elsewhere?**

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

---

### `session`
Use this block to configure the run.

This is where you choose the working stack and execution behavior.

Session contains:

- `library_reference` — which library to use
- `role` — one Role from the library
- `mode` — one Mode from the library
- `steps` — ordered Steps to execute
- `loops` — number of loop cycles
- `explicit_directives` — optional run-specific instructions
- `output_settings` — visibility settings

Ask:
**How should this run behave?**

---

## How to think about the blocks

A good Structured Input usually has this shape:

- **Context** explains the world around the artifact.
- **Instructions** explain what to do.
- **Success conditions** explain what the result must accomplish.
- **Other definitions** capture special constraints.
- **Payload** supplies the source material.
- **Session** selects the method.

That is the simplest way to think about it.

---

## Example use cases

### Revision / corrective work
- Role: `Writer`
- Mode: `PackRanger`
- Steps: `NotLikeThat`, `LikeThisInstead`, `Consolidate`

### Ex-novo generation
- Role: `Seeder`
- Mode: `Creative` or `PackRanger`
- Steps: `ExplodeTheBasis`, `Orthogonalize`, `Consolidate`

### Compression audit
- Role: `Writer`
- Mode: `Creative`
- Steps: `Compress`, `AuditCompress`, `Consolidate`

### Title generation
- Role: `Writer`
- Mode: `Creative`
- Steps: `ExtractTitleSignal`, `TitleFromSignal`

---

## Output settings

```xml
<output_settings>
step_output: [quiet | minimal | full]
loop_output: [quiet | full]
final_payload_output: [off | full]
</output_settings>
```

### `step_output`
Controls per-step visibility.

- `quiet` — print nothing at step level
- `minimal` — print progress lines such as `Loop 1 - Step 2: Done`
- `full` — print step name and step output when present

### `loop_output`
Controls whether the full working payload is shown at the end of each loop.

- `quiet` — no loop-level print
- `full` — print the full `session_payload` after each loop

### `final_payload_output`
Controls whether the final working payload is printed at the end of execution.

- `off` — do not print the final result
- `full` — print the full final `session_payload`

---

## Practical advice

- Do not overload `instructions_definition` with background. Put background in `context_definition`.
- Do not treat `success_conditions_definition` as a restatement of instructions. Use it to define functional success.
- Do not use more Steps than the task requires.
- Do not increase loops unless another pass is likely to produce a real gain.
- Use `other_definitions` to keep the main blocks clean.
- Treat the payload as source material, not as a place for instructions.

---

## Extending the system

One of the strengths of the Orchestrator is how easy it is to extend.

You do not need to rewrite the app to add a new editorial operation. You can add a new Role, Mode, or Step to the Library and then select it in Session.

That makes the system easy to grow without making the engine heavier.

---

## Suggested starting point

If you are new to the system:

- keep the payload focused
- choose one Role
- choose one Mode
- use only the minimum Steps needed
- start with 1–2 loops
- keep output visible enough to inspect but not so noisy that the run becomes hard to read

Then refine from there.
