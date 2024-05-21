# SocAIty - your AI Model Zoo
Easy interface for AI models. Python package to use SOTA models across hosted environments. 
We are your easy-to-use model zoo for generative AI. No GPU needed, no setup required.

We provide generative models for text, audio, and images. Run them hosted on our servers or on your own.

Use this package for simplified inference.

# Model Zoo


### Audio domain

Use-Case      | Description                                                | Models
------------- |------------------------------------------------------------| -------------
Text-to-Speech| Convert text to natural sounding speech. In many languages | Bark
voice2voice  | Convert one persons voice to another.                      |
audio2face | Create expressive facial animation from audio.             |

### Image domain


### Animation
Use-Case      | Description                                                | Models
------------- |------------------------------------------------------------| -------------
audio2face | Create expressive facial animation from audio.             | nvidia auio2face
text2face | Convert text to audio and then to facial animation.         | text2speech, audio2face



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
A ClientAPI defines pre -and post-processing functions and utility functions for those models.
You can identify clientAPIs by a UpperCamelCase name or import them directly from the submodules api.*.
The run function returns the completed job.

```python
from socaity import Bark, await_result
job = Bark("localhost").run("Hello", affe=2) 
audio, sample_rate = await_result(job)
```
The clientAPI also provides the possibility to:
- specify an exact endpoint type like "localhost"
- the provider

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
