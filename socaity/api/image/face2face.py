from typing import Union

import numpy as np

from socaity import ClientAPI, Job
from socaity.core.job.async_server_job import AsyncServerJob
from socaity.new_registry.definitions.enums import EndPointType, ModelTag
from socaity.utils import load_image_from_file
from socaity.utils.utils import get_function_parameters_as_dict


class Face2Face(ClientAPI):
    """
    Face2Face is a generative AI technology to swap faces (aka Deep Fake) in images from one to another.
    For example you can swap your face with Mona Lisa our your favourite superstar. With this repository you can:

    Swap faces from one image to another. Powered by Insightface
    Create face embeddings. With these embeddings you can later swap faces without running the whole stack again.
    """

    def __init__(self, endpoint_type: Union[EndPointType, str] = EndPointType.REMOTE, *args, **kwargs):
        super().__init__(
            model_type=ModelTag.FACE2FACE,
            model_name="face2face",
            endpoint_type=endpoint_type,
            *args, **kwargs
        )

    def __call__(
            self,
            source_image: Union[str, np.ndarray],
            target_image: Union[str, np.ndarray],
            *args, **kwargs
    ):
        """
        Swaps the face of the source image to the target image.
        """

        if isinstance(source_image, str):
            source_image = load_image_from_file(source_image)
        if isinstance(target_image, str):
            target_image = load_image_from_file(target_image)

        return super().__call__(
            source_image=source_image,
            target_image=target_image,
            **kwargs
        )

    def run(self,
            source_image: Union[str, np.ndarray],
            target_image: Union[str, np.ndarray],
            *args, **kwargs) -> Union[Job, AsyncServerJob]:
        # just reuse args to easy pass them to super
        _kwargs = get_function_parameters_as_dict(self.run, locals(), kwargs)
        return self.__call__(**_kwargs)