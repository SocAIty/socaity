import random

from fastsdk.jobs.threaded.internal_job import InternalJob
from fastsdk.fast_sdk import fastSDK, fastJob
from socaity.api.text.chat.i_chat import _BaseChat
from socaity.api.text.chat.llama3.meta_llama_3_instruct_service_client import srvc_meta_llama_3_70b_instruct, \
    srvc_meta_llama_3_8b_instruct


class _BaseMetaLlama3_Instruct(_BaseChat):
    """
    Base version of Llama 3, an 8 billion parameter language model from Meta.
    """
    @fastJob
    def _chat(self, job,
              prompt: str,
              system_prompt: str = "You are a helpful assistant",
              max_new_tokens: int = 512,
              temperature: float = 0.5,
              top_p: float = 0.9,
              length_penalty: float = 1.15,
              stop_sequences: str = "<|end_of_text|>,<|eot_id|>",
              presence_penalty: float = 0.0,
              frequency_penalty: float = 0.2,
              prompt_template: str = """
                <|begin_of_text|><|start_header_id|>system<|end_header_id|>
                You are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>
                {prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
              """,
              seed: int = None,
              **kwargs) -> str:

        if seed is None or not isinstance(seed, int):
            seed = random.randint(0, 1000000)

        response = job.request(
            endpoint_route="/chat",
            prompt=prompt,
            system_prompt=system_prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            length_penalty=length_penalty,
            top_p=top_p,
            stop_sequences=stop_sequences,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            prompt_template=prompt_template,
            seed=seed,
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


@fastSDK(service_client=srvc_meta_llama_3_8b_instruct)
class MetaLLama3_8b_instruct(_BaseMetaLlama3_Instruct):
    """
    Llama 3, an 8 billion parameter language model from Meta.
    """
    pass

@fastSDK(service_client=srvc_meta_llama_3_70b_instruct)
class MetaLLama3_70b_instruct(_BaseMetaLlama3_Instruct):
    """
    Llama 3, an 8 billion parameter language model from Meta.
    """
    pass