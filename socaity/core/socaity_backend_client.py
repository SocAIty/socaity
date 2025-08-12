import httpx
from typing import Dict
import os


class SocaityBackendClient:
    def __init__(self):
        self.infer_backend_url = os.getenv("SOCAITY_INFER_BACKEND_URL", "https://api.socaity.ai/v1/")
        self.api_key = os.getenv("SOCAITY_API_KEY")

    def parse_api_response(self, response: httpx.Response):
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API request failed with status code {response.status_code}")
            return None
        
    def update_package(self, model_id_version: Dict[str, str]) -> Dict:
        """Get comprehensive package update with all necessary information for SDK generation"""
        client = httpx.Client()
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key is not None else None
        try:
            response = client.post(self.infer_backend_url + "sdk/update_package", json=model_id_version, headers=headers, timeout=400)
            return self.parse_api_response(response)
        except Exception as e:
            print(f"Could not update package: {e}")
            return None
        
