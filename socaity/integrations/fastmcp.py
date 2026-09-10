"""Register eligible SDK methods on a FastMCP server."""
from __future__ import annotations

from typing import Callable, Iterable, Optional


def to_fastmcp(mcp, functions: Iterable[Callable], session: Optional[Callable] = None) -> None:
    """Register tool callables on ``mcp`` from canonical ``SocaityClient`` methods."""
    from fastmcp.exceptions import ToolError
    from socaity_cli.errors import BackendApiError, BackendTransportError

    from socaity.integrations.binder import bind_method

    for method in functions:
        _, invoke_async, metadata = bind_method(method, session)

        def make_wrapper(bound_async: Callable) -> Callable:
            async def wrapper(**arguments):
                try:
                    return await bound_async(**arguments)
                except (ValueError, RuntimeError, BackendApiError, BackendTransportError) as error:
                    raise ToolError(str(error)) from error

            wrapper.__name__ = bound_async.__name__
            wrapper.__doc__ = bound_async.__doc__
            wrapper.__module__ = bound_async.__module__
            wrapper.__signature__ = bound_async.__signature__
            wrapper.__annotations__ = bound_async.__annotations__
            return wrapper

        mcp.tool(
            make_wrapper(invoke_async),
            annotations={"destructiveHint": metadata["destructive"]},
        )
