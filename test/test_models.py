

from test_replicate.test_flux_schnell import test_text2img
from test_replicate.test_llama3 import test_llama_models
from test_replicate.test_blip2 import test_image_captioning, test_image_text_matching, test_visual_question_answering


rep_tests = [
    test_text2img,
    test_llama_models,
    test_image_captioning,
    test_image_text_matching,
    test_visual_question_answering
]


if __name__ == "__main__":
    for test in rep_tests:
        test()