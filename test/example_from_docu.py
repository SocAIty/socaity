import os
from socaity import speechcraft
from socaity.sdk.replicate.deepseek_ai import deepseek_v3
from socaity.sdk.replicate.black_forest_labs import flux_schnell

sk_api_key = os.getenv("SOCAITY_API_KEY")

deepseek = deepseek_v3(api_key=sk_api_key)
poem = deepseek(prompt="Write a poem with 3 sentences why a SDK is so much better than plain web requests.").get_result()
poem = "".join(poem)

audiogen = speechcraft(api_key=sk_api_key)
audio = audiogen.text2voice(text=poem, voice="hermine")

my_image_prompt = """
A robot enjoying a stunning sunset in the alps. In the clouds is written in big letters "SOCAITY SDK".
The sky is lit with deep purple and lime colors. It is a wide-shot.
The artwork is striking and cinematic, showcasing a vibrant neon-green lime palette, rendered in an anime-style illustration with 4k detail. 
Influenced by the artistic styles of Simon Kenny, Giorgetto Giugiaro, Brian Stelfreeze, and Laura Iverson.
"""

flux = flux_schnell(api_key=sk_api_key)
images = flux(prompt=my_image_prompt, num_outputs=1, seed=12).get_result()
for i, img in enumerate(images):
    img.save(f"sdk_poem_{i}.png")

audio.get_result().save("sdk_poem.mp3")
