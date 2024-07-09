import time
from typing import Union
import numpy as np
from fastsdk.jobs.threaded.internal_job import InternalJob
from fastsdk import FastSDK
from fastsdk.jobs.threaded.job_progress import JobProgress
from .face2face_service_client import srvc_face2face

face2face_service_client = FastSDK(srvc_face2face)

@face2face_service_client.sdk()
class SpeechCraft:
    """
    SpeechCraft offers Text2Speech, Voice-Cloning and Voice2Voice conversion with the generative audio model bark
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
        :param semantic_temp: the temperature for the semantic model
        """
        return self._text2voice(
            text=text, voice=voice, semantic_temp=semantic_temp, semantic_top_k=semantic_top_k,
            semantic_top_p=semantic_top_p, coarse_temp=coarse_temp, coarse_top_k=coarse_top_k,
            coarse_top_p=coarse_top_p, fine_temp=fine_temp
        )

    def voice2voice(self, voice_name: str, audio_file: Union[str, bytes], save: bool = False) -> InternalJob:
        return self._voice2voice(voice_name=voice_name, audio_file=audio_file, save=save)

    def voice2embedding(self, face_name: str, source_img: Union[str, bytes], save: bool = True) -> InternalJob:
        return self._add_reference_face(face_name=face_name, source_img=source_img, save=save)


    @face2face_service_client.job()
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
        result = endpoint_request.get_result()
        if endpoint_request.error is not None:
            raise Exception(f"Error in text2voice: {endpoint_request.error}")

        return result

    @face2face_service_client.job()
    def _voice2voice(self, job, voice_name: str, audio_file: Union[str, bytes]):
        endpoint_request = job.request("voice2voice", voice_name=voice_name, audio_file=audio_file)
        result = endpoint_request.get_result()
        if endpoint_request.error is not None:
            raise Exception(f"Error in voice2voice: {endpoint_request.error}")

        return result

    @face2face_service_client.job()
    def _voice2embedding(self, job, voice_name: str, audio_file: Union[str, bytes], save: bool = False):
        endpoint_request = job.request("voice2embedding", voice_name=voice_name, audio_file=audio_file, save=save)
        result = endpoint_request.get_result()
        if endpoint_request.error is not None:
            raise Exception(f"Error in voice2embedding: {endpoint_request.error}")

        return result


if __name__ == "__main__":
    f2f = Face2Face()
    img_1 = "A:\\projects\\_face2face\\face2face\\test\\test_media\\test_face_1.jpg"
    img2 = "A:\\projects\\_face2face\\face2face\\test\\test_media\\test_face_2.jpg"

    job = f2f.swap_one(img_1, target_img=img2)
    job.run()
    result = job.wait_for_finished()
    print(result.server_response)