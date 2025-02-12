import os

from socaity import Sam2

genai = Sam2(service="replicate", api_key=os.getenv("REPLICATE_API_KEY", None))
# fluxs = FluxSchnell(service="socaity_local", api_key=os.getenv("SOCAITY_API_KEY", None))

def test_sam2():
    image = "test_files/face2face/test_face_1.jpg"
    fj = genai.segment(image=image)
    masks = fj.get_result()
    print(masks)


if __name__ == "__main__":
    test_sam2()