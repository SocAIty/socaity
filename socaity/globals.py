import logging
from enum import Enum


class EndPointType(Enum):
    LOCAL = "localhost"
    REMOTE = "remote"
    SOCAITY = "socaity"


class EndpointSpecification(Enum):
    SOCAITY = "socaity"  # all servers that support socaity protocol with job queues
    OPENAPI = "openapi"  # for example fastapi servers
    OTHER = "other"  # other servers


class ModelType(Enum):
    TEXT2VOICE = "text2voice"
    VOICE2VOICE = "voice2voice"
    AUDIO2FACE = "audio2face"
    FACE2FACE = "face2face"
    ANY = "any"


logging.getLogger().setLevel(logging.INFO)

SOCAITY_API_URL = "https://localhost:8000/" # "https://socaity.ai/"
SOCAITY_API_VERSION = "v1"
