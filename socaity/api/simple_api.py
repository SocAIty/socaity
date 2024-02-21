from socaity.api.audio import Bark
from socaity.globals import EndPointType


def text2speech(text, *args, **kwargs):
    bark = Bark(endpoint_type=EndPointType.REMOTE)
    return bark.run(text, *args, **kwargs)

def face2face():
    pass

def voice2voice():
    pass