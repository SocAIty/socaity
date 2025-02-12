import os

from socaity.api.image import FluxSchnell

fluxs = FluxSchnell(service="replicate", api_key=os.getenv("REPLICATE_API_KEY", None))
#fluxs = FluxSchnell(service="socaity_local", api_key=os.getenv("SOCAITY_API_KEY", None))
# fluxs = FluxSchnell(service="socaity", api_key=os.getenv("SOCAITY_API_KEY", None))

def test_text2img():
    prompt = (
        """Rick (from Rick and Morty) as a blue whale. The scene is underwater, in twilight. 
The water is shimmering in neon deep-purple and lime-green, blending seamlessly into a cyberpunk-inspired sci-fi scene and bathing the whale into a spotlight.
On the belly of the whale is written in big letters: "DEEPSEEK-R1"
The artwork is minimalistic yet striking and cinematic, showcasing a vibrant neon-green lime palette, rendered in an anime-style illustration with 4k detail. 
Influenced by the artistic styles of Simon Kenny, Giorgetto Giugiaro, Brian Stelfreeze, and Laura Iverson"""
    )
    fj = fluxs.text2img(
        text=prompt, aspect_ratio="1:1", num_outputs=3, num_inference_steps=4, output_format="png",
        disable_safety_checker=True, go_fast=False
    )
    imgs = fj.get_result()
    if not isinstance(imgs, list):
        imgs = [imgs]

    for i, img in enumerate(imgs):
        img.save(f"test_files/output/text2img/test_fluxs_text2img_{i}.png")

if __name__ == "__main__":
    test_text2img()