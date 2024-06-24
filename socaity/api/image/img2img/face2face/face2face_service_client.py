from multimodal_files import ImageFile, VideoFile
from fastsdk.definitions.enums import ModelDomainTag, ModelTag
from fastsdk.web.service_client import ServiceClient


srvc_face2face = ServiceClient(
    service_url="localhost:8020/api",
    model_name="face2face",
    model_domain_tags=[ModelDomainTag.IMAGE, ModelDomainTag.AUDIO],
    model_tags=[ModelTag.FACE2FACE, ModelTag.IMAGE2IMAGE]
)
srvc_face2face.add_endpoint(
    endpoint_route="/swap_one",
    file_params={"source_img": ImageFile, "target_img": ImageFile}
)
srvc_face2face.add_endpoint(
    endpoint_route="swap_from_reference_face",
    post_params={"face_name": str},
    file_params={"target_img": ImageFile}
)
srvc_face2face.add_endpoint(
    endpoint_route="add_reference_face",
    post_params={"face_name": str},
    file_params={"source_img": ImageFile}
)
srvc_face2face.add_endpoint(
    endpoint_route="/swap_video_from_reference_face",
    post_params={"face_name": str},
    file_params={"target_video": VideoFile}
)

srvc_face2face.add_endpoint(endpoint_route="status", get_params={"job_id": str})

