"""
This file is a library of Endpoints.
An Endpoint contains the information to connect to a model hosted on a provider (Remote, Local or Decentralized).
"""
from socaity.globals import EndPointType, ModelType
from socaity.core.endpoint import LocalEndPoint, RemoteEndPoint, SocaityEndpoint

# Todo: Instead of having a list with generative model endpoints and so on:
# Add the endpoints to the registry dynamically when created..?
# therferore make a decorator?


GenerativeModelEndpoints = [
    ### TEXT2VOICE
        ## Bark
            #hosted
            SocaityEndpoint(model_type=ModelType.TEXT2VOICE, model_name="bark"),
            #localhost
            LocalEndPoint(
                model_type=ModelType.TEXT2VOICE,
                model_name="bark",
                service_url="http://localhost:8009",
                endpoint_name="text2voice",
                start_bat_path="A:\\projects\\BarkVoiceCloneREST\\start_server.bat",
                provider="socaity"
            )
]

# Make one dictionary from all endpoint dicts, to make it easier for parsing.
Endpoints = [*GenerativeModelEndpoints]