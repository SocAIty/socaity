"""
This file is a library of Endpoints.
An Endpoint contains the information to connect to a model hosted on a provider (Remote, Local or Decentralized).
"""
from socaity.globals import EndPointType, ModelType
from socaity.core.Endpoint import LocalEndPoint, RemoteEndPoint, SocaityEndpoint

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
                model_name="bark", api_url="http://localhost:8009",
                start_bat_path="A:\\projects\\BarkVoiceCloneREST\\start_server.bat",
            )
]




#GenerativeModelEndpoints = {
#    ModelType.TEXT2VOICE: [
#        {
#            "model_name": "bark",
#            EndPointType.REMOTE: [
#                SocaityEndpoint(model_type=ModelType.TEXT2VOICE, model_name="bark")
#            ],
#            EndPointType.LOCAL: [
#                LocalEndPoint(model_type=ModelType.TEXT2VOICE, model_name="bark", api_url="http://localhost:8009",
#                    start_bat_path="A:\\projects\\BarkVoiceCloneREST\\start_server.bat",
#                ),
#            ],
#        }
#    ],
#}

# Make one dictionary from all endpoint dicts, to make it easier for parsing.
Endpoints = [*GenerativeModelEndpoints]