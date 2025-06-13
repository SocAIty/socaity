import os

from socaity.sdk.replicate.andreasjansson import blip_2

test_img = "https://socaityfiles.blob.core.windows.net/backend-model-meta/llama3.png"
genai = blip2()

#genai = Blip(service="replicate", api_key=os.getenv("REPLICATE_API_KEY", None))
# fluxs = FluxSchnell(service="socaity_local", api_key=os.getenv("SOCAITY_API_KEY", None))

def test_image_captioning():
    fj = genai.caption(image=test_img)
    generated_text = fj.get_result()
    print(generated_text)

def test_image_text_matching():
    fj = genai.text_matching(image=test_img, caption="a beautiful woman in the sunset")
    matching_score = fj.get_result()
    print(matching_score)

def test_visual_question_answering():
    fj = genai.visual_question_answering(image=test_img, question="what animal is on the image?")
    answer = fj.get_result()
    print(answer)


if __name__ == "__main__":
    test_image_captioning()
    test_image_text_matching()
    test_visual_question_answering()
