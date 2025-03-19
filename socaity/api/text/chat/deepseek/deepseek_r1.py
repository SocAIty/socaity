from fastsdk.jobs.threaded.internal_job import InternalJob
from fastsdk.fast_sdk import fastSDK, fastJob
from socaity.api.text.chat.i_chat import _BaseChat
from .deepseek_r1_service_client import srvc_deep_seek_r1


class _BaseDeepSeekR1(_BaseChat):
    """
    """
    @fastJob
    def _chat(self, job,
              prompt: str,
              max_tokens: int = 20480,
              temperature: float = 0.1,
              presence_penalty: float = 0.0,
              frequency_penalty: float = 0.0,
              top_p: float = 1.0,
              **kwargs
        ) -> str:
        response = job.request(
            endpoint_route="/chat",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            top_p=top_p,
            **kwargs,
        )
        result = response.get_result()
        if response.error:
            raise Exception(f"Error in generate_text: {response.error}")

        if isinstance(result, list):
            result = "".join(result)

        return result

    def chat(self,
        prompt: str,
        max_tokens: int = 20480,
        temperature: float = 0.1,
        presence_penalty: float = 0.0,
        frequency_penalty: float = 0.0,
        top_p: float = 1.0, **kwargs) -> InternalJob:
        """
        Generate text from the provided prompt.
        :param prompt: The input text prompt.
        :param max_tokens: Maximum number of tokens to generate.
        :param temperature: Sampling temperature for generation.
        """
        return self._chat(
            prompt=prompt, max_tokens=max_tokens, temperature=temperature,
            presence_penalty=presence_penalty, frequency_penalty=frequency_penalty, top_p=top_p,
            **kwargs
        )

    def pretty(self, answer: str, exclude_thoughts: bool = True):
        if exclude_thoughts:
            pos_think = answer.find("<think>")
            end_think = answer.rfind("</think>")
            if pos_think > -1:
                pos_think += len("<think>")
                #thoughts = answer[pos_think+len("<think>"):end_think]
                answer = answer[end_think+len("</think>"):]

        return answer


@fastSDK(api_client=srvc_deep_seek_r1)
class DeepSeekR1(_BaseDeepSeekR1):
    """
    DeepSeekR1 is the SOTA thinking model of DeepSeek
    """
