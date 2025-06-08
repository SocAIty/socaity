import os
from typing import Dict
from fastsdk.service_management import ServiceManager, FileSystemStore
from fastsdk.sdk_factory import create_sdk
from fastsdk.utils import normalize_name_for_py
import json
import time
import re
from socaity.socaity_backend_client import SocaityBackendClient


class SocaityServiceManager(ServiceManager):
    def __init__(self):
        self.cache_path = os.path.join(os.path.dirname(__file__), "sdk/cache")
        super().__init__(service_store=FileSystemStore(self.cache_path))
        self._model_descriptors_TTL_s = 60 * 60 * 24 * 1 # 1 day
        self._model_descriptors = None
        self._replicate_services = []  # list of service_ids that belong to replicate
        self.socaity_backend_client = SocaityBackendClient()
        
        self.update_package()

    def update_package(self):
        updates = self.socaity_backend_client.check_model_update(self.service_store.get_version_index())
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
        imports_list_replicate = set()
        for service in self.list_services():
            # md = self.get_model_descriptor(service.family_id)
            # import_path = f"from .common.{md['display_name']}.{self.sanitize_id(service.id)} import {normalize_class_name(service.display_name)}"
            #normalized_name = normalize_class_name(service.display_name)
            
            if "/" in service.display_name:
                username = service.display_name.split("/")[0]
                model_name = service.display_name.split("/")[1]
            else:
                username = "official"
                model_name = service.display_name

            # normalize the model name
            username = normalize_name_for_py(username)
            model_name = normalize_name_for_py(model_name)

            normalized_name = normalize_name_for_py(model_name)

            is_replicate_hosted = service.id in self._replicate_services
            if is_replicate_hosted:
                save_path = f"socaity/sdk/replicate/{username}/{normalized_name}.py"
            else:
                save_path = f"socaity/sdk/common/{normalized_name}.py"
            
            import_path = f"from {save_path.replace('.py', '').replace('/', '.')} import {normalized_name}".strip().strip(".")
            imports_list.add(import_path)

            if is_replicate_hosted:
                imports_list_replicate.add(import_path)
            else:
                imports_list.add(import_path)
            
        init_py_path = os.path.join(os.path.dirname(__file__), "sdk")
        os.makedirs(init_py_path, exist_ok=True)

        with open("socaity/sdk/__init__.py", "w") as f:
            f.write("\n".join(imports_list))

        replicate_init_py_path = os.path.join(os.path.dirname(__file__), "sdk", "replicate")
        os.makedirs(replicate_init_py_path, exist_ok=True)
        with open("socaity/sdk/replicate/__init__.py", "w") as f:
            f.write("\n".join(imports_list_replicate))

    def sanitize_id(self, id: str) -> str:
        return "sdk_" + re.sub(r'[^a-zA-Z0-9_]', '_', id)

    def create_sdk(self, mhi: dict):
        
        if not mhi.get("openapi_json"):
            print(f"No openapi_json for {mhi['id']}. Skipping it.")
            return
        
        model_descriptor = self.socaity_backend_client.get_model_descriptors(mhi.get("model_id"))
        if not model_descriptor:
            print(f"No model descriptor for {mhi['id']}. Skipping it.")
            return
        
        display_name = model_descriptor.get("display_name", "")

        if "/" in display_name:
            username = display_name.split("/")[0]
            model_name = display_name.split("/")[1]
        else:
            username = "official"
            model_name = display_name

        model_name = normalize_name_for_py(model_name)
        # get the category from the model descriptor
        descriptor_category = model_descriptor.get("model_category", "")
        service_address = f"{self.socaity_backend_client.infer_backend_url}{model_name}"

        service_def = self.add_service(mhi["openapi_json"], service_id=mhi.get("id"), service_address=service_address, category=descriptor_category, service_name=model_name, family_id=mhi.get("model_id"))
        provider = mhi.get("provider", "socaity")
        
        save_path = f"socaity/sdk/common/{model_name}.py"
        if provider == 'replicate':
            self._replicate_services.append(service_def.id)
            save_path = f"socaity/sdk/replicate/{username}/{model_name}.py"
        
        create_sdk(service_definition=service_def, save_path=save_path)
        
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
        self._model_descriptors = self.socaity_backend_client.get_model_descriptors()
        
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


if __name__ == "__main__":
    sm = SocaityServiceManager()

