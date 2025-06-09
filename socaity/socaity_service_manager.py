import os
from typing import Dict, Set, Optional
from dataclasses import dataclass
from pathlib import Path
from fastsdk.service_management import ServiceManager, FileSystemStore
from fastsdk.sdk_factory import create_sdk
from fastsdk.utils import normalize_name_for_py
import json
import time
from socaity.socaity_backend_client import SocaityBackendClient


@dataclass
class ModelInfo:
    """Data class to hold model information"""
    username: str
    model_name: str
    save_path: Path
    display_name: str


class SocaityServiceManager(ServiceManager):
    SDK_ROOT = Path("sdk")
    COMMON_SDK_DIR = SDK_ROOT / "common"
    REPLICATE_SDK_DIR = SDK_ROOT / "replicate"
    CACHE_DIR = SDK_ROOT / "cache"
    MODEL_DESCRIPTORS_TTL = 60 * 60 * 24  # 1 day

    def __init__(self):
        self.cache_path = os.path.join(os.path.dirname(__file__), str(self.CACHE_DIR))
        super().__init__(service_store=FileSystemStore(self.cache_path))
        self._model_descriptors: Optional[Dict] = None
        self.socaity_backend_client = SocaityBackendClient()
        self._created_sdks: Dict[str, Path] = {}  # model_name (class_name) -> save_path
        self._deleted_sdks: Dict[str, Path] = {}  # model_name (class_name) -> save_path
        self.update_package()

    def _get_model_info(self, mhi: Dict) -> ModelInfo:
        """Extract and normalize model information from model handler info"""
        display_name = mhi.get("display_name", "")
        if "/" in display_name:
            username, model_name = display_name.split("/")
        else:
            username, model_name = "official", display_name

        username = normalize_name_for_py(username)
        model_name = normalize_name_for_py(model_name)

        base_dir = self.REPLICATE_SDK_DIR if mhi.get("provider", "").lower() == "replicate" else self.COMMON_SDK_DIR
        if mhi.get("provider", "").lower() == "replicate":
            save_path = base_dir / username / f"{model_name}.py"
        else:
            save_path = base_dir / f"{model_name}.py"

        return ModelInfo(username, model_name, save_path, display_name)

    def update_package(self) -> None:
        """Update the package with latest model changes"""
        updates = self.socaity_backend_client.check_model_update(self.service_store.get_version_index())
        if not updates:
            return

        print("Updating package...")
        for mhi in updates:
            if mhi.get("version", "") == "DELETE":
                self._handle_model_deletion(mhi)
            else:
                self._handle_model_update(mhi)

        self._update_init_files()

    def _handle_model_deletion(self, mhi: Dict) -> None:
        """Handle deletion of a model"""
        print(f"Deleting {mhi['id']}...")
        self.service_store.delete_service(mhi.get("id"))
        
        model_info = self._get_model_info(mhi)
        self._deleted_sdks[model_info.model_name] = model_info.save_path
        
        try:
            if model_info.save_path.exists():
                model_info.save_path.unlink()
        except OSError as e:
            print(f"Error deleting file {model_info.save_path}: {e}")

    def _handle_model_update(self, mhi: Dict) -> None:
        """Handle update of a model"""
        print(f"Updating {mhi['id']}...")
        if not mhi.get("openapi_json"):
            print(f"No openapi_json for {mhi['id']}. Skipping it.")
            return

        model_descriptor = self.socaity_backend_client.get_model_descriptors(mhi.get("model_id"))
        if not model_descriptor:
            print(f"No model descriptor for {mhi['id']}. Skipping it.")
            return

        model_info = self._get_model_info(model_descriptor)
        service_def = self._create_service_definition(mhi, model_info)
        
        file_path, class_name, _ = create_sdk(
            service_definition=service_def,
            save_path=str(model_info.save_path)
        )
        self._created_sdks[class_name] = Path(file_path)

    def _create_service_definition(self, mhi: Dict, model_info: ModelInfo):
        """Create service definition for a model"""
        descriptor_category = mhi.get("model_category", "")
        service_address = f"{self.socaity_backend_client.infer_backend_url}{model_info.model_name}"
        
        return self.add_service(
            mhi["openapi_json"],
            service_id=mhi.get("id"),
            service_address=service_address,
            category=descriptor_category,
            service_name=model_info.model_name,
            family_id=mhi.get("model_id")
        )

    def _update_init_files(self) -> None:
        """Update all __init__.py files with current imports"""
        self._ensure_sdk_directories()
        
        # Update main SDK __init__.py
        main_imports = self._generate_imports()
        self._write_init_file(self.SDK_ROOT, main_imports)
        
        # Update replicate SDK __init__.py
        replicate_imports = self._generate_imports(replicate_only=True)
        self._write_init_file(self.REPLICATE_SDK_DIR, replicate_imports)

    def _ensure_sdk_directories(self) -> None:
        """Ensure all necessary SDK directories exist"""
        self.SDK_ROOT.mkdir(exist_ok=True)
        self.COMMON_SDK_DIR.mkdir(exist_ok=True)
        self.REPLICATE_SDK_DIR.mkdir(exist_ok=True)

    def _generate_imports(self, replicate_only: bool = False) -> Set[str]:
        """Generate import statements for SDK files"""
        imports = set()
        for class_name, file_path in self._created_sdks.items():
            if replicate_only and "replicate" not in str(file_path):
                continue
            import_path = str(file_path).replace('\\', '/').replace('.py', '').replace('/', '.')
            import_stmt = f"from {import_path} import {class_name}".strip().strip(".")
            imports.add(import_stmt)

        # Add existing imports
        init_path = self.REPLICATE_SDK_DIR if replicate_only else self.SDK_ROOT
        try:
            old_imports = self._load_imports_from_init_py(init_path / "__init__.py")
            imports.update(old_imports)
        except FileNotFoundError:
            pass

        # Remove deleted imports
        self._remove_deleted_imports(imports)
        return imports

    def _write_init_file(self, directory: Path, imports: Set[str]) -> None:
        """Write imports to __init__.py file"""
        init_file = directory / "__init__.py"
        # sort imports first by .common. and then by name in order to have common imports first
        init_file.write_text("\n".join(sorted(imports)))

    def _load_imports_from_init_py(self, path: Path) -> Set[str]:
        """Load existing imports from __init__.py file"""
        imports = set()
        if path.exists():
            for line in path.read_text().splitlines():
                if line.startswith("from"):
                    imports.add(line.strip())
        return imports

    def _remove_deleted_imports(self, imports: Set[str]) -> None:
        """Remove imports of deleted SDKs from the given imports set"""
        imports_to_remove = {
            imp
            for imp in imports 
            for del_path in self._deleted_sdks.values() 
            if str(del_path) in imp
        }
        imports.difference_update(imports_to_remove)

    @property
    def model_descriptors(self) -> Dict:
        """Get model descriptors with caching"""
        if self._model_descriptors:
            return self._model_descriptors

        cache_file = Path(self.cache_path) / "model_descriptors.json"
        
        if self._is_cache_valid(cache_file):
            try:
                return self._load_cache(cache_file)
            except (json.JSONDecodeError, OSError):
                pass

        return self._fetch_and_cache_descriptors(cache_file)

    def _is_cache_valid(self, cache_file: Path) -> bool:
        """Check if cache file is valid and not expired"""
        if not cache_file.exists():
            return False
        return (time.time() - cache_file.stat().st_mtime) < self.MODEL_DESCRIPTORS_TTL

    def _load_cache(self, cache_file: Path) -> Dict:
        """Load model descriptors from cache"""
        self._model_descriptors = json.loads(cache_file.read_text())
        return self._model_descriptors

    def _fetch_and_cache_descriptors(self, cache_file: Path) -> Dict:
        """Fetch new model descriptors and cache them"""
        self._model_descriptors = self.socaity_backend_client.get_model_descriptors()
        cache_file.parent.mkdir(exist_ok=True)
        cache_file.write_text(json.dumps(self._model_descriptors))
        return self._model_descriptors

    def get_model_descriptor(self, model_id: str) -> Optional[Dict]:
        """Get a specific model descriptor by ID"""
        if not model_id:
            return None
        return next((md for md in self.model_descriptors if md["id"] == model_id), None)


if __name__ == "__main__":
    sm = SocaityServiceManager()
