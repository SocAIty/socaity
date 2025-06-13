import httpx
from typing import Dict
import os


class SocaityBackendClient:
    def __init__(self):
        self.infer_backend_url = os.getenv("SOCAITY_INFER_BACKEND_URL", "https://api.socaity.ai/v1/")
        self.api_backend_url = os.getenv("SOCAITY_API_BACKEND_URL", "https://socaity.ai/api/v1/")

    def parse_api_response(self, response: httpx.Response):
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API request failed with status code {response.status_code}")
            return None
        
    def update_package(self, model_id_version: Dict[str, str]) -> Dict:
        """Get comprehensive package update with all necessary information for SDK generation"""
        client = httpx.Client()
        response = client.post(self.api_backend_url + "gen_api_manager/update_package", json=model_id_version, timeout=400)
        return self.parse_api_response(response)
