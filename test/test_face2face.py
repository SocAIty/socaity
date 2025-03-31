from socaity import Face2Face
f2f = Face2Face()

test_face_1 = "test_files/face2face/test_face_1.jpg"
test_face_2 = "test_files/face2face/test_face_2.jpg"
test_face_3 = "test_files/face2face/test_face_3.jpg"
test_video = "test_files/face2face/test_video_ultra_short_short.mp4"

def test_single_face_swap():
    job_swapped = f2f.swap_img_to_img(test_face_1, test_face_2, enhance_face_model=None)
    swapped = job_swapped.get_result()
    swapped.save("test_files/output/face2face/test_face_31_swapped.jpg")
    return swapped


## test embedding face swap
def test_embedding_face_swap():
    ref_face_v_job = f2f.add_face("hagrid", test_face_1, save=True)
    ref_face_vector = ref_face_v_job.get_result()
    job_swapped = f2f.swap(media=test_face_2, faces="hagrid", enhance_face_model="")
    swapped = job_swapped.get_result()
    return swapped


def test_video_swap():
    #ref_face_v_job = f2f.add_face(face_name="black_woman", image=test_face_3, save=True)
    #ref_face_vector = ref_face_v_job.get_result()
    swapped_video_job = f2f.swap_video(face_name="black_woman", target_video=test_video, include_audio=True, enhance_face_model="")
    swapped_video = swapped_video_job.get_result()
    return swapped_video


test_single_face_swap()
# test_video_swap()
# test_embedding_face_swap()