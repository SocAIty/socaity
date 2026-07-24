"""Public project helpers of the socaity SDK."""
from typing import List, Optional, Union

from socaity_schemas.platform import Project

from socaity.core.catalog import _backend


def list_projects(
    filters: Optional[List[str]] = None,
    expand: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
    sort: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[Project]:
    """List projects owned by the authenticated caller."""
    return _backend().query_projects(
        filters=filters,
        expand=expand,
        fields=fields,
        sort=sort,
        limit=limit,
        offset=offset,
    )


def get_project(
    project_id: str,
    expand: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
) -> Optional[Project]:
    return _backend().get_project(project_id, expand=expand, fields=fields)


def upsert_project(
    display_name: Optional[str] = None,
    description: Optional[str] = None,
    project_id: Optional[str] = None,
) -> Optional[str]:
    return _backend().upsert_project(
        display_name=display_name,
        description=description,
        project_id=project_id,
    )


def delete_project(project_id: str) -> bool:
    return _backend().delete_project(project_id)


def modify_project_members(
    project_id: str,
    job_ids: Optional[List[str]] = None,
    file_ids: Optional[List[Union[str, int]]] = None,
    add: bool = True,
) -> bool:
    return _backend().modify_members(
        project_id,
        job_ids=job_ids,
        file_ids=file_ids,
        add=add,
    )
