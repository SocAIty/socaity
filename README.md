# socaity
Easy interface for any python model. Python package to use models across hosted environments. 
We are you're easy to use model zoo for generative AI.

# Inferencing
We provide two APIs for inferencing, SimpleAPI and ClientAPI.
The simpleAPI is literally a wrapper for the ClientAPI but simplifies the usage of the models.

## Simple API
The simple API contains functions for the most used models.

```python
from socaity.api.simple_api import text2speech

text2speech("Hello World")
```

This code internally initializes an API client from the ClientAPI and uses it.


## Client API

The ClientAPI comes with predefined classes for the most used models.
A ClientAPI defines pre -and post-processing functions and utility functions for those models.

```python
from socaity.api import Bark
bark = Bark("localhost")
bark.run("Hello World")
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

Instead of using the predefined classes, you can also create a client directly from an Endpoint and use it.
You can also define your own jobs and submit them to the client.

```python

from socaity.ClientAPI import ClientAPI

client = ClientAPI("http://localhost:5000")
myJob = Job("")
client.run(myJob)

```