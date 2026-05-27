import os
import importlib
from pathlib import Path

from media_toolkit import MediaFile, ImageFile, VideoFile, AudioFile
from fastsdk import FastSDK, FastClient
from apipod_registry.utils.normalization import normalize_name_for_py
from socaity.core.socaity_service_registry import SocaityServiceRegistry

service_registry = FastSDK().service_registry = SocaityServiceRegistry()

# Extend package search path so namespace imports resolve through sdk/:
#   socaity.official       -> socaity/sdk/official/
#   socaity.replicate.X    -> socaity/sdk/replicate/X/
#   socaity.{username}     -> socaity/sdk/community/{username}/
_sdk_root = Path(__file__).parent / "sdk"
__path__.append(str(_sdk_root))

_community_root = _sdk_root / "community"
if _community_root.exists():
    __path__.append(str(_community_root))


def install(service_name_or_id: str) -> None:
    """Install a specific service by name or ID."""
    if service_name_or_id == "all":
        service_registry.install_all()
    else:
        service_registry.install_service(service_name_or_id)


def run(service_name_or_id: str, *, api_key: str = None, **inputs):
    """Install if needed, run a model, and return its result in one call.

    A shortcut over the install, import and call steps:

        img = socaity.run("black-forest-labs/flux-schnell", prompt="a neon fox")
        img.save("fox.png")

    api_key defaults to the SOCAITY_API_KEY environment variable.
    """
    model_cls = _resolve_model_class(service_name_or_id)
    if model_cls is None:
        install(service_name_or_id)
        model_cls = _resolve_model_class(service_name_or_id)
    if model_cls is None:
        raise ValueError(f"Could not resolve or install service '{service_name_or_id}'.")
    model = model_cls(api_key=api_key or os.getenv("SOCAITY_API_KEY"))
    return model(**inputs).get_result()


def _resolve_model_class(service_name_or_id: str):
    """Return the generated FastClient subclass for a service, or None if not installed yet."""
    service_def = service_registry.get_service(service_name_or_id)
    if service_def is not None:
        try:
            module = importlib.import_module(
                f"socaity.sdk.services.{normalize_name_for_py(service_def.id)}"
            )
            for value in vars(module).values():
                if isinstance(value, type) and issubclass(value, FastClient) and value is not FastClient:
                    return value
        except ModuleNotFoundError:
            pass
    # Fallback: resolve via the public replicate namespace (vendor/model)
    if "/" in service_name_or_id:
        vendor, model = service_name_or_id.split("/", 1)
        try:
            namespace = importlib.import_module(f"socaity.replicate.{normalize_name_for_py(vendor)}")
            return getattr(namespace, normalize_name_for_py(model), None)
        except ModuleNotFoundError:
            pass
    return None


# Re-export official services at top level: from socaity import face2face
try:
    from socaity.sdk.official import *  # noqa: F401,F403
except ImportError:
    pass

__all__ = ["install", "run", "service_registry", "MediaFile", "ImageFile", "VideoFile", "AudioFile"]
