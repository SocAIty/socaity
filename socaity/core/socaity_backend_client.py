import httpx
from typing import Dict, List
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
        
    def get_model_descriptors(self, model_descriptor_id: str = None):
        client = httpx.Client()
        if model_descriptor_id:
            model_descriptors = client.get(self.api_backend_url + "model_management/model_descriptors", params={"model_id": model_descriptor_id}, timeout=30)
        else:
            model_descriptors = client.get(self.api_backend_url + "model_management/model_descriptors", timeout=30)
        return self.parse_api_response(model_descriptors)

    def get_model_hosting_information(self, model_id: str):
        client = httpx.Client()
        model_hosting_information = client.get(self.api_backend_url + "model_management/model_hosting_information", params={"model_id": model_id}, timeout=30)
        return self.parse_api_response(model_hosting_information)

    def check_model_update(self, model_id_version: Dict[str, str]) -> List[Dict]:
        client = httpx.Client()
        response = client.post(self.api_backend_url + "model_management/check_model_update", json=model_id_version, timeout=400)
        return self.parse_api_response(response)
