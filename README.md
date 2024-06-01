
# PACKAGE IS UNDER DEVELOPMENT AND NOT YET READY TO USE
## LEAVE A STAR TO GET NOTIFIED WHEN IT IS READY


# SocAIty - your AI Model Zoo
Easy interface for AI models. Python package to use SOTA models across hosted environments.
We are your easy-to-use model zoo for generative AI. No GPU needed, no setup required.
We provide generative models across all domains like text, audio, and image. 

Run models (and services) as if they were python functions:
- hosted on socaity servers
- deployed on your localhost / your own server

Use this package for simplified inference.


## How it works
 
The package sends web requests to models hosted behind REST APIs.
Any REST interface that supports the socaity endpoint specification or any openAPI specification can be used with this package.
The troublesome implementation of threading, sync, async, error handlings and job creation is done under the hood for you.
On this way, you can focus on your business logic and use AI natively like any other python function.

# Model Zoo

Socaity provides a model zoo for generative AI models. The models are categorized by their domain and use-case.
Check-out the socaity_website for more information.

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
