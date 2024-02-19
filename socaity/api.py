"""
This file simplifies the usage of the API.
Instead of using clients and jobs directly, you can use the predefined "model" classes to do the work.
"""
from socaity.core.decorators import ClientAPI
from globals import ModelType, EndPointType


class API:


# Instead of defining local, remote etc. here:
# dynamically swich between local and remote in the API class.
# The client will be created in the clientapi class when a different endpoint is used.
# All clients are stored in the registry.py file.

# The same applies for endpoints. The endpoints get a decorator and then are stored in the registry.py file.
# This makes it easier for the registry to manage the endpoints and clients.



@ClientAPI(model_type=ModelType.TEXT2VOICE, model_name="bark", endpoint_type=EndPointType.LOCAL)
def text2speech(text):
    pass

@ClientAPI(model_type=ModelType.FACE2FACE, model_name="bark", endpoint_type=EndPointType.LOCAL)
