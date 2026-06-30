# socaity SDK Technical README

## TL;DR

The socaity SDK is the **catalog and namespace layer** on top of [fastSDK](https://github.com/SocAIty/fastsdk). It syncs model definitions from the socaity.ai platform, generates typed client stubs, and routes imports through a curated model zoo (`official/`, `replicate/`, `community/`).

fastSDK owns transport: HTTP, polling, cancellation, and streaming. socaity owns platform integration: authentication, backend sync, stub codegen, and import paths.

For job execution internals, streaming modes, and provider stacks, see [fastSDK TECHNICAL_README](https://github.com/SocAIty/fastsdk/blob/main/TECHNICAL_README.md). For server-side schemas and streaming producers, see [APIPod TECHNICAL_README](https://github.com/SocAIty/APIPod/blob/main/docs/TECHNICAL_README.md).

## Public API Surface

| Symbol | Side effects | Returns |
|---|---|---|
| `socaity.install(name)` | backend fetch + stub write + registry upsert | `None` |
| `socaity.service_registry` | shared singleton | `SocaityServiceRegistry` |
| `from socaity import model` | none (import generated stub) | `FastClient` subclass |
| `socaity.connect(source)` | re-export of `fastsdk.connect` | temporary `FastClient` |
| `socaity.generate_stub(...)` | re-export of `fastsdk.generate_stub` | `FastStub` |
| `socaity.APISeex` | re-export | job handle from every model call |

Module-level CLI: `socaity login`, `install`, `update`, plus optional APIPod deploy commands when `[apipod]` is installed.

## Mental Model

Think of socaity as two connected subsystems:

1. **Catalog layer**
   - Talks to `webapi.socaity.ai` for install/update payloads
   - Persists `ServiceDefinition` objects (from `socaity-schemas`) in a local cache
   - Generates `FastClient` subclasses under `socaity/sdk/services/`
   - Wires namespace `__init__.py` files so imports resolve cleanly

2. **Runtime layer (delegated to fastSDK)**
   - Generated stubs call `FastClient.submit_job(endpoint, **params)` → `APISeex`
   - Jobs poll, cancel, and stream through fastSDK's `JobRuntime` + meseex pipeline
   - Media results deserialize via `media-toolkit`

Generated model imports and `connect()` are two entry points into the same runtime.

## Easy Overview

```
Platform (webapi.socaity.ai)
  │  v1/sdk/install_service, v1/sdk/update_package
  ▼
SocaityBackendClient
  ▼
SocaityServiceRegistry
  │  fastsdk.generate_stub(ServiceDefinition) → socaity/sdk/services/{id}.py
  │  namespace __init__.py updates (official/, replicate/, community/)
  ▼
User code: from socaity import speechcraft
  ▼
speechcraft().text2voice(...) → APISeex
  ▼
fastSDK ApiJobManager → inference at api.socaity.ai
```

On import, `socaity/__init__.py` replaces fastSDK's default registry with `SocaityServiceRegistry` backed by `FileSystemStore` at `socaity/sdk/cache/`. Every generated stub and ad-hoc client in the process shares that registry and the same `ApiJobManager`.

## Package Layout

```
socaity/
  __init__.py                     # registry swap, namespace path extension, re-exports
  __main__.py                     # python -m socaity
  cli.py                          # login, install, update, apipod bridge
  cli_auth.py                     # browser device login
  cli_apipod.py                   # lazy apipod CLI delegation
  core/
    credentials.py                # XDG credentials (~/.config/socaity/)
    socaity_backend_client.py     # platform HTTP (install/update only)
    socaity_service_registry.py   # catalog sync + stub generation
  sdk/                            # runtime-generated (mostly empty in git)
    services/                     # one FastClient stub per installed service
    official/                     # re-exports for platform models
    community/{user}/             # user-published services
    replicate/{provider}/{user}/    # third-party Replicate models
    cache/                        # FileSystemStore JSON (gitignored)
```

PyPI ships the skeleton `sdk/` tree. Installed models appear after `socaity login` and `socaity install …`.

## Core Building Blocks

### Registry swap (`socaity/__init__.py`)

```python
from fastsdk import FastSDK
from socaity.core.socaity_service_registry import SocaityServiceRegistry

service_registry = FastSDK().service_registry = SocaityServiceRegistry()
```

This is the single wiring point. Generated stubs use `service_name_or_id="<service-id>"` and resolve definitions from this registry. Override inference URLs at runtime:

```python
from socaity import service_registry
from socaity_schemas import SocaityServiceAddress

service_registry.update_service(
    client.service_definition.id,
    service_address=SocaityServiceAddress(url="https://localhost:8009"),
)
```

### `SocaityServiceRegistry`

Extends `apipod_registry.Registry` with platform-aware install/update.

| Method | Backend endpoint | Effect |
|---|---|---|
| `install_service(name_or_id)` | `POST v1/sdk/install_service` | fetch definition, generate stub, update namespace |
| `update_package(force=False)` | `POST v1/sdk/update_package` | sync stale services (15-minute TTL unless forced) |
| `install_all()` | n/a | not supported by backend yet |

Install/update items carry `action` (`install`, `update`, `delete`), `service_definition`, `is_official`, `third_party_provider`, and creator metadata. The registry routes each model into the correct namespace and calls `FastSDK().generate_stub(...)`, which registers the service and writes the `.py` stub.

### `SocaityBackendClient`

Sync `httpx` client for **platform metadata only** (not inference). Auth via `SOCAITY_API_KEY` or credentials from `socaity login`. Inference traffic goes through fastSDK to `api.socaity.ai`.

### Generated stubs

Each installed service becomes a `FastClient` subclass (Jinja2 template from fastSDK):

```python
class Speechcraft(FastClient):
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="<service-id>", api_key=api_key)

    def text2voice(self, text: str, ...) -> APISeex:
        return self.submit_job("/text2voice", text=text, ...)
```

Every endpoint method returns `APISeex` immediately. Collect with `get_result()`, stream with `stream()`, or cancel with `cancel()`.

### Namespace routing

| Condition | Import path | Example |
|---|---|---|
| `is_official=True` | `socaity.sdk.official` / top-level re-export | `from socaity import speechcraft` |
| `third_party_provider=replicate` | `socaity.sdk.replicate.{provider}.{user}` | `from socaity.sdk.replicate.black_forest_labs import flux_schnell` |
| community model | `socaity.sdk.community.{user}` | `from socaity.sdk.community.alice import my_model` |

Alias conflicts within a namespace get suffixed (`flux_schnell_1`).

## Schemas (`socaity-schemas`)

Shared Pydantic models live in the standalone `socaity-schemas` package. socaity depends on it directly; fastSDK and APIPod consume the same types.

| Module | Contents |
|---|---|
| `socaity_schemas.service_definitions` | `ServiceDefinition`, `EndpointDefinition`, `SocaityServiceAddress`, … |
| `socaity_schemas.schemas` | OpenAI-compatible request/response pairs (`ChatCompletionRequest`, `SpeechRequest`, …) |
| `socaity_schemas.transport` | Job envelopes (`SocaityJobResponse`, `JobLinks`) and `StreamingResponse` sentinel |
| `socaity_schemas.media_files` | `FileModel` wire shape for nested media in schema bodies |

socaity re-exports `ServiceDefinition` and `SocaityServiceAddress` at package level. For typed chat/TTS/image payloads, import request models directly:

```python
from socaity_schemas import ChatCompletionRequest, SpeechRequest
```

Generated stub methods accept plain Python values or dicts; schema-typed bodies are serialized by fastSDK's request formatter when the endpoint expects JSON.

## Streaming

Streaming is implemented entirely in fastSDK. socaity adds no transport code; every model call already returns an `APISeex` handle with full streaming support.

Three modes (same as fastSDK):

1. **Direct SSE** — `stream=True` on a schema endpoint returns `text/event-stream` on the initial POST
2. **Raw binary** — e.g. `SpeechRequest(stream=True)` streams audio bytes
3. **Job + stream link** — queued serverless jobs expose `links.stream`; poll `/status` or read the live stream

### Usage from socaity models

```python
from socaity.sdk.replicate.deepseek_ai import deepseek_v3
from fastsdk.service_interaction.response.sse_assembly import chunk_text

job = deepseek_v3()(messages=[{"role": "user", "content": "Hello"}], stream=True)

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
import socaity

client = socaity.connect("http://localhost:8009")
job = client.submit_job("/chat", messages=[...], stream=True)
```

`connect()` is `fastsdk.connect()` — temporary registry entry, removed when the client closes. Use `generate_stub()` to persist a `.py` file instead.

## Authentication and credentials

| Mechanism | Storage | Used for |
|---|---|---|
| `SOCAITY_API_KEY` env | n/a | inference + backend |
| `socaity login` | `~/.config/socaity/credentials.json` | backend install/update |
| Per-client `api_key=` | n/a | overrides env for that client |

Legacy token migration from `~/.apipod/token` is handled in `credentials.py`.

## CLI

| Command | Module | Notes |
|---|---|---|
| `socaity login` | `cli_auth.py` | browser flow via `v1/cli-auth/start` |
| `socaity install SERVICE` | `cli.py` | requires login; calls `install_service` |
| `socaity update` | `cli.py` | syncs installed services |
| `socaity scan/build/start` | `cli_apipod.py` | requires `pip install socaity[apipod]` |

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
| **socaity SDK** | Platform catalog sync + generated import paths |

Data flow for a catalog model:

1. APIPod service deployed on socaity.ai publishes OpenAPI + schemas
2. Platform stores `ServiceDefinition` (socaity-schemas)
3. `socaity install` fetches definition, generates stub, updates namespace
4. User imports model; fastSDK executes against `api.socaity.ai`

## Cache and Updates

- **Cache path:** `socaity/sdk/cache/` (`FileSystemStore`)
- **TTL:** 15 minutes (`CACHE_TTL_MINUTES`); `update_package()` no-ops when fresh
- **Force refresh:** `service_registry.force_update_package()` or `socaity update` after manual cache delete

Re-running install for the same service upserts (same service ID from backend). Stub files and namespace imports are rewritten.

## Testing

```
test/
  test_cli.py              # CLI wiring, login gate
  test_credentials.py      # credential paths
  test_socaity/            # official model integration (needs SOCAITY_API_KEY)
  test_replicate/          # Replicate namespace models
  stress/simultaneous_jobs.py  # concurrent get_result() from cache bootstrap
```

Integration tests override inference URL via `SOCAITY_INFER_BACKEND_URL`. CI-friendly tests: `test_cli.py`, `test_credentials.py`.

Run with project venv: `pytest` (after `pip install -e ".[dev]"`).

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
- Backend listing of models and personal configurations
- Standalone CLI package imported by socaity
- Agentic workflow execution in the framework layer
