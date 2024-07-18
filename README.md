  <h1 align="center" style="margin-top:-25px">SocAIty SDK</h1>
<p align="center">
  <img align="center" src="docs/socaity_icon.png" height="200" />
</p>
  <h2 align="center" style="margin-top:-10px">Your model zoo and SDK for generative AI. </h2>


The SDK provides generative models and AI tools across all domains including text, audio, and image. 
Think of it as open-CV for generative AI. 
It allows you to run the models as simple python functions either locally, on your own servers, or on Socaity's servers, 
with all complex backend operations handled automatically.

Run models (and services) as if they were python functions:
- deployed on your localhost / your own server
- hybrid deployment
- hosted on socaity servers

The package then provides simplified API calls and AI service inference - also for long running tasks.

<hr />

Get started: Install the package from PyPi:
```python
pip install socaity
```

If you are a Game Developer, Artist or Content Creator, this SDK is for you.

# Examples and Use-Cases

The future of the Internet and the economy is generative. However, there's not one model that fits all.
For real world applications, you need to chain different models together combine them with other services.

AI NPC Agents - How to:
Here's a common example of a game developer who wants to have AI NPC agents in his game. His workflow:
1. Generate the text the NPC should say.
2. use a `text2speech` model to synthesize speech for the NPC.
3. uses the `voice2voice` model to change the voice of the NPC to one of his artists. 
4. uses `audio2face` model to generate facial animations for the NPC.

Automated video content - How to:
1. Create a thumbnail for a video with `text2image`
2. Swap the faces in the video with `face2face`
3. Generate a voice-over for the video with `text2voice`

Look into the UseCases.md for more examples like this.

# Overview



## How it works
 
The package sends web requests to models hosted behind REST APIs.
Any REST interface that is [fastSDK](https://github.com/SocAIty/fastsdk) compatible  (openAPI / [fastTaskAPI](https://github.com/SocAIty/FastTaskAPI)) 
can be used with this package.

The troublesome implementation of threading, sync, async, error handlings and job creation is done under the hood for you.
On this way, you can focus on your business logic and use AI natively like any other python function.

Run models (and services) as if they were python functions:

Model deployment type    | Description                                    | Pros | Cons
------------- |-----------------------------------------------------------| ------------- | ------------
Locally | Install genAI packages on your machine and use it with AnyGEN | Free, Open-Source | GPU needed, more effort
Hosted  | Use the AIs hosted on socaity services.                     | Runs everywhere, Ultra-easy | None
Hybrid | Deploy some services on your servers and use others from     | pyAudio2Face | audio2face



# Generative AI - model zoo

The models are categorized by their domain and use-case.

### Audio domain

Use-Case      | Description                                               | Repositories | Models
------------- |-----------------------------------------------------------| ------------- | ------------
text2voice | Convert text to natural sounding speech. In many languages | SpeechCraft | Bark
voice2voice  | Convert one persons voice to another.                     | Voice2Voice | RVC
audio2face | Create expressive facial animation from audio.            | pyAudio2Face | audio2face

### Image domain
Use-Case      | Description                                    | Repositories | Models
------------- |------------------------------------------------|--------------| ------------
face2face | Swap faces in images. Deep fakes.              | face2face    | inswapper_128
text2image | Convert an image description to expressive art | coming soon  | StableDiffusion, AuraFlow
face-restoration | Restors, bad quality or distorted faces in images | face2face    | GPEN

### Animation
Use-Case      | Description                                                | Models
------------- |------------------------------------------------------------| -------------
audio2face | Create expressive facial animation from audio.             | nvidia auio2face
text2face | Convert text to audio and then to facial animation.         | text2speech, audio2face

### Text domain
Use-Case      | Description               | Models
------------- |---------------------------| -------------
chat | Text-generation with LLMs | chat-gpt, claude

# AI - model zoo

Socaity provides a model zoo for recognition AI models. The models are categorized by their domain and use-case.
### Image domain
Use-Case      | Description                                       | Repositories | Models
------------- |---------------------------------------------------|--------------| ------------
face-recognition | Identify persons in images                        | Face2Face    | inswapper_128




# Usage
We provide two APIs for inferencing, SimpleAPI and ClientAPI.
The simpleAPI is literally a wrapper for the ClientAPI but simplifies the usage of the models.

## Simple API
The simple API contains functions for the most use-cases. Behind

```python
from socaity import text2speech, text2img, voice2voice
text2speech("Hello World")
```

This code internally initializes an API client from the ClientAPI and uses it.


## Client API

The ClientAPI comes with predefined classes for the most used models.

## async usage
```python
from socaity import Bark, await_result
job = Bark("localhost").run("Hello", affe=2) 
audio, sample_rate = await_result(job)  # this is a blocking call until the job is finished
```
A ClientAPI defines pre -and post-processing functions and utility functions for those models.
You can identify clientAPIs by a UpperCamelCase name or import them directly from the submodules api.*.

The clientAPI also provides the possibility to:
- specify an exact endpoint type like "localhost"
- the provider

## sync usage
```python
from socaity import Bark
audio, sample_rate = Bark("localhost").run_sync("Hello", affe=2)
```
# Setup:
Install the package from pip:
```python
pip install socaity
```
or install from source if you want to work with the newest version:
```python
pip install git+git://github.com/SocAIty/socaity
```



## How does the ClientAPI work?
Internally a ClientAPI:
1. creates a client with predefined endpoint parameters
2. on call creates a job and submits it to the client
3. returns the result of the job


## Advanced usage

Subclass the ClientAPI to define your own models and use them with the same interface.


# Endpoints

The endpoints for the models are defined in the `socaity.endpoints` module.
An endpoint contains the information to connect to an API like service_url, endpoint_name, endpoint_type, and provider.
Feel free to add your own endpoints or use the predefined ones.

# Common Questions:

- What is SocAIty?


# Important Note
- PACKAGE IS UNDER DEVELOPMENT AND FAR AWAY FROM BEING PRODUCTION READY
- LEAVE A STAR TO SUPPORT THIS WORK AND FOR MORE MODELS BEING ADDED TO THE LIBRARY

