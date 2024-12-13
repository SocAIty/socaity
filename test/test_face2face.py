import os

from socaity import Face2Face, gather_results


test_face_1 = "test_files/face2face/test_face_1.jpg"
test_face_2 = "test_files/face2face/test_face_2.jpg"
test_face_3 = "test_files/face2face/test_face_3.jpg"
test_video = "test_files/face2face/test_video_ultra_short_short.mp4"

#f2f = Face2Face(service="runpod_localhost", api_key=os.getenv("RUNPOD_API_KEY"))
f2f = Face2Face(service="socaity_local", api_key=os.getenv("SOCAITY_API_KEY", None))

def test_single_face_swap():
    job_swapped = f2f.swap_img_to_img(test_face_1, test_face_2, enhance_face_model=None)
    swapped = job_swapped.get_result()
    swapped.save("test_files/face2face/test_face_1_swapped.jpg")
    return swapped


## test embedding face swap
def test_embedding_face_swap():
    ref_face_v_job = f2f.add_face("hagrid", test_face_1, save=True)
    ref_face_vector = ref_face_v_job.get_result()
    job_swapped = f2f.swap(media=test_face_2, faces="hagrid", enhance_face_model="")
    swapped = job_swapped.get_result()
    return swapped
#swap_job = f2f.swap_from_reference_face("hagrid", test_face_2)
#swapped = swap_job.get_result()
# test video swap


def test_video_swap():
    ref_face_v_job = f2f.add_face(face_name="black_woman", source_img=test_face_3, save=True)
    swapped_video_job = f2f.swap_video(face_name="black_woman", target_video=test_video, include_audio=True, enhance_face_model="")
    swapped_video = swapped_video_job.get_result()
    return swapped_video

test_single_face_swap()
# test_video_swap()
# test_embedding_face_swap()
a = 1