# socaity SDK Technical README

## TL;DR

The socaity SDK is the **catalog and session layer** on top of [fastSDK](https://github.com/SocAIty/fastsdk). Discovery goes through `v1/catalog/*`. Execution is `Client.run` (catalog services), `Client.run_agent`, `Client.run_workflow`, or `Client.connect(source)` then `submit_job`. Addresses retarget to `{gate}/services/v1/{slug}`.

fastSDK owns transport: HTTP, polling, cancellation, and streaming. socaity owns platform integration: authentication, catalog resolve, and the `run` verb.

For job execution internals, streaming modes, and provider stacks, see [fastSDK TECHNICAL_README](https://github.com/SocAIty/fastsdk/blob/main/TECHNICAL_README.md). For server-side schemas and streaming producers, see [APIPod TECHNICAL_README](https://github.com/SocAIty/APIPod/blob/main/docs/TECHNICAL_README.md).

## Public API Surface

Backend methods live on ``Client`` (``SocaityClient``, inherited from ``socaity-cli`` mixins).
There is no module-level function facade. Use the active ``client`` proxy, an
explicit ``Client(...)``, or ``with Session(api_key=...)``.

| Symbol | Side effects | Returns |
|---|---|---|
| ``socaity.service_registry`` | FastSDK in-process registry | ``Registry`` |
| ``client`` / ``Client(...)`` | active session proxy, or an explicit credential-bound handle | ``Client`` |
| ``Session(...)`` | bind credentials for a block; ``with Session(api_key=...)`` | ``Session`` |
| ``Client.query_services(...)`` | one catalog fetch (slim, sparse fieldset) | ``List[Service]`` |
| ``Client.get_service(id_or_slug)`` | one catalog fetch (full) | ``Service`` |
| ``Client.query_models(...)`` / ``get_model(...)`` | catalog fetch | ``List[AIModel]`` / ``AIModel`` |
| ``Client.query_categories()`` | catalog fetch | ``List[ServiceCategory]`` |
| ``Client.list_pricing_rules()`` | catalog fetch | pricing rule rows |
| ``Client.query_jobs(...)`` / ``get_job(...)`` | ``v1/jobs`` query/get | ``List[Job]`` / ``Job`` |
| ``Client.refresh_job(job_id)`` | finished-job webhook refresh | cache + Typesense upsert |
| ``Client.update_job(...)`` / ``delete_job(...)`` | job mutations | ``bool`` |
| ``Client.query_projects(...)`` / ``upsert_project(...)`` / … | ``v1/projects`` | ``List[Project]`` / ids / ``bool`` |
| ``Client.estimate(...)`` / ``get_stats(...)`` / ``get_similar_services(...)`` | ``v1/analytics`` | estimate / stats / similar |
| ``Client.query_interrupts(...)`` / ``get_interrupt(...)`` | ``v1/interrupts`` HIT inbox (pending by default) | ``List[Interrupt]`` / ``Interrupt`` |
| ``Client.resolve_interrupt(id, decision, ...)`` | records decision; ``continue_run=True`` enqueues the agent continue job | ``InterruptResolveResult`` |
| ``Client.connect(source)`` | catalog GET, in-memory Registry, gate address | ``FastClient`` |
| ``Client.run(target, **params)`` | catalog service job | ``APISeex`` |
| ``Client.run_agent(...)`` | ``POST /v1/agents/{id}/chat`` | ``APISeex`` |
| ``Client.run_workflow(...)`` | ``POST /v1/workflows/{id}/run`` | ``APISeex`` |
| ``Client.track_job(job_id)`` | re-attach to a running gateway job | ``APISeex`` |
| ``Client.cancel_job(job_id)`` | ``APISeex.cancel`` on an attached job | cancel summary |
| ``socaity.APISeex`` | re-export | job handle from every model call |

``socaity-cli`` owns all backend HTTP. FastSDK and Meseex own job submission,
polling, streaming, cancellation, and ``APISeex.subscribe``. Eligible
``Client`` methods become FastMCP / LangChain tools through
``to_fastmcp`` / ``to_langchain`` (function-identity policy). MCP and SPAINE
do not redefine those methods. The workflow engine calls ``Client``
directly.

Module-level CLI: `socaity login`, `run`, `list`, `search`, `jobs`, `projects`, `interrupts`, plus optional APIPod deploy commands when `[apipod]` is installed.

`ChatSocaity` (LangChain) forwards OpenAI ``tools``, ``tool_choice``, and
``parallel_tool_calls`` to the catalog chat service. Native ``tool_calls`` on
blocking and streamed turns drive ``create_agent`` tool loops and HITL interrupts.
``image_url`` parts stay on the message. Remote http(s) URLs are sent as the
VLM ``images`` param so current qwen pods download them. Data URIs stay inline.

### Catalog reads: slim by default

List calls request a sparse fieldset (`fields=id,slug,display_name,...`) and optional
`filter` / `q`. Results are schema models (`Service`, `Job`, …), not lazy proxies.
Call ``get_service`` with expand (``details.contract``, ``endpoints``) when you need the
runtime bindings (``details[]``, each optionally carrying a hosting ``deployment``) or contracts.
``run(..., details_id=details[0].id)`` pins the spec. Compute URL is
``details[0].deployment``; connector URL is ``details[0].connector``. Connectors are catalog
services with ``kind == "connector"``; they run like any other service.

## Mental Model

Think of socaity as two connected subsystems:

1. **Catalog layer**
   - Talks to `webapi.socaity.ai`: `v1/catalog/*` for discovery (list, get, search)
   - `connect` loads one `Service`, retargets the binding to `{gate}/services/v1/{slug}`, upserts an in-memory Registry
   - `run` resolves `wf_`/`wr_`, then catalog agent, then compute/connector, then the owner's workflow slug

2. **Runtime layer (delegated to fastSDK)**
   - `connect` returns `FastClient`. `run` calls `submit_job` or the agent/workflow factory
   - Jobs poll, cancel, stream, and notify subscribers through fastSDK's `JobRuntime` + meseex pipeline
   - Media results deserialize via `media-toolkit`

`connect()` and `run()` are the two entry points into the same runtime.

## Easy Overview

```
Platform (webapi.socaity.ai)
  │  v1/catalog/services
  ▼
SocaityClient.get_service / connect / run
  ▼
FastClient(details_id) → POST {gate}/services/v1/{slug}/{path}?details_id=
  ▼
fastSDK ApiJobManager → APISeex
```

`socaity.service_registry` is FastSDK's in-process registry. `connect` upserts with `persist=False`. Workers do not import this package.

## Package Layout

```
socaity/
  __init__.py                     # Client, session, FastSDK re-exports
  __main__.py                     # python -m socaity (delegates to socaity_cli.cli)
  client.py                       # connect + run
  core/
    gateway.py                    # local Service for agent/workflow factory paths
    session.py                    # ContextVar credentials + inference origin
    serialize.py
  sdk/                            # reserved empty package
  integrations/                   # MCP / LangChain policy
```

## Core Building Blocks

### `SocaityBackendClient`

Sync `httpx` client for **platform metadata only** (not inference). Auth via `SOCAITY_API_KEY` or credentials from `socaity login`. Backend URL is resolved per client (constructor, then `SOCAITY_BACKEND_URL`, then the login file, then prod). Looking up an API key never writes `SOCAITY_BACKEND_URL` into the process. Inference traffic goes through fastSDK to `api.socaity.ai`.

Catalog reads use the backend's sparse fieldsets (`select`), relation embedding (`include`) and pagination (`limit`/`offset`).

Every `run` / `submit_job` returns `APISeex` immediately. Collect with `get_result()`, stream with `stream()`, or cancel with `cancel()`.

## Schemas (`socaity-schemas`)

Shared Pydantic models live in the standalone `socaity-schemas` package. socaity depends on it directly; fastSDK and APIPod consume the same types.

| Module | Contents |
|---|---|
| `socaity_schemas.public.inference.language` | Chat, completion, embedding, tools, usage, stream chunks |
| `socaity_schemas.public.inference.generation` | Image, video, audio, vision, 3D (`SpeechRequest`, …) |
| `socaity_schemas.public.inference.media` | `FileModel` wire shape for nested media |
| `socaity_schemas.public.providers` | Job envelopes (`SocaityJobResponse`, `JobLinks`) and `StreamingResponse` |
| `socaity_schemas.public.spec` | `ServiceAddress`, URL helpers, `Endpoint`, `ServiceContract` |
| `socaity_schemas.platform.catalog` | `Service`, `ServiceDetails`, `AIModel`, hosting, pricing |

socaity re-exports catalog types (`Service`, `ServiceDetails`, `AIModel`, `Deployment`, `ServiceCategory`, `PriceEstimate`) and `Job` at package level. For typed chat or speech payloads, import the request models directly:

```python
from socaity_schemas.public.inference.language import ChatCompletionRequest
from socaity_schemas.public.inference.generation import SpeechRequest
```

`run` and `submit_job` accept plain Python values or dicts; schema-typed bodies are serialized by fastSDK's request formatter when the endpoint expects JSON.

## Streaming

Streaming is implemented entirely in fastSDK. socaity adds no transport code; every model call already returns an `APISeex` handle with full streaming support.

Three modes (same as fastSDK):

1. **Direct SSE** — `stream=True` on a schema endpoint returns `text/event-stream` on the initial POST
2. **Raw binary** — e.g. `SpeechRequest(stream=True)` streams audio bytes
3. **Job + stream link** — queued serverless jobs expose `links.stream`; poll `/status` or read the live stream

### Usage from socaity

```python
from socaity import client
from fastsdk.service_interaction.response.sse_assembly import chunk_text

job = client.run("deepseek-v3", messages=[{"role": "user", "content": "Hello"}], stream=True)

# Option A: iterate live
for chunk in job.stream():
    print(chunk_text(chunk), end="", flush=True)

# Option B: blocking assembly (fastSDK joins SSE text or media bytes)
text = job.get_result()
```

`job.stream()` returns a `StreamSession` with sync (`iter_chunks`, `iter_bytes`) and async (`aiter_*`) iterators. One session, both consumer styles. `get_result()` assembles the full payload when you never called `stream()`.

For TTS byte streams:

```python
job = speechcraft().text2voice(text="Hello", stream=True)
audio = job.get_result()  # assembled AudioFile when stream was not consumed
# or
for chunk in job.stream().iter_bytes():
    ...
```

See fastSDK's Streaming section for `JobRuntime` guards, cancellation teardown, and provider URL resolution.

## Jobs, Parallel Execution, Cancellation

Calls return jobs, not blocked connections:

```python
from socaity import gather_results

jobs = [
    flux_schnell()(prompt="sunset"),
    deepseek_v3()(prompt="haiku about SDKs"),
]
images, text = gather_results(jobs)
```

Cancel in-flight work:

```python
job = client.some_endpoint(...)
info = job.cancel()  # local + remote when provider supports it
```

Details: fastSDK TECHNICAL_README (Cancellation, JobRuntime).

## Ad-hoc clients without install

For services not in the catalog, or local APIPod dev servers:

```python
from socaity import client, Client, Session

job = client.connect("http://localhost:8009").submit_job("/chat", messages=[...], stream=True)

mine = Client(api_key=key)
with Session(api_key=other_key):
    client.query_categories()
```

``Client.connect()`` resolves platform identifiers through the catalog, retargets the binding to the gate, and returns a FastClient. URLs, spec paths and `replicate:` references skip the backend and go straight to fastsdk. The package-level ``client`` forwards to the active session. Explicit ``Client(...)`` handles ignore it.

Inside an engine session (agent turn, workflow run), ``run`` and the chat adapter attach the session's ``socaity_options`` and ``socaity_context``. Nested jobs inherit the data policy and become children of the engine job (``parent_job_id``).

## Authentication and credentials

| Mechanism | Storage | Used for |
|---|---|---|
| `SOCAITY_API_KEY` env | n/a | inference + backend |
| `socaity login` | `~/.config/socaity/credentials.json` | backend + run |
| Per-client `api_key=` | n/a | overrides env for that client |

Legacy token migration from `~/.apipod/token` is handled in `socaity_cli.credentials`.

## CLI

The `socaity` command lives in the separate **socaity-cli** package (a hard dependency
of this SDK). It bundles login, catalog browsing, `socaity run`, and APIPod deployment
commands with minimal dependencies (httpx + socaity-schemas). `socaity run` delegates
into `SocaityClient.run` via `requires("socaity")`; `scan` / `build` / `start` delegate
to `apipod` the same way. `SocaityBackendClient` and credentials handling are imported
from `socaity_cli`.

| Command | Needs | Notes |
|---|---|---|
| `socaity login` | - | browser flow via `v1/cli-auth/start` |
| `socaity run TARGET` | socaity | catalog service job |
| `socaity list services\|models` | - | catalog listing, `--category`, `--family`, `--limit` |
| `socaity search QUERY` | - | typo-tolerant fuzzy search over services and models |
| `socaity scan/build/start` | apipod | delegates to the apipod CLI |

The socaity CLI does not duplicate fastSDK's `inspect` / `call` / `registry` commands. Use `fastsdk` for generic OpenAPI/Replicate tooling; use `socaity` for catalog management.

## Relationship to the Ecosystem

| Package | Role relative to socaity |
|---|---|
| **APIPod** | Server framework; produces OpenAPI + standardized schemas |
| **socaity-schemas** | Shared Pydantic models (definitions, AI payloads, transport) |
| **apipod-registry** | Registry base class + spec parsers |
| **fastSDK** | Client runtime: jobs, polling, streaming, stub factory |
| **media-toolkit** | Media I/O on results |
| **meseex** | Async job orchestration inside fastSDK |
| **socaity SDK** | Catalog resolve + `client.run` |

Data flow for a catalog model:

1. APIPod service deployed on socaity.ai publishes OpenAPI + schemas
2. Platform stores `Service` + `ServiceDetails` (socaity-schemas)
3. `client.run("slug/path", **params)` loads the catalog, retargets to the gate
4. fastSDK executes against `{gate}/services/v1/{slug}`

## Cache

The gate holds a 24h LRU of catalog rows and prepared materializers. `catalog.changed` evicts. The SDK does not write stubs.

## Testing

```
test/
  bundle/test_core.py      # PyPI publish gate: invariants + stacked platform e2e
  test_e2e_catalog.py      # catalog list/get/search
  test_e2e_files.py        # file_service
  test_e2e_jobs.py         # one flux via client.run; search finds the prompt
  test_e2e_conversations.py
  test_e2e_agent_hitl.py
  test_e2e_wait_cancel.py
  test_e2e_workflow_repair.py
  test_e2e_publish_fork.py # two-user (not in the core bundle)
  test_e2e_agent_image_vlm.py
  test_replicate.py        # platform-mediated Replicate (marker: replicate)
  test_chat_socaity_request.py
  test_langchain_chat.py   # ChatServiceAdapter vs APIPod debug services
  manual/                  # face2face + speechcraft; run as scripts
  stress/simultaneous_jobs.py
```

Default ``pytest`` collects the e2e files (they skip when the stack is down) and skips ``manual``, ``replicate``, and the core bundle. Official hosted services are manual:

    python test/manual/test_face2face.py
    python test/manual/test_speechcraft.py

Replicate through the platform (not the default suite):

    pytest test/test_replicate.py -v -s

PyPI publish gate (local stack required: backend :8000, gate :8001, SPAINE in catalog):

    pytest test/bundle/test_core.py -v -s

Integration tests force the local gate via ``agentic_utils`` (``APIPOD_GATE_URL=http://127.0.0.1:8001``). Credentials: ``SOCAITY_API_KEY`` / ``SOCAITY_POOR_API_KEY`` in the repo ``.env``.

Run with the project venv: `pytest` (after `pip install -e ".[dev]"`).

## Why the Architecture Looks Like This

Python users want `from socaity import flux_schnell`, not manual OpenAPI hunting per model. The platform already owns service metadata; duplicating transport in socaity would fork fastSDK.

socaity therefore stays thin:

- **Platform sync** is socaity-specific (backend endpoints, namespaces, credentials)
- **Everything after stub generation** is fastSDK (including streaming added in 0.3.0)
- **Schema contracts** are centralized in socaity-schemas so APIPod servers and clients stay aligned

Future platform features (model search, cost estimation, agentic workflows) will extend the catalog layer and backend client without moving transport back into socaity.

## Planned Extensions (not implemented here)

For context only. These are roadmap items, not current API:

- Native chat helpers and LangChain-style integrations
- Job cost/runtime estimation endpoints
- Standalone CLI package imported by socaity
- Agentic workflow execution in the framework layer
