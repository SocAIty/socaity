from socaity.sdk import face2face
from socaity import MediaFile
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "test_files", "face2face")
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "face2face")

test_face_1 = f"{INPUT_DIR}/test_face_1.jpg"
test_face_2 = f"{INPUT_DIR}/test_face_2.jpg"
test_face_3 = f"{INPUT_DIR}/test_face_3.jpg"
test_video = f"{INPUT_DIR}/test_video_ultra_short.mp4"


f2f = face2face(api_key=os.getenv("SOCAITY_API_KEY"))


def test_face2face_initialization():
    """Test that face2face model initializes correctly"""
    assert f2f is not None
    assert hasattr(f2f, 'swap_img_to_img')
    assert hasattr(f2f, 'add_face')
    assert hasattr(f2f, 'swap')


def test_single_face_swap():
    job_swapped = f2f.swap_img_to_img(test_face_1, test_face_2, enhance_face_model=None)
    swapped = job_swapped.get_result()
    swapped.save(f"{OUTPUT_DIR}/test_face_31_swapped.jpg")
    return swapped


def test_create_embedding(face_name: str, face_file: str):
    ref_face_v_job = f2f.add_face(face_name, face_file, save=False)
    ref_face_vector = ref_face_v_job.get_result()
    assert ref_face_vector is not None, "Reference face vector should not be None"
    ref_face_vector.save(f"{OUTPUT_DIR}/{face_name}.npy")


def test_embedding_face_swap():
    if not os.path.exists(f"{OUTPUT_DIR}/hagrid.npy"):
        test_create_embedding("hagrid", test_face_1)

    ref_face_vector = MediaFile().from_file(f"{OUTPUT_DIR}/hagrid.npy")

    job_swapped = f2f.swap(media=test_face_2, faces=ref_face_vector, enhance_face_model="gpen_bfr")
    swapped = job_swapped.get_result()
    return swapped


def test_video_swap():
    if not os.path.exists(f"{OUTPUT_DIR}/hagrid.npy"):
        test_create_embedding("hagrid", test_face_1)

    embeddings = MediaFile().from_file(f"{OUTPUT_DIR}/hagrid.npy")
    swapped_video_job = f2f.swap_video(
        faces=embeddings,
        target_video=test_video,
        include_audio=True,
        enhance_face_model="gpen_bfr_512"
    )
    swapped_video = swapped_video_job.get_result()
    assert swapped_video is not None, "Swapped video should not be None"
    swapped_video.save(f"{OUTPUT_DIR}/swapped_video.mp4")
    return swapped_video


def test_face2face():
    test_face2face_initialization()
    test_single_face_swap()
    test_embedding_face_swap()
    test_video_swap()
    return True


if __name__ == "__main__":
    # test_single_face_swap()
    test_video_swap()
    test_embedding_face_swap()
