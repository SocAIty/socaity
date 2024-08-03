from fastsdk import ImageFile, VideoFile
from fastsdk.definitions.ai_model import AIModelDescription
from fastsdk.definitions.enums import ModelDomainTag, ModelTag
from fastsdk.web.service_client import ServiceClient
from socaity.settings import DEFAULT_SOCAITY_URL

srvc_face2face = ServiceClient(
    service_name="face2face",
    service_description="Instantly swap faces in images and videos. Face restoration and recognition.",
    service_urls={
        "localhost": "localhost:8020/api",
        "runpod": "localhost:8020",
        "socaity": f"{DEFAULT_SOCAITY_URL}/face2face/api"
    },
    model_description=AIModelDescription(
        model_name="face2face",
        model_domain_tags=[ModelDomainTag.IMAGE, ModelDomainTag.AUDIO],
        model_tags=[ModelTag.FACE2FACE, ModelTag.IMAGE2IMAGE]
    )
)
srvc_face2face.add_endpoint(
    endpoint_route="/swap_img_to_img",
    post_params={"enhance_face_model": str},
    file_params={"source_img": ImageFile, "target_img": ImageFile}
)
srvc_face2face.add_endpoint(
    endpoint_route="/swap",
    post_params={"faces": str, "enhance_face_model": str},
    file_params={"media": ImageFile}
)
srvc_face2face.add_endpoint(
    endpoint_route="/add_face",
    post_params={"face_name": str},
    file_params={"image": ImageFile}
)
srvc_face2face.add_endpoint(
    endpoint_route="/swap_video",
    post_params={"face_name": str, "include_audio": bool, "enhance_face_model": str},
    file_params={"target_video": VideoFile},
    refresh_interval=3  # check every 3 seconds for progress
)

srvc_face2face.add_endpoint(endpoint_route="status", get_params={"job_id": str})

