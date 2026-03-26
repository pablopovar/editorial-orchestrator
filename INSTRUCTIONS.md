# Instructions

## Intended use

Use the app as a loadable editorial runtime.

The app should be loaded first.
Once loaded, the assistant should acknowledge and wait for Structured Input.

## Operating model

- `payload` = source input
- `session_payload` = mutable working state
- Roles and Modes influence Steps
- Steps execute in Session order
- `session_payload` changes only when a Step returns payload
- Output follows `Session.output_settings`, or Quiet Output if unspecified

## Recommended workflow

1. Load the app.
2. Keep the system in standby.
3. Provide Structured Input only when ready to run.
4. Select only the library objects needed for the task.
5. Keep loops low unless iteration is truly needed.

## Structured Input Template

Use this template for every run.

```xml
<context_definition>
[Place contextual information here. Include the situation, audience, domain, page/article context, constraints, or any framing the system needs to understand the work.]
</context_definition>

<instructions_definition>
[Place direct instructions here. State what should be done to the payload, what to preserve, what to reduce, what to prioritize, and any execution-specific guidance.]
</instructions_definition>

<success_conditions_definition>
[Place success conditions here. Define what a successful result must achieve, how the result should function, and what “good” looks like for this run.]
</success_conditions_definition>

<other_definitions>
[Optional. Add exclusions, tone constraints, editorial pressure points, publication context, or any other supporting definitions that do not fit cleanly in the three main blocks.]
</other_definitions>

<payload>
[Place the source input here. This is the original content or object the run is based on.]
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
[Optional. Add run-specific directives that should shape this execution beyond the main definitions blocks.]
</explicit_directives>

<output_settings>
step_output: [quiet | minimal | full]
loop_output: [quiet | full]
final_payload_output: [off | full]
</output_settings>

</session>
```

## Block breakdown

### `context_definition`
Use this for background and framing.
What is this artifact? Who is it for? In what context will it be read or used? What surrounding conditions matter?

### `instructions_definition`
Use this for direct task instructions.
What should the system do? Rewrite, compress, audit, generate, title, restructure, etc.

### `success_conditions_definition`
Use this for outcome criteria.
How should the result function? What would make the output successful?

### `other_definitions`
Use this for anything important that does not belong naturally in the first three blocks.
This is where tone constraints, exclusions, pressure points, caveats, or publication logic can live.

### `payload`
Use this for the source input.
This is the content the run starts from.

### `session`
Use this to select the stack and execution settings.
This is where you choose the Role, Mode, Steps, number of loops, optional directives, and output behavior.

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

## Output settings

```xml
<output_settings>
step_output: [quiet | minimal | full]
loop_output: [quiet | full]
final_payload_output: [off | full]
</output_settings>
```
