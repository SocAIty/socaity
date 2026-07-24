<h1 align="center" style="margin-top:-25px">SocAIty SDK</h1>
<p align="center">
  <img align="center" src="docs/socaity_icon.png" height="200" alt="SocAIty SDK" />
</p>
<h3 align="center" style="margin-top:-10px">Build AI-powered applications with ease</h3>

<p align="center">
  <a href="https://pypi.org/project/socaity/"><img src="https://badge.fury.io/py/socaity.svg" alt="PyPI version" /></a>
  <a href="LICENSE.txt"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="License: GPL v3" /></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+" /></a>
  <a href="https://www.socaity.ai?utm_source=github&utm_content=socaity-sdk"><img src="https://img.shields.io/badge/platform-socaity.ai-0A86BF" alt="socaity.ai" /></a>
</p>

<p align="center">
  <b>socaity SDK</b> ships the full <a href="https://www.socaity.ai">socaity.ai</a> model catalog ready to import.<br/>
  One line to install. One import to call. Hosted in the EU, or on your own hardware.
</p>

<p align="center">
  <a href="#quickstart">Quickstart</a> ·
  <a href="#why-socaity-sdk">Why this</a> ·
  <a href="#key-features">Features</a> ·
  <a href="#compose-models">Compose models</a> ·
  <a href="#langchain">LangChain</a> ·
  <a href="#mcp">MCP</a> ·
  <a href="#model-zoo">Model zoo</a> ·
  <a href="#ecosystem">Ecosystem</a>
</p>

---

## Quickstart

Two steps. Under five minutes. You get any LLM running or an audio file on disk.

```python
import os
from socaity import speechcraft

client = speechcraft()
job = client.text2voice(text="Welcome to generative AI", voice="hermine")
job.get_result().save("welcome.mp3")
```

That is the whole pattern: **import a model, call it like a function, save the result.**

Need a specific model from the community catalog?

```bash
socaity -i black-forest-labs/flux-schnell
# or
python -m socaity install speechcraft
```

Official models sync on install. Community and third-party models install on demand.

Authentication. We support CLI Login, but for production environment we recommend to set the API key as environment variable.
```bash
pip install socaity
export SOCAITY_API_KEY=sk-...   # free key at socaity.ai
```

---

## Why socaity SDK

Real applications chain models: LLM → image → speech → video. Raw HTTP, per-provider SDKs, and hand-rolled polling make that slow and brittle.

| | Raw HTTP | Per-provider SDKs | socaity SDK |
|---|---|---|---|
| Call pattern | Write requests yourself | One SDK per provider | `from socaity import model` |
| Long-running jobs | Build your own poll loop | Varies | Built-in via [fastSDK](https://github.com/SocAIty/fastsdk) |
| Media I/O | Manual upload/download | Partial | [media-toolkit](https://github.com/SocAIty/media-toolkit) handles files |
| Multi-model apps | Glue code everywhere | Fragmented imports | One package, parallel jobs |
| Hosting | Your problem | Mostly US clouds | [socaity.ai](https://www.socaity.ai) (EU) or bring your own |
| Compliance | Your problem | Rarely GDPR-ready | GDPR and EU AI Act aligned by design |

**Why not just use fastSDK?** You can. fastSDK connects to any OpenAPI, APIPod, RunPod, or Replicate service. socaity SDK adds the curated model zoo, selective install, and auto-sync from the socaity.ai catalog so you skip spec hunting and stub generation for every model.

**Why not OpenRouter or Replicate alone?** Both are pay-per-call model catalogs. Neither gives you deployment, workflow orchestration, or EU-sovereign hosting. socaity combines MaaS, deployment, and agentic workflows in one stack. The SDK is your entry point to all of it.

---

## Key features

**Import and call.** Models are Python classes with typed methods. No GPU setup, no REST boilerplate.

**Parallel by default.** Every call returns a job immediately. Run ten models at once, collect results when you need them.

```python
llm_job = deepseek_v3(prompt="Write a haiku about SDKs.")
img_job = flux_schnell(prompt="A robot at sunset in the Alps.")
# ... do other work ...
text, images = llm_job.get_result(), img_job.get_result()
```

**Selective install.** Official models ship with the package. Install only what your app needs via CLI or `socaity.install("model_id")`.

**Switch models without rewriting.** Want to try another model? No need to rewrite your code-base just switch the call. Having a local model? Point at it at use it likewise from the same sdk.

**EU-first platform.** Socaity runs on European infrastructure (Scaleway PAR-1), Models run where you choose. Data stays in the EU. Workflows are traceable. Pricing is predictable.

---

## Compose models

No single model covers a real task. The SDK is built for composition.

```python
import os
from socaity import speechcraft
from socaity.sdk.replicate.deepseek_ai import deepseek_v3
from socaity.sdk.replicate.black_forest_labs import flux_schnell

poem = deepseek_v3()(
    prompt="Three sentences on why an SDK beats raw HTTP."
).get_result()

speechcraft().text2voice(text="".join(poem), voice="hermine").get_result().save("poem.mp3")

flux_schnell()(
    prompt="A robot at sunset in the Alps, cinematic anime, 4k.",
    num_outputs=1,
).get_result()[0].save("poem.png")
```

https://github.com/user-attachments/assets/978ee377-3ceb-4a87-add5-daee15306231

### Jobs vs. results

Calls return a **job** handle, not a blocked connection. Poll when ready, cancel when not, run hundreds in parallel.

```python
job = deepseek_v3("What a time to be alive.")
# ... other work ...
result = job.get_result()
```

**Price estimate.** Before you submit, ask for predicted cost and runtime (Socaity-hosted services):

```python
client = socaity.connect("black-forest-labs-flux-schnell")
estimate = client.estimate("/predictions", prompt="a lighthouse at sunset")
print(estimate.estimated_price_eur, estimate.estimated_inference_time_s)
```

**Streaming.** Schema endpoints (chat, TTS, video) accept `stream=True`. Iterate live tokens or bytes, or let `get_result()` assemble the full payload when you skip streaming.

```python
job = deepseek_v3()(messages=[{"role": "user", "content": "Hello"}], stream=True)
for chunk in job.stream():
    print(chunk, end="", flush=True)
```

Under the hood, [fastSDK](https://github.com/SocAIty/fastsdk) orchestrates requests through [meseex](https://github.com/SocAIty/meseex), a lightweight job runtime for async I/O, parallel execution, and streaming.

---

## LangChain

You already build agents with LangChain or LangGraph. `ChatSocaity` is a LangChain chat model that talks to any Socaity or APIPod chat service: a hosted model slug, a catalog service id, or a local URL while you develop.

Install LangChain separately (`pip install langchain-core`). The socaity package does not pull it in.

```python
from langchain.agents import create_agent
from socaity.integrations.langchain import ChatSocaity

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model=ChatSocaity(model="Qwen3.6-27B-FP8"),
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke({"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]})
print(result["messages"][-1].content_blocks)
```

You can immediately use the model for chatting

```python
from langchain_core.messages import HumanMessage
from socaity.integrations.langchain import ChatSocaity

model = ChatSocaity(model="socaity-model-slug")  # Go to the MaaS catalog to find your service.

answer = model.invoke([HumanMessage("Summarize why an SDK beats raw HTTP in one sentence.")])
print(answer.text)
```

Stream token by token, bind tools, or force a specific function with `tool_choice`. Conversation history, tool round trips, reasoning blocks, and usage metadata work the same way as with other LangChain chat models. For LangGraph and checkpointers you change nothing on the model side: persist graph state outside the model as you already do.

```python
for chunk in model.stream([HumanMessage("What color is the sky?")]):
    print(chunk.text, end="", flush=True)

def get_weather(location: str) -> str:
    """Current weather for a city."""
    return "sunny"

bound = model.bind_tools([get_weather])
ai = bound.invoke([HumanMessage("Weather in Boston?")])
```

Hosted service on socaity.ai, or your own APIPod instance on localhost: same API. See `test/test_langchain_chat.py` for the full matrix (plain, serverless, tools, streaming).

---

## MCP

Claude Code and similar hosts can drive the platform through a FastMCP server: search services/models, list jobs/chats/projects, run any endpoint with `service@/endpoint`, then download result files on demand.

```bash
pip install 'socaity[mcp]'
# Auth: socaity login   or   export SOCAITY_API_KEY=sk_...
socaity-mcp
# equivalent: python -m socaity.integrations.mcp
```

Agent call shape:

```text
run_service(
  call="bytedance/sdxl-lightning-4step@/predict",
  args={"prompt": "a cute robot dog"},
)
get_files(url="<result url>", save_path="./robot-dog.png")
```

Job tools return file URLs, not downloaded bytes (set by `FASTSDK_MATERIALIZE_MEDIA=0`). Rate limit defaults to 60 tool calls/min (`SOCAITY_MCP_RPM`).

---

## Real-world use

**Game developers** building AI NPCs: generate dialogue with an LLM, synthesize speech, clone a voice, drive facial animation. Four models, one Python script.

**Content creators** automating video pipelines: generate a thumbnail with text-to-image, swap faces in footage, add a voice-over with text-to-speech.

**SMEs** replacing agency workflows: marketing copy, product images, and localized audio from one codebase, without a dedicated ML team.

More patterns on our [docs](https://docs.socaity.ai?utm_source=github&utm_content=socaity-sdk) or on [socaity.ai](https://www.socaity.ai?utm_source=github&utm_content=socaity-sdk).

---

## Model zoo

The catalog lives at [socaity.ai](https://www.socaity.ai/APIs/Overview?utm_source=github&utm_content=socaity-sdk). Install any listed model into your local SDK:

```bash
socaity -i model_name_or_id
```

Representative domains available today:

| Domain | Examples |
|---|---|
| Text |  Qwen, DeepSeek, LLama, GLM |
| Image | Flux Schnell, SAM 2, Photomaker |
| Audio | [SpeechCraft](https://github.com/SocAIty/SpeechCraft) (TTS, voice cloning, voice conversion) |
| Video | Hunyuan Video and growing |

New models land frequently. The SDK syncs official services on install and checks for updates every 15 minutes.

Browse the full list, pricing, and API keys at [socaity.ai](https://www.socaity.ai?utm_source=github&utm_content=socaity-sdk).

---

## Authentication

Set your API key as an environment variable. This keeps secrets out of source control.

```bash
export SOCAITY_API_KEY=sk-...
```

You can pass `api_key=` directly in code for local experiments, but do not commit it.

```python
from socaity import face2face
client = face2face(api_key=os.getenv("SOCAITY_API_KEY"))
```

---

## Hosted, local, or hybrid

| Mode | What it means | Best when |
|---|---|---|
| **Hosted** | Models on socaity.ai | Fastest path, no GPU, always current |
| **Local** | APIPod or fastSDK-compatible service on your machine | Full control, offline, custom models |
| **Hybrid** | Mix socaity.ai with RunPod, Replicate, or self-hosted | Scale bursts, keep sensitive data local |

Any [fastSDK](https://github.com/SocAIty/fastsdk)-compatible service (OpenAPI, [APIPod](https://github.com/SocAIty/APIPod), RunPod, Replicate) works with this package. Override the service address in the registry when you need a custom backend.

Publish an APIPod service to socaity.ai and it appears in the catalog. Public services can earn platform credits.

---

## Ecosystem

Three packages, one pipeline:

| Package | Role |
|---|---|
| **[APIPod](https://github.com/SocAIty/APIPod)** | Build and deploy AI services (server side) |
| **[fastSDK](https://github.com/SocAIty/fastsdk)** | Connect to any compatible API (client runtime, streaming, jobs) |
| **[socaity-schemas](https://github.com/SocAIty/socaity-schemas)** | Shared Pydantic models for AI payloads and service definitions |
| **socaity SDK** (this repo) | Curated model zoo + generated clients for socaity.ai |

Build a service with APIPod. Consume it with fastSDK. Import it from socaity when it is in the catalog.

<img src="https://github.com/SocAIty/APIPod/blob/main/docs/fastsdk_to_apipod.png?raw=true" width="50%" alt="fastSDK and APIPod" />

[socaity.ai](https://www.socaity.ai) ties deployment, MaaS, and agentic workflows (SPAINE) into one EU-sovereign platform. The SDK is how developers access the model layer today.

---

## Documentation

| Resource | What you get |
|---|---|
| [socaity.ai](https://www.socaity.ai) | Model catalog, pricing, API keys, deployment |
| [fastSDK README](https://github.com/SocAIty/fastsdk) | Generic client: connect, generate stubs, CLI |
| [APIPod README](https://github.com/SocAIty/APIPod) | Build and deploy your own AI services |
| [docs/UseCases.md](docs/UseCases.md) | Composition patterns by domain |
| [TECHNICAL_README.md](TECHNICAL_README.md) | Architecture: catalog sync, namespaces, streaming, schemas |

Deep architecture docs for fastSDK and APIPod live in each repo's `TECHNICAL_README.md`. The README here stays focused on getting you to a first result.

---

## Status

**Alpha.** Syntax and APIs will change. Pin your version in production. We ship fast because the catalog and capabilities grows fast.

---

## Contribute

Issues and pull requests welcome. 

```bash
git clone https://github.com/SocAIty/socaity.git
cd socaity
pip install -e ".[dev]"
pytest
```

---

## License

GPL-3.0. See [LICENSE.txt](LICENSE.txt).

---

<p align="center">
  Made with ❤️ by <a href="https://www.socaity.ai?utm_source=github&utm_content=socaity-sdk-08-30-06-2026">SocAIty</a>
</p>