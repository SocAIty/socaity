import random
from collections import Counter

from socaity.socaity_client import UploadFile, ImageFile
from socaity.socaity_client.jobs.job_utils import gather_results, gather_generator
from socaity.socaity_client.jobs.threaded.job_status import JOB_STATUS
from tests.fries_maker.fries_maker_client_api import FriesMaker

import cv2
import base64

# get the media files
test_file_folder = "./test_media/"
img_potato_one = test_file_folder + "potato_one.jpeg"
img_potato_two = test_file_folder + "potato_two.png"
audio_potato = test_file_folder + "audio_potato.m4a"
video_potato = test_file_folder + "video_potato.mp4"


fries_maker = FriesMaker()
count = 0
def test_simple_rpc():
    global count
    count += 1
    easy_job = fries_maker.make_fries(f"super_chilli_fries {count}", count)
    easy_job.debug_mode = True
    easy_job.run()
    return easy_job

def test_upload_file():
    file_jobs = fries_maker.make_file_fries(img_potato_one, img_potato_two)
    result = file_jobs.wait_for_finished()
    return result

"""
Images: tests upload of standard file types
"""
def test_image_upload():
    # standard python file handle
    potato_handle = open(img_potato_one, "rb")
    job_handle = fries_maker.make_image_fries(potato_handle)
    job_handle.run()
    # read file
    with open(img_potato_one, "rb") as f:
        potato_bytes = f.read()

    job_bytes = fries_maker.make_image_fries(potato_bytes)
    job_bytes.run()
    # read with cv2
    potato_cv2 = cv2.imread(img_potato_one)
    job_cv2 = fries_maker.make_image_fries(potato_cv2)
    job_cv2.run()
    # as file instance
    upload_file_instance = UploadFile()
    upload_file_instance.from_file(img_potato_two)
    job_upload_file_instance = fries_maker.make_image_fries(upload_file_instance)
    job_upload_file_instance.run()
    # as image file instance
    img_file_instance = ImageFile()
    img_file_instance.from_bytes(potato_bytes)
    job_img_file_instance = fries_maker.make_image_fries(img_file_instance)
    job_img_file_instance.run()
    # as b64
    potato_b64 = base64.b64encode(potato_bytes).decode('utf-8')
    job_b64 = fries_maker.make_image_fries(potato_b64)
    job_b64.run()
    # test one by one
    # res_handle = job_handle.wait_for_finished()
    # res_bytes = job_bytes.wait_for_finished()
    # res_cv2 = job_cv2.wait_for_finished()
    # res_uf = job_upload_file_instance.wait_for_finished()
    # res_if = job_img_file_instance.wait_for_finished()
    # res_b64 = job_b64.wait_for_finished()

    all_jobs = [job_handle, job_bytes, job_cv2, job_upload_file_instance, job_img_file_instance, job_b64]

    #for finished_job in gather_generator(all_jobs):
    #    print(finished_job.result)

    return all_jobs


def test_audio_upload():

    audio_job = fries_maker.make_audio_fries(audio_potato, audio_potato).run_sync()
    #video_jobs = fries_maker.make_video_fries(video_potato, video_potato)

    # gather results
    all_results = gather_results([easy_job, file_jobs, audio_job, video_jobs])



if __name__ == "__main__":

    #test_simple_rpc()
    #test_image_upload()
    # test_audio_upload()

    # mini stress test
    def stress_test(func, num_iters=10):
        jobs = [func() for i in range(num_iters)]
        for finished_job in gather_generator(jobs):
            print(finished_job.result)

    #stress_test(test_simple_rpc, 10)
    stress_test(test_image_upload, 10)
