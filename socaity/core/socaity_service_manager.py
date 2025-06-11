from typing import Dict, Set, Optional
from pathlib import Path
from fastsdk.service_management import ServiceManager, FileSystemStore
from fastsdk.sdk_factory import create_sdk
from fastsdk.utils import normalize_name_for_py
import json
import time
from socaity.core.socaity_backend_client import SocaityBackendClient


class SocaityServiceManager(ServiceManager):
    SDK_ROOT = Path(__file__).parent.parent / "sdk"
    OFFICIAL_SDK_DIR = SDK_ROOT / "official"
    COMMUNITY_SDK_DIR = SDK_ROOT / "community"
    REPLICATE_SDK_DIR = SDK_ROOT / "replicate"
    CACHE_DIR = SDK_ROOT / "cache"
    MODEL_DESCRIPTORS_TTL = 60 * 60 * 24  # 1 day

    def __init__(self):
        super().__init__(service_store=FileSystemStore(self.CACHE_DIR))
        self._model_descriptors: Optional[Dict] = None
        self.socaity_backend_client = SocaityBackendClient()
        self._created_sdks: Dict[str, Path] = {}  # class_name -> save_path
        self._deleted_sdks: Dict[str, Path] = {}  # model_name -> save_path
        self.update_package()

    def _get_save_path(self, provider: str, username: str, model_name: str, is_official: bool = False) -> Path:
        """Get the appropriate save path based on provider and model info"""
        if provider.lower() == "replicate":
            return self.REPLICATE_SDK_DIR / username / f"{model_name}.py"
        elif is_official:
            return self.OFFICIAL_SDK_DIR / f"{model_name}.py"
        else:
            return self.COMMUNITY_SDK_DIR / f"{model_name}.py"

    def _parse_display_name(self, display_name: str) -> tuple[str, str]:
        """Parse display name into username and model name"""
        if "/" in display_name:
            username, model_name = display_name.split("/", 1)
        else:
            username, model_name = "official", display_name
        
        return normalize_name_for_py(username), normalize_name_for_py(model_name)

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
        # Get provider from model hosting information (mhi)
        try:
            provider = mhi.get("provider", "socaity")
            display_name = mhi.get("display_name", "")
            username, model_name = self._parse_display_name(display_name)
            
            # For socaity models, we need to check both official and community dirs
            if provider.lower() != "replicate":
                official_path = self.OFFICIAL_SDK_DIR / f"{model_name}.py"
                community_path = self.COMMUNITY_SDK_DIR / f"{model_name}.py"
                
                if official_path.exists():
                    save_path = official_path
                elif community_path.exists():
                    save_path = community_path
                else:
                    save_path = None
            else:
                save_path = self._get_save_path(provider, username, model_name, False)
                
            if save_path and save_path.exists():
                self._deleted_sdks[model_name] = save_path
                save_path.unlink()
        except Exception as e:
            print(f"Error deleting file {mhi.get('id')}: {e}")

        try:
            self.service_store.delete_service(mhi.get("id"))
        except Exception as e:
            print(f"Error deleting service {mhi['id']}: {e}")

    def _handle_model_update(self, mhi: Dict) -> None:
        """Handle update of a model"""
        print(f"Updating {mhi['id']}...")
        if not mhi.get("openapi_json"):
            print(f"No openapi_json for {mhi['id']}. Skipping it.")
            return

        # Get model descriptor for additional information
        model_descriptor = self.socaity_backend_client.get_model_descriptors(mhi.get("model_id"))
        if not model_descriptor:
            print(f"No model descriptor for {mhi['id']}. Skipping it.")
            return

        # Extract information from correct sources
        provider = mhi.get("provider", "socaity")  # Provider from hosting info
        display_name = model_descriptor.get("display_name", "")  # Display name from descriptor
        username, model_name = self._parse_display_name(display_name)
        
        # Determine if model is official (only for socaity models)
        is_official = model_descriptor.get("is_official", False) if provider.lower() != "replicate" else False
        
        save_path = self._get_save_path(provider, username, model_name, is_official)
        service_def = self._create_service_definition(mhi, model_descriptor, model_name)
        
        file_path, class_name, _ = create_sdk(
            service_definition=service_def,
            save_path=str(save_path)
        )
        self._created_sdks[class_name] = Path(file_path)

    def _create_service_definition(self, mhi: Dict, model_descriptor: Dict, model_name: str):
        """Create service definition for a model"""
        # Category from model descriptor, other service info from hosting info
        descriptor_category = model_descriptor.get("model_category", "")
        service_address = f"{self.socaity_backend_client.infer_backend_url}{model_name}"
        
        return self.add_service(
            mhi["openapi_json"],
            service_id=mhi.get("id"),
            service_address=service_address,
            category=descriptor_category,
            service_name=model_name,
            family_id=mhi.get("model_id")
        )

    def _update_init_files(self) -> None:
        """Update all __init__.py files with current imports"""
        self._ensure_sdk_directories()
        
        # Update main SDK __init__.py (only import official models)
        main_content = "from socaity.sdk.official import *"
        self._write_init_content(self.SDK_ROOT, main_content)
        
        # Update official SDK __init__.py
        official_imports = self._generate_imports(target="official")
        self._write_init_file(self.OFFICIAL_SDK_DIR, official_imports)
        
        # Update community SDK __init__.py
        community_imports = self._generate_imports(target="community")
        self._write_init_file(self.COMMUNITY_SDK_DIR, community_imports)
        
        # Update replicate username-specific __init__.py files
        self._update_replicate_init_files()

    def _ensure_sdk_directories(self) -> None:
        """Ensure all necessary SDK directories exist"""
        self.SDK_ROOT.mkdir(exist_ok=True)
        self.OFFICIAL_SDK_DIR.mkdir(exist_ok=True)
        self.COMMUNITY_SDK_DIR.mkdir(exist_ok=True)
        self.REPLICATE_SDK_DIR.mkdir(exist_ok=True)

    def _update_replicate_init_files(self) -> None:
        """Update __init__.py files for each replicate username directory"""
        # Get all replicate usernames from created SDKs
        replicate_usernames = set()
        for class_name, file_path in self._created_sdks.items():
            if "replicate" in str(file_path):
                try:
                    relative_path = file_path.relative_to(self.REPLICATE_SDK_DIR)
                    username = relative_path.parts[0]  # First part is the username
                    replicate_usernames.add(username)
                except ValueError:
                    continue
        
        # Create __init__.py for each username directory
        for username in replicate_usernames:
            username_dir = self.REPLICATE_SDK_DIR / username
            if username_dir.exists():
                username_imports = self._generate_replicate_imports(username)
                self._write_init_file(username_dir, username_imports)

    def _generate_replicate_imports(self, username: str) -> Set[str]:
        """Generate import statements specifically for replicate username directories"""
        imports = set()
        
        for class_name, file_path in self._created_sdks.items():
            # Check if this file belongs to this specific username
            if "replicate" in str(file_path) and username in str(file_path):
                try:
                    # Get the relative path from SDK_ROOT
                    relative_path = file_path.relative_to(self.SDK_ROOT)
                    # Convert path to import format
                    path_as_import = str(relative_path).replace('\\', '/').replace('/', '.').replace('.py', '')
                    # Construct import path
                    import_path = f"socaity.sdk.{path_as_import}"
                    import_stmt = f"from {import_path} import {class_name}"
                    imports.add(import_stmt)
                except Exception as e:
                    print(f"Error processing replicate import for {file_path}: {e}")
                    continue

        # Add existing imports from the username directory
        username_dir = self.REPLICATE_SDK_DIR / username
        try:
            old_imports = self._load_imports_from_init_py(username_dir / "__init__.py")
            imports.update(old_imports)
        except FileNotFoundError:
            pass

        # Remove deleted imports
        self._remove_deleted_imports(imports)
        return imports

    def _generate_imports(self, target: str = None) -> Set[str]:
        """Generate import statements for SDK files
        
        Args:
            target: The target for imports - "official", "community"
        """
        imports = set()
        
        for class_name, file_path in self._created_sdks.items():
            # Filter based on target
            if target is not None and target not in str(file_path):
                continue

            try:
                # Get the relative path from SDK_ROOT
                relative_path = file_path.relative_to(self.SDK_ROOT)
                # Convert path to import format
                path_as_import = str(relative_path).replace('\\', '/').replace('/', '.').replace('.py', '')
                # Construct import path
                import_path = f"socaity.sdk.{path_as_import}"
                import_stmt = f"from {import_path} import {class_name}"
                imports.add(import_stmt)
            except Exception as e:
                print(f"Error processing import for {file_path}: {e}")
                continue

        # Add existing imports
        if target == "official":
            init_path = self.OFFICIAL_SDK_DIR
        elif target == "community":
            init_path = self.COMMUNITY_SDK_DIR
        else:
            init_path = self.SDK_ROOT
            
        try:
            old_imports = self._load_imports_from_init_py(init_path / "__init__.py")
            imports.update(old_imports)
        except FileNotFoundError:
            pass

        # Remove deleted imports
        self._remove_deleted_imports(imports)
        return imports

    def _write_init_content(self, directory: Path, content: str) -> None:
        """Write specific content to __init__.py file"""
        init_file = directory / "__init__.py"
        init_file.write_text(content)

    def _write_init_file(self, directory: Path, imports: Set[str]) -> None:
        """Write imports to __init__.py file"""
        init_file = directory / "__init__.py"
        # Sort imports to have common imports first, then alphabetically
        sorted_imports = sorted(imports, key=lambda x: ('.common.' not in x, x))
        init_file.write_text("\n".join(sorted_imports))

    def _load_imports_from_init_py(self, path: Path) -> Set[str]:
        """Load existing imports from __init__.py file"""
        imports = set()
        if path.exists():
            for line in path.read_text().splitlines():
                if line.strip() and line.startswith("from"):
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

        cache_file = self.CACHE_DIR / "model_descriptors.json"
        
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
