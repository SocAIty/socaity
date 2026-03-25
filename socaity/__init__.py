from pathlib import Path

from media_toolkit import MediaFile, ImageFile, VideoFile, AudioFile
from fastsdk import FastSDK
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


# Re-export official services at top level: from socaity import face2face
try:
    from socaity.sdk.official import *  # noqa: F401,F403
except ImportError:
    pass

__all__ = ["install", "service_registry", "MediaFile", "ImageFile", "VideoFile", "AudioFile"]
