import os

from socaity.api.image import FluxSchnell

# fluxs = FluxSchnell(service="replicate", api_key=os.getenv("REPLICATE_API_KEY", None))
fluxs = FluxSchnell(service="socaity_local", api_key=os.getenv("SOCAITY_API_KEY", None))

def test_text2img():
    prompt = (
        "Rick of Rick and Morty sitting in a bathtub smoking pot. "
        "The bathtub has the lable 'flux schnell'."
        "The bathtub is in a dark room with a neon deep-purple light."
        "Sci-fi. Cyberpunk neon-punk style. Vibrant Neon-Green lime colors. Anime. Illustration."
    )
    fj = fluxs.text2img(
        text=prompt, aspect_ratio="16:9", num_outputs=2, num_inference_steps=4, output_format="png",
        disable_safety_checker=True, go_fast=False
    )
    imgs = fj.get_result()
    for i, img in enumerate(imgs):
        img.save(f"test_files/output/text2img/test_fluxs_text2img_{i}.png")

if __name__ == "__main__":
    test_text2img()