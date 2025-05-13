from fastsdk.definitions.ai_model import AIModelDescription
from fastsdk.definitions.enums import ModelDomainTag
from fastsdk.client.api_client import APIClient
from socaity.settings import DEFAULT_SOCAITY_URL, DEFAULT_REPLICATE_URL
from socaity.api.text.chat.llama3.meta_llama3_schema import MetaLlama3_InstructInput

srvc_meta_llama_3_8b_instruct = APIClient(
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/meta-llama-3-8b-instruct",
        "replicate": f"{DEFAULT_REPLICATE_URL}/meta/meta-llama-3-8b-instruct",
        "socaity_local": f"http://localhost:8000/v0/meta-llama-3-8b-instruct",
    },
    service_name="meta-llama-3-8b-instruct",
    model_description=AIModelDescription(
        model_name="meta-llama-3-8b-instruct",
        model_domain_tags=[ModelDomainTag.TEXT]
    ),
)

srvc_meta_llama_3_8b_instruct.add_endpoint(
    endpoint_route="/chat",
    query_params=MetaLlama3_InstructInput(),
    refresh_interval_s=5,
)



srvc_meta_llama_3_70b_instruct = APIClient(
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/meta-llama-3-70b-instruct",
        "replicate": f"{DEFAULT_REPLICATE_URL}/meta/meta-llama-3-70b-instruct",
        "socaity_local": f"http://localhost:8000/v0/meta-llama-3-70b-instruct",
    },
    service_name="meta-llama-3-70b-instruct",
    model_description=AIModelDescription(
        model_name="meta-llama-3-70b-instruct",
        model_domain_tags=[ModelDomainTag.TEXT]
    ),
)

srvc_meta_llama_3_70b_instruct.add_endpoint(
    endpoint_route="/chat",
    query_params=MetaLlama3_InstructInput(),
    refresh_interval_s=5,
)
