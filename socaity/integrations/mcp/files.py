"""Fetch job/result files by URL or job id without pulling them through run_service."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import httpx

from socaity.core.jobs import get_job
from socaity.integrations.mcp.auth import ensure_api_key
from socaity.integrations.mcp.serialize import to_jsonable

_URL_RE = re.compile(r"^https?://", re.I)


def get_files(
    *,
    job_id: Optional[str] = None,
    url: Optional[str] = None,
    file_id: Optional[int] = None,
    save_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Resolve file metadata and optionally download bytes to ``save_path``.

    Prefer ``url`` from a prior job result. ``job_id`` lists attached files.
    ``file_id`` selects one entry from that job's ``files`` list.
    """
    ensure_api_key()
    if not job_id and not url:
        raise ValueError("Provide job_id and/or url.")

    files: List[Dict[str, Any]] = []
    if job_id:
        job = get_job(job_id, expand=["files", "data"])
        if job is None:
            raise ValueError(f"Job not found: {job_id}")
        for f in job.files or []:
            files.append(to_jsonable(f))
        # Also surface URL-shaped values nested in output_data.
        files.extend(_urls_from_value(getattr(getattr(job, "data", None), "output_data", None)))

    if file_id is not None:
        files = [f for f in files if f.get("id") == file_id]
        if not files and url is None:
            raise ValueError(f"file_id={file_id} not found on job {job_id}")

    target_url = url
    if target_url is None and files:
        target_url = files[0].get("url")

    downloaded = None
    if save_path and target_url:
        if not _URL_RE.match(target_url):
            raise ValueError("save_path requires an http(s) url")
        downloaded = _download(target_url, save_path)

    return {
        "job_id": job_id,
        "files": files,
        "url": target_url,
        "downloaded": downloaded,
        "hint": "curl -L -o out.bin \"<url>\"",
    }


def _download(url: str, save_path: str) -> Dict[str, Any]:
    path = Path(save_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    with httpx.stream("GET", url, follow_redirects=True, timeout=120.0) as response:
        response.raise_for_status()
        size = 0
        with path.open("wb") as out:
            for chunk in response.iter_bytes():
                out.write(chunk)
                size += len(chunk)
    return {"path": str(path), "bytes": size, "url": url}


def _urls_from_value(value: Any) -> List[Dict[str, Any]]:
    found: List[Dict[str, Any]] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            content = node.get("content") or node.get("url")
            if isinstance(content, str) and _URL_RE.match(content):
                found.append({
                    "url": content,
                    "content_type": node.get("content_type"),
                    "file_name": node.get("file_name") or Path(urlparse(content).path).name,
                })
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, str) and _URL_RE.match(node):
            found.append({"url": node, "file_name": Path(urlparse(node).path).name})

    walk(value)
    return found
