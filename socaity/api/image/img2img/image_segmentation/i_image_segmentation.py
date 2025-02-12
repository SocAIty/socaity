from abc import abstractmethod
from typing import Union, List

from fastsdk.jobs.threaded.internal_job import InternalJob
from media_toolkit import ImageFile


class _BaseSegmentation:
    """
    Base implementation for segmentation models, the Segment Anything v2 model from Meta.
    """
    @abstractmethod
    def segment(self,  job, image: Union[str, bytes, ImageFile], *args, **kwargs) -> InternalJob:
        """
        Interface for performing image segmentation.
        :param image: URL or path to the input image.
        """
        raise NotImplementedError("Implement in subclass")


def image_segmentation(
        image: Union[ImageFile, List[ImageFile], str, List[str]],
        model="sam2", service="socaity", *args, **kwargs) -> Union[ImageFile, List[ImageFile], dict, None]:

    from .sam2 import Sam2
    names_cl = {
        "sam2": Sam2,
    }
    names_cl = {k.lower().replace("-", ""): v for k, v in names_cl.items()}
    mdlcl = names_cl.get(model.lower().replace("-", ""), Sam2)
    return mdlcl(service=service).segment(image=image, *args, **kwargs)
