from fastsdk import ImageFile, VideoFile
from fastsdk.definitions.ai_model import AIModelDescription
from fastsdk.definitions.enums import ModelDomainTag, ModelTag
from fastsdk.web.req.cloud_storage.cloud_storage_factory import create_cloud_storage
from fastsdk.web.service_client import ServiceClient
from socaity.settings import (DEFAULT_SOCAITY_URL, AZURE_SAS_ACCESS_TOKEN,
                              AZURE_SAS_CONNECTION_STRING, S3_ENDPOINT_URL, S3_ACCESS_KEY_ID, S3_ACCESS_KEY_SECRET)

srvc_face2face = ServiceClient(
    service_name="face2face",
    service_description="Instantly swap faces in images and videos. Face restoration and recognition.",
    service_urls={
        "localhost": "localhost:8020/api",
        "runpod": "https://api.runpod.ai/v2/5vuwqrpymiueqr",
        "socaity": f"{DEFAULT_SOCAITY_URL}/face2face/api"
    },
    model_description=AIModelDescription(
        model_name="face2face",
        model_domain_tags=[ModelDomainTag.IMAGE, ModelDomainTag.AUDIO],
        model_tags=[ModelTag.FACE2FACE, ModelTag.IMAGE2IMAGE]
    ),
    cloud_storage=create_cloud_storage(
        azure_sas_access_token=AZURE_SAS_ACCESS_TOKEN,
        azure_connection_string=AZURE_SAS_CONNECTION_STRING,
        s3_endpoint_url=S3_ENDPOINT_URL,
        s3_access_key_id=S3_ACCESS_KEY_ID,
        s3_access_key_secret=S3_ACCESS_KEY_SECRET
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

