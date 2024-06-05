from socaity.socaity_client.definitions.enums import ModelDomainTag, ModelTag
from socaity.socaity_client.web.service_client import ServiceClient


srvc_face2face = ServiceClient(
    service_url="localhost:8020/api",
    model_name="face2face",
    model_domain_tags=[ModelDomainTag.IMAGE, ModelDomainTag.AUDIO],
    model_tags=[ModelTag.FACE2FACE, ModelTag.IMAGE2IMAGE]
)

srvc_face2face.add_endpoint(endpoint_route="swap_from_reference_face",
                            file_params={"source_img": bytes, "target_img": bytes})
srvc_face2face.add_endpoint(
    endpoint_route="add_reference_face",
    post_params={"face_name": str},
    file_params={"source_img": bytes}
)
srvc_face2face.add_endpoint(
    endpoint_route="/swap_one",
    file_params={"source_img": bytes, "target_img": bytes}

)
srvc_face2face.add_endpoint(endpoint_route="status", get_params={"job_id": str})

