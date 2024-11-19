import time
from typing import Union
import numpy as np
from fastsdk.jobs.threaded.internal_job import InternalJob
from fastsdk import fastSDK, fastJob
from .speech_craft_service_client import srvc_speechcraft

@fastSDK(service_client=srvc_speechcraft)
class SpeechCraft:
    """
    SpeechCraft offers Text2Speech, Voice-Cloning and Voice2Voice conversion with the generative audio model_description bark
    SDK for the SpeechCraft https://github.com/SocAIty/SpeechCraft fast-task-api service.
    """
    def text2voice(
            self,
            text: str,
            voice: str = "en_speaker_3",
            semantic_temp: float = 0.7,
            semantic_top_k: int = 50,
            semantic_top_p: float = 0.95,
            coarse_temp: float = 0.7,
            coarse_top_k: int = 50,
            coarse_top_p: float = 0.95,
            fine_temp: float = 0.5
    ) -> InternalJob:
        """
        :param text: the text to be converted to speech
        :param voice: the name of the voice to be used. Uses the pretrained voices of SpeechCraft
        :param semantic_temp: the temperature for the semantic model_description
        """
        return self._text2voice(
            text=text, voice=voice, semantic_temp=semantic_temp, semantic_top_k=semantic_top_k,
            semantic_top_p=semantic_top_p, coarse_temp=coarse_temp, coarse_top_k=coarse_top_k,
            coarse_top_p=coarse_top_p, fine_temp=fine_temp
        )

    def voice2voice(self, voice_name: str, audio_file: Union[str, bytes]) -> InternalJob:
        return self._voice2voice(voice_name=voice_name, audio_file=audio_file)

    def voice2embedding(self, voice_name: str, audio_file: Union[str, bytes], save: bool = False) -> InternalJob:
        return self._voice2embedding(voice_name=voice_name, audio_file=audio_file, save=save)

    @fastJob
    def _text2voice(
            self,
            job: InternalJob,
            text: str,
            voice: str = "en_speaker_3",
            semantic_temp: float = 0.7,
            semantic_top_k: int = 50,
            semantic_top_p: float = 0.95,
            coarse_temp: float = 0.7,
            coarse_top_k: int = 50,
            coarse_top_p: float = 0.95,
            fine_temp: float = 0.5
         ) -> np.array:
        """
        Swaps a face from source_img to target_img;
        in the manner that the face from source_img is placed on the face from target_img.
        :param source_img: The image containing the face to be swapped. Read with open() -> f.read()
        :param target_img: The image containing the face to be swapped to. Read with open() -> f.read()
        """
        endpoint_request = job.request(
            endpoint_route="text2voice",
            text=text,
            voice=voice,
            semantic_temp=semantic_temp,
            semantic_top_k=semantic_top_k,
            semantic_top_p=semantic_top_p,
            coarse_temp=coarse_temp,
            coarse_top_k=coarse_top_k,
            coarse_top_p=coarse_top_p,
            fine_temp=fine_temp
        )
        while not endpoint_request.is_finished():
            progress, message = endpoint_request.progress
            job.set_progress(progress, message)
            time.sleep(0)

        if endpoint_request.error is not None:
            raise Exception(f"Error in text2voice: {endpoint_request.error}")

        return endpoint_request.get_result()

    @fastJob
    def _voice2voice(self, job: InternalJob, voice_name: str, audio_file: Union[str, bytes]):
        endpoint_request = job.request("voice2voice", voice_name=voice_name, audio_file=audio_file)
        while not endpoint_request.is_finished():
            progress, message = endpoint_request.progress
            job.set_progress(progress, message)
            time.sleep(0)

        if endpoint_request.error is not None:
            raise Exception(f"Error in voice2voice: {endpoint_request.error}")

        return endpoint_request.get_result()

    @fastJob
    def _voice2embedding(self, job: InternalJob, voice_name: str, audio_file: Union[str, bytes], save: bool = False):
        endpoint_request = job.request("voice2embedding", voice_name=voice_name, audio_file=audio_file, save=save)

        # update progress bar
        while not endpoint_request.is_finished():
            progress, message = endpoint_request.progress
            job.set_progress(progress, message)
            time.sleep(0)

        if endpoint_request.error is not None:
            raise Exception(f"Error in voice2embedding: {endpoint_request.error}")

        return endpoint_request.get_result()

