"""Register agent tools on a FastMCP server with optional Session bind."""

from __future__ import annotations

import functools
from typing import Callable, Iterable, Optional


def to_fastmcp(mcp, functions: Iterable[Callable], session: Optional[Callable] = None) -> None:
    """Register tool callables on ``mcp``. Wraps each with ``session()`` when given."""
    from fastmcp.exceptions import ToolError

    for fn in functions:

        def make_wrapper(tool_fn: Callable) -> Callable:
            @functools.wraps(tool_fn)
            def wrapper(*args, **kwargs):
                try:
                    if session is not None:
                        with session():
                            return tool_fn(*args, **kwargs)
                    return tool_fn(*args, **kwargs)
                except (ValueError, RuntimeError) as error:
                    raise ToolError(str(error)) from error

            return wrapper

        mcp.tool(make_wrapper(fn))
