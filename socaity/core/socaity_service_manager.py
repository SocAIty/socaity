from typing import Dict, Set
from pathlib import Path
from datetime import datetime, timedelta
from fastsdk.service_management import ServiceManager, FileSystemStore, ServiceDefinition
from fastsdk.sdk_factory import create_sdk
from fastsdk.utils import normalize_name_for_py
from socaity.core.socaity_backend_client import SocaityBackendClient


class SocaityServiceManager(ServiceManager):
    SDK_ROOT = Path(__file__).parent.parent / "sdk"
    OFFICIAL_SDK_DIR = SDK_ROOT / "official"
    COMMUNITY_SDK_DIR = SDK_ROOT / "community"
    REPLICATE_SDK_DIR = SDK_ROOT / "replicate"
    CACHE_DIR = SDK_ROOT / "cache"
    CACHE_TTL_MINUTES = 15

    def __init__(self):
        super().__init__(service_store=FileSystemStore(self.CACHE_DIR))
        self.socaity_backend_client = SocaityBackendClient()
        self._created_sdks: Dict[str, Path] = {}  # class_name -> save_path
        self._deleted_sdks: Dict[str, Path] = {}  # model_name -> save_path
        self.update_package()

    def _is_cache_stale(self) -> bool:
        """Check if the cache is older than the TTL by examining cache directory modification time"""
        if not self.CACHE_DIR.exists():
            return True  # No cache exists, needs update
        
        try:
            cache_mtime = datetime.fromtimestamp(self.CACHE_DIR.stat().st_mtime)
            cache_age = datetime.now() - cache_mtime
            ttl = timedelta(minutes=self.CACHE_TTL_MINUTES)
            
            return cache_age > ttl
        except OSError:
            return True  # If we can't check, assume stale

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
        if not self._is_cache_stale():
            return
        
        package_updates = self.socaity_backend_client.update_package(self.service_store.get_version_index())
        if not package_updates or not package_updates.get("updates"):
            return

        print("Updating package...")
        for update_item in package_updates["updates"]:
            if update_item.get("action") == "delete":
                self._handle_model_deletion(update_item)
            else:
                self._handle_model_update(update_item)

        self._update_init_files()
        # Touch the cache directory to update its modification time
        self._touch_cache_dir()

    def _touch_cache_dir(self) -> None:
        """Update the cache directory modification time to current time"""
        if self.CACHE_DIR.exists():
            self.CACHE_DIR.touch()

    def force_update_package(self) -> None:
        """Force update the package regardless of cache TTL"""
        self.update_package()

    def _handle_model_deletion(self, update_item: Dict) -> None:
        """Handle deletion of a model"""
        mhi = update_item.get("model_hosting_info", {})
        hosted_model_id = mhi.get("id")
        print(f"Deleting {hosted_model_id}...")
        
        try:
            # Get provider and display name for path calculation
            provider = update_item.get("provider", "socaity")
            display_name = update_item.get("display_name", "")
            username, model_name = self._parse_display_name(display_name)
            
            # For socaity models, we need to check both official and community dirs
            if provider and provider.lower() != "replicate":
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
            print(f"Error deleting file {hosted_model_id}: {e}")

        try:
            self.service_store.delete_service(hosted_model_id)
        except Exception as e:
            print(f"Error deleting service {hosted_model_id}: {e}")

    def _handle_model_update(self, update_item: Dict) -> None:
        """Handle update of a model"""
        mhi = update_item.get("model_hosting_info", {})
        service_def_data = update_item.get("service_definition")
        hosted_model_id = mhi.get("id")
        
        print(f"Updating {hosted_model_id}...")
        
        if not service_def_data:
            print(f"No service definition for {hosted_model_id}. Skipping it.")
            return

        # Convert the dictionary to a ServiceDefinition object if needed
        if isinstance(service_def_data, dict):
            service_def = ServiceDefinition(**service_def_data)
        else:
            service_def = service_def_data

        # Extract information from the update item
        provider = update_item.get("provider", "socaity")
        display_name = update_item.get("display_name", "")
        is_official = update_item.get("is_official", False)
        
        username, model_name = self._parse_display_name(display_name)
        
        # Determine if model is official (only for socaity models)  
        is_official = is_official if provider.lower() != "replicate" else False
        
        save_path = self._get_save_path(provider, username, model_name, is_official)
        
        # Normalize the model name for use as a Python class name
        class_name = normalize_name_for_py(model_name)
        
        # Use the service definition directly (already contains all needed information)
        try:
            file_path, actual_class_name, _ = create_sdk(
                service_definition=service_def,
                save_path=str(save_path),
                class_name=class_name  # Use just the model name for the class name
            )
            self._created_sdks[actual_class_name] = Path(file_path)
        except Exception as e:
            print(f"Error creating SDK for {hosted_model_id}: {e}")

        # Store the service definition in the service store for caching and reload
        try:
            self.service_store.save_service(service_def)
        except Exception as e:
            print(f"Warning: Failed to save service definition for {hosted_model_id}: {e}")

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

    def _get_path_as_import(self, file_path: Path) -> str:
        """Get the path as import for a given file path"""
        path_as_import = str(file_path).replace('\\', '/')
        if path_as_import.endswith('.py'):
            path_as_import = path_as_import[:-3]  # Remove .py extension
        path_as_import = path_as_import.replace('/', '.')
        return path_as_import

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
                    path_as_import = self._get_path_as_import(relative_path)
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
                path_as_import = self._get_path_as_import(relative_path)
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


if __name__ == "__main__":
    sm = SocaityServiceManager()
