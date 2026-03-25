import httpx
from typing import Dict, List
import os


class SocaityBackendClient:
    def __init__(self):
        self.backend_url = os.getenv("SOCAITY_BACKEND_URL", "https://webapi.socaity.ai/")
        self.api_key = os.getenv("SOCAITY_API_KEY")

    def parse_api_response(self, response: httpx.Response):
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API request failed with status code {response.status_code}")
            return None
        
    def update_package(self, model_id_version: Dict[str, str], install_ids: List[str] = None) -> Dict:
        """Get comprehensive package update with all necessary information for SDK generation"""
        client = httpx.Client()
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key is not None else None
        
        payload = {
            "current_versions": model_id_version,
            "install_ids": install_ids or []
        }

        try:
            response = client.post(self.backend_url + "v1/sdk/update_package", json=payload, headers=headers, timeout=400)
            return self.parse_api_response(response)
        except Exception as e:
            print(f"Could not update package: {e}")
            return None
        
