from enum import Enum


class EndPointType(Enum):
    LOCAL = "localhost"
    REMOTE = "remote"


class ModelType(Enum):
    TEXT2VOICE = "text2voice"
    VOICE2VOICE = "voice2voice"
    AUDIO2FACE = "audio2face"
    FACE2FACE = "face2face"