"""Dense agent instructions for using the Socaity MCP effectively."""

AGENT_PLAYBOOK = """
# Socaity MCP playbook

You are connected to the Socaity MaaS platform. Prefer tools over guessing.

## Auth
1. Call `whoami`. If it fails, call `login` (opens browser; stores a temporary tk_ key).
2. Production hosts may set `SOCAITY_API_KEY` instead of login.

## Discovery (search is keyword / fuzzy, NOT intent-compose)
Use `search_services` / `search_models` with short concrete terms.
Examples:
- text to image: q="sdxl" or q="flux" or q="text2image"
- speech: q="tts" or q="speechcraft"
- chat LLM: q="qwen" or q="llm"
Optional filters use backend grammar: field:op:value
  filter=["categories:contains:image", "is_official:eq:true"]
Sort preference when ranking: higher `n_usages`, official services, matching display_name.

Do NOT invent service names. Always search or list first, then `get_service`.

## Run any service (agent-first call syntax)
`run_service(call="service@/endpoint", args={...}, wait=true)`

Rules:
- `service` = catalog `name` or id (may contain `/`, e.g. bytedance/sdxl-lightning-4step)
- `@` separates service from endpoint path
- endpoint usually matches OpenAPI path (`/predict`, `/chat`, …); leading `/` optional
- `args` is a JSON object of endpoint parameters (see `get_service` endpoints schema)

Example image generation:
1. search_services(q="sdxl lightning")
2. get_service(id_or_name="bytedance/sdxl-lightning-4step")
3. run_service(
     call="bytedance/sdxl-lightning-4step@/predict",
     args={"prompt": "a cute robot dog"},
     wait=true
   )
4. From the job result, take file `url` fields. Call get_files to download.

## Multi-step media workflows (compose yourself)
Socaity does not auto-compose pipelines. Typical video path:
1. text2image → starting frame URL
2. image-edit / keyframes (optional)
3. image2video with those frames
Search each stage separately; pass prior `url` values as next-stage inputs.

## Files
Job results return URLs (not downloaded bytes). Use `get_files(url=..., save_path=...)`
to fetch. Mini download example outside MCP:
  curl -L -o out.png "https://..."

## Chats / jobs / projects
- list_chats / get_chat for conversation history
- list_jobs / get_job for execution records
- list_projects for workspace grouping
""".strip()
