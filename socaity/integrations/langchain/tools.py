"""LangChain tool conversion from canonical ``SocaityClient`` methods."""
from __future__ import annotations

from typing import Callable, Iterable, List, Optional

from langchain_core.tools import BaseTool, StructuredTool

from socaity.integrations.binder import bind_method


def to_langchain(functions: Iterable[Callable], session: Optional[Callable] = None) -> List[BaseTool]:
    """Build LangChain tools from unbound ``SocaityClient`` methods."""
    tools: List[BaseTool] = []
    for method in functions:
        invoke_sync, invoke_async, metadata = bind_method(method, session)
        tools.append(
            StructuredTool.from_function(
                func=invoke_sync,
                coroutine=invoke_async,
                parse_docstring=True,
                error_on_invalid_docstring=False,
                metadata=metadata,
            )
        )
    return tools
