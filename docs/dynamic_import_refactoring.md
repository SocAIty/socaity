# Dynamic Import Refactoring: `.pyi` Stubs + `__getattr__` Routing

This document explains the architecture behind the new SDK import system and provides a
step-by-step refactoring plan to migrate from generated `.py` client files to a dynamic
`.pyi` + `__getattr__` approach.

---

## Table of Contents

1. [How Python Imports Work](#1-how-python-imports-work)
2. [What `.pyi` Files Are and Why We Need Them](#2-what-pyi-files-are-and-why-we-need-them)
3. [The Overall Idea](#3-the-overall-idea)
4. [Current Architecture](#4-current-architecture)
5. [Target Architecture](#5-target-architecture)
6. [Refactoring Plan](#6-refactoring-plan)

---

## 1. How Python Imports Work

### Regular imports

When Python encounters `import socaity.official.face2face`, it does the following:

1. **Checks `sys.modules`** — if the module was already imported, returns the cached version.
2. **Finds the module** — walks the filesystem (or other finders on `sys.meta_path`) to
   locate `socaity/official/face2face.py` or `socaity/official/face2face/__init__.py`.
3. **Executes the module** — runs the file and creates a module object.
4. **Caches it** — stores the module in `sys.modules`.

### `from X import Y`

`from socaity.official import face2face` does something subtly different:

1. Imports `socaity` (runs `socaity/__init__.py`).
2. Imports `socaity.official` (runs `socaity/official/__init__.py`).
3. Looks for `face2face` as an **attribute** of the `socaity.official` module object.
4. If not found directly, falls back to the module-level `__getattr__` function (PEP 562).

### PEP 562: Module `__getattr__`

[PEP 562](https://peps.python.org/pep-0562/) (Python 3.7+) allows a module to define a
`__getattr__(name)` function. When an attribute lookup on the module fails the normal
path, Python calls this function instead of raising `AttributeError`.

```python
# socaity/official/__init__.py
def __getattr__(name: str):
    # Called when someone does: from socaity.official import <name>
    # and <name> is not a regular attribute of this module.
    ...
```

### Critical limitation: subpackage resolution

`__getattr__` only intercepts **attribute access** on an already-imported module. It does
**not** intercept subpackage/submodule imports.

```python
# This works — attribute access triggers __getattr__:
from socaity.official import face2face

# This requires socaity/replicate/black_forest_labs/__init__.py to exist on disk.
# Python resolves the dotted path by walking directories BEFORE calling __getattr__:
from socaity.replicate.black_forest_labs import flux_schnell
```

This means every intermediate package in the import path must be a real directory with a
real `__init__.py`. Only the **leaf name** (the service) can be resolved dynamically via
`__getattr__`.

---

## 2. What `.pyi` Files Are and Why We Need Them

### Stub files

A `.pyi` file is a **type stub** — a Python file that contains only type annotations and
no runtime logic. It is read by IDEs (PyCharm, VS Code/Pylance) and type checkers
(mypy, pyright) but **never executed** by the Python interpreter.

```python
# face2face.pyi — describes the shape of the class for IDEs
from fastsdk import FastClient, APISeex
from typing import Union, List, Literal

class face2face(FastClient):
    """Swap faces from images and videos."""
    def __init__(self, api_key: str = None) -> None: ...
    def swap(self, faces: Union[List[str], ...], media: ...) -> APISeex: ...
    run = swap
    __call__ = swap
```

Key properties:

- **Method bodies are `...` (ellipsis)** — no implementation code.
- **All type annotations are present** — the IDE uses these for autocompletion and hover docs.
- **Docstrings are included** — IDEs display them in hover tooltips.
- **Imports are present** — so the IDE can resolve referenced types.

### Why stubs solve our problem

| Concern | Generated `.py` files (current) | `.pyi` stubs (new) |
|---|---|---|
| IDE autocompletion | Works (real code) | Works (stub describes the type) |
| Hover docs | Works | Works (docstrings in stub) |
| Runtime logic | Full class with methods | None — `__getattr__` handles it |
| File size | Large (full implementation) | Small (signatures only) |
| Version control noise | Every update rewrites large files | Minimal `.pyi` diffs |
| Name conflicts | UUID filenames to avoid clashes | Registry + namespace dirs |

### How IDEs discover `.pyi` files

When an IDE resolves `from socaity.official import face2face`, it checks (in order):

1. `socaity/official/__init__.pyi` — if it re-exports `face2face`, the IDE follows.
2. `socaity/official/face2face.pyi` — describes the `face2face` module/class.
3. Falls back to `socaity/official/__init__.py` and infers from runtime code.

We generate **both** a per-service `.pyi` and an `__init__.pyi` that re-exports it:

```python
# socaity/official/__init__.pyi
from .face2face import face2face as face2face
```

```python
# socaity/official/face2face.pyi
from fastsdk import FastClient, APISeex
...
class face2face(FastClient): ...
```

The explicit `as face2face` in the re-export tells the type checker this is a
**public re-export** (PEP 484 convention), so the IDE offers it in completions.

---

## 3. The Overall Idea

### Two parallel systems

```
 ┌─────────────────────────────────────────────────────────────┐
 │                       IDE / Type Checker                    │
 │                                                             │
 │  Reads .pyi stubs for autocompletion, hover docs, and      │
 │  type checking. Never executes any code.                    │
 │                                                             │
 │  socaity/official/face2face.pyi  ──►  class face2face       │
 │  socaity/official/__init__.pyi   ──►  re-exports face2face  │
 └─────────────────────────────────────────────────────────────┘

 ┌─────────────────────────────────────────────────────────────┐
 │                     Python Runtime                          │
 │                                                             │
 │  from socaity.official import face2face                     │
 │       │                                                     │
 │       ▼                                                     │
 │  socaity/official/__init__.py  →  __getattr__("face2face")  │
 │       │                                                     │
 │       ▼                                                     │
 │  Import Index lookup:  "face2face" in "official" namespace  │
 │       │                        → service_id = "0d69b..."    │
 │       ▼                                                     │
 │  Load ServiceDefinition from cache/{service_id}.json        │
 │       │                                                     │
 │       ▼                                                     │
 │  Dynamic class factory  →  creates FastClient subclass      │
 │  with methods that delegate to submit_job()                 │
 │       │                                                     │
 │       ▼                                                     │
 │  Return the class (cached for subsequent imports)           │
 └─────────────────────────────────────────────────────────────┘
```

### Developer workflow

1. **Install**: `socaity -i replicate/flux-schnell`
2. **Backend responds** with `PackageUpdateItem` containing the `ServiceDefinition`.
3. **SDK generates**:
   - `socaity/replicate/black_forest_labs/flux_schnell.pyi` (type stub)
   - `socaity/replicate/black_forest_labs/__init__.pyi` (re-export)
   - `socaity/replicate/black_forest_labs/__init__.py` (router, if not exists)
   - Updates `cache/{service_id}.json` and `import_index.json`
4. **User writes code** with full IDE support:
   ```python
   from socaity.replicate.black_forest_labs import flux_schnell
   model = flux_schnell(api_key="...")
   result = model.predictions(prompt="a cat")
   ```
5. **At runtime**: `__getattr__` resolves `flux_schnell` → loads `ServiceDefinition` →
   builds a `FastClient` subclass dynamically → returns the class.

### Supported import patterns

```python
# Official services — available at top level and under official/
from socaity import face2face
from socaity.official import face2face

# Replicate services — under replicate/<username>/
from socaity.replicate.black_forest_labs import flux_schnell

# Community services — under <username>/
from socaity.some_user import chat_model
```

---

## 4. Current Architecture

### File generation flow

```
Backend (PackageUpdateItem)
    │
    ▼
SocaityServiceRegistry._handle_model_update()
    │
    ├── create_sdk()  [fastsdk/sdk_factory/sdk_factory.py]
    │       │
    │       ├── Loads sdk_template.j2 (Jinja2 template)
    │       ├── Prepares endpoint data (type hints, defaults, descriptions)
    │       ├── Renders full .py file with FastClient subclass
    │       └── Writes to socaity/sdk/{official|replicate|community}/...
    │
    └── service_store.save_service()  →  cache/{service_id}.json
         │
         ▼
SocaityServiceRegistry._update_init_files()
    │
    ├── Scans _created_sdks dict for new class→path mappings
    ├── Generates "from socaity.sdk.X.Y import Z" lines
    └── Writes to each __init__.py
```

### Current directory layout

```
socaity/
├── __init__.py                        # "from socaity.sdk.official import *"
├── core/
│   ├── socaity_backend_client.py      # HTTP client to backend
│   └── socaity_service_registry.py    # Orchestrates install + generation
├── cli.py                             # "socaity -i <name>"
└── sdk/
    ├── __init__.py                    # "from socaity.sdk.official import *"
    ├── cache/
    │   ├── version_index.json         # {service_id: version_hash}
    │   └── {service_id}.json          # Full ServiceDefinition JSON
    ├── official/
    │   ├── __init__.py                # "from socaity.sdk.official.__uuid import face2face"
    │   └── __uuid.py                  # Generated FastClient subclass
    ├── replicate/
    │   ├── __init__.py                # Import lines for all replicate services
    │   └── black_forest_labs/
    │       ├── __init__.py            # "from ...flux_schnell import flux_schnell"
    │       └── flux_schnell.py        # Generated FastClient subclass
    └── community/
        └── __init__.py
```

### Problems with the current approach

1. **UUID filenames**: Official services use `__<uuid>.py` filenames which are unreadable.
2. **Large generated files**: Each `.py` contains full class implementations (100+ lines).
3. **Fragile `__init__.py` management**: Imports are managed by string manipulation of
   init files, parsing existing lines and merging new ones.
4. **Deep import paths**: `from socaity.sdk.official.__uuid import face2face` is not
   user-friendly.
5. **Version control noise**: Every service update rewrites large `.py` files and multiple
   `__init__.py` files.

---

## 5. Target Architecture

### New directory layout

```
socaity/
├── __init__.py                        # Existing exports + __getattr__ for officials
├── __init__.pyi                       # Re-exports official service classes
├── core/
│   ├── socaity_backend_client.py      # Unchanged
│   ├── socaity_service_registry.py    # Refactored: generates .pyi instead of .py
│   └── _dynamic_resolver.py           # NEW: shared __getattr__ logic + class cache
├── cli.py                             # Minor updates
├── cache/
│   ├── version_index.json             # Unchanged format
│   ├── import_index.json              # NEW: maps (namespace, name) → service_id
│   └── {service_id}.json              # Unchanged: full ServiceDefinition JSON
├── official/
│   ├── __init__.py                    # __getattr__ via _dynamic_resolver
│   ├── __init__.pyi                   # "from .face2face import face2face as face2face"
│   └── face2face.pyi                  # Type stub for face2face class
├── replicate/
│   ├── __init__.py                    # Package marker (+ optional __getattr__)
│   ├── __init__.pyi                   # Re-exports all replicate subpackages
│   └── black_forest_labs/
│       ├── __init__.py                # __getattr__ via _dynamic_resolver
│       ├── __init__.pyi               # "from .flux_schnell import flux_schnell as ..."
│       └── flux_schnell.pyi           # Type stub for flux_schnell class
└── <username>/                        # Created on install for community services
    ├── __init__.py                    # __getattr__ via _dynamic_resolver
    ├── __init__.pyi                   # Re-exports
    └── <service_name>.pyi             # Type stub
```

### Import index (`import_index.json`)

Replaces the current `__init__.py` import-line management. This single JSON file maps
every importable name to its service ID and namespace:

```json
{
  "namespaces": {
    "official": {
      "face2face": "0d69b27a-f893-4582-b3e8-a18c1f588e90"
    },
    "replicate/black_forest_labs": {
      "flux_schnell": "404643cc-3870-4be7-9169-f57b0bbc4091"
    },
    "replicate/deepseek_ai": {
      "deepseek_v3": "50100977-19d8-4d59-8a5a-50d7dbe7ffc7"
    },
    "some_user": {
      "chat_model": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    }
  }
}
```

The namespace key corresponds to the directory path relative to the `socaity/` package
root. For example, `"replicate/black_forest_labs"` maps to
`socaity/replicate/black_forest_labs/`.

### The dynamic resolver (`socaity/core/_dynamic_resolver.py`)

A single shared module that every `__init__.py` delegates to:

```python
# socaity/core/_dynamic_resolver.py
import json
from pathlib import Path
from functools import lru_cache
from fastsdk import FastClient
from apipod_registry import ServiceDefinition
from apipod_registry.utils.normalization import normalize_name_for_py

CACHE_DIR = Path(__file__).parent.parent / "cache"
INDEX_PATH = CACHE_DIR / "import_index.json"

# In-memory class cache: (namespace, name) → class
_class_cache: dict[tuple[str, str], type] = {}


def _load_import_index() -> dict:
    if INDEX_PATH.exists():
        return json.loads(INDEX_PATH.read_text())
    return {"namespaces": {}}


def _load_service_definition(service_id: str) -> ServiceDefinition:
    path = CACHE_DIR / f"{service_id}.json"
    data = json.loads(path.read_text())
    return ServiceDefinition(**data)


def _build_client_class(service_def: ServiceDefinition, class_name: str) -> type:
    """
    Dynamically create a FastClient subclass from a ServiceDefinition.
    Methods accept **kwargs and delegate to submit_job().
    The .pyi stub provides the typed signatures for the IDE.
    """
    service_id = service_def.id

    def make_init(sid):
        def __init__(self, api_key=None):
            FastClient.__init__(self, service_name_or_id=sid, api_key=api_key)
        return __init__

    attrs = {
        "__init__": make_init(service_id),
        "__doc__": service_def.description or service_def.short_desc or class_name,
    }

    for endpoint in service_def.endpoints:
        method_name = normalize_name_for_py(endpoint.path)
        ep_path = endpoint.path

        def make_method(path):
            def method(self, **kwargs):
                return self.submit_job(path, **kwargs)
            return method

        attrs[method_name] = make_method(ep_path)

    # Convenience aliases for the first endpoint
    if service_def.endpoints:
        first = normalize_name_for_py(service_def.endpoints[0].path)
        attrs["run"] = attrs[first]
        attrs["__call__"] = attrs[first]

    return type(class_name, (FastClient,), attrs)


def create_resolver(namespace: str):
    """
    Returns a __getattr__ function for a given namespace.
    Used in each __init__.py:

        from socaity.core._dynamic_resolver import create_resolver
        __getattr__ = create_resolver("official")
    """
    def __getattr__(name: str):
        cache_key = (namespace, name)
        if cache_key in _class_cache:
            return _class_cache[cache_key]

        index = _load_import_index()
        ns_map = index.get("namespaces", {}).get(namespace, {})
        service_id = ns_map.get(name)

        if service_id is None:
            raise AttributeError(
                f"module 'socaity.{namespace.replace('/', '.')}' "
                f"has no service named '{name}'"
            )

        service_def = _load_service_definition(service_id)
        cls = _build_client_class(service_def, name)
        _class_cache[cache_key] = cls
        return cls

    return __getattr__
```

Each generated `__init__.py` becomes two lines:

```python
# socaity/official/__init__.py
from socaity.core._dynamic_resolver import create_resolver
__getattr__ = create_resolver("official")
```

```python
# socaity/replicate/black_forest_labs/__init__.py
from socaity.core._dynamic_resolver import create_resolver
__getattr__ = create_resolver("replicate/black_forest_labs")
```

### The top-level `socaity/__init__.py`

```python
from socaity.core.socaity_service_registry import SocaityServiceRegistry
from media_toolkit import MediaFile, ImageFile, VideoFile, AudioFile
from fastsdk import FastSDK

service_manager = FastSDK().service_manager = SocaityServiceRegistry()

def install(service_name_or_id: str) -> None:
    if service_name_or_id == "all":
        service_manager.install_all()
    else:
        service_manager.install_service(service_name_or_id)

# Dynamic resolution of official services at the top level
from socaity.core._dynamic_resolver import create_resolver
_resolve_official = create_resolver("official")

def __getattr__(name: str):
    return _resolve_official(name)

__all__ = ["install", "service_manager", "MediaFile", "ImageFile", "VideoFile", "AudioFile"]
```

This allows `from socaity import face2face` — official services are available at the
package root.

### Stub generation (fastsdk)

A new Jinja2 template `stub_template.j2` produces `.pyi` files:

```jinja2
from fastsdk import FastClient, APISeex
{%- if imports_typing %}
from typing import {{ imports_typing }}
{% endif %}
{%- if imports_media_toolkit %}
from media_toolkit import {{ imports_media_toolkit }}
{% endif %}

class {{ class_name }}(FastClient):
    """
    {{ service.description or service.short_desc or "" }}
    """
    def __init__(self, api_key: str = None) -> None: ...
    {% for endpoint in endpoints %}
    def {{ endpoint.method_name }}(
        self,
        {%- for param in endpoint.parameters %}
        {{ param.name }}
        {%- if param.default_value %}: {{ param.type_hint }} = {{ param.default_value }}
        {%- elif param.optional %}: Optional[{{ param.type_hint }}] = None
        {%- else %}: {{ param.type_hint }}
        {%- endif %},
        {%- endfor %}
        **kwargs,
    ) -> APISeex:
        """
        {{ endpoint.description | trim }}
        {% if endpoint.parameters and not endpoint.description_contains_args %}

        Args:
            {% for param in endpoint.parameters -%}
            {{ param.name }}: {{ param.description or "No description available." }}
            {%- if param.default_value %} Defaults to {{ param.default_value }}.{% elif param.optional %} Optional.{% endif %}
            {% endfor -%}
        {% endif %}
        """
        ...
    {% endfor %}
    {%- if endpoints %}
    run = {{ endpoints[0].method_name }}
    __call__ = {{ endpoints[0].method_name }}
    {%- endif %}
```

A new function `create_stub()` in `sdk_factory.py` uses this template:

```python
def create_stub(
    service_definition: ServiceDefinition,
    save_path: str | Path,
    class_name: str | None = None,
) -> tuple[str, str]:
    """
    Generate a .pyi stub file for a service definition.
    Returns (file_path, class_name).
    """
    # Same data preparation as create_sdk() but renders stub_template.j2
    # and writes to a .pyi file instead of .py.
    ...
```

---

## 6. Refactoring Plan

### Phase 1: Foundation — new modules and templates

#### 1.1 Create `stub_template.j2` in fastsdk

**File**: `fastsdk/fastsdk/sdk_factory/stub_template.j2`

Create the Jinja2 template shown in Section 5. It mirrors the existing `sdk_template.j2`
structure but replaces method bodies with `...` and saves as `.pyi`.

#### 1.2 Add `create_stub()` to `sdk_factory.py`

**File**: `fastsdk/fastsdk/sdk_factory/sdk_factory.py`

Add a new function `create_stub()` that:
- Accepts `ServiceDefinition`, `save_path` (ending in `.pyi`), and optional `class_name`.
- Reuses the existing `_prepare_endpoint_data()`, `_detect_required_imports()`, and
  `_get_type_hint()` helpers (no duplication).
- Renders `stub_template.j2` instead of `sdk_template.j2`.
- Returns `(file_path, class_name)`.

Update `fastsdk/fastsdk/sdk_factory/__init__.py` to export `create_stub`.

#### 1.3 Create `_dynamic_resolver.py` in socaity

**File**: `socaity/socaity/core/_dynamic_resolver.py`

Implement the resolver module as shown in Section 5. Key components:
- `_load_import_index()` — reads `import_index.json`.
- `_load_service_definition(service_id)` — reads cached JSON.
- `_build_client_class(service_def, class_name)` — dynamic `type()` call.
- `create_resolver(namespace)` — returns a `__getattr__` closure.

### Phase 2: Restructure socaity directory layout

#### 2.1 Create new package directories

Create the following directories with placeholder `__init__.py` files:
- `socaity/socaity/official/__init__.py`
- `socaity/socaity/replicate/__init__.py`

Each `__init__.py` contains:
```python
from socaity.core._dynamic_resolver import create_resolver
__getattr__ = create_resolver("<namespace>")
```

#### 2.2 Move cache directory

Move `socaity/socaity/sdk/cache/` to `socaity/socaity/cache/`.

Update all references to the cache path:
- `SocaityServiceRegistry.CACHE_DIR`
- `_dynamic_resolver.py` CACHE_DIR
- `pyproject.toml` package-data glob

#### 2.3 Update `pyproject.toml`

```toml
[tool.setuptools.package-data]
socaity = [
    "cache/**/*.json",
    "**/*.pyi",
]
```

The `**/*.pyi` glob ensures stub files are included in the built package.

### Phase 3: Refactor `SocaityServiceRegistry`

#### 3.1 Update path constants

**File**: `socaity/socaity/core/socaity_service_registry.py`

```python
class SocaityServiceRegistry(Registry):
    PKG_ROOT = Path(__file__).parent.parent          # socaity/
    CACHE_DIR = PKG_ROOT / "cache"
    OFFICIAL_DIR = PKG_ROOT / "official"
    REPLICATE_DIR = PKG_ROOT / "replicate"
    IMPORT_INDEX_PATH = CACHE_DIR / "import_index.json"
    RESERVED_NAMESPACES = {"core", "cli", "sdk", "official", "replicate", "cache"}
```

#### 3.2 Rewrite `_get_save_path()` to return `.pyi` paths

```python
def _get_save_path(self, provider, service_id, display_name, is_official=False) -> Path:
    if provider.lower() == "replicate":
        username, model_name = display_name.split("/", 1) if "/" in display_name else ("official", display_name)
        username = normalize_name_for_py(username)
        model_name = normalize_name_for_py(model_name)
        return self.REPLICATE_DIR / username / f"{model_name}.pyi"

    class_name = normalize_name_for_py(display_name)
    if is_official:
        return self.OFFICIAL_DIR / f"{class_name}.pyi"
    else:
        username = normalize_name_for_py(update_item.get("username", "community"))
        return self.PKG_ROOT / username / f"{class_name}.pyi"
```

#### 3.3 Rewrite `_handle_model_update()` to call `create_stub()`

Replace the call to `create_sdk()` with `create_stub()`:

```python
from fastsdk.sdk_factory import create_stub

def _handle_model_update(self, update_item):
    ...
    save_path = self._get_save_path(provider, service_id, display_name, is_official)

    file_path, actual_class_name = create_stub(
        service_definition=service_def,
        save_path=str(save_path),
        class_name=class_name
    )
    self._created_stubs[actual_class_name] = Path(file_path)

    # Save service definition to cache
    self.service_store.save_service(service_def)

    # Update the import index
    namespace = self._get_namespace(provider, display_name, is_official, update_item)
    self._update_import_index(namespace, actual_class_name, service_id)
```

#### 3.4 Replace `_update_init_files()` with `_update_stub_indexes()`

Instead of writing import lines to `__init__.py`, the new method:

1. Ensures each namespace directory has an `__init__.py` with `create_resolver(...)`.
2. Generates `__init__.pyi` in each namespace directory with re-export lines.
3. Generates `socaity/__init__.pyi` with re-exports for official services.

```python
def _update_stub_indexes(self):
    """Regenerate __init__.pyi re-exports and ensure __init__.py routers exist."""
    index = self._load_import_index()

    for namespace, services in index.get("namespaces", {}).items():
        ns_dir = self.PKG_ROOT / namespace.replace("/", os.sep)
        ns_dir.mkdir(parents=True, exist_ok=True)

        # Ensure __init__.py with resolver exists
        init_py = ns_dir / "__init__.py"
        if not init_py.exists() or "_dynamic_resolver" not in init_py.read_text():
            init_py.write_text(
                f'from socaity.core._dynamic_resolver import create_resolver\n'
                f'__getattr__ = create_resolver("{namespace}")\n'
            )

        # Generate __init__.pyi with re-exports
        lines = []
        for service_name in sorted(services.keys()):
            lines.append(f"from .{service_name} import {service_name} as {service_name}")
        (ns_dir / "__init__.pyi").write_text("\n".join(lines) + "\n")

    # Top-level __init__.pyi re-exports officials
    official_services = index.get("namespaces", {}).get("official", {})
    if official_services:
        lines = []
        for name in sorted(official_services.keys()):
            lines.append(f"from .official.{name} import {name} as {name}")
        # Append existing non-service exports
        lines.extend([
            "",
            "from media_toolkit import MediaFile, ImageFile, VideoFile, AudioFile",
            "",
            "def install(service_name_or_id: str) -> None: ...",
        ])
        (self.PKG_ROOT / "__init__.pyi").write_text("\n".join(lines) + "\n")
```

#### 3.5 Add `_update_import_index()` and `_load_import_index()` helpers

```python
def _load_import_index(self) -> dict:
    if self.IMPORT_INDEX_PATH.exists():
        return json.loads(self.IMPORT_INDEX_PATH.read_text())
    return {"namespaces": {}}

def _save_import_index(self, index: dict):
    self.IMPORT_INDEX_PATH.write_text(json.dumps(index, indent=2))

def _update_import_index(self, namespace: str, service_name: str, service_id: str):
    index = self._load_import_index()
    ns = index.setdefault("namespaces", {}).setdefault(namespace, {})
    ns[service_name] = service_id
    self._save_import_index(index)

def _get_namespace(self, provider, display_name, is_official, update_item) -> str:
    if provider.lower() == "replicate":
        username, _ = display_name.split("/", 1) if "/" in display_name else ("official", display_name)
        return f"replicate/{normalize_name_for_py(username)}"
    if is_official:
        return "official"
    username = normalize_name_for_py(update_item.get("username", "community"))
    return username
```

#### 3.6 Update deletion handling

Update `_handle_model_deletion()` to:
- Delete the `.pyi` stub file (not `.py`).
- Remove the entry from `import_index.json`.
- Regenerate `__init__.pyi` for the affected namespace.

### Phase 4: Update `socaity/__init__.py`

**File**: `socaity/socaity/__init__.py`

```python
from socaity.core.socaity_service_registry import SocaityServiceRegistry
from media_toolkit import MediaFile, ImageFile, VideoFile, AudioFile
from fastsdk import FastSDK

service_manager = FastSDK().service_manager = SocaityServiceRegistry()

def install(service_name_or_id: str) -> None:
    if service_name_or_id == "all":
        service_manager.install_all()
    else:
        service_manager.install_service(service_name_or_id)

# Official services are importable from the top level: from socaity import face2face
from socaity.core._dynamic_resolver import create_resolver
_resolve_official = create_resolver("official")

def __getattr__(name: str):
    return _resolve_official(name)

__all__ = ["install", "service_manager", "MediaFile", "ImageFile", "VideoFile", "AudioFile"]
```

### Phase 5: Clean up old system

#### 5.1 Remove old `socaity/sdk/` directory

Delete the entire `socaity/sdk/` tree (except keep cache data and migrate it to
`socaity/cache/`).

Specifically remove:
- `socaity/sdk/__init__.py`
- `socaity/sdk/official/` (all `.py` files)
- `socaity/sdk/replicate/` (all `.py` files and `__init__.py` files)
- `socaity/sdk/community/`

#### 5.2 Remove `_created_sdks` / `_deleted_sdks` tracking in `SocaityServiceRegistry`

Replace with `_created_stubs` / `_deleted_stubs` if needed, or simplify by reading
directly from `import_index.json`.

#### 5.3 Update `fastsdk/__init__.py` exports

Export the new `create_stub` alongside existing `create_sdk`:

```python
from .sdk_factory import create_sdk, create_stub
```

### Phase 6: Reserved namespace protection

Add validation in `SocaityServiceRegistry._get_namespace()`:

```python
RESERVED_NAMESPACES = {"core", "cli", "sdk", "official", "replicate", "cache", "__pycache__"}

def _get_namespace(self, provider, display_name, is_official, update_item) -> str:
    ...
    if namespace in self.RESERVED_NAMESPACES:
        namespace = f"u_{namespace}"
    return namespace
```

### Migration checklist

| Step | Action | Files changed |
|------|--------|---------------|
| 1.1 | Create `stub_template.j2` | `fastsdk/fastsdk/sdk_factory/stub_template.j2` |
| 1.2 | Add `create_stub()` | `fastsdk/fastsdk/sdk_factory/sdk_factory.py`, `__init__.py` |
| 1.3 | Create `_dynamic_resolver.py` | `socaity/socaity/core/_dynamic_resolver.py` |
| 2.1 | Create `official/`, `replicate/` dirs | `socaity/socaity/official/__init__.py`, `socaity/socaity/replicate/__init__.py` |
| 2.2 | Move cache | `socaity/socaity/cache/` |
| 2.3 | Update pyproject.toml | `socaity/pyproject.toml` |
| 3.1 | Update path constants | `socaity/socaity/core/socaity_service_registry.py` |
| 3.2 | `.pyi` save paths | `socaity/socaity/core/socaity_service_registry.py` |
| 3.3 | Call `create_stub()` | `socaity/socaity/core/socaity_service_registry.py` |
| 3.4 | Stub index generation | `socaity/socaity/core/socaity_service_registry.py` |
| 3.5 | Import index helpers | `socaity/socaity/core/socaity_service_registry.py` |
| 3.6 | Deletion handling | `socaity/socaity/core/socaity_service_registry.py` |
| 4 | Top-level `__init__.py` | `socaity/socaity/__init__.py` |
| 5.1 | Remove old `sdk/` | `socaity/socaity/sdk/` |
| 5.2 | Clean tracking dicts | `socaity/socaity/core/socaity_service_registry.py` |
| 5.3 | Export `create_stub` | `fastsdk/fastsdk/__init__.py`, `fastsdk/fastsdk/sdk_factory/__init__.py` |
| 6 | Namespace protection | `socaity/socaity/core/socaity_service_registry.py` |
