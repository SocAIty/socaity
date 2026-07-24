"""Run: ``python -m socaity.integrations.mcp`` (stdio) or with FASTMCP transport args."""
from __future__ import annotations

import argparse

from socaity.integrations.mcp.server import mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="Socaity MCP server")
    parser.add_argument(
        "--transport",
        default="stdio",
        choices=["stdio", "http", "sse", "streamable-http"],
        help="MCP transport (default: stdio for Claude Code / Cursor)",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    if args.transport == "stdio":
        mcp.run()
    else:
        mcp.run(transport=args.transport, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
