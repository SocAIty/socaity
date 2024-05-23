"""
This file is a library of Endpoints.
An Endpoint contains the information to connect to a model hosted on a endpoint_specification (Remote, Local or Decentralized).
"""
from socaity.globals import ModelType, EndpointSpecification
from socaity.core.endpoint import LocalEndPoint, SocaityServerEndpoint

# Todo: Instead of having a list with generative model endpoints and so on:
# Add the endpoints to the registry dynamically when created..?
# therferore make a decorator?


GenerativeModelEndpoints = [
    # Text Domain
    ### TEXT2VOICE
        ## Bark
            #hosted
            SocaityServerEndpoint(model_type=ModelType.TEXT2VOICE, model_name="bark"),
            #localhost
            LocalEndPoint(
                model_type=ModelType.TEXT2VOICE,
                model_name="bark",
                service_url="http://localhost:8009",
                endpoint_name="text2voice",
                start_bat_path="A:\\projects\\BarkVoiceCloneREST\\start_server.bat",
                endpoint_specification=EndpointSpecification.SOCAITY
            ),

   # Image Domain
   ### FACE2FACE
        # hosted
        SocaityServerEndpoint(model_type=ModelType.FACE2FACE, model_name="face2face"),
        LocalEndPoint(
            model_type=ModelType.FACE2FACE,
            model_name="face2face",
            service_url="http://localhost:8020",
            endpoint_name="swap_one",
            start_bat_path="A:\\projects\\face2face\\start_server.bat",
            endpoint_specification=EndpointSpecification.SOCAITY
        ),
]

# Make one dictionary from all endpoint dicts, to make it easier for parsing.
Endpoints = [*GenerativeModelEndpoints]