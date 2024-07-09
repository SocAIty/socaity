import time
from typing import Union
import numpy as np
from fastsdk.jobs.threaded.internal_job import InternalJob
from fastsdk import FastSDK
from .face2face_service_client import srvc_face2face

face2face_service_client = FastSDK(srvc_face2face)

@face2face_service_client.sdk()
class Face2Face:

    def swap_one(self, source_img: Union[str, bytes], target_img: Union[str, bytes]) -> InternalJob:
        """
        Swaps a face from source_img to target_img;
        in the manner that the face from source_img is placed on the face from target_img.
        :param source_img: Path to the image containing the face to be swapped.
            Or the image itself as bytes (with open(f): f.read()) .
        :param target_img: Path to the image containing the face to be swapped to.
            Or the image itself as bytes (with open(f): f.read()) .
        """
        return self._swap_one(source_img=source_img, target_img=target_img)

    def swap_from_reference_face(self, face_name: str, target_img: Union[str, bytes]) -> InternalJob:
        return self._swap_from_reference_face(face_name=face_name, target_img=target_img)

    def add_reference_face(self, face_name: str, source_img: Union[str, bytes], save: bool = True) -> InternalJob:
        return self._add_reference_face(face_name=face_name, source_img=source_img, save=save)

    def swap_video(self, face_name: str, target_video: Union[str, bytes], include_audio: bool = True) -> InternalJob:
        return self._swap_video(face_name=face_name, target_video=target_video, include_audio=include_audio)

    @face2face_service_client.job()
    def _swap_one(self, job: InternalJob, source_img: Union[np.array, bytes, str], target_img: Union[np.array, bytes, str]) -> np.array:
        """
        Swaps a face from source_img to target_img;
        in the manner that the face from source_img is placed on the face from target_img.
        :param source_img: The image containing the face to be swapped. Read with open() -> f.read()
        :param target_img: The image containing the face to be swapped to. Read with open() -> f.read()
        """
        endpoint_request = job.request(endpoint_route="swap_one", source_img=source_img, target_img=target_img)
        result = endpoint_request.get_result()
        if endpoint_request.error is not None:
            raise Exception(f"Error in swap_one: {endpoint_request.error}")

        return result

    @face2face_service_client.job()
    def _swap_from_reference_face(self, job, face_name: str, target_img: bytes):
        endpoint_request = job.request("swap_from_reference_face", face_name, target_img)
        result = endpoint_request.get_result()
        if endpoint_request.error is not None:
            raise Exception(f"Error in swap_from_reference_face: {endpoint_request.error}")

        return result

    @face2face_service_client.job()
    def _add_reference_face(self, job, face_name: str, source_img: bytes, save: bool = True):
        endpoint_request = job.request("add_reference_face", face_name, source_img, save)
        result = endpoint_request.get_result()
        if endpoint_request.error is not None:
            raise Exception(f"Error in add_reference_face: {endpoint_request.error}")

        return result

    @face2face_service_client.job()
    def _swap_video(self, job, face_name: str, target_video: str, include_audio: bool = True):
        request_result = job.request(
            "swap_video", face_name=face_name, target_video=target_video, include_audio=include_audio
            )

        # update progress bar
        while not request_result.is_finished():
            progress, message = request_result.progress
            job.set_progress(progress, message)
            time.sleep(0)

        if request_result.error is not None:
            raise Exception(f"Error in swap_video: {request_result.error}")

        return request_result.get_result()


if __name__ == "__main__":
    f2f = Face2Face()
    img_1 = "A:\\projects\\_face2face\\face2face\\test\\test_media\\test_face_1.jpg"
    img2 = "A:\\projects\\_face2face\\face2face\\test\\test_media\\test_face_2.jpg"

    job = f2f.swap_one(img_1, target_img=img2)
    job.run()
    result = job.wait_for_finished()
    print(result.server_response)