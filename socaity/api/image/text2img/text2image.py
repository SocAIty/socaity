from abc import abstractmethod
from typing import Union, List

import media_toolkit as mt

class _BaseText2Image:

    @abstractmethod
    def text2img(self, text, *args, **kwargs) -> Union[mt.ImageFile, List[mt.ImageFile], None]:
        """
        Converts text to an image
        :param text: The text to convert to an image
        :return: The image
        """
        raise NotImplementedError("Please implement this method")


# Factory method for generalized model_hosting_info calling
def text2img(text, model="flux-schnell", service="socaity", *args, **kwargs) -> Union[mt.ImageFile, List[mt.ImageFile], None]:
    if model == "flux-schnell":
        from .flux_schnell import FluxSchnell
        s = FluxSchnell(service=service)
        return s.text2img(text, *args, **kwargs)

    return None
