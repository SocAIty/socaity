from socaity import Face2Face, gather_results

test_face_1 = "test_files/test_face_1.jpg"
test_face_2 = "test_files/test_face_2.jpg"


f2f = Face2Face()

# test single face swap
job_swapped = f2f.swap_one(test_face_1, test_face_2)
swapped = job_swapped.get_result()
cv2.imshow("swapped_face", swapped)

# test embedding face swap
ref_face_vector = f2f.add_reference_face("hagrid", test_face_1, save=False)
swapped = f2f.swap_from_reference_face("hagrid", test_face_2)
cv2.imshow("swapped_face_from_embedding", swapped)
cv2.waitKey(10)


