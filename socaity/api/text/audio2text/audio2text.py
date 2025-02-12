from abc import abstractmethod
from typing import Union, List

import media_toolkit as mt
import numpy as np

class _BaseAudio2Text:
    @abstractmethod
    def transcribe(self, audio: Union[np.array, bytes, str, mt.AudioFile], *args, **kwargs) -> str:
        """
        Creates an image caption or description from an image.
        :param text: The text to convert to an image
        :return: The image
        """
        raise NotImplementedError("Please implement this method")

    # alias
    audio2text = transcribe




def transcribe(audio: Union[np.array, bytes, str, mt.AudioFile],
               model="insanely-fast-whisper",
               service="socaity", *args, **kwargs) -> str:
    from .whisper import InsanelyFastWhisper
    names_cl = {
        "insanely-fast-whisper": InsanelyFastWhisper,
    }
    names_cl = {k.lower().replace("-", ""): v for k, v in names_cl.items()}
    mdlcl = names_cl.get(model.lower().replace("-", ""), InsanelyFastWhisper)
    return mdlcl(service=service).image2text(audio=audio, *args, **kwargs)

