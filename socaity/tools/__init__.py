"""Agent tools over the socaity SDK. Assembly is in ``registry``; execution in ``run``."""

from socaity.tools.json import dump_entity, page
from socaity.tools.mcp import to_fastmcp
from socaity.tools.registry import (
    JOB_DETAIL_EXPAND,
    REGISTRY,
    SERVICE_DETAIL_EXPAND,
    TOOLS,
)
from socaity.tools.agents import run_agent
from socaity.tools.jobs import cancel_job_run, interrupt_job, wait_for_job
from socaity.tools.run import estimate_price, run_service
from socaity.tools.workflows import run_workflow

__all__ = [
    "REGISTRY",
    "TOOLS",
    "SERVICE_DETAIL_EXPAND",
    "JOB_DETAIL_EXPAND",
    "dump_entity",
    "page",
    "run_service",
    "estimate_price",
    "run_agent",
    "cancel_job_run",
    "interrupt_job",
    "wait_for_job",
    "run_workflow",
    "to_fastmcp",
]
