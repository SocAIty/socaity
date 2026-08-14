"""E2E: agentic chat against a live platform (test or local).

Mimics a real client that:
  1. authenticates against the platform API
  2. discovers a chat-capable catalog service
  3. completes + streams without persistence
  4. starts a conversation with ``store=true`` (client-owned conversation_id)
  5. continues the thread, optionally branches, searches, patches, deletes
  6. links jobs back via ``expand=chat_item``

Requires a live backend with credentials, plus a chat-capable service:
``ChatCompletionRequest`` schema or path ``/chat`` (APIPod). The test catalog
is mostly Replicate ``/predictions`` models — those cannot exercise
``store=true`` conversation persistence. Deploy a chat service or pass
``--url`` / ``CHAT_SERVICE_URL``.

    export SOCAITY_API_KEY=sk_...   # or: socaity login --backend-url $SOCAITY_BACKEND_URL
    # optional overrides:
    #   CHAT_SERVICE=<catalog-name>
    #   CHAT_SERVICE_URL=http://127.0.0.1:8010
    #   SOCAITY_BACKEND_URL=...
    #   INFERENCE_BACKEND_URL=https://test.api.socaity.ai

    python test/test_e2e_agentic_chat.py
    python test/test_e2e_agentic_chat.py --diagnose
    python test/test_e2e_agentic_chat.py --url http://127.0.0.1:8010
    # or
    pytest test/test_e2e_agentic_chat.py -v -s
"""
from __future__ import annotations

import json
import os
import sys
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx
import pytest


# ---------------------------------------------------------------------------
# Env bootstrap (must run before socaity / cli clients are constructed)
# ---------------------------------------------------------------------------

TEST_BACKEND = (
    "https://testsocaitybackend6cabe2ac-test-socaity-backend.functions.fnc.fr-par.scw.cloud"
)
TEST_INFER = "https://test.api.socaity.ai"
TEST_FRONTEND = "https://wonderful-wave-0a392ca03.2.azurestaticapps.net"

CHAT_SCHEMA = "ChatCompletionRequest"
PERSIST_TIMEOUT_S = float(os.getenv("AGENTIC_PERSIST_TIMEOUT_S", "180"))
SEARCH_TIMEOUT_S = float(os.getenv("AGENTIC_SEARCH_TIMEOUT_S", "90"))
CHAT_TIMEOUT_S = float(os.getenv("AGENTIC_CHAT_TIMEOUT_S", "300"))


def _load_repo_env() -> None:
    env_file = Path(__file__).resolve().parents[1] / ".env"
    if not env_file.is_file():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip('"'))


_load_repo_env()
os.environ.setdefault("SOCAITY_BACKEND_URL", TEST_BACKEND)
os.environ.setdefault("SOCAITY_FRONTEND_URL", TEST_FRONTEND)
os.environ.setdefault("INFERENCE_BACKEND_URL", TEST_INFER)
os.environ.setdefault("SOCAITY_INFER_BACKEND_URL", TEST_INFER.rstrip("/") + "/v1/")

import socaity  # noqa: E402
import socaity.core.catalog as catalog_mod  # noqa: E402
from socaity.integrations import ChatServiceAdapter  # noqa: E402
from socaity_cli.credentials import get_api_key  # noqa: E402

catalog_mod._client = None

BACKEND = os.environ["SOCAITY_BACKEND_URL"].rstrip("/") + "/"
TOKEN = f"agentic-e2e-{uuid.uuid4().hex[:10]}"


# ---------------------------------------------------------------------------
# Preconditions
# ---------------------------------------------------------------------------


def _has_credentials() -> bool:
    if os.getenv("SOCAITY_API_KEY"):
        return True
    return (Path.home() / ".config" / "socaity" / "credentials.json").is_file()


def _backend_up() -> bool:
    try:
        return (
            httpx.get(BACKEND + "v1/catalog/services", params={"limit": 1}, timeout=15).status_code
            == 200
        )
    except httpx.HTTPError:
        return False


pytestmark = [
    pytest.mark.skipif(not _backend_up(), reason=f"backend not reachable at {BACKEND}"),
    pytest.mark.skipif(not _has_credentials(), reason="no SOCAITY_API_KEY / socaity login"),
]


# ---------------------------------------------------------------------------
# HTTP helpers for conversations (CLI has no chat client yet)
# ---------------------------------------------------------------------------


def _auth_headers() -> Dict[str, str]:
    key = get_api_key()
    if not key:
        raise RuntimeError("No API key. Set SOCAITY_API_KEY or run: socaity login")
    return {"Authorization": f"Bearer {key}"}


def _platform(
    method: str,
    path: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    json_body: Any = None,
    expect: Tuple[int, ...] = (200, 202),
) -> Any:
    flat: Dict[str, Any] = {}
    for key, value in (params or {}).items():
        if value is None:
            continue
        flat[key] = value
    with httpx.Client(timeout=60) as client:
        response = client.request(
            method,
            BACKEND + path.lstrip("/"),
            params=flat,
            json=json_body,
            headers=_auth_headers(),
        )
    if response.status_code not in expect:
        raise AssertionError(
            f"{method} {path} -> {response.status_code}: {response.text[:500]}"
        )
    if not response.content:
        return None
    return response.json()


def _entities(payload: Any) -> List[Any]:
    if payload is None:
        return []
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and "entities" in payload:
        return payload.get("entities") or []
    return []


def _log(step: str, msg: str) -> None:
    print(f"[{step}] {msg}", flush=True)


# ---------------------------------------------------------------------------
# Chat service discovery
# ---------------------------------------------------------------------------


def _attr(obj: Any, *names: str, default: Any = None) -> Any:
    if obj is None:
        return default
    if isinstance(obj, dict):
        for name in names:
            if name in obj and obj[name] is not None:
                return obj[name]
        return default
    for name in names:
        value = getattr(obj, name, None)
        if value is not None:
            return value
    return default


def _endpoint_is_chat(endpoint: Any) -> bool:
    """True only for APIPod OpenAI-chat endpoints.

    Replicate ``/predictions`` models sometimes expose a ``messages`` field, but
    they do not return ``chat.completion`` objects and will not trigger orch
    ``store=true`` persistence. Do not treat them as chat-capable.
    """
    path = _attr(endpoint, "path")
    if isinstance(path, str) and path.rstrip("/").endswith("/predictions"):
        return False

    schema = _attr(endpoint, "schema_name", "schema", "standard_schema")
    if schema == CHAT_SCHEMA:
        return True
    if schema and str(schema).endswith("ChatCompletionRequest"):
        return True
    if isinstance(path, str) and path.rstrip("/").endswith("/chat"):
        return True

    # Nested body parameter typed as ChatCompletionRequest (APIPod schema route).
    for param in _attr(endpoint, "parameters", default=[]) or []:
        if _attr(param, "name") != "request":
            continue
        schema_obj = _attr(param, "param_schema", "definition", default={}) or {}
        if not isinstance(schema_obj, dict):
            continue
        title = schema_obj.get("title") or schema_obj.get("x-socaity-schema")
        ref = schema_obj.get("$ref") or ""
        if title == CHAT_SCHEMA or str(ref).endswith(CHAT_SCHEMA):
            return True
        props = schema_obj.get("properties") or {}
        # ChatCompletionRequest always has messages + optional store/metadata.
        if "messages" in props and ("store" in props or "model" in props):
            return True
    return False


def _iter_contract_endpoints(service: Any) -> List[Any]:
    endpoints: List[Any] = []
    for deployment in _attr(service, "deployments", default=[]) or []:
        contract = _attr(deployment, "contract")
        if contract is None:
            continue
        endpoints.extend(_attr(contract, "endpoints", default=[]) or [])
    return endpoints


def _chat_path(service: Any) -> Optional[str]:
    """Prefer platform endpoint metadata, then materialized deployment contract."""
    for endpoint in _attr(service, "endpoints", default=[]) or []:
        if _endpoint_is_chat(endpoint):
            return _attr(endpoint, "path") or "/chat"
    for endpoint in _iter_contract_endpoints(service):
        if _endpoint_is_chat(endpoint):
            return _attr(endpoint, "path") or "/chat"
    return None


def _looks_like_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def _diagnose_catalog() -> str:
    """Explain why auto-discovery failed on this backend."""
    lines = [
        "No APIPod chat service (ChatCompletionRequest or path /chat) found on",
        f"{BACKEND}.",
        "",
        "Models like openai-gpt-4o-mini expose Replicate /predictions with a",
        "'messages' field — that is NOT enough. Orch only persists conversations",
        "when the job output is a chat.completion object (APIPod /chat).",
        "",
        "Also, ChatServiceAdapter + /predictions stringifies nested messages,",
        "which is the validation error you hit (list expected, got JSON string).",
        "",
        "Fix options:",
        "  1) Deploy qwen-models (or any APIPod service with /chat) onto the",
        "     test inference stack, then:",
        "       python test/test_e2e_agentic_chat.py --service <catalog-name>",
        "  2) For local complete/stream smoke only (no platform store=true):",
        "       python test/test_e2e_agentic_chat.py --url http://127.0.0.1:8010",
        "",
        "Nearby text models on this catalog (Replicate — cannot test agentic store):",
    ]
    samples: List[str] = []
    for q in ("gpt-4o", "instruct", "claude", "llama", "qwen"):
        try:
            hits = socaity.list_services(q=q, expand=["endpoints"], limit=5)
        except Exception:
            continue
        for hit in hits:
            raw = getattr(hit, "raw", hit)
            name = _attr(raw, "name", "id")
            if not name or name in samples:
                continue
            paths = [
                str(_attr(ep, "path") or "?")
                for ep in (_attr(raw, "endpoints", default=[]) or [])
            ]
            samples.append(name)
            lines.append(f"  - {name}  endpoints={paths or ['(none on list)']}")
            if len(samples) >= 8:
                break
        if len(samples) >= 8:
            break
    if not samples:
        lines.append("  (could not list sample services)")
    return "\n".join(lines)


def discover_chat_service(
    override: Optional[str] = None,
    url: Optional[str] = None,
) -> Tuple[str, str]:
    """Return (service_slug_or_id_or_url, chat_endpoint_path)."""
    url = url or os.getenv("CHAT_SERVICE_URL")
    if url:
        path = os.getenv("CHAT_ENDPOINT_PATH", "/chat")
        return url.rstrip("/"), path if path.startswith("/") else f"/{path}"

    override = override or os.getenv("CHAT_SERVICE")
    if override and _looks_like_url(override):
        path = os.getenv("CHAT_ENDPOINT_PATH", "/chat")
        return override.rstrip("/"), path if path.startswith("/") else f"/{path}"

    expand = ["endpoints", "deployments", "deployments.contract"]
    if override:
        svc = socaity.get_service(override, expand=expand)
        if svc is None:
            raise AssertionError(f"CHAT_SERVICE={override!r} not found in catalog")
        path = _chat_path(svc)
        if not path:
            raise AssertionError(
                f"CHAT_SERVICE={override!r} has no ChatCompletionRequest /chat endpoint.\n"
                + _diagnose_catalog()
            )
        return (svc.name or override, path)

    queries = ["qwen", "deepseek", "llm", "chat"]
    seen: set[str] = set()
    candidates: List[Tuple[str, str, int, bool]] = []
    for q in queries:
        for hit in socaity.list_services(q=q, expand=["endpoints"], limit=15):
            raw = getattr(hit, "raw", hit)
            name = _attr(raw, "name", "id")
            if not name or name in seen:
                continue
            seen.add(name)
            svc = socaity.get_service(name, expand=expand)
            if svc is None:
                continue
            path = _chat_path(svc)
            if not path:
                continue
            usages = 0
            for ep in svc.endpoints or []:
                usages = max(usages, int(_attr(ep, "n_usages", default=0) or 0))
            official = bool(_attr(svc, "is_official", default=False))
            candidates.append((svc.name or name, path, usages, official))

    if not candidates:
        raise AssertionError(_diagnose_catalog())
    candidates.sort(key=lambda row: (row[3], row[2]), reverse=True)
    return candidates[0][0], candidates[0][1]


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


def _assistant_text(completion: Dict[str, Any]) -> str:
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
            # 404 until orch persists the first turn
            if "404" not in str(exc):
                raise
            time.sleep(2)
            continue
        items = last.get("items") if isinstance(last, dict) else None
        if items is None:
            items = _platform(
                "GET",
                f"v1/conversations/{conversation_id}/items",
                params={"branch": "active", "limit": 100},
            )
        if isinstance(items, list) and len(items) >= min_items:
            if isinstance(last, dict):
                last = {**last, "items": items}
            return last
        time.sleep(2)
    raise AssertionError(
        f"conversation {conversation_id} did not persist >= {min_items} items "
        f"within {PERSIST_TIMEOUT_S}s (last={last!r}). "
        "Check orch ChatHistoryWriter + chats SQL on this environment."
    )


def _wait_search_hit(query: str, conversation_id: str) -> None:
    deadline = time.time() + SEARCH_TIMEOUT_S
    while time.time() < deadline:
        payload = _platform("GET", "v1/conversations", params={"q": query, "limit": 20})
        ids = [
            row.get("id") if isinstance(row, dict) else getattr(row, "id", None)
            for row in _entities(payload)
        ]
        if conversation_id in ids:
            return
        # Nudge Typesense via the indexed webhook (orch may have already called it).
        _platform(
            "POST",
            "v1/conversations/webhooks/indexed",
            params={"conversation_id": conversation_id},
        )
        time.sleep(2)
    raise AssertionError(
        f"conversation {conversation_id} not found via q={query!r} within {SEARCH_TIMEOUT_S}s"
    )


def _active_assistant_item(conversation: Dict[str, Any]) -> Dict[str, Any]:
    items = conversation.get("items") or []
    assistants = [i for i in items if isinstance(i, dict) and i.get("role") == "assistant"]
    if not assistants:
        raise AssertionError(f"no assistant items in conversation: {conversation!r}")
    # Prefer the active leaf when present.
    active_id = conversation.get("active_item_id")
    for item in assistants:
        if item.get("id") == active_id:
            return item
    return assistants[-1]


# ---------------------------------------------------------------------------
# Scenario
# ---------------------------------------------------------------------------


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


@dataclass
class ScenarioResult:
    service: str = ""
    endpoint: str = ""
    conversation_id: str = ""
    job_ids: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


def run_scenario(
    *,
    chat_service: Optional[str] = None,
    chat_url: Optional[str] = None,
    try_tools: bool = True,
) -> ScenarioResult:
    result = ScenarioResult()
    result.conversation_id = str(uuid.uuid4())

    _log("0", f"backend={BACKEND}")
    _log("0", f"marker token={TOKEN}")

    # --- auth / catalog smoke -------------------------------------------------
    _log("0a", "checking credentials + catalog")
    key = get_api_key()
    assert key, "missing API key"
    services = socaity.list_services(limit=1)
    assert services, "catalog returned no services"

    conv_smoke = _platform("GET", "v1/conversations", params={"limit": 1})
    assert isinstance(conv_smoke, (dict, list)), f"unexpected conversations payload: {conv_smoke!r}"
    _log("0a", "conversations list OK")

    # --- discover chat service -----------------------------------------------
    _log("1", "discovering chat-capable service")
    service_name, endpoint_path = discover_chat_service(chat_service, url=chat_url)
    result.service, result.endpoint = service_name, endpoint_path
    _log("1", f"using {service_name} @ {endpoint_path}")
    if _looks_like_url(service_name):
        note = (
            "direct URL mode: complete/stream work locally, but store=true "
            "conversation persistence needs a catalog-registered chat deployment "
            "so jobs flow through the test orch"
        )
        result.notes.append(note)
        _log("1", f"WARNING: {note}")

    adapter = ChatServiceAdapter(service_name, endpoint_path=endpoint_path)

    # --- basic completion (no store) -----------------------------------------
    _log("2a", "non-streaming completion without store")
    completion = adapter.complete(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Reply with exactly one short sentence mentioning {TOKEN}.",
                }
            ],
            "max_tokens": 128,
            "temperature": 0.2,
        },
        timeout_s=CHAT_TIMEOUT_S,
    )
    text = _assistant_text(completion)
    assert text.strip(), f"empty assistant content: {completion!r}"
    job = adapter.last_job()
    assert job is not None
    job_id = _platform_job_id(job)
    result.job_ids.append(job_id)
    _log("2a", f"ok job={job_id} text={text[:120]!r}")

    # --- streaming ------------------------------------------------------------
    _log("2b", "streaming completion without store")
    pieces: List[str] = []
    for chunk in adapter.stream_chunks(
        {
            "messages": [{"role": "user", "content": f"Say hi in five words. Ref {TOKEN}."}],
            "max_tokens": 64,
            "temperature": 0.2,
        }
    ):
        delta = ((chunk.get("choices") or [{}])[0].get("delta") or {})
        if delta.get("content"):
            pieces.append(delta["content"])
    streamed = "".join(pieces)
    assert streamed.strip(), "stream produced no content deltas"
    stream_job = adapter.last_job()
    assert stream_job is not None
    result.job_ids.append(_platform_job_id(stream_job))
    _log("2b", f"ok streamed={streamed[:120]!r}")

    # --- persist first turn ---------------------------------------------------
    _log("4a", f"persist first turn store=true conversation_id={result.conversation_id}")
    landmark = f"lighthouse-{TOKEN}"
    first = adapter.complete(
        {
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
            "metadata": {"conversation_id": result.conversation_id},
            "max_tokens": 128,
            "temperature": 0.2,
        },
        timeout_s=CHAT_TIMEOUT_S,
    )
    first_text = _assistant_text(first)
    assert first_text.strip(), first
    first_job_id = _platform_job_id(adapter.last_job())
    result.job_ids.append(first_job_id)
    _log("4a", f"chat job finished job={first_job_id}")

    conversation = _wait_conversation(result.conversation_id, min_items=2)
    n_messages = conversation.get("n_messages") or len(conversation.get("items") or [])
    _log("4a", f"persisted n_messages={n_messages} items={len(conversation.get('items') or [])}")

    # --- job ↔ chat_item link -------------------------------------------------
    _log("4b", "GET job expand=chat_item")
    linked = socaity.get_job(first_job_id, expand=["chat_item", "data"])
    assert linked is not None, first_job_id
    chat_item = getattr(linked, "chat_item", None)
    assert chat_item is not None, (
        f"job {first_job_id} has no chat_item expand — orch may not have linked the turn"
    )
    _log("4b", f"chat_item id={getattr(chat_item, 'id', None)} role={getattr(chat_item, 'role', None)}")

    # --- continue thread ------------------------------------------------------
    _log("4c", "continue conversation (same conversation_id)")
    second = adapter.complete(
        {
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
            "metadata": {"conversation_id": result.conversation_id},
            "max_tokens": 64,
            "temperature": 0,
        },
        timeout_s=CHAT_TIMEOUT_S,
    )
    second_text = _assistant_text(second)
    second_job_id = _platform_job_id(adapter.last_job())
    result.job_ids.append(second_job_id)
    conversation = _wait_conversation(result.conversation_id, min_items=4)
    _log("4c", f"continued job={second_job_id} reply={second_text[:80]!r}")

    # --- optional client tool round-trip -------------------------------------
    if try_tools:
        _log("3", "client-side tool call attempt (best-effort)")
        tool_completion = adapter.complete(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "What is the weather in Boston? Use the get_weather tool.",
                    }
                ],
                "tools": [WEATHER_TOOL],
                "tool_choice": "auto",
                "store": True,
                "metadata": {"conversation_id": result.conversation_id},
                "max_tokens": 256,
                "temperature": 0,
            },
            timeout_s=CHAT_TIMEOUT_S,
        )
        tool_job_id = _platform_job_id(adapter.last_job())
        result.job_ids.append(tool_job_id)
        tool_choice = (tool_completion.get("choices") or [{}])[0]
        tool_message = tool_choice.get("message") or {}
        tool_calls = tool_message.get("tool_calls") or []
        if tool_calls:
            call = tool_calls[0]
            call_id = call.get("id") or "call_weather"
            _log("3", f"model requested tool_calls={json.dumps(tool_calls)[:200]}")
            follow = adapter.complete(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": "What is the weather in Boston? Use the get_weather tool.",
                        },
                        tool_message,
                        {
                            "role": "tool",
                            "tool_call_id": call_id,
                            "content": "sunny, 22C",
                        },
                    ],
                    "tools": [WEATHER_TOOL],
                    "store": True,
                    "metadata": {"conversation_id": result.conversation_id},
                    "max_tokens": 128,
                    "temperature": 0,
                },
                timeout_s=CHAT_TIMEOUT_S,
            )
            result.job_ids.append(_platform_job_id(adapter.last_job()))
            _log("3", f"tool follow-up={_assistant_text(follow)[:120]!r}")
        else:
            note = "model did not emit tool_calls; tools were still accepted on the request"
            result.notes.append(note)
            _log("3", f"skip hard assert — {note}")
    else:
        result.notes.append("tools step skipped (--no-tools)")
        _log("3", "skipped (--no-tools)")

    conversation = _wait_conversation(result.conversation_id, min_items=4)

    # --- branching ------------------------------------------------------------
    _log("6", "branch via parent_item_id")
    leaf = _active_assistant_item(conversation)
    # Prefer an earlier assistant item as branch parent when available.
    assistants = [
        i for i in (conversation.get("items") or [])
        if isinstance(i, dict) and i.get("role") == "assistant"
    ]
    branch_parent = assistants[0] if assistants else leaf
    parent_item_id = branch_parent.get("id")
    assert parent_item_id, branch_parent
    branch = adapter.complete(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"Alternate timeline. Secret was '{landmark}'. "
                        "Reply with: BRANCH_OK and the codeword."
                    ),
                }
            ],
            "store": True,
            "metadata": {
                "conversation_id": result.conversation_id,
                "parent_item_id": parent_item_id,
            },
            "max_tokens": 64,
            "temperature": 0,
        },
        timeout_s=CHAT_TIMEOUT_S,
    )
    result.job_ids.append(_platform_job_id(adapter.last_job()))
    _log("6", f"branch reply={_assistant_text(branch)[:80]!r} parent={parent_item_id}")

    all_items = _platform(
        "GET",
        f"v1/conversations/{result.conversation_id}/items",
        params={"branch": "all", "limit": 200},
    )
    active_items = _platform(
        "GET",
        f"v1/conversations/{result.conversation_id}/items",
        params={"branch": "active", "limit": 200},
    )
    assert isinstance(all_items, list) and len(all_items) >= len(active_items or []), (
        f"branch=all ({len(all_items or [])}) should cover active ({len(active_items or [])})"
    )
    _log("6", f"items active={len(active_items or [])} all={len(all_items or [])}")

    # --- list / search / patch -----------------------------------------------
    _log("5a", "list conversations includes ours")
    listed = _entities(_platform("GET", "v1/conversations", params={"limit": 50}))
    assert any(isinstance(r, dict) and r.get("id") == result.conversation_id for r in listed), [
        r.get("id") if isinstance(r, dict) else r for r in listed[:10]
    ]

    _log("5b", f"Typesense search q={landmark}")
    _wait_search_hit(landmark, result.conversation_id)
    _log("5b", "search hit OK")

    _log("5c", "PATCH title + status")
    patched = _platform(
        "PATCH",
        f"v1/conversations/{result.conversation_id}",
        params={"title": f"E2E {TOKEN}", "status": "active"},
    )
    assert isinstance(patched, dict)
    assert patched.get("title") == f"E2E {TOKEN}"
    _log("5c", f"title={patched.get('title')!r}")

    # --- delete cascade -------------------------------------------------------
    _log("5d", "DELETE conversation")
    _platform("DELETE", f"v1/conversations/{result.conversation_id}", expect=(200, 204))
    # Soft-delete: get should 404 for the owner list hydrate path
    with httpx.Client(timeout=30) as client:
        gone = client.get(
            BACKEND + f"v1/conversations/{result.conversation_id}",
            headers=_auth_headers(),
        )
    assert gone.status_code == 404, f"expected 404 after delete, got {gone.status_code}: {gone.text[:200]}"
    _log("5d", "delete confirmed (404 on get)")

    _log("done", f"service={result.service} jobs={len(result.job_ids)} notes={result.notes or ['none']}")
    return result


# ---------------------------------------------------------------------------
# Pytest entry + CLI
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def scenario() -> ScenarioResult:
    return run_scenario()


def test_agentic_chat_end_to_end(scenario: ScenarioResult):
    assert scenario.service
    assert scenario.conversation_id
    assert len(scenario.job_ids) >= 3


def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Agentic chat E2E against a live Socaity backend")
    parser.add_argument(
        "--service",
        default=os.getenv("CHAT_SERVICE"),
        help="Catalog service name/id with ChatCompletionRequest or /chat (or set CHAT_SERVICE)",
    )
    parser.add_argument(
        "--url",
        default=os.getenv("CHAT_SERVICE_URL"),
        help="Direct APIPod base URL with /chat (or set CHAT_SERVICE_URL)",
    )
    parser.add_argument(
        "--diagnose",
        action="store_true",
        help="Only print catalog chat-discovery diagnosis and exit",
    )
    parser.add_argument(
        "--no-tools",
        action="store_true",
        help="Skip the client-side tool-calling attempt",
    )
    args = parser.parse_args(argv)

    print("=" * 72)
    print("Socaity agentic chat E2E (real-world backend path)")
    print("=" * 72)
    if not _backend_up():
        print(f"FAIL: backend not reachable at {BACKEND}", file=sys.stderr)
        return 2
    if not _has_credentials():
        print(
            "FAIL: set SOCAITY_API_KEY or run:\n"
            f"  socaity login --backend-url {BACKEND.rstrip('/')}",
            file=sys.stderr,
        )
        return 2
    if args.diagnose:
        print(_diagnose_catalog())
        return 0
    try:
        result = run_scenario(
            chat_service=args.service,
            chat_url=args.url,
            try_tools=not args.no_tools,
        )
    except Exception as exc:
        print(f"\nFAIL: {exc}", file=sys.stderr)
        return 1
    print("\nPASS")
    print(json.dumps({
        "service": result.service,
        "endpoint": result.endpoint,
        "conversation_id": result.conversation_id,
        "job_ids": result.job_ids,
        "notes": result.notes,
        "backend": BACKEND,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
