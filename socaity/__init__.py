from socaity.core.socaity_service_manager import SocaityServiceManager

from media_toolkit import MediaFile, ImageFile, VideoFile, AudioFile

from fastsdk import FastSDK
service_manager = FastSDK().service_manager = SocaityServiceManager()


def install(service_name_or_id: str) -> None:
    """Install a specific service by name or ID"""
    if service_name_or_id == "all":
        service_manager.install_all()
    else:
        service_manager.install_service(service_name_or_id)


__all__ = ["install", "service_manager", "MediaFile", "ImageFile", "VideoFile", "AudioFile"]
