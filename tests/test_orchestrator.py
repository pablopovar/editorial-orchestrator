from pathlib import Path

import pytest

from app.library import LibraryRepository
from app.model_client import ModelTurn
from app.orchestrator import EdOrOrchestrator
from app.schemas import LibraryObjectWrite, RunRequest, StructuredInput


class RecordingModelClient:
    def __init__(self, responses=None):
        self.calls = []
        self.responses = list(responses or [])

    async def generate(self, *, model: str, messages: list[dict]) -> ModelTurn:
        self.calls.append({"model": model, "messages": messages})
        if self.responses:
            return self.responses.pop(0)
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


def build_orchestrator(tmp_path, client, step_count=2):
    repository = LibraryRepository(tmp_path / "library")
    add_object(repository, "roles", "role", "Writer", "ROLE DEFINITION")
    add_object(repository, "modes", "mode", "Analytic", "MODE DEFINITION")
    add_object(repository, "steps", "one", "First", "FIRST EXECUTION LOGIC")
    if step_count == 2:
        add_object(repository, "steps", "two", "Second", "SECOND EXECUTION LOGIC")
    return EdOrOrchestrator(
        library=repository,
        model_client=client,
        runs_dir=tmp_path / "runs",
        default_model="test-model",
    )


def request(step_count=2, loops=2):
    return RunRequest(
        role_id="role",
        mode_id="mode",
        step_ids=["one", "two"] if step_count == 2 else ["one"],
        loops=loops,
        structured_input=StructuredInput(
            contextual_data="CONTEXT",
            instructions_definition="INSTRUCTIONS",
            goals_success_definition="SUCCESS",
            payload="ORIGINAL",
        ),
    )


@pytest.mark.asyncio
async def test_sequence_and_loops_chain_only_returned_material(tmp_path: Path):
    client = RecordingModelClient()
    orchestrator = build_orchestrator(tmp_path, client)

    result = await orchestrator.execute(request())

    assert result.status == "completed"
    assert len(client.calls) == 4
    prompts = [call["messages"][1]["content"] for call in client.calls]

    for call, prompt in zip(client.calls, prompts):
        assert call["messages"][0]["role"] == "system"
        assert "<<<EDOR_MATERIAL>>>" in call["messages"][0]["content"]
        assert "## Context\n\nCONTEXT" in prompt
        assert "## Instructions\n\nINSTRUCTIONS" in prompt
        assert "## Desired Outcome and What Success Looks Like\n\nSUCCESS" in prompt
        assert "ROLE DEFINITION" in prompt
        assert "MODE DEFINITION" in prompt

    assert "## The Material\n\nORIGINAL" in prompts[0]
    assert "## The Material\n\noutput-1" in prompts[1]
    assert "## The Material\n\noutput-2" in prompts[2]
    assert "## The Material\n\noutput-3" in prompts[3]
    assert "FIRST EXECUTION LOGIC" in prompts[0]
    assert "SECOND EXECUTION LOGIC" not in prompts[0]
    assert "SECOND EXECUTION LOGIC" in prompts[1]
    assert "FIRST EXECUTION LOGIC" not in prompts[1]

    assert result.final_session_payload == "output-4"
    assert [step.trace_output for step in result.steps] == [
        "trace-1",
        "trace-2",
        "trace-3",
        "trace-4",
    ]
    assert [step.loop_number for step in result.steps] == [1, 1, 2, 2]
    assert [step.step_index for step in result.steps] == [1, 2, 1, 2]


@pytest.mark.asyncio
async def test_delimited_material_is_removed_from_trace_and_handed_off(tmp_path: Path):
    client = RecordingModelClient([
        ModelTurn(
            trace_output=(
                "Visible explanation.\n"
                "<<<EDOR_MATERIAL>>>\nREFORMULATED\n"
                "<<<END_EDOR_MATERIAL>>>"
            ),
            returned_payload=None,
        )
    ])
    orchestrator = build_orchestrator(tmp_path, client, step_count=1)

    result = await orchestrator.execute(request(step_count=1, loops=1))

    assert result.status == "completed"
    assert result.final_session_payload == "REFORMULATED"
    assert result.steps[0].trace_output == "Visible explanation."
    assert result.steps[0].payload_returned is True
    assert len(client.calls) == 1


@pytest.mark.asyncio
async def test_missing_handoff_gets_one_same_conversation_retry(tmp_path: Path):
    client = RecordingModelClient([
        ModelTurn(trace_output="Initial analysis.", returned_payload=None),
        ModelTurn(
            trace_output=(
                "<<<EDOR_MATERIAL>>>\nREPAIRED\n"
                "<<<END_EDOR_MATERIAL>>>"
            ),
            returned_payload=None,
        ),
    ])
    orchestrator = build_orchestrator(tmp_path, client, step_count=1)

    result = await orchestrator.execute(request(step_count=1, loops=1))

    assert result.status == "completed"
    assert result.final_session_payload == "REPAIRED"
    assert result.steps[0].trace_output == "Initial analysis."
    assert len(client.calls) == 2
    retry_messages = client.calls[1]["messages"]
    assert [message["role"] for message in retry_messages] == [
        "system",
        "user",
        "assistant",
        "user",
    ]
    assert retry_messages[2]["content"] == "Initial analysis."
    assert "Do not repeat your analysis" in retry_messages[3]["content"]


@pytest.mark.asyncio
async def test_missing_handoff_twice_fails_before_next_step(tmp_path: Path):
    client = RecordingModelClient([
        ModelTurn(trace_output="First response.", returned_payload=None),
        ModelTurn(trace_output="Second response.", returned_payload=None),
    ])
    orchestrator = build_orchestrator(tmp_path, client)

    result = await orchestrator.execute(request(loops=1))

    assert result.status == "failed"
    assert len(client.calls) == 2
    assert len(result.steps) == 1
    assert result.steps[0].step_id == "one"
    assert result.steps[0].payload_returned is False
    assert result.steps[0].trace_output == "First response.\n\nSecond response."
    assert result.final_session_payload == "ORIGINAL"
    assert "stopped before the next Step" in result.error
