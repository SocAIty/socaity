from abc import abstractmethod
from typing import Union

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