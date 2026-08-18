"""ChatSocaity: LangChain chat model backed by a Socaity platform service.

Translates between LangChain messages and the OpenAI-compatible wire format
of ``socaity_schemas``; the platform protocol (connect, jobs, SSE) lives in
:class:`socaity.integrations.ChatServiceAdapter`.

Supported: full conversation history, sync/async streaming (text, reasoning
and tool-call deltas as standard v1 content blocks), ``bind_tools`` (and with
it ``with_structured_output``), usage metadata and job introspection via
``.jobs`` / ``.job_status()``. Memory/checkpointers need nothing from the
model: LangGraph persists graph state outside of it.
"""
from __future__ import annotations

import json
from typing import Any, AsyncIterator, Dict, Iterator, List, Mapping, Optional

from langchain_core.callbacks import AsyncCallbackManagerForLLMRun, CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, AIMessageChunk, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.messages.ai import UsageMetadata
from langchain_core.messages.tool import tool_call_chunk
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
from langchain_core.utils.function_calling import convert_to_openai_tool
from pydantic import Field, PrivateAttr

from socaity.integrations.chat_adapter import ChatServiceAdapter


class ChatSocaity(BaseChatModel):
    """Chat model backed by a Socaity platform service.

    Args:
        model: Service slug, id or direct URL (resolved via the catalog).
        api_key: Socaity API key; falls back to the stored login.
        endpoint_path: Chat endpoint override (default: auto-resolved).
        temperature / max_tokens / top_p / seed: Default sampling parameters,
            overridable per call via ``.bind(...)`` or invoke kwargs.
    """

    model: str
    api_key: Optional[str] = None
    endpoint_path: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    top_p: Optional[float] = None
    seed: Optional[int] = None
    output_version: str = "v1"  # store standard content blocks in .content

    _adapter: Optional[ChatServiceAdapter] = PrivateAttr(default=None)

    # ------------------------------------------------------------------
    # LangChain identity
    # ------------------------------------------------------------------

    @property
    def _llm_type(self) -> str:
        return "socaity"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {
            "model_name": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "seed": self.seed,
        }

    # ------------------------------------------------------------------
    # Platform access
    # ------------------------------------------------------------------

    @property
    def adapter(self) -> ChatServiceAdapter:
        """The underlying platform adapter (connects lazily on first call)."""
        if self._adapter is None:
            self._adapter = ChatServiceAdapter(self.model, api_key=self.api_key, endpoint_path=self.endpoint_path)
        return self._adapter

    @property
    def jobs(self):
        """APISeex handles of every job this model submitted."""
        return self.adapter.jobs

    def job_status(self, job=None) -> Dict[str, Any]:
        """Status snapshot of a submitted job (default: the most recent one)."""
        job = job or self.adapter.last_job()
        if job is None:
            raise ValueError("No jobs have been submitted yet.")
        return ChatServiceAdapter.job_status(job)

    # ------------------------------------------------------------------
    # Tools
    # ------------------------------------------------------------------

    def bind_tools(self, tools, *, tool_choice=None, **kwargs):
        formatted = [convert_to_openai_tool(tool) for tool in tools]
        if tool_choice:
            if tool_choice == "any":
                tool_choice = "required"
            if isinstance(tool_choice, str) and tool_choice not in ("auto", "none", "required"):
                tool_choice = {"type": "function", "function": {"name": tool_choice}}
            kwargs["tool_choice"] = tool_choice
        return super().bind(tools=formatted, **kwargs)

    # ------------------------------------------------------------------
    # Request building (LangChain -> wire)
    # ------------------------------------------------------------------

    def _request(self, messages: List[BaseMessage], stop: Optional[List[str]], **kwargs: Any) -> Dict[str, Any]:
        request: Dict[str, Any] = {"messages": [_wire_message(message) for message in messages]}
        defaults = {
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "seed": self.seed,
            "stop": stop,
        }
        request.update({key: value for key, value in defaults.items() if value is not None})
        kwargs.pop("ls_structured_output_format", None)  # tracing-only kwarg from with_structured_output
        request.update({key: value for key, value in kwargs.items() if value is not None})
        # Test/prod vLLM for Qwen3.8 rejects OpenAI tool fields (HTTP 400).
        # Emulate tool calling in the prompt; create_agent still sees tool_calls.
        tools = request.pop("tools", None)
        for key in ("tool_choice", "parallel_tool_calls", "functions", "function_call"):
            request.pop(key, None)
        if tools:
            request["messages"] = _emulate_tool_messages(request["messages"], tools)
            request["_emulated_tools"] = True
        allowed = {
            "messages", "model", "temperature", "max_tokens", "max_completion_tokens",
            "top_p", "n", "stream", "stop", "seed", "presence_penalty", "frequency_penalty",
            "reasoning_effort", "_emulated_tools",
        }
        return {key: value for key, value in request.items() if key in allowed}

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        request = self._request(messages, stop, **kwargs)
        emulated = request.pop("_emulated_tools", False)
        request["messages"] = _coerce_message_content(request["messages"])
        response = self.adapter.complete(request)
        if emulated:
            response = _promote_emulated_tool_calls(response)
        choice = response["choices"][0]
        message = self._ai_message(choice, response.get("usage"))
        return ChatResult(generations=[ChatGeneration(
            message=message, generation_info={"finish_reason": choice.get("finish_reason")},
        )])

    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        request = self._request(messages, stop, **kwargs)
        request.pop("_emulated_tools", None)
        translator = _ChunkTranslator(self.model)
        for chunk in self.adapter.stream_chunks(request):
            generation_chunk = translator.translate(chunk)
            if generation_chunk is not None:
                yield generation_chunk

    async def _astream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        request = self._request(messages, stop, **kwargs)
        request.pop("_emulated_tools", None)
        translator = _ChunkTranslator(self.model)
        async for chunk in self.adapter.astream_chunks(request):
            generation_chunk = translator.translate(chunk)
            if generation_chunk is not None:
                yield generation_chunk

    # ------------------------------------------------------------------
    # Response translation (wire -> LangChain)
    # ------------------------------------------------------------------

    def _ai_message(self, choice: Dict[str, Any], usage: Optional[Dict[str, Any]]) -> AIMessage:
        message = choice.get("message") or {}
        blocks: List[dict] = []
        if message.get("reasoning_content"):
            blocks.append({"type": "reasoning", "reasoning": message["reasoning_content"]})
        text = _content_text(message.get("content"))
        if text:
            blocks.append({"type": "text", "text": text})

        tool_calls, invalid_tool_calls = [], []
        for call in message.get("tool_calls") or []:
            function = call.get("function") or {}
            raw_args = function.get("arguments") or "{}"
            try:
                args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
                tool_calls.append({"type": "tool_call", "name": function.get("name"), "args": args, "id": call.get("id")})
            except ValueError:
                invalid_tool_calls.append({
                    "type": "invalid_tool_call", "name": function.get("name"),
                    "args": raw_args, "id": call.get("id"), "error": "Malformed JSON arguments",
                })

        return AIMessage(
            content_blocks=blocks,
            tool_calls=tool_calls,
            invalid_tool_calls=invalid_tool_calls,
            usage_metadata=_usage_metadata(usage),
            response_metadata={
                "model_name": self.model,
                "model_provider": "socaity",
                "finish_reason": choice.get("finish_reason"),
            },
        )


class _ChunkTranslator:
    """Stateful ChatCompletionChunk -> ChatGenerationChunk translation.

    Tracks the content block index (blocks sharing an index merge on
    aggregation) and builds the closing ``chunk_position='last'`` chunk from
    the platform's finish chunk.
    """

    def __init__(self, model_name: str):
        self._model_name = model_name
        self._block_index = -1
        self._block_type: Optional[str] = None

    def translate(self, chunk: Dict[str, Any]) -> Optional[ChatGenerationChunk]:
        choices = chunk.get("choices") or []
        if not choices:
            return None
        choice = choices[0]
        delta = choice.get("delta") or {}
        finish_reason = choice.get("finish_reason")

        if delta.get("tool_calls"):
            return self._tool_chunk(delta["tool_calls"])
        if delta.get("reasoning_content"):
            return self._content_chunk("reasoning", {"reasoning": delta["reasoning_content"]})
        if delta.get("content"):
            return self._content_chunk("text", {"text": delta["content"]})
        if finish_reason:
            return self._final_chunk(finish_reason, chunk.get("usage"))
        return None

    def _next_index(self, block_type: str) -> int:
        if block_type != self._block_type:
            self._block_index += 1
            self._block_type = block_type
        return self._block_index

    def _content_chunk(self, block_type: str, payload: dict) -> ChatGenerationChunk:
        block = {"type": block_type, "index": self._next_index(block_type), **payload}
        return ChatGenerationChunk(message=AIMessageChunk(content=[block]))

    def _tool_chunk(self, tool_calls: List[dict]) -> ChatGenerationChunk:
        self._block_type = "tool_call"  # next text/reasoning block gets a fresh index
        chunks = []
        for call in tool_calls:
            function = call.get("function") or {}
            chunks.append(tool_call_chunk(
                name=function.get("name"),
                args=function.get("arguments"),
                id=call.get("id"),
                index=call.get("index"),
            ))
        return ChatGenerationChunk(message=AIMessageChunk(content=[], tool_call_chunks=chunks))

    def _final_chunk(self, finish_reason: str, usage: Optional[dict]) -> ChatGenerationChunk:
        message = AIMessageChunk(
            content=[],
            chunk_position="last",
            usage_metadata=_usage_metadata(usage),
            response_metadata={
                "model_name": self._model_name,
                "model_provider": "socaity",
                "finish_reason": finish_reason,
            },
        )
        return ChatGenerationChunk(message=message, generation_info={"finish_reason": finish_reason})


# ---------------------------------------------------------------------------
# Message translation helpers
# ---------------------------------------------------------------------------


def _usage_metadata(usage: Optional[Dict[str, Any]]) -> Optional[UsageMetadata]:
    if not usage:
        return None
    return UsageMetadata(
        input_tokens=usage.get("prompt_tokens") or 0,
        output_tokens=usage.get("completion_tokens") or 0,
        total_tokens=usage.get("total_tokens") or 0,
    )


def _wire_message(message: BaseMessage) -> Dict[str, Any]:
    """One LangChain message -> OpenAI-compatible wire dict."""
    if isinstance(message, SystemMessage):
        return {"role": "system", "content": message.text}
    if isinstance(message, HumanMessage):
        return {"role": "user", "content": _wire_content(message.content)}
    if isinstance(message, ToolMessage):
        return {"role": "tool", "content": message.text, "tool_call_id": message.tool_call_id}
    if isinstance(message, AIMessage):
        wire: Dict[str, Any] = {"role": "assistant", "content": message.text or None}
        if message.tool_calls:
            wire["tool_calls"] = [
                {
                    "id": call.get("id"),
                    "type": "function",
                    "function": {"name": call["name"], "arguments": json.dumps(call["args"], ensure_ascii=False)},
                }
                for call in message.tool_calls
            ]
        return wire
    raise ValueError(f"Unsupported message type for Socaity chat: {type(message).__name__}")


def _wire_content(content) -> Any:
    """LangChain content (str or block list) -> string or OpenAI content parts."""
    if isinstance(content, str):
        return content
    parts = []
    for block in content:
        if isinstance(block, str):
            parts.append({"type": "text", "text": block})
        elif block.get("type") == "text":
            parts.append({"type": "text", "text": block.get("text", "")})
        elif block.get("type") in ("image", "image_url"):
            parts.append({"type": "image_url", "image_url": {"url": _image_url(block)}})
        # other block types (reasoning etc.) are not user-input content; skip
    return parts


_TOOL_PROMPT = (
    "You can use tools. To call one, reply with ONLY a JSON object and no other text:\n"
    '{{"name": "<tool_name>", "arguments": {{<args>}}}}\n'
    "When you do not need a tool, reply in plain language.\n"
    "Available tools:\n{specs}"
)


def _coerce_message_content(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Force string content and drop keys the test vLLM 400s on."""
    coerced = []
    for message in messages:
        role = message.get("role") or "user"
        text = _content_text(message.get("content"))
        if not text and role == "assistant":
            text = ""
        coerced.append({"role": role, "content": text})
    return coerced


def _emulate_tool_messages(messages: List[Dict[str, Any]], tools: List[dict]) -> List[Dict[str, Any]]:
    """Rewrite native tool turns into text so vLLM never sees `tools` or `role=tool`."""
    specs = []
    for tool in tools:
        function = tool.get("function") or tool
        params = (function.get("parameters") or {}).get("properties") or {}
        required = (function.get("parameters") or {}).get("required") or []
        desc = (function.get("description") or "").split("\n", 1)[0]
        specs.append(f"- {function.get('name')}({', '.join(required)}): {desc}")
        if params:
            specs.append(f"  args: {', '.join(params)}")
    instruction = {"role": "system", "content": _TOOL_PROMPT.format(specs="\n".join(specs))}
    rewritten: List[Dict[str, Any]] = []
    for message in messages:
        role = message.get("role")
        if role == "tool":
            result = _content_text(message.get("content"))
            if len(result) > 2000:
                result = result[:2000] + "..."
            rewritten.append({
                "role": "user",
                "content": f"Tool result ({message.get('tool_call_id') or 'tool'}):\n{result}",
            })
            continue
        if role == "assistant" and message.get("tool_calls"):
            calls = []
            for call in message["tool_calls"]:
                function = call.get("function") or {}
                calls.append(f"{function.get('name')}({function.get('arguments')})")
            text = message.get("content") or ""
            rewritten.append({
                "role": "assistant",
                "content": ((text + "\n") if text else "") + "Called: " + "; ".join(calls),
            })
            continue
        rewritten.append(message)
    if rewritten and rewritten[0].get("role") == "system":
        rewritten[0] = {
            "role": "system",
            "content": (rewritten[0].get("content") or "") + "\n\n" + instruction["content"],
        }
        return rewritten
    return [instruction, *rewritten]


def _promote_emulated_tool_calls(response: Dict[str, Any]) -> Dict[str, Any]:
    """If the assistant text is a tool-call JSON, lift it onto ``message.tool_calls``."""
    choices = response.get("choices") or []
    if not choices:
        return response
    message = dict(choices[0].get("message") or {})
    calls = _parse_emulated_tool_calls(_content_text(message.get("content")))
    if not calls:
        return response
    message["tool_calls"] = calls
    message["content"] = None
    choices[0] = {**choices[0], "message": message, "finish_reason": "tool_calls"}
    return {**response, "choices": choices}


def _content_text(content: Any) -> str:
    """Flatten OpenAI content (string or typed parts) to plain text."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                parts.append(block.get("text") or block.get("content") or "")
        return "".join(parts)
    if isinstance(content, dict):
        return content.get("text") or content.get("content") or json.dumps(content, ensure_ascii=False)
    return str(content)


def _parse_emulated_tool_calls(text: str) -> List[dict]:
    """Read a JSON tool call from model text. Empty when the reply is prose."""
    payload = _first_json_value(text)
    if payload is None:
        return []
    items = payload if isinstance(payload, list) else [payload]
    calls = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            return []
        name = item.get("name") or (item.get("function") or {}).get("name")
        arguments = item.get("arguments")
        if arguments is None and isinstance(item.get("function"), dict):
            arguments = item["function"].get("arguments")
        if not name or arguments is None:
            return []
        if not isinstance(arguments, str):
            arguments = json.dumps(arguments, ensure_ascii=False)
        calls.append({
            "id": item.get("id") or f"call_{index}",
            "type": "function",
            "function": {"name": name, "arguments": arguments},
        })
    return calls


def _first_json_value(text: str) -> Any:
    stripped = (text or "").strip()
    if not stripped:
        return None
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        if stripped.lower().startswith("json"):
            stripped = stripped[4:].strip()
    try:
        return json.loads(stripped)
    except ValueError:
        pass
    start = stripped.find("{")
    if start < 0:
        return None
    depth = 0
    for index, char in enumerate(stripped[start:], start):
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(stripped[start : index + 1])
                except ValueError:
                    return None
    return None


def _image_url(block: dict) -> str:
    """Standard v1 image block or legacy image_url block -> URL / data URI."""
    if block.get("type") == "image_url":
        image_url = block.get("image_url")
        return image_url.get("url", "") if isinstance(image_url, dict) else str(image_url)
    if block.get("url"):
        return block["url"]
    if block.get("base64"):
        mime = block.get("mime_type", "image/png")
        return f"data:{mime};base64,{block['base64']}"
    raise ValueError("Image block needs a 'url' or 'base64' value.")
