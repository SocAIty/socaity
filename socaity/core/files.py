"""Public files helpers of the socaity SDK.

Thin layer over ``/v1/files`` (list, get, upload, update, delete, usage).
"""
from pathlib import Path
from typing import Dict, List, Optional, Union

from socaity.core.catalog import _backend


def get_storage_usage() -> Optional[Dict]:
    """Return the caller's storage quota and usage."""
    return _backend().get_storage_usage()


def query_files(
    purpose: Union[str, List[str]] = "USER_UPLOAD",
    include_expired: bool = False,
    include_deleted: bool = False,
    is_public: Optional[bool] = None,
    expand: Optional[List[str]] = None,
    limit: int = 25,
    offset: int = 0,
) -> List[Dict]:
    """Query stored files visible to the authenticated caller."""
    return _backend().query_files(
        purpose=purpose,
        include_expired=include_expired,
        include_deleted=include_deleted,
        is_public=is_public,
        expand=expand,
        limit=limit,
        offset=offset,
    )


def get_file(selector: Union[str, int], expand: Optional[List[str]] = None) -> Optional[Dict]:
    """Resolve one file by file id, job id, or storage URL."""
    return _backend().get_file(selector, expand=expand)


def update_file(
    file_id: Union[str, int],
    is_public: Optional[bool] = None,
    expires_at: Optional[str] = None,
    clear_expires_at: bool = False,
) -> Optional[Dict]:
    """Patch file metadata the caller owns."""
    return _backend().update_file(
        file_id,
        is_public=is_public,
        expires_at=expires_at,
        clear_expires_at=clear_expires_at,
    )


def delete_file(file_id: Union[str, int]) -> bool:
    """Hard-delete a file the caller owns."""
    return _backend().delete_file(file_id)


def upload_files(
    files: Union[str, Path, bytes, List[Union[str, Path, bytes]]],
    purpose: str = "USER_UPLOAD",
    is_public: bool = False,
    expires_at: Optional[str] = None,
    job_id: Optional[str] = None,
) -> List[Dict]:
    """Multipart upload of one or more files."""
    return _backend().upload_files(
        files,
        purpose=purpose,
        is_public=is_public,
        expires_at=expires_at,
        job_id=job_id,
    )
