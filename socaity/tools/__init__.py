"""Agent tools over the socaity SDK. Assembly is in ``registry``; execution in ``run``."""

from socaity.tools.json import dump_entity, page
from socaity.tools.mcp import to_fastmcp
from socaity.tools.registry import (
    JOB_DETAIL_EXPAND,
    REGISTRY,
    SERVICE_DETAIL_EXPAND,
    TOOLS,
)
from socaity.tools.agents import execute_agent, run_agent
from socaity.tools.jobs import cancel_job_run
from socaity.tools.run import estimate_price, execute_service, run_service
from socaity.tools.workflows import execute_workflow, run_workflow

__all__ = [
    "REGISTRY",
    "TOOLS",
    "SERVICE_DETAIL_EXPAND",
    "JOB_DETAIL_EXPAND",
    "dump_entity",
    "page",
    "run_service",
    "execute_service",
    "estimate_price",
    "execute_agent",
    "run_agent",
    "cancel_job_run",
    "execute_workflow",
    "run_workflow",
    "to_fastmcp",
]
