"""Public jobs helpers of the socaity SDK.

Thin layer over ``GET /v1/jobs`` (list/search/get) and the finished-job webhook
used to refresh the jobs catalog index after inference completes.
"""
from typing import List, Optional

from socaity_schemas.platform import Job

from socaity.core.catalog import _backend


def list_jobs(
    q: Optional[str] = None,
    filters: Optional[List[str]] = None,
    expand: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
    visibility: str = "user_visible",
    sort: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[Job]:
    """List or fuzzy-search jobs visible to the authenticated caller."""
    return _backend().query_jobs(
        q=q,
        filters=filters,
        expand=expand,
        fields=fields,
        visibility=visibility,
        sort=sort,
        limit=limit,
        offset=offset,
    )


def get_job(job_id: str, expand: Optional[List[str]] = None, fields: Optional[List[str]] = None) -> Optional[Job]:
    """Fetch one job by id."""
    return _backend().get_job(job_id, expand=expand, fields=fields)


def refresh_job(job_id: str) -> Optional[dict]:
    """Ask the backend to reload a finished job into cache + Typesense."""
    return _backend().refresh_job(job_id)
