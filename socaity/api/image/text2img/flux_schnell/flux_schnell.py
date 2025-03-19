import random

import media_toolkit as mt
from typing import Union, Tuple, List

from fastsdk import fastSDK, fastJob
from fastsdk.jobs.threaded.internal_job import InternalJob
from media_toolkit import ImageFile
from socaity.api.image.text2img.flux_schnell.flux_schnell_service_client import srvc_flux_schnell
from socaity.api.image.text2img.text2image import _BaseText2Image
from socaity.api.utils import execute_job_function


@fastSDK(api_client=srvc_flux_schnell)
class FluxSchnell(_BaseText2Image):
    @fastJob
    def _text2img(
            self,
            job: InternalJob,
            text: str,
            aspect_ratio: Union[str, Tuple[int, int]] = "1:1",
            num_outputs: int = 1,
            num_inference_steps: int = 4,
            seed: int = None,
            output_format: str = 'png',
            disable_safety_checker: bool = True,
            go_fast: bool = False
    ) -> Union[mt.ImageFile, List[mt.ImageFile], None]:
        if seed is None:
            seed = random.Random().randint(0, 1000000)

        if isinstance(aspect_ratio, tuple):
            aspect_ratio = f"{aspect_ratio[0]}:{aspect_ratio[1]}"
        if not aspect_ratio or not isinstance(aspect_ratio, str):
            aspect_ratio = "1:1"

        endpoint_request = job.request(
            endpoint_route="text2img",
            prompt=text, aspect_ratio=aspect_ratio, num_outputs=num_outputs, num_inference_steps=num_inference_steps,
            seed=seed, output_format=output_format, disable_safety_checker=disable_safety_checker, go_fast=go_fast
        )

        while not endpoint_request.is_finished():
            pass

        if endpoint_request.error is not None:
            raise Exception(f"Error in text2image with flux_schnell: {endpoint_request.error}")

        res = endpoint_request.get_result()
        if isinstance(res, list):
            if len(res) == 1:
                return ImageFile().from_any(res[0])
            return [ImageFile().from_any(img) for img in res]

        return ImageFile().from_any(res)

    def text2img(
            self,
            text: str,
            aspect_ratio: Union[str, Tuple[int, int]] = "1:1",
            num_outputs: int = 1,
            num_inference_steps: int = 4,
            seed: int = None,
            output_format: str = 'png',
            disable_safety_checker: bool = True,
            go_fast: bool = False
    ) -> InternalJob:
        """
        Converts text to an image.
        :param text: The prompt to be converted to an image.
        """
        return execute_job_function(self._text2img, pam_locals=locals())

