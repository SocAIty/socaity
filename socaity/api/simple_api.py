import api
from core.Endpoint import EndPointType


def text2speech(text, *args, **kwargs):
    bark = api.bark(endpoint_type=EndPointType.REMOTE)
    return bark.run(text, *args, **kwargs)

def face2face():
    pass

def voice2voice():
    pass