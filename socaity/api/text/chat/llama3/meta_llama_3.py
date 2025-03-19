import random

from fastsdk.jobs.threaded.internal_job import InternalJob
from fastsdk.fast_sdk import fastSDK, fastJob
from socaity.api.text.chat.i_chat import _BaseChat
from socaity.api.text.chat.llama3.meta_llama_3_service_client import srvc_meta_llama_3_8b, srvc_meta_llama_3_70b


class _BaseMetaLlama3(_BaseChat):
    """
    Base version of Llama 3, an 8 billion parameter language model from Meta.
    """
    @fastJob
    def _chat(self, job,
              prompt: str, max_tokens: int = 512, temperature: float = 0.5, top_p: float =0.9,
              presence_penalty: float = 1.15, frequency_penalty: float = 0.2,
              prompt_template: str = "{prompt}",
              seed: int = None,
              **kwargs) -> str:

        if seed is None or not isinstance(seed, int):
            seed = random.randint(0, 1000000)

        response = job.request(
            endpoint_route="/chat",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            seed=seed,
            prompt_template=prompt_template,
            **kwargs,
        )
        result = response.get_result()
        if response.error:
            raise Exception(f"Error in generate_text: {response.error}")

        if isinstance(result, list):
            result = "".join(result)

        return result

    def chat(self, prompt: str, max_tokens: int = 512, temperature: float = 0.5, **kwargs) -> InternalJob:
        """
        Generate text from the provided prompt.
        :param prompt: The input text prompt.
        :param max_tokens: Maximum number of tokens to generate.
        :param temperature: Sampling temperature for generation.
        """
        return self._chat(prompt=prompt, max_tokens=max_tokens, temperature=temperature, **kwargs)


@fastSDK(api_client=srvc_meta_llama_3_8b)
class MetaLLama3_8b(_BaseMetaLlama3):
    """
    Llama 3, an 8 billion parameter language model from Meta.
    """
    pass

@fastSDK(api_client=srvc_meta_llama_3_70b)
class MetaLLama3_70b(_BaseMetaLlama3):
    """
    Llama 3, an 8 billion parameter language model from Meta.
    """
    pass