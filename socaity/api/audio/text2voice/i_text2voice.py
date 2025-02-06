from abc import abstractmethod
from typing import Union, List

import media_toolkit as mt

class _BaseText2Voice:

    @abstractmethod
    def text2voice(self, text, *args, **kwargs) -> Union[mt.AudioFile, List[mt.AudioFile], None]:
        """
        Converts text to an image
        :param text: The text to convert to an image
        :return: The image
        """
        raise NotImplementedError("Please implement this method")


# Factory method for generalized model_hosting_info calling
def text2voice(text, model="speechcraft", service="socaity", *args, **kwargs) -> Union[mt.AudioFile, List[mt.AudioFile], None]:
    if model == "flux-schnell":
        from .speechcraft.speechcraft_api import SpeechCraft
        s = SpeechCraft(service=service)
        return s.text2voice(text, *args, **kwargs)

    return None
