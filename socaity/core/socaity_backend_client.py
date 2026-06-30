import os
from typing import Dict, List, Optional

import httpx

from socaity.core.credentials import DEFAULT_BACKEND_URL, get_api_key


class SocaityBackendClient:
    def __init__(self):
        default_backend = DEFAULT_BACKEND_URL.rstrip("/") + "/"
        self.backend_url = os.getenv("SOCAITY_BACKEND_URL", default_backend)
        self.api_key = get_api_key() or os.getenv("SOCAITY_API_KEY")

    @property
    def _auth_headers(self) -> Optional[Dict]:
        return {"Authorization": f"Bearer {self.api_key}"} if self.api_key else None

    def _post(self, path: str, payload=None, params: Dict = None) -> Optional[any]:
        try:
            with httpx.Client() as client:
                response = client.post(
                    self.backend_url + path,
                    json=payload,
                    params=params,
                    headers=self._auth_headers,
                    timeout=400,
                )
            if response.status_code == 200:
                return response.json()
            print(f"Request to {path} failed with status {response.status_code}")
            return None
        except Exception as e:
            print(f"Request to {path} failed: {e}")
            return None

    def get_service_updates(self, version_index: Dict[str, str]) -> List[Dict]:
        """Check installed services for updates or deletions.

        Sends the current {service_hosting_id: version} map and receives a list of
        PackageUpdateItems for services that are outdated or no longer exist.
        """
        payload = [
            {"service_hosting_id": sid, "version": ver}
            for sid, ver in version_index.items()
        ]
        return self._post("v1/sdk/update_package", payload) or []

    def install_service(self, service_identifier: str) -> Optional[Dict]:
        """Resolve and fetch a service by name, UUID, or 'user/service' identifier."""
        return self._post("v1/sdk/install_service", params={"service": service_identifier})
