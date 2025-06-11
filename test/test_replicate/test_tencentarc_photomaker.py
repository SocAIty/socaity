from socaity import TencentPhotoMaker, ImageFile
import os

genai = TencentPhotoMaker(service="replicate", api_key=os.getenv("REPLICATE_API_KEY", None))

def test_TencentPhotoMaker():
    image = "test_files/face2face/test_face_1.jpg"
    fj = genai.create_socaity_avatar(input_image=image, num_outputs=3)
    avatars = fj.get_result()
    if not isinstance(avatars, list):
        avatars = [avatars]

    for i, avatar in enumerate(avatars):
        avatar = ImageFile().from_any(avatar)
        avatar.save(f"test_files/output/tencent_photomaker/avatar_{i}.jpg")


if __name__ == "__main__":
    test_TencentPhotoMaker()