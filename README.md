# SocAIty - Your AI Model Zoo
Easy interface for AI models. Python package to use models across hosted environments. 
We are your easy-to-use model zoo for generative AI.
We provide generative models for text, audio, and images. Run them hosted on our servers or on your own.

Use this package for simplified inference.

# Inferencing
We provide two APIs for inferencing, SimpleAPI and ClientAPI.
The simpleAPI is literally a wrapper for the ClientAPI but simplifies the usage of the models.

## Simple API
The simple API contains functions for the most used models.

```python
from socaity import text2speech

text2speech("Hello World")
```

This code internally initializes an API client from the ClientAPI and uses it.


## Client API

The ClientAPI comes with predefined classes for the most used models.
A ClientAPI defines pre -and post-processing functions and utility functions for those models.
You can identify clientAPIs by a UpperCamelCase name or import them directly from the submodules api.*.
The run function returns the completed job.

```python
from socaity import Bark
job = Bark("localhost").run("Hello", affe=2) 
audio, sample_rate = job.result
```
The clientAPI also provides the possibility to:
- specify an exact endpoint type like "localhost"
- the provider

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
