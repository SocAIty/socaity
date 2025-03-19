import random
from enum import Enum
from typing import Union, List

from fastsdk.jobs.threaded.internal_job import InternalJob
from fastsdk.fast_sdk import fastSDK, fastJob
from fastsdk.utils import get_function_parameters_as_dict
from media_toolkit import ImageFile
from socaity.api.text.img2text.blib.blib_service_client import srvc_blip


class BlipTasks(Enum):
    CAPTION = "image_captioning"
    VQA = "visual_question_answering"
    IMAGE_TEXT_MATCHING = "image_text_matching"


@fastSDK(api_client=srvc_blip)
class Blip:
    """
    Base implementation for SAM 2, the Segment Anything v2 model from Meta.
    """
    def __init__(self):
        self._socaity_avatar_reference_image_1 = "https://socaityfiles.blob.core.windows.net/backend-model-meta/socaity_icon_no_shoulders_eyes.ico"

    @fastJob
    def _caption(self, job,
        image: Union[str, bytes, ImageFile],
        **kwargs
    ) -> str:
        """
        Create an image description (caption) for the input image.
        """
        response = job.request(
            endpoint_route="/capture",
            image=image,
            task=BlipTasks.CAPTION.value,
            caption="",
            **kwargs,
        )
        res = response.get_result()
        if response.error:
            raise Exception(f"Error in blip: {response.error}")

        return res

    @fastJob
    def _text_matching(self, job,
        image: Union[str, bytes, ImageFile],
        caption: str,
        **kwargs
    ) -> str:
        """
        Measure how well an image description is matched by the input image.
        """
        response = job.request(
            endpoint_route="/capture",
            image=image,
            task=BlipTasks.IMAGE_TEXT_MATCHING.value,
            caption=caption,
            **kwargs,
        )
        res = response.get_result()
        if response.error:
            raise Exception(f"Error in blip: {response.error}")

        return res

    @fastJob
    def _visual_question_answering(self, job,
        image: Union[str, bytes, ImageFile],
        question: str,
        **kwargs
    ):
        response = job.request(
            endpoint_route="/capture",
            image=image,
            task=BlipTasks.VQA.value,
            question=question,
            **kwargs,
        )
        res = response.get_result()
        if response.error:
            raise Exception(f"Error in blip: {response.error}")

        return res

    def caption(self, image: Union[str, bytes, ImageFile]) -> InternalJob:
        return self._caption(image=image)

    def text_matching(self, image: Union[str, bytes, ImageFile], caption: str) -> InternalJob:
        return self._text_matching(image=image, caption=caption)

    def visual_question_answering(self, image: Union[str, bytes, ImageFile], question: str) -> InternalJob:
        return self._visual_question_answering(image=image, question=question)
