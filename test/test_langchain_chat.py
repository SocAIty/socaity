"""Chat integration tests: with and without LangChain, in all APIPod launch modes.

Runs :class:`socaity.integrations.ChatServiceAdapter` (raw, no LangChain) and
:class:`socaity.integrations.langchain.ChatSocaity` against the local APIPod
debug test service (a deterministic fake LLM covering plain replies, reasoning
tags and tool calls; see ``apipod/test/services/streaming_service.py``).

Each launch mode gets its own service instance, spawned by the module fixture:

- ``plain``             standard FastAPI (direct responses / SSE)
- ``serverless``        job queue emulation (job envelope + stream store)
- ``serverless-runpod`` RunPod routing emulation

Requirements (dev machine layout): sibling ``apipod`` repo with its own venv,
sibling ``socaity-schemas`` / ``socaity-cli`` / ``APIPodRegistry`` checkouts,
and ``langchain-core`` in this repo's venv for the LangChain tests.

    pytest test/test_langchain_chat.py -v
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import httpx
import pytest

PROJECTS_ROOT = Path(__file__).resolve().parents[2]
APIPOD_REPO = PROJECTS_ROOT / "apipod"
LAUNCHER = APIPOD_REPO / "test" / "debug_test_services.py"
CHAT_ENDPOINT = "/streaming/chat"
STARTUP_TIMEOUT_S = 120.0

# Mirrors apipod/test/services/streaming_service.py (stable fake-LLM contract).
CHAT_TEXT = "Hello, world!"
REASONING_TEXT = "The user greets; greet back."
TOOL_RESULT_ANSWER = "It is sunny in Boston."

WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"],
        },
    },
}

TIME_TOOL = {
    "type": "function",
    "function": {
        "name": "get_time",
        "description": "Current time for a city.",
        "parameters": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"],
        },
    },
}

MODES = [
    ("plain", None, 8021),
    ("serverless", "serverless", 8022),
    ("serverless-runpod", "serverless-runpod", 8023),
]


# ---------------------------------------------------------------------------
# Service lifecycle
# ---------------------------------------------------------------------------


def _apipod_python() -> Path:
    exe = APIPOD_REPO / "venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    return exe if exe.is_file() else Path(sys.executable)


def _sibling_pythonpath() -> str:
    """Sibling source checkouts take precedence over installed releases."""
    siblings = ("apipod", "socaity-schemas", "socaity-cli", "APIPodRegistry", "media-toolkit")
    paths = [str(PROJECTS_ROOT / name) for name in siblings if (PROJECTS_ROOT / name).is_dir()]
    if os.environ.get("PYTHONPATH"):
        paths.append(os.environ["PYTHONPATH"])
    return os.pathsep.join(paths)


def _wait_ready(url: str, process: subprocess.Popen, log_path: Path) -> None:
    deadline = time.time() + STARTUP_TIMEOUT_S
    while time.time() < deadline:
        if process.poll() is not None:
            output = log_path.read_text(encoding="utf-8", errors="replace") if log_path.is_file() else ""
            pytest.fail(f"debug service exited with {process.returncode}:\n{output[-3000:]}")
        try:
            if httpx.get(f"{url}/openapi.json", timeout=5).status_code == 200:
                return
        except httpx.HTTPError:
            pass
        time.sleep(1.0)
    pytest.fail(f"debug service at {url} not ready within {STARTUP_TIMEOUT_S}s")


@pytest.fixture(scope="module", params=MODES, ids=lambda mode: mode[0])
def chat_service(request):
    """One running debug service per launch mode; yields its base URL."""
    name, simulate, port = request.param
    if not LAUNCHER.is_file():
        pytest.skip(f"apipod repo not found at {APIPOD_REPO}")

    env = {**os.environ, "APIPOD_DEBUG_PORT": str(port), "PYTHONPATH": _sibling_pythonpath()}
    env.pop("APIPOD_SIMULATE", None)
    env.pop("APIPOD_NATIVE", None)
    if simulate:
        env["APIPOD_SIMULATE"] = simulate

    # Service output goes to a file, never a pipe: an unread pipe buffer fills
    # up with uvicorn access logs and blocks the server mid-run.
    log_path = Path(tempfile.gettempdir()) / f"apipod_debug_{name}.log"
    with log_path.open("wb") as log_file:
        process = subprocess.Popen(
            [str(_apipod_python()), str(LAUNCHER)],
            env=env,
            stdout=log_file,
            stderr=subprocess.STDOUT,
        )
        url = f"http://127.0.0.1:{port}"
        try:
            _wait_ready(url, process, log_path)
            yield url
        finally:
            process.kill()
            process.wait(timeout=10)


def _adapter(url: str):
    from socaity.integrations import ChatServiceAdapter

    return ChatServiceAdapter(url, endpoint_path=CHAT_ENDPOINT)


def _langchain_model(url: str):
    pytest.importorskip("langchain_core", reason="langchain-core not installed")
    from socaity.integrations.langchain import ChatSocaity

    return ChatSocaity(model=url, endpoint_path=CHAT_ENDPOINT)


# ---------------------------------------------------------------------------
# Without LangChain: raw ChatServiceAdapter
# ---------------------------------------------------------------------------


def test_adapter_complete(chat_service):
    adapter = _adapter(chat_service)
    response = adapter.complete({"messages": [{"role": "user", "content": "hi"}]})
    assert response["choices"][0]["message"]["content"] == CHAT_TEXT
    assert response["choices"][0]["finish_reason"] == "stop"

    status = adapter.job_status(adapter.last_job())
    assert status["is_terminal"] is True
    assert status["error"] is None


def test_adapter_stream(chat_service):
    adapter = _adapter(chat_service)
    text = ""
    for chunk in adapter.stream_chunks({"messages": [{"role": "user", "content": "hi"}]}):
        delta = chunk["choices"][0].get("delta") or {}
        text += delta.get("content") or ""
    assert text == CHAT_TEXT


def test_adapter_tool_call(chat_service):
    adapter = _adapter(chat_service)
    response = adapter.complete({
        "messages": [{"role": "user", "content": "What is the weather in Boston?"}],
        "tools": [WEATHER_TOOL],
    })
    choice = response["choices"][0]
    assert choice["finish_reason"] == "tool_calls"
    call = choice["message"]["tool_calls"][0]
    assert call["function"]["name"] == "get_weather"
    assert call["id"]


# ---------------------------------------------------------------------------
# With LangChain: ChatSocaity
# ---------------------------------------------------------------------------


def test_langchain_invoke(chat_service):
    from langchain_core.messages import HumanMessage

    model = _langchain_model(chat_service)
    result = model.invoke([HumanMessage("hi")])
    assert result.text == CHAT_TEXT
    assert result.response_metadata["finish_reason"] == "stop"


def test_langchain_stream(chat_service):
    from langchain_core.messages import HumanMessage

    model = _langchain_model(chat_service)
    chunks = list(model.stream([HumanMessage("hi")]))
    assert "".join(chunk.text for chunk in chunks) == CHAT_TEXT
    assert len(chunks) > 1, "expected token-level streaming, got one blob"


def test_langchain_reasoning(chat_service):
    from langchain_core.messages import HumanMessage

    model = _langchain_model(chat_service)
    result = model.invoke([HumanMessage("hi, think first")])
    reasoning = [block for block in result.content_blocks if block["type"] == "reasoning"]
    assert reasoning and reasoning[0]["reasoning"] == REASONING_TEXT
    assert result.text == CHAT_TEXT and "<think>" not in result.text


def test_langchain_tool_round_trip(chat_service):
    from langchain_core.messages import HumanMessage, ToolMessage

    def get_weather(location: str) -> str:
        """Current weather for a city."""
        return "sunny, 21 degrees"

    model = _langchain_model(chat_service)
    bound = model.bind_tools([get_weather])
    messages = [HumanMessage("What is the weather in Boston?")]

    ai = bound.invoke(messages)
    assert ai.tool_calls, f"no tool call, text was: {ai.text!r}"
    call = ai.tool_calls[0]
    assert call["name"] == "get_weather"

    messages += [ai, ToolMessage(get_weather(**call["args"]), tool_call_id=call["id"])]
    final = bound.invoke(messages)
    assert final.text == TOOL_RESULT_ANSWER


def test_langchain_tool_choice(chat_service):
    """User choice: a named tool_choice forces that function, 'none' disables tools."""
    from langchain_core.messages import HumanMessage

    model = _langchain_model(chat_service)

    forced = model.bind_tools([WEATHER_TOOL, TIME_TOOL], tool_choice="get_time")
    ai = forced.invoke([HumanMessage("What is the weather in Boston?")])
    assert ai.tool_calls and ai.tool_calls[0]["name"] == "get_time"

    disabled = model.bind_tools([WEATHER_TOOL], tool_choice="none")
    ai = disabled.invoke([HumanMessage("What is the weather in Boston?")])
    assert not ai.tool_calls
    assert ai.text == CHAT_TEXT


def test_langchain_streamed_tool_call(chat_service):
    from langchain_core.messages import HumanMessage

    model = My goal is, that users easily can use an MCP server I wrote with LangGraph and any Agenet framework. I have a CLI Auth in place with supabase. Now I want to(chat_service)
    bound = model.bind_tools([WEATHER_TOOL])
    chunks = list(bound.stream([HumanMessage("What is the weather in Boston?")]))

    merged = chunks[0]
    for chunk in chunks[1:]:
        merged = merged + chunk
    assert merged.tool_calls and merged.tool_calls[0]["name"] == "get_weather"
    assert merged.response_metadata.get("finish_reason") == "tool_calls"
