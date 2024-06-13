from socaity.socaity_client.jobs.job_utils import gather_results
from tests.fries_maker.fries_maker_client_api import FriesMaker

# get the media files
test_file_folder = "./test_media/"
img_potato_one = test_file_folder + "potato_one.jpeg"
img_potato_two = test_file_folder + "potato_two.png"
audio_potato = test_file_folder + "audio_potato.m4a"
video_potato = test_file_folder + "video_potato.mp4"


fries_maker = FriesMaker()
# send to the server
# easy_job = fries_maker.make_fries("super_chilli_fries", 10).run()
#a = 1
#file_jobs = fries_maker.make_file_fries(img_potato_one, img_potato_two)
#result = file_jobs.wait_for_finished()

image_jobs = fries_maker.make_image_fries(img_potato_one)
image_results = gather_results(image_jobs)

audio_job = fries_maker.make_audio_fries(audio_potato, audio_potato).run_sync()
#video_jobs = fries_maker.make_video_fries(video_potato, video_potato)

# gather results
all_results = gather_results([easy_job, file_jobs, audio_job, video_jobs])
