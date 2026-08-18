"""Category id/name mapping.

Services carry category ids, and the catalog never fills the slug field, so a raw
service listing shows an agent nothing but UUIDs. The category list is small and
near static, so both directions of the mapping are built once per process.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Dict, Iterable, List, Optional

from socaity.core.catalog import list_categories


@lru_cache(maxsize=1)
def index() -> Dict[str, str]:
    """Category id to display name. Reads the public catalog on first use."""
    return {category.id: category.display_name for category in list_categories() if category.id}


def names(ids: Optional[Iterable[str]]) -> List[str]:
    """Display names for category ids, keeping unknown ids as they are."""
    mapping = index()
    return [mapping.get(category_id, category_id) for category_id in ids or []]


def resolve(term: Optional[str]) -> Optional[str]:
    """Turn a category id or display name into the id the catalog filters on."""
    if not term:
        return None
    mapping = index()
    if term in mapping:
        return term
    wanted = term.strip().lower()
    return next(
        (category_id for category_id, display in mapping.items() if (display or "").lower() == wanted),
        term,
    )
