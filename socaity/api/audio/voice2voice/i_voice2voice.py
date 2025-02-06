from abc import abstractmethod
from typing import Union, List

import media_toolkit as mt

class _BaseVoice2Voice:

    @abstractmethod
    def voice2voice(
            self,
            voice_name: str,
            audio_file: Union[str, bytes],
            *args, **kwargs
    ) -> Union[mt.AudioFile, List[mt.AudioFile], None]:
        """
        Converts text to an image
        :param text: The text to convert to an image
        :return: The image
        """
        raise NotImplementedError("Please implement this method")


# Factory method for generalized model_hosting_info calling
def voice2voice(
        voice_name: str,
        audio_file: Union[str, bytes],
        model="speechcraft",
        service="socaity",
        *args, **kwargs
) -> Union[mt.AudioFile, List[mt.AudioFile], None]:
    if model == "speechcraft":
        from socaity.api.audio.text2voice.speechcraft.speechcraft_api import SpeechCraft
        s = SpeechCraft(service=service)
        return s.voice2voice(voice_name=voice_name, audio_file=audio_file, *args, **kwargs)

    return None
