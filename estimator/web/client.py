from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass
class BackendConfig:
    base_url: str = "http://localhost:8000"
    timeout: int = 120


class BackendClientError(RuntimeError):
    """Raised when the backend cannot be reached or returns an error."""


def build_payload(
    transcription: str,
    preprocessing: str,
    example_format: str,
    num_examples: int,
    use_examples: bool,
    model: str | None,
    max_tokens: int,
    thinking_budget: int | None,
    evaluate: bool,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "transcription": transcription,
        "preprocessing": preprocessing,
        "example_format": example_format,
        "num_examples": num_examples,
        "use_examples": use_examples,
        "max_tokens": max_tokens,
        "evaluate": evaluate,
    }
    if model:
        payload["model"] = model
    if thinking_budget is not None:
        payload["thinking_budget"] = thinking_budget
    return payload


def estimate_software_project(config: BackendConfig, payload: dict[str, Any]) -> dict[str, Any]:
    url = f"{config.base_url.rstrip('/')}/api/v1/estimate"
    body = json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=config.timeout) as response:
            raw = response.read().decode("utf-8")
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise BackendClientError(
            f"Backend returned HTTP {exc.code}: {detail or exc.reason}"
        ) from exc
    except URLError as exc:
        raise BackendClientError(f"Could not reach backend at {url}: {exc.reason}") from exc

    return json.loads(raw)
