from socaity import Face2Face, gather_results

test_face_1 = "test_files/test_face_1.jpg"
test_face_2 = "test_files/test_face_2.jpg"
test_face_3 = "test_files/test_face_3.jpg"
test_video = "test_files/smithy.mp4"

f2f = Face2Face()

# test single face swap
#job_swapped = f2f.swap_one(test_face_1, test_face_2)
#swapped = job_swapped.get_result()
#cv2.imshow("swapped_face", np.array(swapped))
#
## test embedding face swap
#ref_face_v_job = f2f.add_reference_face("hagrid", test_face_1, save=True)
#ref_face_vector = ref_face_v_job.get_result()

#swap_job = f2f.swap_from_reference_face("hagrid", test_face_2)
#swapped = swap_job.get_result()
# test video swap


#ref_face_v_job = f2f.add_reference_face(face_name="black_woman", source_img=test_face_3, save=True)
swapped_video_job = f2f.swap_video(face_name="black_woman", target_video=test_video, include_audio=True)
swapped_video_job.debug_mode = True
swapped_video = swapped_video_job.get_result()
a = 1