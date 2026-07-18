# EdOr Web beta

EdOr Web is a standalone Python orchestrator for EdOr sequences.

Current beta behavior:

- Roles, Modes, and Steps are file-backed library objects.
- Adding a Markdown file to a bucket adds an object.
- Objects can also be created and edited from the UI.
- Structured Input is built from separate fields.
- Every Step is a separate model call.
- The complete Structured Input is presented to every model call.
- Python initializes `session_payload` from the submitted `payload`.
- Only `session_payload` mutates during execution.
- Each Step receives the selected Role, selected Mode, its own execution logic, and the current `session_payload`.
- Python passes the returned `session_payload` to the next Step.
- The ordered Step sequence repeats for the requested number of loops.

The beta does not implement UserStep, TurnTurnover, pause/resume, StepContext, dependency validation, control-step machinery, or the broader protocol runtime.

## Run

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
cp .env.example .env
set -a; source .env; set +a
.venv/bin/uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.

The model endpoint must expose an OpenAI-compatible `POST /chat/completions` endpoint.

## Library buckets

```text
library/
├── roles/
├── modes/
└── steps/
```

A library object is a Markdown file with front matter:

```markdown
---
name: Critical Editor
description: Evaluates material without social padding.
enabled: true
---

Object definition or Step execution logic.
```

The filename is the beta object's stable filesystem ID.

Run records are written as JSON under `data/runs/`.
