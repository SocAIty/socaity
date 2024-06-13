from typing import List

from socaity.socaity_client import ImageFile, UploadFile
from socaity.socaity_client.jobs.threaded.internal_job import InternalJob
from socaity.socaity_client.service_client_api import ServiceClientAPI
from tests.fries_maker.service_fries_maker import srvc_fries_maker
import cv2
import base64
import librosa

fries_maker_client_api = ServiceClientAPI(srvc_fries_maker)

class FriesMaker:

    @fries_maker_client_api.job()
    def _make_fries(self, job: InternalJob, fries_name: str, amount: int = 1):
        endpoint_request = job.request_sync(endpoint_route="make_fries", fries_name=fries_name, amount=amount)

        if endpoint_request.error is not None:
            raise Exception(f"Error in making fries: {endpoint_request.error}")

        return endpoint_request.result

    @fries_maker_client_api.job()
    def _make_file_fries(self, job: InternalJob, potato_one: bytes, potato_two: bytes, potato_three: bytes):
        endpoint_request = job.request_sync(
            endpoint_route="make_file_fries", potato_one=potato_one, potato_two=potato_two, potato_three=potato_three
        )

        if endpoint_request.error is not None:
            raise Exception(f"Error in making fries: {endpoint_request.error}")

        return endpoint_request.result

    @fries_maker_client_api.job()
    def _make_image_fries(self, job: InternalJob, potato_one: bytes):
        endpoint_request = job.request_sync(endpoint_route="make_image_fries", potato_one=potato_one)

        if endpoint_request.error is not None:
            raise Exception(f"Error in making fries: {endpoint_request.error}")

        return endpoint_request.result

    @fries_maker_client_api.job()
    def _make_audio_fries(self, job: InternalJob, potato_one: bytes, potato_two: bytes):
        endpoint_request = job.request_sync(
            endpoint_route="make_audio_fries", potato_one=potato_one, potato_two=potato_two
        )

        if endpoint_request.error is not None:
            raise Exception(f"Error in making fries: {endpoint_request.error}")

        return endpoint_request.result

    @fries_maker_client_api.job()
    def _make_video_fries(self, job: InternalJob, potato_one: bytes, potato_two: bytes):
        endpoint_request = job.request_sync(
            endpoint_route="make_video_fries", potato_one=potato_one, potato_two=potato_two
        )

        if endpoint_request.error is not None:
            raise Exception(f"Error in making fries: {endpoint_request.error}")

        return endpoint_request.result

    def make_fries(self, fries_name: str, amount: int) -> InternalJob:
        return self._make_fries(fries_name, amount)

    def make_file_fries(self, potato_one: str, potato_two: str) -> InternalJob:
        potato_three = potato_two
        # standard python file handle
        potato_one = open(potato_one, "rb")
        # read with cv2
        potato_two = cv2.imread(potato_two)
        return self._make_file_fries(potato_one, potato_two, potato_three)

    def make_image_fries(self, potato_one: str) -> List[InternalJob]:
        """
        Tests upload of standard file types.
        """
        # standard python file handle
        potato_handle = open(potato_one, "rb")
        job_handle = self._make_image_fries(potato_handle)

        # read file
        with open(potato_one, "rb") as f:
            potato_bytes = f.read()

        job_bytes = self._make_image_fries(potato_bytes)

        # read with cv2
        potato_cv2 = cv2.imread(potato_one)
        job_cv2 = self._make_image_fries(potato_cv2)
        job_cv2.debug_mode = True

        # as file instance
        upload_file_instance = UploadFile()
        upload_file_instance.from_file(potato_one)
        job_upload_file_instance = self._make_image_fries(upload_file_instance)
        job_upload_file_instance.debug_mode = True

        # as image file instance
        img_file_instance = ImageFile()
        img_file_instance.from_bytes(potato_bytes)
        job_img_file_instance = self._make_image_fries(img_file_instance)
        job_img_file_instance.debug_mode = True

        # as b64
        potato_b64 = base64.b64encode(potato_bytes).decode('utf-8')
        job_b64 = self._make_image_fries(potato_b64)
        job_b64.debug_mode = True

        # test one by one
        #res_handle = job_handle.wait_for_finished()
        #res_bytes = job_bytes.wait_for_finished()
        res_cv2 = job_cv2.wait_for_finished()
        res_uf = job_upload_file_instance.wait_for_finished()
        res_if = job_img_file_instance.wait_for_finished()

        return [job_handle, job_bytes, job_cv2, job_upload_file_instance, job_img_file_instance, job_b64]


    def make_audio_fries(self, potato_one: str, potato_two: str) -> InternalJob:
        """
        Tests upload of standard file types.
        """
        # standard python file handle
        potato_one = open(potato_one, "rb")
        # read with librosa
        potato_two = librosa.load(potato_two)

        return self._make_audio_fries(potato_one, potato_two)

    def make_video_fries(self, potato_one: str, potato_two: str) -> List[InternalJob]:
        """
        Tests upload of standard file types.
        """
        # standard python file handle
        potato_one = open(potato_one, "rb")

        # read with cv2
        potato_three = cv2.VideoCapture(potato_two)

        # read file
        with open(potato_two, "rb") as f:
            potato_two = f.read()

        job_files = self._make_video_fries(potato_one, potato_two)
        job_cv2 = self._make_video_fries(potato_one, potato_three)
        return [job_files, job_cv2]