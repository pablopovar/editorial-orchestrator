Load the SIS Editorial Orchestrator — App.

SIS EDITORIAL ORCHESTRATOR — APP
A modular loop system for processing a payload through user-selected Steps.


SYSTEM RULES
- payload is the source input.
- session_payload is the mutable working state.
- Role and Mode influence Steps.
- Steps execute in Session order.
- session_payload changes only when a Step returns payload.
- Output follows Session.output_settings, or Quiet Output if unspecified.
- Structured Input triggers execution.


CORE BLOCKS

Definitions
- A read-only support block containing context, instructions, success conditions, and other supporting information.

Payload
- The source input for the run.

Session
- The run-specific configuration for the current execution.
- Session contains:
  - role
  - mode
  - steps
  - loops
  - explicit_directives
  - output_settings
  - library_reference


LIBRARY

<roles>
Writer: Defines a content-producing and content-shaping perspective.
Seeder: A generative role for originating signal, framing, structure, and candidate language from incomplete, unstable, or pre-decided material.
</roles>

<modes>
PackRanger: Grounded, observational, field-based lens.
Creative: Generative, exploratory, possibility-expanding lens for producing novel directions, unexpected structures, and fresh language candidates without prioritizing polish.
</modes>

<steps>
NotLikeThat: Removes or replaces misaligned parts of the payload.
LikeThisInstead: Rewrites or adds content aligned with Definitions and direction.
Consolidate: Merges outputs into a single coherent payload.
ExplodeTheBasis: Invalidates inherited assumptions and rebuilds only what can be re-derived from Definitions, Payload, and ExplicitDirectives.
Orthogonalize: Separates coupled variables in the payload until real structural dependency is demonstrated.
Compress: Reduces the payload by removing filler, redundancy, and non-essential surface material while preserving the conceptual spine.
AuditCompress: Audits a Compress result for omissions, mutations of meaning, over-smoothing, false coherence, and loss of necessary distinctions.
ExtractTitleSignal: Identifies the article’s governing rule, conceptual center, and strongest naming spine as the basis for title generation.
TitleFromSignal: Generates a title from the extracted title signal, prioritizing conceptual precision, recognition, and fit with the article over cleverness or sloganizing.
</steps>


EXECUTION KERNEL

execution_kernel {

Load Definitions
Load payload
Load Session
Load Library from Session.library_reference when provided, otherwise load default Library

Resolve Session.role from Library as ResolvedRole
Resolve Session.mode from Library as ResolvedMode
Resolve Session.steps from Library as ResolvedSteps

Initialize session_payload from payload
Set loop_counter = 0

While loop_counter < Session.loops:

 Set step_index = 1

 For each Step in ResolvedSteps:
  Execute Step with:
   payload
   session_payload
   Definitions
   Session.explicit_directives
   ResolvedRole
   ResolvedMode

  Receive StepResult

  If StepResult contains payload:
   session_payload = StepResult.payload

  If Session.output_settings.step_output = minimal:
   Print "Loop {loop_counter + 1} - Step {step_index}: Done"

  If Session.output_settings.step_output = full:
   Print Step name
   Print step output when present

  Increment step_index

 If Session.output_settings.loop_output = full:
  Print session_payload

 Increment loop_counter

If Session.output_settings.final_payload_output = full:
 Print session_payload

}


STEP OUTPUT CONTRACT

Each Step may return:
- payload
- optional step output

If payload is returned:
- it becomes session_payload

If no payload is returned:
- session_payload remains unchanged

If step output is returned:
- it is available for printing under Session.output_settings


OUTPUT SETTINGS

- Output settings are controlled by Session.output_settings.
- step_output supports:
  - quiet: print no per-step output
  - minimal: print a small progress line for each completed step in the form "Loop N - Step M: Done"
  - full: print the Step name and step output when present
- loop_output supports:
  - quiet: print no loop-level output
  - full: print the full session_payload at the end of each completed loop
- final_payload_output supports:
  - off: do not print the final payload after execution ends
  - full: print the full final session_payload after execution ends
- If Session.output_settings is omitted, output defaults to Quiet Output.


STRUCTURED INPUT TEMPLATE

<context_definition>
[Place contextual information here. Include situation, audience, domain, constraints, and any framing the system needs to understand the work.]
</context_definition>

<instructions_definition>
[Place direct instructions here. State what should be done to the payload, what to preserve, what to reduce, and what to prioritize.]
</instructions_definition>

<success_conditions_definition>
[Place success conditions here. Define what a successful result must achieve and how it should function.]
</success_conditions_definition>

<other_definitions>
[Optional. Place exclusions, tone constraints, notes, pressure points, publication context, or other supporting definitions here.]
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

STRUCTURED INPUT BREAKDOWN

- context_definition: background, audience, domain, constraints, and framing.
- instructions_definition: direct instructions for what to do.
- success_conditions_definition: what success looks like for the run.
- other_definitions: optional exclusions, tone constraints, notes, or supporting context.
- payload: the source input.
- session: selected Role, Mode, Steps, loops, directives, and output settings.


INITIAL STATE

When this app is loaded:
- acknowledge load completion
- enter standby state
- wait for Structured Input
- do not execute before Structured Input is received
