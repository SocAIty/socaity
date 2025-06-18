import os
from socaity.sdk.replicate.meta import sam_2

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
INPUT_IMG = os.path.join(BASE_DIR, "test_files", "face2face", "test_face_1.jpg")


def test_sam2():
    genai = sam_2(api_key=os.getenv("SOCAITY_API_KEY", None))
    fj = genai(image=INPUT_IMG)
    masks = fj.get_result()
    print(masks)
    return masks


if __name__ == "__main__":
    test_sam2()