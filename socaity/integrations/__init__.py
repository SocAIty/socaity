"""Framework integrations for the socaity SDK.

``ChatServiceAdapter`` wraps platform chat services (connect, endpoint
resolution, job submission, SSE decoding) behind one framework-neutral
surface. Framework-specific adapters translate message formats only:

- ``socaity.integrations.langchain``: LangChain chat model (``ChatSocaity``).

The platform MCP server lives in the separate ``socaity-mcp`` package
(agent ↔ MCP ↔ backend / inference), not in this SDK.

Framework packages (langchain, ...) are optional dependencies; importing a
specific integration raises a helpful error when its package is missing.
"""

from socaity.integrations.chat_adapter import ChatServiceAdapter

__all__ = ["ChatServiceAdapter"]
