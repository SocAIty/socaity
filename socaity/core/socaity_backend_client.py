"""HTTP client for the socaity backend: catalog reads, search and SDK installs.

Catalog list calls use sparse fieldsets (``select``) and pagination so the
client only transfers what it renders. Full objects are fetched on demand
(see ``socaity.core.lazy``).
"""
import os
from typing import Any, Dict, List, Optional

import httpx

from socaity_schemas.platform import AIModel, AIService, ServiceCategory

from socaity.core.credentials import DEFAULT_BACKEND_URL, get_api_key

# What list views need; everything else loads lazily.
SERVICE_LIST_SELECT = "id,name,display_name,short_desc,categories,is_official,n_usages"
MODEL_LIST_SELECT = "id,name,display_name,family,release_date,hugging_face_url"


class SocaityBackendClient:
    def __init__(self):
        default_backend = DEFAULT_BACKEND_URL.rstrip("/") + "/"
        self.backend_url = os.getenv("SOCAITY_BACKEND_URL", default_backend)
        self.api_key = get_api_key() or os.getenv("SOCAITY_API_KEY")

    @property
    def _auth_headers(self) -> Optional[Dict]:
        return {"Authorization": f"Bearer {self.api_key}"} if self.api_key else None

    def _request(self, method: str, path: str, payload=None, params: Dict = None) -> Optional[Any]:
        params = {k: v for k, v in (params or {}).items() if v is not None}
        try:
            with httpx.Client() as client:
                response = client.request(
                    method,
                    self.backend_url + path,
                    json=payload,
                    params=params,
                    headers=self._auth_headers,
                    timeout=400,
                )
            if response.status_code == 200:
                return response.json()
            print(f"Request to {path} failed with status {response.status_code}: {response.text[:300]}")
            return None
        except Exception as e:
            print(f"Request to {path} failed: {e}")
            return None

    def _post(self, path: str, payload=None, params: Dict = None) -> Optional[Any]:
        return self._request("POST", path, payload=payload, params=params)

    def _get(self, path: str, params: Dict = None) -> Optional[Any]:
        return self._request("GET", path, params=params)

    # ---- catalog reads ----

    def list_services(
        self,
        category: Optional[str] = None,
        select: Optional[str] = SERVICE_LIST_SELECT,
        include: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[AIService]:
        rows = self._get("v1/catalog/services", params={
            "category": category, "select": select, "include": include,
            "limit": limit, "offset": offset,
        }) or []
        return [AIService(**row) for row in rows]

    def get_service(self, id_or_name: str, include: str = "deployments,endpoints,models") -> Optional[AIService]:
        row = self._get(f"v1/catalog/services/{id_or_name}", params={"include": include})
        return AIService(**row) if row else None

    def list_models(
        self,
        family: Optional[str] = None,
        task: Optional[str] = None,
        select: Optional[str] = MODEL_LIST_SELECT,
        limit: int = 100,
        offset: int = 0,
    ) -> List[AIModel]:
        rows = self._get("v1/catalog/models", params={
            "family": family, "task": task, "select": select,
            "limit": limit, "offset": offset,
        }) or []
        return [AIModel(**row) for row in rows]

    def get_model(self, id_or_name: str) -> Optional[AIModel]:
        row = self._get(f"v1/catalog/models/{id_or_name}")
        return AIModel(**row) if row else None

    def list_categories(self) -> List[ServiceCategory]:
        rows = self._get("v1/catalog/categories") or []
        return [ServiceCategory(**row) for row in rows]

    def search(self, query: str, collections: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """Fuzzy search over services and models; returns raw hits (collection, id, score, document)."""
        result = self._get("v1/catalog/search", params={
            "q": query, "collections": collections, "limit": limit,
        })
        return (result or {}).get("hits", [])

    # ---- SDK install/update ----

    def get_service_updates(self, version_index: Dict[str, str]) -> List[Dict]:
        """Check installed services for updates or deletions.

        Sends the current {deployment_id: specification_hash} map and receives
        PackageUpdateItems for services that are outdated or no longer exist.
        """
        payload = [
            {"deployment_id": deployment_id, "specification_hash": spec_hash or ""}
            for deployment_id, spec_hash in version_index.items()
        ]
        return self._post("v1/sdk/update_package", payload) or []

    def install_service(self, service_identifier: str) -> Optional[Dict]:
        """Resolve and fetch a service by name, UUID, or 'user/service' identifier."""
        return self._post("v1/sdk/install_service", params={"service": service_identifier})
