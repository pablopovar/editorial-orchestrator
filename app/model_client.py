from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Protocol

import httpx


# EDOR_MARKDOWN_TURNS_V1
@dataclass(frozen=True)
class ModelTurn:
    trace_output: str
    returned_payload: str | None


class ModelClient(Protocol):
    async def generate(
        self,
        *,
        model: str,
        user_prompt: str,
    ) -> ModelTurn:
        ...


def extract_endpoint_error(
    response: httpx.Response,
) -> str:
    try:
        body: Any = response.json()
    except ValueError:
        body = response.text.strip()

    message: str

    if isinstance(body, dict):
        error = body.get("error")

        if isinstance(error, dict):
            message = str(
                error.get("message")
                or json.dumps(
                    error,
                    ensure_ascii=False,
                )
            )
        elif error:
            message = str(error)
        elif body.get("detail"):
            detail = body["detail"]

            if isinstance(detail, str):
                message = detail
            else:
                message = json.dumps(
                    detail,
                    ensure_ascii=False,
                )
        else:
            message = json.dumps(
                body,
                ensure_ascii=False,
            )
    elif isinstance(body, str) and body:
        message = body
    else:
        message = "No response body returned."

    if len(message) > 8000:
        message = (
            message[:8000]
            + "\n[response truncated]"
        )

    return message


class OpenAICompatibleClient:
    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        timeout_seconds: float,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds

    def _headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
        }

        if self.api_key:
            headers["Authorization"] = (
                f"Bearer {self.api_key}"
            )

        return headers

    async def list_models(self) -> list[str]:
        endpoint = f"{self.base_url}/models"

        try:
            async with httpx.AsyncClient(
                timeout=self.timeout_seconds,
            ) as client:
                response = await client.get(
                    endpoint,
                    headers=self._headers(),
                )
        except httpx.TimeoutException as exc:
            raise RuntimeError(
                "Model-list request timed out after "
                f"{self.timeout_seconds:g} seconds.\n"
                f"Endpoint: {endpoint}\n"
                f"Error type: {type(exc).__name__}"
            ) from exc
        except httpx.RequestError as exc:
            raise RuntimeError(
                "Could not reach model endpoint "
                f"{endpoint}.\n"
                f"Error type: {type(exc).__name__}\n"
                f"Error: {str(exc) or repr(exc)}"
            ) from exc

        if response.is_error:
            raise RuntimeError(
                "Model endpoint returned "
                f"HTTP {response.status_code} "
                "while listing models.\n"
                f"Endpoint: {endpoint}\n"
                "Response: "
                f"{extract_endpoint_error(response)}"
            )

        try:
            payload = response.json()
        except ValueError as exc:
            raise RuntimeError(
                "Model endpoint returned an "
                "invalid model list."
            ) from exc

        data = payload.get("data")

        if not isinstance(data, list):
            raise RuntimeError(
                "Model endpoint returned an "
                "unexpected model-list response."
            )

        models = []

        for item in data:
            if isinstance(item, dict):
                model_id = item.get("id")

                if (
                    isinstance(model_id, str)
                    and model_id
                ):
                    models.append(model_id)

        return sorted(
            set(models),
            key=str.casefold,
        )

    async def generate(
        self,
        *,
        model: str,
        user_prompt: str,
    ) -> ModelTurn:
        body = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "return_payload",
                        "description": (
                            "Return the complete material that should be "
                            "handed to the next task. Use this when the "
                            "current task produces replacement material. "
                            "Write any requested explanation in the normal "
                            "assistant response, then call this tool with "
                            "only the complete replacement material. If "
                            "older task instructions mention returning or "
                            "populating StepResult.session_payload, supply "
                            "that material through this tool."
                        ),
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "material": {
                                    "type": "string",
                                    "description": (
                                        "The complete material to hand to "
                                        "the next task."
                                    ),
                                },
                            },
                            "required": ["material"],
                            "additionalProperties": False,
                        },
                    },
                },
            ],
            "tool_choice": "auto",
            "stream": False,
        }

        endpoint = (
            f"{self.base_url}/chat/completions"
        )

        try:
            async with httpx.AsyncClient(
                timeout=self.timeout_seconds,
            ) as client:
                response = await client.post(
                    endpoint,
                    headers=self._headers(),
                    json=body,
                )
        except httpx.TimeoutException as exc:
            raise RuntimeError(
                "Model request timed out after "
                f"{self.timeout_seconds:g} seconds.\n"
                f"Model: {model}\n"
                f"Endpoint: {endpoint}\n"
                f"Error type: {type(exc).__name__}"
            ) from exc
        except httpx.RequestError as exc:
            raise RuntimeError(
                "Could not reach model endpoint "
                f"{endpoint}.\n"
                f"Model: {model}\n"
                f"Error type: {type(exc).__name__}\n"
                f"Error: {str(exc) or repr(exc)}"
            ) from exc

        if response.is_error:
            endpoint_error = (
                extract_endpoint_error(response)
            )

            raise RuntimeError(
                "Model endpoint returned "
                f"HTTP {response.status_code} "
                f"for model {model!r}.\n"
                f"Endpoint: {endpoint}\n"
                f"Response: {endpoint_error}"
            )

        try:
            payload = response.json()
        except ValueError as exc:
            response_preview = (
                response.text.strip()[:4000]
            )

            raise RuntimeError(
                "Model endpoint returned HTTP 200 "
                "but the response was not valid JSON.\n"
                f"Endpoint: {endpoint}\n"
                f"Response: {response_preview}"
            ) from exc

        try:
            message = payload["choices"][0]["message"]
        except (
            KeyError,
            IndexError,
            TypeError,
        ) as exc:
            raise RuntimeError(
                "Model endpoint returned an "
                "unexpected successful response.\n"
                f"Endpoint: {endpoint}\n"
                "Response: "
                + json.dumps(
                    payload,
                    ensure_ascii=False,
                )[:8000]
            ) from exc

        if not isinstance(message, dict):
            raise RuntimeError(
                "Model endpoint returned an unexpected "
                "message object."
            )

        content = message.get("content")
        trace_output = (
            content.strip()
            if isinstance(content, str)
            else ""
        )

        returned_payload: str | None = None
        tool_calls = message.get("tool_calls") or []

        if not isinstance(tool_calls, list):
            raise RuntimeError(
                "Model endpoint returned invalid tool_calls."
            )

        for tool_call in tool_calls:
            if not isinstance(tool_call, dict):
                continue

            function = tool_call.get("function")
            if not isinstance(function, dict):
                continue
            if function.get("name") != "return_payload":
                continue

            if returned_payload is not None:
                raise RuntimeError(
                    "Model called return_payload more than once."
                )

            arguments = function.get("arguments", {})
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError as exc:
                    raise RuntimeError(
                        "Model returned invalid JSON arguments "
                        "for return_payload."
                    ) from exc

            if not isinstance(arguments, dict):
                raise RuntimeError(
                    "Model returned invalid arguments "
                    "for return_payload."
                )

            material = arguments.get("material")
            if (
                not isinstance(material, str)
                or not material.strip()
            ):
                raise RuntimeError(
                    "Model called return_payload without "
                    "non-empty material."
                )
            returned_payload = material.strip()

        if not trace_output and returned_payload is None:
            raise RuntimeError(
                "Model endpoint returned neither visible trace "
                "nor replacement material."
            )

        return ModelTurn(
            trace_output=trace_output,
            returned_payload=returned_payload,
        )
