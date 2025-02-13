from abc import abstractmethod
from typing import Union, List

import media_toolkit as mt
from fastsdk.jobs.threaded.internal_job import InternalJob
from socaity.api.utils import get_model_instance


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
def text2img(
        text: str, model: str = "flux-schnell", service: str = "socaity", wait_for_result: bool = False, *args, **kwargs
) -> Union[InternalJob, mt.ImageFile, List[mt.ImageFile], None]:
    """
    Creates a beautiful image from the given text.
    :param text: The text to convert to an image.
    :param model: The model to use for the conversion.
    :param service: The service to use for the conversion.
    :param wait_for_result: Whether to wait for the result. If False (default), returns the job.
    """

    from .flux_schnell import FluxSchnell
    names_cl = {"flux-schnell": FluxSchnell}
    mdl = get_model_instance(names_cl, model_name=model, service=service, default_instance=FluxSchnell)
    job = mdl.text2img(text=text, *args, **kwargs)
    if wait_for_result:
        return job.get_result()
    return job
