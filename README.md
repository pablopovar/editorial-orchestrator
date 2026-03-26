# SIS Editorial Orchestrator

The SIS Editorial Orchestrator is a small editorial runtime.

It does not hardcode one editorial method. It loads a **source payload**, a **session**, and a **selected stack** of library objects, then runs the stack in order. The core stays the same. The method changes by changing the selected Role, Mode, and Steps.

## What it is

The Orchestrator is built from three parts:

- **App** — the execution engine
- **Library** — selectable Roles, Modes, and Steps
- **Structured Input** — the run configuration and source material

The app is deliberately simple:

- `payload` = source input
- `session_payload` = mutable working state
- Role and Mode influence Steps
- Steps execute in Session order
- `session_payload` changes only when a Step returns payload

## How the loop works

A run is a loop over selected Steps.

1. Load Definitions, payload, Session, and Library.
2. Resolve the selected Role, Mode, and Steps from the Library.
3. Initialize `session_payload` from `payload`.
4. Run the selected Steps in order.
5. If a Step returns payload, replace `session_payload`.
6. Repeat for the configured number of loops.
7. Print according to `output_settings`.

This means the system can support very different editorial jobs without changing the core.

## Example step behavior

A Step is just a named operation in the Library.

Example:

`Compress: Reduces the payload by removing filler, redundancy, and non-essential surface material while preserving the conceptual spine.`

If `Compress` is included in the session stack, it will run where it appears in the step order. If it returns a new payload, that new payload becomes the next `session_payload`.

## Example stacks

### Revision / corrective work
- Role: `Writer`
- Mode: `PackRanger`
- Steps: `NotLikeThat`, `LikeThisInstead`, `Consolidate`

### Ex-novo generation
- Role: `Seeder`
- Mode: `Creative`
- Steps: `ExplodeTheBasis`, `Orthogonalize`, `Consolidate`

### Compression audit
- Role: `Writer`
- Mode: `Creative`
- Steps: `Compress`, `AuditCompress`, `Consolidate`

### Title generation
- Role: `Writer`
- Mode: `Creative`
- Steps: `ExtractTitleSignal`, `TitleFromSignal`

## Why the library matters

The library is flexible on purpose.

One of the system’s strengths is how easy it is to add new Steps without changing the app. The core logic does not need to know whether a Step is corrective, generative, auditing, compressive, or title-related. It only needs to run the selected stack in order.

That keeps the system lean:

- the **app** stays small
- the **library** grows as needed
- the **session** selects only the objects needed for the task

## Repository contents

- `README.md` — overview, loop concept, and examples
- `INSTRUCTIONS.md` — usage guidance and structured-input template with field notes
- `APP.md` — the loadable app / engine
- `sample-definitions-block.xml` — sample definitions block for article improvement

## Quick start

1. Load `APP.md`.
2. Wait for the assistant to acknowledge and enter **Structured Input** standby.
3. Submit your customized Structured Input.
4. Review the result.
5. Refine the input and rerun if necessary.
