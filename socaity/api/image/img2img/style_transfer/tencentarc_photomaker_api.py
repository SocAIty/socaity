import random
from dataclasses import dataclass
from enum import Enum
from typing import Union, List

from fastsdk.jobs.threaded.internal_job import InternalJob
from fastsdk.fast_sdk import fastSDK, fastJob
from fastsdk.utils import get_function_parameters_as_dict
from media_toolkit import ImageFile
from .tencentarc_photomaker_service_client import srvc_photomaker


class TencentPhotoMakerStyleTemplate(Enum):
    CINEMATIC = "Cinematic"
    DISNEY = "Disney Charactor"
    DIGITAL_ART = "Digital Art"
    PHOTOGRAPHIC = "Photographic"
    FANTASY_ART = "Fantasy art"
    NEONPUNK = "Neonpunk"
    ENHANCE = "Enhance"
    COMIC = "Comic book"
    LOWPOLY = "Lowpoly"
    LINEART = "Lineart"

@fastSDK(service_client=srvc_photomaker)
class TencentPhotoMaker:
    """
    Base implementation for SAM 2, the Segment Anything v2 model from Meta.
    """
    def __init__(self):
        self._socaity_avatar_reference_image_1 = "https://socaityfiles.blob.core.windows.net/backend-model-meta/socaity_icon_no_shoulders_eyes.ico"

    @fastJob
    def _generate(self, job,
        input_image: Union[str, bytes, ImageFile],
        input_image1: Union[str, bytes, ImageFile],
        input_image2: Union[str, bytes, ImageFile],
        input_image3: Union[str, bytes, ImageFile],
        input_image4: Union[str, bytes, ImageFile],
        prompt: str = "",
        style_name: str = None,
        negative_prompt: str = "",
        num_steps: int = 50,
        style_strength_ratio: float = 35,
        num_outputs: int = 1,
        guidance_scale: float = 5,
        seed: int = None,
        disable_safety_checker: bool = False,
        **kwargs) -> Union[ImageFile, List[ImageFile]]:
        """
        Create photos, paintings and avatars for anyone in any style within seconds.
        :param image: URL or path to the input image.
        :param points_per_side: Number of points per side for segmentation.
        :param pred_iou_thresh: Prediction IoU threshold.
        :param stability_score_thresh: Stability score threshold.
        :param use_m2m: Whether to enable model-to-model interaction.
        :return: Segmentation results as a dictionary.
        """
        if not seed or not isinstance(seed, int) or seed < 0:
            seed = random.randint(0, 1000)

        response = job.request(
            endpoint_route="/generate",
            input_image=input_image,
            input_image1=input_image1,
            input_image2=input_image2,
            input_image3=input_image3,
            input_image4=input_image4,
            prompt=prompt,
            style_name=style_name,
            negative_prompt=negative_prompt,
            num_steps=num_steps,
            style_strength_ratio=style_strength_ratio,
            num_outputs=num_outputs,
            guidance_scale=guidance_scale,
            seed=seed,
            disable_safety_checker=disable_safety_checker,
            **kwargs,
        )
        res = response.get_result()
        if response.error:
            raise Exception(f"Error in photomaker: {response.error}")

        if isinstance(res, list):
            if len(res) == 1:
                return ImageFile().from_any(res[0])
            return [ImageFile().from_any(img) for img in res]

        return ImageFile().from_any(res)

    def generate(self,
        input_image: Union[str, bytes, ImageFile],
        input_image1: Union[str, bytes, ImageFile] = None,
        input_image2: Union[str, bytes, ImageFile] = None,
        input_image3: Union[str, bytes, ImageFile] = None,
        input_image4: Union[str, bytes, ImageFile] = None,
        prompt: str = "",
        style_name: str = TencentPhotoMakerStyleTemplate.PHOTOGRAPHIC,
        negative_prompt: str = "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry",
        num_steps: int = 50,
        style_strength_ratio: float = 35,
        num_outputs: int = 1,
        guidance_scale: float = 5,
        seed: int = None,
        disable_safety_checker: bool = False,
        *args,
        **kwargs) -> InternalJob:
        """
        Perform image segmentation using SAM 2.
        :param image: URL or path to the input image.
        """
        # Check if style_name is an instance of TencentPhotoMakerStyleTemplate or can be converted to
        if isinstance(style_name, str):
            try:
                style_name = TencentPhotoMakerStyleTemplate(style_name)
            except ValueError:
                print(f"Invalid style name: {style_name} using photographic style")
                style_name = TencentPhotoMakerStyleTemplate.PHOTOGRAPHIC

        # convert style name to string
        if isinstance(style_name, TencentPhotoMakerStyleTemplate):
            style_name = style_name.value

        pams = get_function_parameters_as_dict(
            self._generate,
            exclude_param_names="job",
            func_kwargs=locals()
        )
        return self._generate(**pams)

    def create_socaity_avatar(
            self,
            input_image: Union[str, bytes, ImageFile],
            num_outputs: int = 1
    ):
        """
        Create a socaity avatar from an image.
        :param input_image: Your profile picture that gets converted. Best results with a close up portrait.
        """
        return self.generate(
            input_image=input_image,
            input_image1=self._socaity_avatar_reference_image_1,
            prompt="""
            A minimalist, sci-fi img featuring a close-up of Rick's face from Rick and Morty.
            The eyes are glowing neon green bioluminescent. The background is entirely black.
            The face is showcasing a vibrant neon-green lime palette, rendered in an anime-style illustration with 4k detail.
            8bit style. Icon.
            """,
            style_name=TencentPhotoMakerStyleTemplate.NEONPUNK,
            num_outputs=num_outputs
        )
