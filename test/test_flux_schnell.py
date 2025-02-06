import os

from socaity.api.image import FluxSchnell

#fluxs = FluxSchnell(service="replicate", api_key=os.getenv("REPLICATE_API_KEY", None))
fluxs = FluxSchnell(service="socaity_local", api_key=os.getenv("SOCAITY_API_KEY", None))

def test_text2img():
    prompt = (
        "Rick (of Rick and Morty) standing in a computer store. "
        "Rick is holding a NVIDIA GPU in his hand. The desk has the form of an Cloud like the upload icon."
        "Rick is blurry, the store items are in focus."
        "The store offers GPUs, RAMs, Servers."
        "The store is lit in neon deep-purple light."
        "Sci-fi. Cyberpunk neon-punk style. 4k. Vibrant Neon-Green lime colors. Anime. Illustration. Minimalistic."
        "by Simon Kenny, Giorgetto Giugiaro, Brian Stelfreeze, Laura Iverson"
    )
    fj = fluxs.text2img(
        text=prompt, aspect_ratio="1:1", num_outputs=1, num_inference_steps=4, output_format="png",
        disable_safety_checker=True, go_fast=False
    )
    imgs = fj.get_result()
    if not isinstance(imgs, list):
        imgs = [imgs]

    for i, img in enumerate(imgs):
        img.save(f"test_files/output/text2img/test_fluxs_text2img_{i}.png")

if __name__ == "__main__":
    test_text2img()