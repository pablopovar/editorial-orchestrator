from pathlib import Path

import pytest

from app.library import LibraryRepository
from app.model_client import ModelTurn
from app.orchestrator import EdOrOrchestrator
from app.schemas import LibraryObjectWrite, RunRequest, StructuredInput


class RecordingModelClient:
    def __init__(self):
        self.calls = []

    async def generate(self, *, model: str, user_prompt: str) -> ModelTurn:
        self.calls.append(
            {
                "model": model,
                "user_prompt": user_prompt,
            }
        )
        call_number = len(self.calls)
        return ModelTurn(
            trace_output=f"trace-{call_number}",
            returned_payload=f"output-{call_number}",
        )


def add_object(repository, bucket, object_id, name, content):
    repository.save(
        bucket,
        object_id,
        LibraryObjectWrite(name=name, content=content),
    )


@pytest.mark.asyncio
async def test_full_structured_input_is_sent_and_session_payload_is_chained(tmp_path: Path):
    repository = LibraryRepository(tmp_path / "library")
    add_object(repository, "roles", "role", "Writer", "ROLE DEFINITION")
    add_object(repository, "modes", "mode", "Analytic", "MODE DEFINITION")
    add_object(repository, "steps", "one", "First", "FIRST EXECUTION LOGIC")
    add_object(repository, "steps", "two", "Second", "SECOND EXECUTION LOGIC")

    client = RecordingModelClient()
    orchestrator = EdOrOrchestrator(
        library=repository,
        model_client=client,
        runs_dir=tmp_path / "runs",
        default_model="test-model",
    )

    result = await orchestrator.execute(
        RunRequest(
            role_id="role",
            mode_id="mode",
            step_ids=["one", "two"],
            loops=2,
            structured_input=StructuredInput(
                contextual_data="CONTEXT",
                instructions_definition="INSTRUCTIONS",
                goals_success_definition="SUCCESS",
                payload="ORIGINAL",
            ),
        )
    )

    assert result.status == "completed"
    assert len(client.calls) == 4

    for call in client.calls:
        prompt = call["user_prompt"]
        assert "## What You Should Know\n\nCONTEXT" in prompt
        assert "## Instructions\n\nINSTRUCTIONS" in prompt
        assert (
            "## Desired Outcome and What Success Looks Like\n\nSUCCESS"
            in prompt
        )
        assert "## Your Role Writer\n\nROLE DEFINITION" in prompt
        assert "## Your Approach Analytic\n\nMODE DEFINITION" in prompt
        assert "<structured_input>" not in prompt
        assert "<session_payload>" not in prompt

    assert "## Material\n\nORIGINAL" in client.calls[0]["user_prompt"]
    assert "## Material\n\noutput-1" in client.calls[1]["user_prompt"]
    assert "## Material\n\noutput-2" in client.calls[2]["user_prompt"]
    assert "## Material\n\noutput-3" in client.calls[3]["user_prompt"]

    assert "FIRST EXECUTION LOGIC" in client.calls[0]["user_prompt"]
    assert "SECOND EXECUTION LOGIC" not in client.calls[0]["user_prompt"]
    assert "SECOND EXECUTION LOGIC" in client.calls[1]["user_prompt"]
    assert "FIRST EXECUTION LOGIC" not in client.calls[1]["user_prompt"]

    assert result.original_payload == "ORIGINAL"
    assert result.final_session_payload == "output-4"
    assert [step.trace_output for step in result.steps] == [
        "trace-1",
        "trace-2",
        "trace-3",
        "trace-4",
    ]
    assert all(step.payload_returned for step in result.steps)
    assert [step.loop_number for step in result.steps] == [1, 1, 2, 2]
    assert [step.step_index for step in result.steps] == [1, 2, 1, 2]
