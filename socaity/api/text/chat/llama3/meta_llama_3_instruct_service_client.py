from fastsdk.definitions.ai_model import AIModelDescription
from fastsdk.definitions.enums import ModelDomainTag
from fastsdk.web.service_client import ServiceClient
from socaity import DEFAULT_SOCAITY_URL, DEFAULT_REPLICATE_URL
from socaity.api.text.chat.llama3.meta_llama3_schema import MetaLlama3_InstructInput

srvc_meta_llama_3_8b_instruct = ServiceClient(
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/meta-llama-3-8b-instruct",
        "replicate": f"{DEFAULT_REPLICATE_URL}/meta/meta-llama-3-8b-instruct",
    },
    service_name="meta-llama-3-8b-instruct",
    model_description=AIModelDescription(
        model_name="meta-llama-3-8b-instruct",
        model_domain_tags=[ModelDomainTag.TEXT]
    ),
)

srvc_meta_llama_3_8b_instruct.add_endpoint(
    endpoint_route="/chat",
    body_params=MetaLlama3_InstructInput(),
    refresh_interval_s=5,
)



srvc_meta_llama_3_70b_instruct = ServiceClient(
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/meta-llama-3-70b-instruct",
        "replicate": f"{DEFAULT_REPLICATE_URL}/meta/meta-llama-3-70b-instruct",
    },
    service_name="meta-llama-3-70b-instruct",
    model_description=AIModelDescription(
        model_name="meta-llama-3-70b-instruct",
        model_domain_tags=[ModelDomainTag.TEXT]
    ),
)

srvc_meta_llama_3_70b_instruct.add_endpoint(
    endpoint_route="/chat",
    body_params=MetaLlama3_InstructInput(),
    refresh_interval_s=5,
)
