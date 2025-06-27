  <h1 align="center" style="margin-top:-25px">SocAIty SDK</h1>
<p align="center">
  <img align="center" src="docs/socaity_icon.png" height="200" />
</p>
  <h2 align="center" style="margin-top:-10px">Build AI-powered applications with ease </h2>


The SDK provides generative models and AI tools across all domains including text, audio, image and more. 
Our APIs and SDK allows you to run models as simple python functions. No GPU or AI knowledge required.
Build your dream application by composing different models together.

If you are a Software Engineer, Game Developer, Artist, Content Creator and you want to automate with AI this SDK is for you.

For an overview of all models and to obtain an API key visit [socaity.ai](https://www.socaity.ai)

Run models as if they were python functions nomatter where they are deployed:

You can focus on your app, while we handle all the complicated stuff under the hood.

<hr />

Quicklinks:
- [Quick Start](#quick-start) contains a simple example to get you started
- [Models Zoo](#model-zoo) an overview of all models.
- [Working locally or with other providers](#working-locally-or-with-other-providers)

<hr />

# Getting started

## Installation
Install the package from PyPi
```python
pip install socaity
```

## Authentication

For using socaity.ai services you need to set the environment variable `SOCAITY_API_KEY`.
You can obtain an API key from [socaity.ai](https://www.socaity.ai) after signing up.
Now you are ready to use the SDK.

**Alternatively** you can set the API key in your code when using the SDK. 
We don't recommend this, as it a common mistake to push your code including your API key to a public repository.
```python
from socaity import FluxSchnell
flux_schnell = FluxSchnell(service="socaity", api_key="sai..your_api_key")
```

If you **instead** want to directly communicate with your runpod services or replicate you can set 
the environment variable `RUNPOD_API_KEY` or `REPLICATE_API_KEY`.
When initializing your ModelClient you can additionally pass which provider you want to use by using "service" parameter.

# Quick start

Import a model from the model-zoo or just use the simple API (text2img, text2speech etc.)
```python
from socaity import speechcraft
audiogen = speechcraft(api_key=os.getenv("SOCAITY_API_KEY"))
```
Then you can use it as a function
```python
audio_job = audiogen.text2voice(text="welcome to generative ai", voice="hermine")
audio_job.get_result().save("welcome.mp3")
```

### Example 1: Combine llm, text2img and text2speech

We will use different models to showcase how to create for example a perfect combination for a blog.
```python
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
```
This results in something like this:

https://github.com/user-attachments/assets/978ee377-3ceb-4a87-add5-daee15306231

### Jobs vs. Results

When you invoke an service, internally we use threading and asyncio to check the socaity endpoints for the result.
This makes it possible to run multiple services in parallel and is very efficient.
```python
# the base method always returns a job
d_job = deepseek_v3("what a time to be alive")
# in the meantime you can call other services or do what you want
... do other things here ... 
# when you need the result you can call get_result()
poem = d_job.get_result()
```

# Model zoo

A curated list of hosted models you always find on [socaity.ai](https://www.socaity.ai).

To start here's a list of some of the models you can use with the SDK.
Just import them with ```from socaity import ...``` to use them.

### Text domain
- DeepSeek models
- OpenAPI models
- LLama3 Family (8b, 13b, 70b models)

### Image domain
- FluxSchnell (Text2Image)
- SAM2 (Image and video segmentation)
- TencentArc Photomaker

### Audio domain
- [SpeechCraft](https://github.com/SocAIty/SpeechCraft) (Text2Voice, VoiceCloning)


Note that we have just launched the startup. Expect new models coming highly frequently.


# Working locally or with other providers

Any service that is [fastSDK](https://github.com/SocAIty/fastsdk) compatible  (openAPI / [fastTaskAPI](https://github.com/SocAIty/FastTaskAPI), replicate and [runpod](https://www.runpod.io/)) 
can be used with this package.

Model deployment type    | Description                                                    | Pros                                           | Cons
-------------            |----------------------------------------------------------------|------------------------------------------------| ------------
Locally         | Install genAI packages on your machine and use it with socaity | Free, Open-Source                              | GPU needed, more effort
Hosted  | Use the AIs hosted on socaity servers or of another provider.  | Runs everywhere, Ultra-easy, always up to date | Slightly higher cost
Hybrid | Deploy on runpod, locally and use socaity services.            | Full flexibility                               | Effort




### Hosting a service on Socaity.ai

Any service created with [fasttaskapi]() can be hosted on socaity.ai for free if made public. You can even earn some credits.
The service will then be added to the socaity SDK.
Checkout [https://www.socaity.ai] for more information.

Furthermore: any service that is created with [FastTaskAPI](https://github.com/SocAIty/FastTaskAPI) can be easily used in combination with [FastSDK](https://github.com/SocaIty/fastsdk).
Checkout the [FastSDK](https://github.com/SocaIty/fastsdk) documentation for more information.


# Important Note
PACKAGE IS IN ALPHA RELEASE. 
EXPECT RAPID CHANGES TO SYNTAX AND FUNCTIONALITY.

# Contribute

Any help with maintaining and extending the package is welcome. 
Feel free to open an issue or a pull request.

## PLEASE LEAVE A :star: TO SUPPORT THIS WORK
