from fastsdk.jobs.threaded.internal_job import InternalJob
from fastsdk.fast_sdk import fastSDK, fastJob
from socaity.api.text.chat.i_chat import _BaseChat
from socaity.api.text.chat.llama3.meta_llama_3_code_service_client import srvc_codellama_13b, srvc_codellama_70b


class _BaseMetaLlama3_Code(_BaseChat):
    """
    Base version of Llama 3, an 8 billion parameter language model from Meta.
    """
    @fastJob
    def _chat(self, job,
              prompt: str,
              system_prompt: str,
              max_new_tokens: int = 512,
              temperature: float = 0.5,
              top_p: float =0.9,
              length_penalty: float = 1.15,
              stop_sequences: str = "<|end_of_text|>,<|eot_id|>",
              presence_penalty: float = 0.0,
              frequency_penalty: float = 0.2,
              repeat_penalty: float = 1.1,
              **kwargs) -> str:
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
            repeat_penalty=repeat_penalty,
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


@fastSDK(service_client=srvc_codellama_13b)
class MetaLLama3_13b_code(_BaseMetaLlama3_Code):
    """
    Llama 3, an 8 billion parameter language model from Meta.
    """
    pass

@fastSDK(service_client=srvc_codellama_70b)
class MetaLLama3_70b_code(_BaseMetaLlama3_Code):
    """
    Llama 3, a language model from Meta.
    """
    pass