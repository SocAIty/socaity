from abc import abstractmethod

class _BaseChat:
    @abstractmethod
    def chat(self, prompt: str, *args, **kwargs) -> str:
        """
        Prompts an LLM.
        :param text: The text to prompt the LLM with.
        :return: The generated response from the llm.
        """
        raise NotImplementedError("Please implement this method")


# Factory method for generalized model_hosting_info calling
def chat(prompt: str, model="meta-llama-3", service="socaity", *args, **kwargs) -> str:
    return None
