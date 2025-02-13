from socaity import DeepSeekR1, text2voice, text2img

deepseek = DeepSeekR1()
poem = deepseek.chat("Write a poem with 3 sentences why a SDK is so much better than plain web requests.").get_result()
poem = deepseek.pretty(poem)

audio = text2voice(poem, model="speechcraft", voice="hermine")

my_image_prompt = """
A robot enjoying a stunning sunset in the alps. In the clouds is written in big letters "SOCAITY SDK".
The sky is lit with deep purple and lime colors. It is a wide-shot.
The artwork is striking and cinematic, showcasing a vibrant neon-green lime palette, rendered in an anime-style illustration with 4k detail. 
Influenced by the artistic styles of Simon Kenny, Giorgetto Giugiaro, Brian Stelfreeze, and Laura Iverson.
"""

image = text2img(text=my_image_prompt, model="flux-schnell", num_outputs=1)
audio.get_result().save("sdk_poem.mp3")
image.get_result().save("sdk_poem.png")

