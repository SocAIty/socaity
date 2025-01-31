from fastsdk import ImageFile, VideoFile
from fastsdk.definitions.ai_model import AIModelDescription
from fastsdk.definitions.enums import ModelDomainTag
from fastsdk.web.definitions.service_adress import SocaityServiceAddress
from fastsdk.web.service_client import ServiceClient
from socaity.settings import DEFAULT_SOCAITY_URL


srvc_face2face = ServiceClient(
    service_name="face2face",
    service_description="Instantly swap faces in images and videos. Face restoration and recognition.",
    service_urls={
        "localhost": "localhost:8020/api",
        "runpod": "https://api.runpod.ai/v2/v1n4b07cwp2mbo",
        "runpod_localhost": "http://localhost:8020/",
        "socaity": f"{DEFAULT_SOCAITY_URL}/face2face/api",
        "socaity_local1": SocaityServiceAddress("http://localhost:8000/api/v0/face2face"),
        "socaity_local": "http://localhost:8000/api/v0/face2face"
    },
    model_description=AIModelDescription(
        model_name="face2face",
        model_domain_tags=[ModelDomainTag.IMAGE, ModelDomainTag.AUDIO]
    )
)
srvc_face2face.add_endpoint(
    endpoint_route="/swap_img_to_img",
    query_params={"enhance_face_model": str},
    file_params={"source_img": ImageFile, "target_img": ImageFile}
)
srvc_face2face.add_endpoint(
    endpoint_route="/swap",
    query_params={"faces": str, "enhance_face_model": str},
    file_params={"media": ImageFile}
)
srvc_face2face.add_endpoint(
    endpoint_route="/add_face",
    query_params={"face_name": str, "save": bool},
    file_params={"image": ImageFile}
)
srvc_face2face.add_endpoint(
    endpoint_route="/swap_video",
    query_params={"face_name": str, "include_audio": bool, "enhance_face_model": str},
    file_params={"target_video": VideoFile},
    refresh_interval_s=3  # check every 3 seconds for progress
)
