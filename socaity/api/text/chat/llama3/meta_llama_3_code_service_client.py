from fastsdk.definitions.ai_model import AIModelDescription
from fastsdk.definitions.enums import ModelDomainTag
from fastsdk.web.api_client import APIClient
from socaity.settings import DEFAULT_SOCAITY_URL, DEFAULT_REPLICATE_URL
from socaity.api.text.chat.llama3.meta_llama3_schema import MetaCodeLlama3_Input

srvc_codellama_13b = APIClient(
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/codellama-13b",
        "replicate": f"{DEFAULT_REPLICATE_URL}/meta/codellama-13b",
        "socaity_local": f"http://localhost:8000/v0/codellama-70b-python",
    },
    service_name="codellama-13b",
    model_description=AIModelDescription(
        model_name="codellama-13b",
        model_domain_tags=[ModelDomainTag.TEXT],
    ),
)

srvc_codellama_13b.add_endpoint(endpoint_route="/chat", query_params=MetaCodeLlama3_Input(), refresh_interval_s=5)


srvc_codellama_70b_python = APIClient(
    service_urls={
        "socaity": f"{DEFAULT_SOCAITY_URL}/codellama-70b-python",
        "replicate": "https://replicate.com/meta/codellama-70b-python",
    },
    service_name="codellama-70b-python",
    model_description=AIModelDescription(
        model_name="codellama-70b-python",
        model_domain_tags=[ModelDomainTag.TEXT],
    ),
)

srvc_codellama_70b_python.add_endpoint(endpoint_route="/chat", query_params=MetaCodeLlama3_Input(), refresh_interval_s=5)
