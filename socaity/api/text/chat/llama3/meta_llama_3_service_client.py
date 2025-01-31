from fastsdk.definitions.ai_model import AIModelDescription
from fastsdk.definitions.enums import ModelDomainTag
from fastsdk.web.service_client import ServiceClient
from socaity import DEFAULT_SOCAITY_URL, DEFAULT_REPLICATE_URL
from socaity.api.text.chat.llama3.meta_llama3_schema import MetaLlama3_Input


srvc_meta_llama_3_8b = ServiceClient(
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/meta-llama-3-8b",
        "replicate": f"{DEFAULT_REPLICATE_URL}/meta/meta-llama-3-8b",
    },
    service_name="meta-llama-3-8b",
    model_description=AIModelDescription(
        model_name="meta-llama-3-8b",
        model_domain_tags=[ModelDomainTag.TEXT],
        model_tags=["llm"],
    )
)

srvc_meta_llama_3_8b.add_endpoint(endpoint_route="/chat", body_params=MetaLlama3_Input(), refresh_interval_s=0.5)

srvc_meta_llama_3_70b = ServiceClient(
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/meta-llama-3-70b",
        "replicate": f"{DEFAULT_REPLICATE_URL}/meta/meta-llama-3-8b",
    },
    service_name="meta-llama-3-70b",
    model_description=AIModelDescription(
        model_name="meta-llama-3-70b",
        model_domain_tags=[ModelDomainTag.TEXT],
        model_tags=["llm"]
    )
)

srvc_meta_llama_3_70b.add_endpoint(endpoint_route="/chat", body_params=MetaLlama3_Input(), refresh_interval_s=0.5)