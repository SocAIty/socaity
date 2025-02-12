import random

import media_toolkit as mt
from typing import Union, List

from fastsdk import fastSDK, fastJob
from fastsdk.jobs.threaded.internal_job import InternalJob
from media_toolkit import VideoFile
from socaity.api.video.text2video.hunyuan_video.hunyuan_video_service_client import srvc_hunyuan_video
from socaity.api.video.text2video.text2video import _BaseText2Video


@fastSDK(service_client=srvc_hunyuan_video)
class HunyuanVideo(_BaseText2Video):
    @fastJob
    def _text2video(
            self,
            job: InternalJob,
            prompt: str,
            width: int = 854,
            height: int = 480,
            video_length: int = 129,  # in frames
            infer_steps: int = 50,
            seed: int = None,
            embedded_guidance_scale: int = 6
    ) -> Union[mt.VideoFile, List[mt.VideoFile], None]:
        if not seed or not isinstance(seed, int):
            seed = random.Random().randint(0, 10000)

        if (video_length-1) % 4 != 0:
            raise ValueError(f"video_length-1 must be multiple of 4 got {video_length}")

        endpoint_request = job.request(
            endpoint_route="text2video",
            prompt=prompt,
            width=width,
            height=height,
            video_length=video_length,
            infer_steps=infer_steps,
            seed=seed,
            embedded_guidance_scale=embedded_guidance_scale
        )

        while not endpoint_request.is_finished():
            pass

        if endpoint_request.error is not None:
            raise Exception(f"Error in text2video with huanyan_video: {endpoint_request.error}")

        res = endpoint_request.get_result()
        if isinstance(res, list) and not isinstance(res, str):
            if len(res) == 1:
                return VideoFile().from_any(res[0])
            return [VideoFile().from_any(vid) for vid in res]

        return VideoFile().from_any(res)

    def text2video(
            self,
            text: str,
            width: int = 854,
            height: int = 480,
            video_length: int = 129,  # in frames
            infer_steps: int = 50,
            seed: int = None,
            embedded_guidance_scale: int = 6,
            *args,
            **kwargs
    ) -> InternalJob:
        """
        Converts text to an image.
        :param text: The prompt to be converted to an image.
        """
        return self._text2video(
            prompt=text,
            width=width,
            height=height,
            video_length=video_length,
            infer_steps=infer_steps,
            seed=seed,
            embedded_guidance_scale=embedded_guidance_scale
        )