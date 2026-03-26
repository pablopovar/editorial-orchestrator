# SIS Editorial Orchestrator

SIS Editorial Orchestrator is a modular editorial runtime for AI-assisted writing, rewriting, compression, auditing, title generation, and ex-novo content development.

It is designed for people who want something more controlled than a one-off prompt and more flexible than a single hardcoded workflow.

Instead of baking one editorial method into the system, the Orchestrator separates the work into three parts:

- **App** — the execution engine
- **Library** — selectable Roles, Modes, and Steps
- **Structured Input** — the source material and run configuration

That separation is the point.

The **core stays fixed**.  
The **method changes by selecting a different stack**.

---

## What the Editorial Orchestrator is

The Orchestrator is a loop-based editorial system.

You give it:

- a **source payload**
- a **session**
- a selected **Role**
- a selected **Mode**
- an ordered list of **Steps**

It then runs the selected stack against the payload using the same execution model every time.

This makes it useful for very different editorial jobs without rewriting the engine itself.

Examples:

- improve an article draft
- generate copy from unstable material
- compress a long draft without losing the spine
- audit a compressed result for omissions and distortion
- derive a title from an article
- run multiple editorial passes using the same source input

---

## Core idea

The system uses two payload states:

- `payload` = the source input
- `session_payload` = the mutable working state

That distinction matters.

Some editorial tasks transform the source directly. Others derive a working artifact from the source and iterate there.

Because the Orchestrator preserves this separation, the same engine can support rewrite workflows, audit workflows, and derivative workflows like title generation.

Compressed:

**The system is fixed. The method is selected.**

---

## How the loop works

A run is a loop over selected Steps.

1. Load the app.
2. Load Structured Input.
3. Resolve the selected Role, Mode, and Steps from the Library.
4. Initialize `session_payload` from `payload`.
5. Run the selected Steps in Session order.
6. If a Step returns payload, replace `session_payload`.
7. Repeat for the configured number of loops.
8. Print according to `output_settings`.

This means the Orchestrator is not tied to one editorial ideology. It can run a corrective stack, a generative stack, a compression stack, or a title-generation stack using the same core logic.

---

## Example: what a Step is

A Step is a named operation in the Library.

Example:

`Compress: Reduces the payload by removing filler, redundancy, and non-essential surface material while preserving the conceptual spine.`

That definition is intentionally simple.

The app handles execution. The Session handles selection and order. The Library only needs to define what the Step is.

That makes the system easy to extend.

---

## Why this exists

Most AI writing workflows fall into one of two weak patterns:

- a generic prompt that tries to do everything at once
- a rigid workflow that is difficult to adapt

The Orchestrator takes a different approach.

It gives you:

- a reusable editorial engine
- a lightweight library of editorial operations
- structured input that makes runs inspectable and repeatable
- the ability to change method without changing system logic

This makes it useful for:

- prompt engineering
- editorial systems design
- AI writing workflows
- structured rewriting
- content strategy
- article development
- title generation
- compression and audit work
- experimental stack design

---

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

---

## Why the Library matters

The Library is deliberately simple and flexible.

One of the system’s strengths is how easy it is to add new Steps without changing the app.

You do not need to rewrite the engine to introduce a new editorial operation.

You only need to define a new library object and then select it in a Session.

That keeps the system lean:

- the **app** remains stable
- the **library** grows as needed
- the **session** selects only what the task requires

This is one of the main reasons the Orchestrator is useful as a real working system rather than a single prompt.

---

## Structured Input

The app does not run from unstructured instruction alone.

It expects Structured Input.

Structured Input contains:

- **Definitions** — context, instructions, success conditions, and supporting constraints
- **Payload** — the source input
- **Session** — the selected stack and execution settings

This gives each run a visible shape and makes editorial work easier to inspect, rerun, and refine.

See `INSTRUCTIONS.md` for the full template and block-by-block guidance.

---

## Repository contents

- `README.md` — what the Orchestrator is, how it works, and why it exists
- `INSTRUCTIONS.md` — usage guidance, structured-input template, and block breakdown
- `APP.md` — the loadable app / engine
- `sample-definitions-block.xml` — a sample definitions block for article improvement

---

## Quick start

1. Load `APP.md` into the assistant.
2. The assistant acknowledges load completion and transitions to **waiting for Structured Input**.
3. Provide your customized Structured Input using the template and examples in `INSTRUCTIONS.md` and `sample-definitions-block.xml`.
4. The assistant runs the selected stack against your payload.
5. Review the final output.
6. Adjust your Structured Input and run again if needed.

---

## Who this is for

This repository is most useful for people working on:

- AI-assisted editorial systems
- structured content improvement
- repeatable prompt workflows
- high-signal rewriting
- modular prompt architecture
- article shaping and audit workflows

If you want a reusable editorial runtime rather than a single-purpose prompt, this is what this project is for.
