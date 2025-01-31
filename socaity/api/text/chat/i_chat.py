from abc import abstractmethod

class _BaseChat:
    @abstractmethod
    def chat(self, prompt: str, *args, **kwargs) -> str:
        """
        Converts text to an image
        :param text: The text to convert to an image
        :return: The image
        """
        raise NotImplementedError("Please implement this method")


# Factory method for generalized model_hosting_info calling
def chat(prompt: str, model="flux-schnell", service="socaity", *args, **kwargs) -> str:
    return None
