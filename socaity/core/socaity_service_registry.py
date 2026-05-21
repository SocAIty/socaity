import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Set
from pathlib import Path
from datetime import datetime, timedelta

from apipod_registry import Registry, ServiceDefinition
from apipod_registry.definitions.service_definitions import ReplicateServiceAddress
from apipod_registry.service_registry.file_system_registry import FileSystemStore
from apipod_registry.utils.normalization import normalize_name_for_py
from fastsdk.sdk_factory import create_sdk
from socaity.core.socaity_backend_client import SocaityBackendClient

IMPORT_PATTERN = re.compile(
    r"^from\s+socaity\.sdk\.services\.(\w+)\s+import\s+(\w+)(?:\s+as\s+(\w+))?$"
)


@dataclass
class ImportEntry:
    """Single import statement in a namespace __init__.py."""
    module_name: str
    class_name: str
    alias: str

    def to_statement(self) -> str:
        stmt = f"from socaity.sdk.services.{self.module_name} import {self.class_name}"
        if self.alias != self.class_name:
            stmt += f" as {self.alias}"
        return stmt

    @staticmethod
    def parse(line: str) -> Optional['ImportEntry']:
        match = IMPORT_PATTERN.match(line.strip())
        if not match:
            return None
        module_name, class_name, alias = match.groups()
        return ImportEntry(module_name, class_name, alias or class_name)


class SocaityServiceRegistry(Registry):
    SDK_ROOT = Path(__file__).parent.parent / "sdk"
    SERVICES_DIR = SDK_ROOT / "services"
    CACHE_DIR = SDK_ROOT / "cache"
    CACHE_TTL_MINUTES = 15

    def __init__(self):
        super().__init__(service_store=FileSystemStore(self.CACHE_DIR))
        self._backend = SocaityBackendClient()
        self._namespace_additions: Dict[str, List[ImportEntry]] = {}
        self._namespace_deletions: Dict[str, Set[str]] = {}
        self._ensure_sdk_structure()

    # ---- Public API ----

    def install_service(self, service_name_or_id: str) -> None:
        """Install a service by name, UUID, or 'user/service' identifier."""
        item = self._backend.install_service(service_name_or_id)
        if not item:
            print(f"Could not resolve service '{service_name_or_id}'.")
            return
        print(f"Installing {service_name_or_id}...")
        self._dispatch_item(item)
        self._flush_init_files()
        self._touch_cache_dir()

    def install_all(self) -> None:
        """Install all available services (not currently supported by backend)."""
        print("install_all is not supported by the current backend.")

    def force_update_package(self) -> None:
        self.update_package(force=True)

    def update_package(self, force: bool = False) -> None:
        """Check installed services for updates and apply them."""
        if not force and not self._is_cache_stale():
            return

        items = self._backend.get_service_updates(self.service_store.get_version_index())
        if not items:
            return

        print("Updating package...")
        for item in items:
            self._dispatch_item(item)

        self._flush_init_files()
        self._touch_cache_dir()

    # ---- Routing ----

    def _dispatch_item(self, item: dict) -> None:
        action = item.get("action")
        if action == "delete":
            self._handle_deletion(item)
        elif action in ("update", "install"):
            self._handle_update(item)
        else:
            print(f"  Unknown action '{action}'. Skipping.")

    # ---- Provider / namespace resolution ----

    @staticmethod
    def _resolve_namespace(
        service_def: ServiceDefinition,
        is_official: bool,
        creator_display_name: str,
        third_party_provider: Optional[str] = None,
    ) -> tuple[str, str]:
        """Return (namespace_path_relative_to_SDK_ROOT, alias)."""
        display_name = service_def.display_name or service_def.id

        if third_party_provider and third_party_provider.lower() != "socaity":
            provider = normalize_name_for_py(third_party_provider)
            if "/" in display_name:
                username, model_name = display_name.split("/", 1)
            else:
                username, model_name = "unknown", display_name
            return (
                f"{provider}/{normalize_name_for_py(username)}",
                normalize_name_for_py(model_name),
            )

        alias = normalize_name_for_py(display_name)
        if is_official:
            return "official", alias

        user = normalize_name_for_py(creator_display_name or "unknown")
        return f"community/{user}", alias

    @staticmethod
    def _derive_class_name(service_def: ServiceDefinition, third_party_provider: Optional[str] = None) -> str:
        display_name = service_def.display_name or service_def.id
        if third_party_provider and third_party_provider.lower() != "socaity" and "/" in display_name:
            _, model_name = display_name.split("/", 1)
            return normalize_name_for_py(model_name)
        return normalize_name_for_py(display_name)

    # ---- Update / delete handlers ----

    def _handle_update(self, item: dict) -> None:
        service_def = self._extract_service_def(item)
        if not service_def:
            return

        is_official = item.get("is_official", False)
        creator_display_name = self._extract_creator_display_name(item)
        third_party_provider = item.get("third_party_provider")

        module_name = normalize_name_for_py(service_def.id)
        save_path = self.SERVICES_DIR / f"{module_name}.py"
        class_name = self._derive_class_name(service_def, third_party_provider)
        namespace, alias = self._resolve_namespace(service_def, is_official, creator_display_name, third_party_provider)

        print(f"  Installing {service_def.display_name} -> {namespace}/{alias}")

        try:
            _, actual_class_name, _ = create_sdk(
                service_definition=service_def,
                save_path=str(save_path),
                class_name=class_name,
            )
        except Exception as e:
            print(f"  Error creating SDK for {service_def.id}: {e}")
            return

        self._namespace_additions.setdefault(namespace, []).append(
            ImportEntry(module_name, actual_class_name, alias)
        )

        try:
            self.service_store.save_service(service_def)
        except Exception as e:
            print(f"  Warning: cache write failed for {service_def.id}: {e}")

    def _handle_deletion(self, item: dict) -> None:
        service_def_data = item.get("service_definition")
        message = item.get("message", "")

        if not service_def_data:
            # Deletion without a service_definition — only a message, no file to remove.
            print(f"  Delete notice: {message}")
            return

        if isinstance(service_def_data, dict):
            service_id = service_def_data.get("id")
            display_name = service_def_data.get("display_name", service_id)
        else:
            service_id = service_def_data.id
            display_name = service_def_data.display_name

        is_official = item.get("is_official", False)
        creator_display_name = self._extract_creator_display_name(item)
        third_party_provider = item.get("third_party_provider")

        # Reconstruct a minimal ServiceDefinition for namespace resolution
        try:
            minimal_def = (
                ServiceDefinition(**service_def_data)
                if isinstance(service_def_data, dict)
                else service_def_data
            )
            namespace, _ = self._resolve_namespace(minimal_def, is_official, creator_display_name, third_party_provider)
        except Exception:
            namespace = "community/unknown"

        module_name = normalize_name_for_py(service_id)
        service_file = self.SERVICES_DIR / f"{module_name}.py"

        print(f"  Deleting {display_name} from {namespace}")

        if service_file.exists():
            service_file.unlink()

        self._namespace_deletions.setdefault(namespace, set()).add(module_name)

        try:
            self.service_store.delete_service(service_id)
        except Exception as e:
            print(f"  Error removing {service_id} from store: {e}")

    # ---- Init-file management ----

    def _flush_init_files(self) -> None:
        """Apply all pending additions/deletions to namespace __init__.py files."""
        affected = set(self._namespace_additions) | set(self._namespace_deletions)

        for namespace in affected:
            ns_dir = self._ensure_namespace_package(namespace)
            init_file = ns_dir / "__init__.py"

            entries = self._load_namespace_imports(init_file)

            for module_name in self._namespace_deletions.get(namespace, set()):
                entries = {a: e for a, e in entries.items() if e.module_name != module_name}

            for entry in self._namespace_additions.get(namespace, []):
                resolved = self._resolve_alias_conflict(entry.alias, entries, entry.module_name)
                if resolved != entry.alias:
                    print(f"  Name conflict in {namespace}: '{entry.alias}' -> '{resolved}'")
                    entry = ImportEntry(entry.module_name, entry.class_name, resolved)
                entries[entry.alias] = entry

            self._write_namespace_init(init_file, entries)

        self._write_sdk_init()
        self._namespace_additions.clear()
        self._namespace_deletions.clear()

    @staticmethod
    def _load_namespace_imports(init_file: Path) -> Dict[str, ImportEntry]:
        entries: Dict[str, ImportEntry] = {}
        if not init_file.exists():
            return entries
        for line in init_file.read_text().splitlines():
            entry = ImportEntry.parse(line)
            if entry:
                entries[entry.alias] = entry
        return entries

    @staticmethod
    def _resolve_alias_conflict(alias: str, existing: Dict[str, ImportEntry], module_name: str) -> str:
        if alias not in existing or existing[alias].module_name == module_name:
            return alias
        counter = 1
        while f"{alias}_{counter}" in existing:
            counter += 1
        return f"{alias}_{counter}"

    @staticmethod
    def _write_namespace_init(init_file: Path, entries: Dict[str, ImportEntry]) -> None:
        statements = sorted(e.to_statement() for e in entries.values())
        init_file.write_text("\n".join(statements) + "\n" if statements else "")

    def _write_sdk_init(self) -> None:
        (self.SDK_ROOT / "__init__.py").write_text("from socaity.sdk.official import *\n")

    # ---- Directory helpers ----

    def _ensure_sdk_structure(self) -> None:
        for d in (self.SERVICES_DIR, self.CACHE_DIR,
                  self.SDK_ROOT / "official",
                  self.SDK_ROOT / "community",
                  self.SDK_ROOT / "replicate"):
            d.mkdir(parents=True, exist_ok=True)

        for d in (self.SERVICES_DIR,
                  self.SDK_ROOT / "official",
                  self.SDK_ROOT / "community",
                  self.SDK_ROOT / "replicate"):
            init = d / "__init__.py"
            if not init.exists():
                init.write_text("")

        self._write_sdk_init()

    def _ensure_namespace_package(self, namespace: str) -> Path:
        current = self.SDK_ROOT
        for part in Path(namespace).parts:
            current = current / part
            current.mkdir(parents=True, exist_ok=True)
            init = current / "__init__.py"
            if not init.exists():
                init.write_text("")
        return current

    # ---- Misc helpers ----

    @staticmethod
    def _extract_service_def(item: dict) -> Optional[ServiceDefinition]:
        data = item.get("service_definition")
        if not data:
            print(f"  No service definition in item: {item.get('message', '')}. Skipping.")
            return None
        if isinstance(data, dict):
            return ServiceDefinition(**data)
        return data

    @staticmethod
    def _extract_creator_display_name(item: dict) -> str:
        created_by = item.get("created_by")
        if not created_by:
            return ""
        if isinstance(created_by, dict):
            return created_by.get("display_name", "")
        return getattr(created_by, "display_name", "")

    def _is_cache_stale(self) -> bool:
        if not self.CACHE_DIR.exists():
            return True
        try:
            age = datetime.now() - datetime.fromtimestamp(self.CACHE_DIR.stat().st_mtime)
            return age > timedelta(minutes=self.CACHE_TTL_MINUTES)
        except OSError:
            return True

    def _touch_cache_dir(self) -> None:
        if self.CACHE_DIR.exists():
            self.CACHE_DIR.touch()


# for debugging purposes
if __name__ == "__main__":
    registry = SocaityServiceRegistry()
    registry.update_package(force=True)

