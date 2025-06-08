import os

from socaity import service_manager  # imported to create update first run
from socaity import FluxSchnell


fluxs = FluxSchnell(service="replicate", api_key=os.getenv("REPLICATE_API_KEY", None))
# fluxs = FluxSchnell(service="socaity_local", api_key=os.getenv("SOCAITY_API_KEY", None))
# fluxs = FluxSchnell()

#from socaity import text2img
#my_generated_image = text2img("An elephant swimming in a lake")


def test_text2img():
    prompt = (
        """
A massive beautiful sci-fi robot giant sequoia tree. The full tree including deep roots is showcased. The canopy layer branches into three big branches. The stem is kept shorter. 
The roots look like cables. The stem like a server farm. Branches are fine and robotic structures.

The purpose of the image is to show different technology layers of a companys tech stack.
The root layer will represent the foundational technology blending in typical cloud, server, docker and kubernetes icons.
The stem represents the API and SDK layer.
The canopy layer represents key operating pillars of the company including youtube icon, wordpress, agentic heads, and a sci-fi fashion store.
The upper emergent layer, leaves spaces for additional concrete products.
Theres a swift seperation line between the layers like in an rainforest ecosystem illustration.
The artwork is minimalistic yet striking, showcasing a vibrant deep-purple and neon-green lime palette, rendered in an anime-style illustration with 4k detail. 
Influenced by the artistic styles of Simon Kenny, Giorgetto Giugiaro, Brian Stelfreeze, and Laura Iverson
        """
    )
    fj = fluxs.text2img(
        text=prompt, aspect_ratio="9:16", num_outputs=4, num_inference_steps=4, output_format="png",
        disable_safety_checker=True, go_fast=False
    )
    imgs = fj.get_result()
    if not isinstance(imgs, list):
        imgs = [imgs]

    for i, img in enumerate(imgs):
        img.save(f"test_files/output/text2img/test_fluxs_text2img_{i}.png")


if __name__ == "__main__":
    test_text2img()
