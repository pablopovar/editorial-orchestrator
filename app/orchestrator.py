from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from pathlib import Path

from .library import LibraryRepository
from .model_client import ModelClient
from .schemas import RunRequest, RunResult, StepResult


# EDOR_MARKDOWN_TURNS_V1
USER_TEMPLATE = """## What You Should Know

{contextual_data}

## Instructions

{instructions_definition}

## Desired Outcome and What Success Looks Like

{goals_success_definition}

## Material

{session_payload}

## Your Role {role_name}

{role_definition}

## Your Approach {mode_name}

{mode_definition}

## Your Task

{step_execution_logic}
"""


class EdOrOrchestrator:
    def __init__(
        self,
        *,
        library: LibraryRepository,
        model_client: ModelClient,
        runs_dir: Path,
        default_model: str,
    ) -> None:
        self.library = library
        self.model_client = model_client
        self.runs_dir = runs_dir
        self.default_model = default_model
        self.runs_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _now() -> str:
        return datetime.now(UTC).isoformat()

    def _run_path(self, run_id: str) -> Path:
        if not run_id.isalnum():
            raise ValueError("Invalid run ID")
        return self.runs_dir / f"{run_id}.json"

    def initialize(
        self,
        request: RunRequest,
        *,
        run_id: str | None = None,
    ) -> tuple[RunResult, bool]:
        resolved_run_id = (
            run_id
            or request.run_id
            or uuid.uuid4().hex
        )
        path = self._run_path(resolved_run_id)

        if path.exists():
            record = self.read_run(resolved_run_id)
            return (
                RunResult.model_validate(record["result"]),
                False,
            )

        now = self._now()
        model = request.model or self.default_model
        original_payload = request.structured_input.payload

        result = RunResult(
            run_id=resolved_run_id,
            status="queued",
            created_at=now,
            updated_at=now,
            role_id=request.role_id,
            mode_id=request.mode_id,
            pre_step_ids=request.pre_step_ids,
            step_ids=request.step_ids,
            post_step_ids=request.post_step_ids,
            model=model,
            loops=request.loops,
            original_payload=original_payload,
            final_session_payload=original_payload,
            steps=[],
        )
        self._persist(result, request)
        return result, True

    async def execute(
        self,
        request: RunRequest,
        *,
        run_id: str | None = None,
    ) -> RunResult:
        result, created = self.initialize(
            request,
            run_id=run_id,
        )

        if not created and result.status != "queued":
            return result

        result.status = "running"
        result.updated_at = self._now()
        self._persist(result, request)

        model = result.model
        original_payload = result.original_payload
        session_payload = result.final_session_payload
        step_results = result.steps

        try:
            role = self.library.get(
                "roles",
                request.role_id,
            )
            mode = self.library.get(
                "modes",
                request.mode_id,
            )

            pre_steps = [
                self.library.get("steps", step_id)
                for step_id in request.pre_step_ids
            ]
            steps = [
                self.library.get("steps", step_id)
                for step_id in request.step_ids
            ]
            post_steps = [
                self.library.get("steps", step_id)
                for step_id in request.post_step_ids
            ]

            if not role.enabled:
                raise ValueError(
                    f"Role is disabled: {role.object_id}"
                )
            if not mode.enabled:
                raise ValueError(
                    f"Mode is disabled: {mode.object_id}"
                )

            all_steps = [
                *pre_steps,
                *steps,
                *post_steps,
            ]
            disabled_steps = [
                step.object_id
                for step in all_steps
                if not step.enabled
            ]
            if disabled_steps:
                disabled_names = ", ".join(
                    dict.fromkeys(disabled_steps)
                )
                raise ValueError(
                    "Disabled Steps selected: "
                    f"{disabled_names}"
                )

            call_index = len(step_results)

            async def execute_sequence(
                *,
                phase: str,
                sequence: list,
                loop_number: int,
            ) -> None:
                nonlocal call_index
                nonlocal session_payload

                for step_index, step in enumerate(
                    sequence,
                    start=1,
                ):
                    call_index += 1

                    result.current_phase = phase
                    result.current_loop = loop_number
                    result.current_step_index = step_index
                    result.current_step_id = step.object_id
                    result.current_step_name = step.name
                    result.current_call_index = call_index
                    result.updated_at = self._now()
                    self._persist(result, request)

                    user_prompt = USER_TEMPLATE.format(
                        contextual_data=(
                            request.structured_input.contextual_data
                        ),
                        instructions_definition=(
                            request.structured_input.instructions_definition
                        ),
                        goals_success_definition=(
                            request.structured_input.goals_success_definition
                        ),
                        role_name=role.name,
                        mode_name=mode.name,
                        role_definition=role.content,
                        mode_definition=mode.content,
                        session_payload=session_payload,
                        step_execution_logic=step.content,
                    )

                    model_turn = (
                        await self.model_client.generate(
                            model=model,
                            user_prompt=user_prompt,
                        )
                    )
                    output_session_payload = (
                        model_turn.returned_payload
                        if model_turn.returned_payload is not None
                        else session_payload
                    )

                    step_results.append(
                        StepResult(
                            call_index=call_index,
                            phase=phase,
                            loop_number=loop_number,
                            step_index=step_index,
                            step_id=step.object_id,
                            step_name=step.name,
                            input_session_payload=(
                                session_payload
                            ),
                            output_session_payload=(
                                output_session_payload
                            ),
                            trace_output=(
                                model_turn.trace_output
                            ),
                            payload_returned=(
                                model_turn.returned_payload
                                is not None
                            ),
                            system_prompt="",
                            user_prompt=user_prompt,
                        )
                    )
                    session_payload = output_session_payload
                    result.final_session_payload = session_payload
                    result.steps = step_results
                    result.updated_at = self._now()
                    self._persist(result, request)

            await execute_sequence(
                phase="pre",
                sequence=pre_steps,
                loop_number=0,
            )

            for loop_number in range(
                1,
                request.loops + 1,
            ):
                await execute_sequence(
                    phase="loop",
                    sequence=steps,
                    loop_number=loop_number,
                )

            await execute_sequence(
                phase="post",
                sequence=post_steps,
                loop_number=request.loops,
            )

            result.status = "completed"
            result.current_phase = None
            result.current_loop = None
            result.current_step_index = None
            result.current_step_id = None
            result.current_step_name = None
            result.current_call_index = None
            result.updated_at = self._now()
        except Exception as exc:
            result.status = "failed"
            result.error_type = type(exc).__name__
            result.error = (
                str(exc)
                or repr(exc)
            )
            result.final_session_payload = session_payload
            result.steps = step_results
            result.updated_at = self._now()

        self._persist(result, request)
        return result

    def _persist(self, result: RunResult, request: RunRequest) -> None:
        record = {
            "created_at": result.created_at,
            "updated_at": result.updated_at,
            "request": request.model_dump(),
            "result": result.model_dump(),
        }
        path = self._run_path(result.run_id)
        temporary = path.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(record, indent=2), encoding="utf-8")
        temporary.replace(path)

    def read_run(self, run_id: str) -> dict:
        path = self._run_path(run_id)
        if not path.exists():
            raise FileNotFoundError(run_id)
        return json.loads(path.read_text(encoding="utf-8"))

    def list_runs(self, limit: int = 20) -> list[dict]:
        paths = sorted(
            self.runs_dir.glob("*.json"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )[:limit]
        summaries = []

        for path in paths:
            try:
                record = json.loads(
                    path.read_text(encoding="utf-8")
                )
                result = record["result"]
            except (OSError, ValueError, KeyError):
                continue

            summaries.append({
                "run_id": result.get("run_id"),
                "status": result.get("status"),
                "created_at": record.get("created_at"),
                "updated_at": record.get("updated_at"),
                "model": result.get("model"),
                "role_id": result.get("role_id"),
                "mode_id": result.get("mode_id"),
                "completed_calls": len(
                    result.get("steps") or []
                ),
                "current_phase": result.get(
                    "current_phase"
                ),
                "current_loop": result.get(
                    "current_loop"
                ),
                "current_step_name": result.get(
                    "current_step_name"
                ),
            })

        return summaries

    def recover_incomplete_runs(self) -> int:
        recovered = 0

        for path in self.runs_dir.glob("*.json"):
            try:
                record = json.loads(
                    path.read_text(encoding="utf-8")
                )
                result = record["result"]
            except (OSError, ValueError, KeyError):
                continue

            if result.get("status") not in {
                "queued",
                "running",
            }:
                continue

            now = self._now()
            result["status"] = "interrupted"
            result["updated_at"] = now
            result["error_type"] = "ServerRestart"
            result["error"] = (
                "The EdOr process restarted before this run "
                "reached a terminal state."
            )
            record["updated_at"] = now

            temporary = path.with_suffix(".json.tmp")
            temporary.write_text(
                json.dumps(record, indent=2),
                encoding="utf-8",
            )
            temporary.replace(path)
            recovered += 1

        return recovered
