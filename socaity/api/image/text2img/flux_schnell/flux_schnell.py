import media_toolkit as mt
from typing import Union

from fastsdk import fastSDK, fastJob
from fastsdk.jobs.threaded.internal_job import InternalJob
from socaity.api.image.text2img.flux_schnell.flux_schnell_service_client import srvc_flux_schnell
from socaity.api.image.text2img.text2image import Text2Image


@fastSDK(service_client=srvc_flux_schnell)
class FluxSchnell(Text2Image):
    @fastJob
    def text2img(
            self,
            text: str,
            aspect_ratio: Union[str, (int, int)],
            num_outputs: int = 1,
            seed: int = None
    ) -> mt.ImageFile:
        """
        Converts text to an image.
        :param text: The text to be converted to an image.
        """
        return self._text2img(text=text, aspect_ratio=aspect_ratio, num_outputs=num_outputs, seed=seed)


    def _text2img(
            self,
            job: InternalJob,
            text: str,
            aspect_ratio: Union[str, (int, int)],
            num_outputs: int = 1,
            seed: int = None
    ):
        endpoint_request = job.request(
            endpoint_route="text2img",
            text=text, aspect_ratio=aspect_ratio, num_outputs=num_outputs, seed=seed
        )

        while not endpoint_request.is_finished():
            pass

        if endpoint_request.error is not None:
            raise Exception(f"Error in text2image with flux_schnell: {endpoint_request.error}")

        return endpoint_request.get_result()
