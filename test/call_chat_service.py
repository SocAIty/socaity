"""Chat + agentic smoke via generated socaity SDK stub (stub style).

From the ``socaity`` package dir:

  export SOCAITY_API_KEY=sk_...
  python test/call_chat_service.py
  python test/call_chat_service.py --only basic
  python test/call_chat_service.py --only stream
  python test/call_chat_service.py --only persist
  python test/call_chat_service.py --only tools
  python test/call_chat_service.py --skip tools
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx


TEST_BACKEND = (
    "https://testsocaitybackend6cabe2ac-test-socaity-backend.functions.fnc.fr-par.scw.cloud"
)
TEST_INFER = "https://test.api.socaity.ai"
PERSIST_TIMEOUT_S = float(os.getenv("AGENTIC_PERSIST_TIMEOUT_S", "180"))
CHAT_TIMEOUT_S = float(os.getenv("CHAT_TIMEOUT_S", "300"))

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


def _bootstrap_env() -> None:
    os.environ.setdefault("SOCAITY_BACKEND_URL", TEST_BACKEND)
    os.environ.setdefault("INFERENCE_BACKEND_URL", TEST_INFER)
    os.environ.setdefault(
        "SOCAITY_INFER_BACKEND_URL",
        os.environ["INFERENCE_BACKEND_URL"].rstrip("/") + "/v1/",
    )
    here = Path(__file__).resolve()
    for candidate in (
        here.parent / ".env",
        here.parent.parent / ".env",
        here.parents[2] / "socaity" / ".env" if len(here.parents) > 2 else None,
    ):
        if candidate is None or not candidate.is_file():
            continue
        for line in candidate.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip().strip('"'))
        break


_bootstrap_env()

from socaity.sdk.community._6b398a33_0e5e_440b_89dc_5dfde43654a4 import (  # noqa: E402
    qwen39_1,
)
import socaity  # noqa: E402

BACKEND = os.environ["SOCAITY_BACKEND_URL"].rstrip("/") + "/"


def _log(step: str, msg: str) -> None:
    print(f"[{step}] {msg}", flush=True)


def _api_key() -> str:
    key = os.getenv("SOCAITY_API_KEY")
    if not key:
        raise SystemExit("No API key. Set SOCAITY_API_KEY or run: socaity login")
    return key


def _client():
    return qwen39_1(api_key=_api_key())


def _auth_headers() -> Dict[str, str]:
    return {"Authorization": f"Bearer {_api_key()}"}


def _platform(
    method: str,
    path: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    expect: Tuple[int, ...] = (200, 202),
) -> Any:
    with httpx.Client(timeout=60) as http:
        response = http.request(
            method,
            BACKEND + path.lstrip("/"),
            params={k: v for k, v in (params or {}).items() if v is not None},
            headers=_auth_headers(),
        )
    if response.status_code not in expect:
        raise AssertionError(
            f"{method} {path} -> {response.status_code}: {response.text[:500]}"
        )
    if not response.content:
        return None
    return response.json()


def _platform_job_id(handle) -> str:
    resp = getattr(handle, "response", None)
    for candidate in (
        getattr(resp, "job_id", None),
        getattr(resp, "id", None),
        getattr(handle, "job_id", None),
    ):
        if candidate:
            return str(candidate)
    raise AssertionError(f"could not resolve platform job id from handle={handle!r}")


def _unwrap_completion(payload: Any) -> Dict[str, Any]:
    """Normalize job envelopes and raw chat.completion dicts.

    Gate/SDK ``get_result()`` often returns::

        {"job_id": ..., "status": "finished", "result": {chat.completion...}, ...}

    RunPod ``return_aggregate_stream`` can also wrap a single JobResult as
    ``[{...}]``. Always prefer the nested chat completion when present.
    """
    if isinstance(payload, list) and len(payload) == 1:
        payload = payload[0]
    if not isinstance(payload, dict):
        return {}
    nested = payload.get("result")
    if isinstance(nested, list) and len(nested) == 1:
        nested = nested[0]
    if isinstance(nested, dict) and (
        "choices" in nested or nested.get("object") == "chat.completion"
    ):
        return nested
    if "choices" in payload or payload.get("object") == "chat.completion":
        return payload
    return payload


def _assistant_text(completion: Dict[str, Any]) -> str:
    completion = _unwrap_completion(completion)
    choice = (completion.get("choices") or [{}])[0]
    message = choice.get("message") or {}
    content = message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                parts.append(part.get("text") or "")
            elif isinstance(part, str):
                parts.append(part)
        return "".join(parts)
    return ""


def _message_for_request(message: Dict[str, Any]) -> Dict[str, Any]:
    """Copy an assistant message so tool_call arguments are JSON strings.

    Some services return ``function.arguments`` as a parsed object; the request
    schema requires a string (OpenAI wire format).
    """
    out = dict(message)
    tool_calls = out.get("tool_calls")
    if not isinstance(tool_calls, list):
        return out
    normalized = []
    for call in tool_calls:
        if not isinstance(call, dict):
            normalized.append(call)
            continue
        call = dict(call)
        fn = call.get("function")
        if isinstance(fn, dict):
            fn = dict(fn)
            args = fn.get("arguments")
            if args is not None and not isinstance(args, str):
                fn["arguments"] = json.dumps(args)
            call["function"] = fn
        normalized.append(call)
    out["tool_calls"] = normalized
    return out


def _wait_conversation(conversation_id: str, *, min_items: int = 1) -> Dict[str, Any]:
    deadline = time.time() + PERSIST_TIMEOUT_S
    last: Any = None
    while time.time() < deadline:
        try:
            last = _platform(
                "GET",
                f"v1/conversations/{conversation_id}",
                params={"expand": ["items"]},
            )
        except AssertionError as exc:
            if "404" not in str(exc):
                raise
            time.sleep(2)
            continue
        items = (last or {}).get("items") if isinstance(last, dict) else None
        if isinstance(items, list) and len(items) >= min_items:
            return last
        time.sleep(2)
    raise AssertionError(
        f"conversation {conversation_id} did not persist >= {min_items} items "
        f"within {PERSIST_TIMEOUT_S}s (last={last!r})"
    )


# ---------------------------------------------------------------------------
# Steps (all use stub client.chat(request=...))
# ---------------------------------------------------------------------------


def step_basic(client) -> None:
    _log("basic", "non-streaming completion")
    job = client.chat(
        request={
            "messages": [
                {"role": "user", "content": "Reply with exactly one short sentence."},
            ],
            "max_tokens": 128,
            "temperature": 0.2,
        }
    )
    try:
        completion = job.get_result(timeout_s=CHAT_TIMEOUT_S)
    except Exception as exc:
        if "cancelled" in type(exc).__name__.lower() or "cancelled" in str(exc).lower():
            job_id = _platform_job_id(job)
            gate = None
            try:
                infer = os.environ.get("INFERENCE_BACKEND_URL", TEST_INFER).rstrip("/")
                with httpx.Client(timeout=30) as http:
                    gate = http.get(
                        f"{infer}/status/{job_id}",
                        headers=_auth_headers(),
                    ).json()
            except Exception:
                gate = None
            raise AssertionError(
                f"job cancelled while waiting | platform_job={job_id!r} "
                f"gate_status={gate!r}. Message 'Job cancelled by user request' "
                f"means POST /cancel was sent (UI, another client, or Ctrl+C path)."
            ) from exc
        raise
    if completion is None and not job.is_terminal:
        raise TimeoutError(
            f"chat job still running after {CHAT_TIMEOUT_S:.0f}s "
            f"(platform_job={_platform_job_id(job)!r}; often RunPod IN_QUEUE / cold start). "
            f"Raise CHAT_TIMEOUT_S or check the endpoint workers."
        )
    text = _assistant_text(completion)
    assert text.strip(), f"empty assistant content: {completion!r}"
    _log("basic", f"job={_platform_job_id(job)} text={text[:120]!r}")


def step_stream(client) -> None:
    _log("stream", "streaming completion")
    job = client.chat(
        request={
            "messages": [{"role": "user", "content": "Say hi in five words."}],
            "stream": True,
            "max_tokens": 64,
            "temperature": 0.2,
        }
    )
    pieces: List[str] = []
    try:
        session = job.stream(timeout_s=CHAT_TIMEOUT_S)
    except ValueError as exc:
        raise AssertionError(
            f"stream unavailable for job={_platform_job_id(job)!r}: {exc}. "
            "Workers must forward RunPod /stream polls into the gate Redis stream."
        ) from exc
    try:
        for chunk in session.iter_chunks():
            if not isinstance(chunk, dict):
                continue
            delta = ((chunk.get("choices") or [{}])[0].get("delta") or {})
            if delta.get("content"):
                pieces.append(delta["content"])
    finally:
        session.close()
    streamed = "".join(pieces)
    assert streamed.strip(), "stream produced no content deltas"
    _log("stream", f"job={_platform_job_id(job)} streamed={streamed[:120]!r}")


def step_persist(client) -> None:
    conversation_id = str(uuid.uuid4())
    landmark = f"lighthouse-{uuid.uuid4().hex[:8]}"
    _log("persist", f"store=true conversation_id={conversation_id}")

    job1 = client.chat(
        request={
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Remember the secret codeword '{landmark}'. "
                        "Confirm you received it in one short sentence."
                    ),
                }
            ],
            "store": True,
            "metadata": {"conversation_id": conversation_id},
            "max_tokens": 128,
            "temperature": 0.2,
        }
    )
    first = job1.get_result(timeout_s=CHAT_TIMEOUT_S)
    first_text = _assistant_text(first)
    assert first_text.strip(), first
    job1_id = _platform_job_id(job1)
    _log("persist", f"first job={job1_id} text={first_text[:100]!r}")

    conversation = _wait_conversation(conversation_id, min_items=2)
    _log(
        "persist",
        f"persisted n_messages={conversation.get('n_messages')} "
        f"items={len(conversation.get('items') or [])}",
    )

    linked = socaity.get_job(job1_id, expand=["chat_item", "data"])
    chat_item = getattr(linked, "chat_item", None) if linked is not None else None
    _log(
        "persist",
        f"job expand chat_item id={getattr(chat_item, 'id', None)} "
        f"role={getattr(chat_item, 'role', None)}",
    )

    job2 = client.chat(
        request={
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Remember the secret codeword '{landmark}'. "
                        "Confirm you received it in one short sentence."
                    ),
                },
                {"role": "assistant", "content": first_text},
                {
                    "role": "user",
                    "content": "What was the secret codeword? Reply with only the codeword.",
                },
            ],
            "store": True,
            "metadata": {"conversation_id": conversation_id},
            "max_tokens": 64,
            "temperature": 0,
        }
    )
    second = job2.get_result(timeout_s=CHAT_TIMEOUT_S)
    second_text = _assistant_text(second)
    _log("persist", f"continue job={_platform_job_id(job2)} reply={second_text[:80]!r}")
    _wait_conversation(conversation_id, min_items=4)

    listed = _platform("GET", "v1/conversations", params={"limit": 5})
    _log("persist", f"conversations list ok type={type(listed).__name__}")


def step_tools(client) -> None:
    conversation_id = str(uuid.uuid4())
    _log("tools", "client-side tool round-trip (best-effort)")
    job = client.chat(
        request={
            "messages": [
                {
                    "role": "user",
                    "content": "What is the weather in Boston? Use the get_weather tool.",
                }
            ],
            "tools": [WEATHER_TOOL],
            "tool_choice": "auto",
            "store": True,
            "metadata": {"conversation_id": conversation_id},
            "max_tokens": 256,
            "temperature": 0,
        }
    )
    completion = _unwrap_completion(job.get_result(timeout_s=CHAT_TIMEOUT_S))
    tool_choice = (completion.get("choices") or [{}])[0]
    tool_message = tool_choice.get("message") or {}
    tool_calls = tool_message.get("tool_calls") or []
    _log("tools", f"job={_platform_job_id(job)} tool_calls={bool(tool_calls)}")

    if not tool_calls:
        _log("tools", "model did not emit tool_calls; request still accepted")
        return

    call = tool_calls[0]
    call_id = call.get("id") or "call_weather"
    follow = client.chat(
        request={
            "messages": [
                {
                    "role": "user",
                    "content": "What is the weather in Boston? Use the get_weather tool.",
                },
                _message_for_request(tool_message),
                {
                    "role": "tool",
                    "tool_call_id": call_id,
                    "content": "sunny, 22C",
                },
            ],
            "tools": [WEATHER_TOOL],
            "store": True,
            "metadata": {"conversation_id": conversation_id},
            "max_tokens": 128,
            "temperature": 0,
        }
    )
    follow_completion = follow.get_result(timeout_s=CHAT_TIMEOUT_S)
    _log(
        "tools",
        f"follow-up job={_platform_job_id(follow)} "
        f"text={_assistant_text(follow_completion)[:120]!r}",
    )


STEPS = {
    "basic": step_basic,
    "stream": step_stream,
    "persist": step_persist,
    "tools": step_tools,
}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Stub-style chat + agentic smoke")
    parser.add_argument(
        "--only",
        choices=list(STEPS),
        action="append",
        help="Run only these steps (repeatable). Default: all",
    )
    parser.add_argument(
        "--skip",
        choices=list(STEPS),
        action="append",
        default=[],
        help="Skip these steps (repeatable)",
    )
    args = parser.parse_args(argv)

    _log("env", f"backend={BACKEND}")
    _log("env", f"infer={os.environ.get('INFERENCE_BACKEND_URL')}")
    client = _client()

    selected = args.only or list(STEPS)
    for name in selected:
        if name in (args.skip or []):
            _log(name, "skipped")
            continue
        STEPS[name](client)

    _log("done", "ok")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        raise
