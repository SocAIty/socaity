from fastsdk.definitions.ai_model import AIModelDescription
from fastsdk.definitions.enums import ModelDomainTag
from fastsdk.web.service_client import ServiceClient
from socaity.settings import DEFAULT_SOCAITY_URL, DEFAULT_REPLICATE_URL
from socaity.api.text.chat.deepseek.deepseek_r1_schema import DeepSeekR1_Input


srvc_deep_seek_r1 = ServiceClient(
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/deepseek-r1",
        "replicate": f"{DEFAULT_REPLICATE_URL}/deepseek-ai/deepseek-r1",
    },
    service_name="deepseek-r1",
    model_description=AIModelDescription(
        model_name="deepseek-r1",
        model_domain_tags=[ModelDomainTag.TEXT],
        model_tags=["llm"],
    )
)

srvc_deep_seek_r1.add_endpoint(endpoint_route="/chat", query_params=DeepSeekR1_Input(), refresh_interval_s=0.5)
