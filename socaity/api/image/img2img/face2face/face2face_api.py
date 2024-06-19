from typing import Union
import numpy as np
from socaity_client.jobs.threaded.internal_job import InternalJob
from socaity_client.service_client_api import ServiceClientAPI
from .face2face_service_client import srvc_face2face

face2face_service_client = ServiceClientAPI(srvc_face2face)


class Face2Face:
    @staticmethod
    def _read_img(img: Union[str, bytes]):
        if isinstance(img, str):
            return open(img, "rb")
        return img

    def swap_one(self, source_img: Union[str, bytes], target_img: Union[str, bytes]) -> InternalJob:
        """
        Swaps a face from source_img to target_img;
        in the manner that the face from source_img is placed on the face from target_img.
        :param source_img: Path to the image containing the face to be swapped.
            Or the image itself as bytes (with open(f): f.read()) .
        :param target_img: Path to the image containing the face to be swapped to.
            Or the image itself as bytes (with open(f): f.read()) .
        """
        source_img = self._read_img(source_img)
        target_img = self._read_img(target_img)
        return self._swap_one(source_img=source_img, target_img=target_img)

    def swap_from_reference_face(self, face_name: str, target_img: Union[str, bytes]) -> InternalJob:
        target_img = self._read_img(target_img)
        return self._swap_from_reference_face(face_name=face_name, target_img=target_img)

    def add_reference_face(self, face_name: str, source_img: Union[str, bytes], save: bool = True) -> InternalJob:
        source_img = self._read_img(source_img)
        return self._add_reference_face(face_name=face_name, source_img=source_img, save=save)

    @face2face_service_client.job()
    def _swap_one(self, job: InternalJob, source_img: Union[np.array, bytes, str], target_img: Union[np.array, bytes, str]) -> np.array:
        """
        Swaps a face from source_img to target_img;
        in the manner that the face from source_img is placed on the face from target_img.
        :param source_img: The image containing the face to be swapped. Read with open() -> f.read()
        :param target_img: The image containing the face to be swapped to. Read with open() -> f.read()
        """
        endpoint_request = job.request(endpoint_route="swap_one", source_img=source_img, target_img=target_img)

        if endpoint_request.error is not None:
            raise Exception(f"Error in swap_one: {endpoint_request.error}")

        return endpoint_request.get_result()

    @face2face_service_client.job()
    def _swap_from_reference_face(self, job, face_name: str, target_img: bytes):
        request_result = job.request("swap_from_reference", face_name, target_img)
        return request_result

    @face2face_service_client.job()
    def _add_reference_face(self, face_name: str, source_img: bytes, save: bool = True):
        request_result = job.request("add_reference_face", face_name, source_img, save)
        return request_result


if __name__ == "__main__":
    f2f = Face2Face()
    img_1 = "A:\\projects\\_face2face\\face2face\\test\\test_media\\test_face_1.jpg"
    img2 = "A:\\projects\\_face2face\\face2face\\test\\test_media\\test_face_2.jpg"

    job = f2f.swap_one(img_1, target_img=img2)
    job.run()
    result = job.wait_for_finished()
    print(result.server_response)