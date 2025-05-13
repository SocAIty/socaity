import httpx
import os
from typing import Dict, List
from fastsdk.service_management import ServiceManager, FileSystemStore
from fastsdk.sdk_factory import create_sdk, normalize_class_name
import json
import time
import re


class SocaityServiceManager(ServiceManager):
    def __init__(self):
        self.cache_path = os.path.join(os.path.dirname(__file__), "sdk/cache")
        super().__init__(service_store=FileSystemStore(self.cache_path))
        self._model_descriptors_TTL_s = 60 * 60 * 24 * 1 # 1 day
        self.infer_backend_url = os.getenv("SOCAITY_INFER_BACKEND_URL", "https://api.socaity.ai/v1/")
        self.api_backend_url = os.getenv("SOCAITY_API_BACKEND_URL", "https://socaity.ai/api/v1/")
        self._model_descriptors = None
        
        self.update_package()

    def update_package(self):
        updates = self.check_model_update(self.service_store.get_version_index())
        if not updates or len(updates) == 0:
            return
        
        print("Updating package...")
        for mhi in updates:
            if mhi.get("version", "") == "DELETE":
                print(f"Deleting {mhi['id']}...")
                self.service_store.delete_service(mhi.get("id"))
                # delete .py file
                try:
                    os.remove(os.path.join(os.path.dirname(__file__), "sdk", "common", f"{mhi.get('id')}.py"))
                except FileNotFoundError:
                    pass
                continue
            
            print(f"Updating {mhi['id']}...")
            self.create_sdk(mhi)

        self.create_init_py()

    def create_init_py(self):
        imports_list = set()
        for service in self.list_services():
            # md = self.get_model_descriptor(service.family_id)
            # import_path = f"from .common.{md['display_name']}.{self.sanitize_id(service.id)} import {normalize_class_name(service.display_name)}"
            normalized_name = normalize_class_name(service.display_name)
            import_path = f"from .common.{normalized_name} import {normalized_name}"
            imports_list.add(import_path)
        
        init_py_path = os.path.join(os.path.dirname(__file__), "sdk")
        os.makedirs(init_py_path, exist_ok=True)

        with open("socaity/sdk/__init__.py", "w") as f:
            f.write("\n".join(imports_list))

    def sanitize_id(self, id: str) -> str:
        return "sdk_" + re.sub(r'[^a-zA-Z0-9_]', '_', id)

    def create_sdk(self, mhi: dict):
        model_descriptor = self.get_model_descriptor(mhi.get("model_id"))
        if not model_descriptor:
            print(f"No model descriptor for {mhi['id']}. Skipping it.")
            return
        
        display_name = model_descriptor.get("display_name", "")
        normalized_name = normalize_class_name(display_name)
        # get the category from the model descriptor
        descriptor_category = model_descriptor.get("model_category", "")
        service_address = f"{self.infer_backend_url}{normalized_name}"

        service_def = self.add_service(mhi["openapi_json"], service_id=mhi.get("id"), service_address=service_address, category=descriptor_category, service_name=normalized_name, family_id=mhi.get("model_id"))
        create_sdk(service_definition=service_def, save_path=f"socaity/sdk/common/{normalized_name}.py")
        
    @property
    def model_descriptors(self):
        """
        Checks cached model descriptors if expired fetch again from socaity.ai
        Returns cached data if it exists and is not expired, otherwise fetches new data
        """
        if self._model_descriptors:
            return self._model_descriptors
        
        # check if cache exi
        cache_file = os.path.join(self.cache_path, "model_descriptors.json")
        
        # Check if cache exists and is not expired
        if os.path.exists(cache_file):
            file_mtime = os.path.getmtime(cache_file)
            current_time = time.time()
            if current_time - file_mtime < self._model_descriptors_TTL_s:
                try:
                    with open(cache_file, "r") as f:
                        self._model_descriptors = json.load(f)
                    return self._model_descriptors
                except (json.JSONDecodeError, IOError):
                    # If cache file is corrupted, we'll fetch new data
                    pass
        
        # Fetch new data if cache doesn't exist or is expired
        self._model_descriptors = self.get_model_descriptors()
        
        # Save to cache
        os.makedirs(self.cache_path, exist_ok=True)
        with open(cache_file, "w") as f:
            json.dump(self._model_descriptors, f)
            
        return self._model_descriptors

    def get_model_descriptor(self, model_id: str) -> Dict:
        if not model_id:
            return None
        for md in self.model_descriptors:
            if md["id"] == model_id:
                return md
        return None
    
    def parse_api_response(self, response: httpx.Response):
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API request failed with status code {response.status_code}")
            return None
        
    def get_model_descriptors(self):
        client = httpx.Client()        
        model_descriptors = client.get(self.api_backend_url + "model_management/model_descriptors", timeout=30)
        return self.parse_api_response(model_descriptors)

    def get_model_hosting_information(self, model_id: str):
        client = httpx.Client()
        model_hosting_information = client.get(self.api_backend_url + "model_management/model_hosting_information", params={"model_id": model_id}, timeout=30)
        return self.parse_api_response(model_hosting_information)

    def check_model_update(self, model_id_version: Dict[str, str]) -> List[Dict]:
        client = httpx.Client()
        response = client.post(self.api_backend_url + "model_management/check_model_update", json=model_id_version, timeout=30)
        return self.parse_api_response(response)


if __name__ == "__main__":
    sm = SocaityServiceManager()

