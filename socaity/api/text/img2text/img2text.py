from abc import abstractmethod
from typing import Union, List

import media_toolkit as mt
import numpy as np

class _BaseImage2Text:

    @abstractmethod
    def image2text(self, image: Union[np.array, bytes, str, mt.ImageFile], *args, **kwargs) -> str:
        """
        Creates an image caption or description from an image.
        :param text: The text to convert to an image
        :return: The image
        """
        raise NotImplementedError("Please implement this method")

    # alias
    caption_image = image2text

    def visual_question_answering(self, image: Union[np.array, bytes, str, mt.ImageFile], question: str) -> str:
        """
        Answers a question about an image.
        :param image: The image to ask a question about
        :param question: The question to ask
        :return: The answer to the question
        """
        raise NotImplementedError("Please implement this method")

    def image_text_matching(self, image: Union[np.array, bytes, str, mt.ImageFile], caption: str) -> str:
        """
        Measures how well an image description is matched by the input image.
        :param image: The image to match
        :param caption: The caption to match
        :return: The matching score
        """
        raise NotImplementedError("Please implement this method")



def image2text(image: Union[np.array, bytes, str, mt.ImageFile], model="blip", service="socaity", *args, **kwargs) -> str:
    from .blib.blib import Blip
    names_cl = {
        "blib": Blip,
    }
    names_cl = {k.lower().replace("-", ""): v for k, v in names_cl.items()}
    mdlcl = names_cl.get(model.lower().replace("-", ""), Blip)
    return mdlcl(service=service).image2text(image=image, *args, **kwargs)

def image_captioning(image: Union[np.array, bytes, str, mt.ImageFile], model="blip", service="socaity", *args, **kwarg) -> str:
    return image2text(image=image, model=model, service=service, *args, **kwarg)

def visual_question_answering(image: Union[np.array, bytes, str, mt.ImageFile], question: str, model="blip", service="socaity", *args, **kwargs) -> str:
    from .blib.blib import Blip
    names_cl = {
        "blib": Blip,
    }
    names_cl = {k.lower().replace("-", ""): v for k, v in names_cl.items()}
    mdlcl = names_cl.get(model.lower().replace("-", ""), Blip)
    return mdlcl(service=service).visual_question_answering(image=image, question=question, *args, **kwargs)

def image_text_matching(image: Union[np.array, bytes, str, mt.ImageFile], caption: str, model="blip", service="socaity", *args, **kwargs) -> str:
    from .blib.blib import Blip
    names_cl = {
        "blib": Blip,
    }
    names_cl = {k.lower().replace("-", ""): v for k, v in names_cl.items()}
    mdlcl = names_cl.get(model.lower().replace("-", ""), Blip)
    return mdlcl(service=service).image_text_matching(image=image, caption=caption, *args, **kwargs)