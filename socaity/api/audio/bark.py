from typing import Union

from socaity import AsyncServerJob
from socaity.core.job import Job
from socaity.core.client_api import ClientAPI
from socaity.globals import ModelType, EndPointType
from socaity.utils.audio import audio_from_bytes
from socaity.utils.utils import get_function_parameters_as_dict


class Bark(ClientAPI):
    """
    With Bark (adapted by socAIty) you can:
    - Convert text to natural sounding speech with predefined speakers in 100+ languages.
    - Clone voices by creating embeddings from audio files
    - Convert voice2voice aka voice cloning

    For available speakers visit:
    - Official page of suno: https://suno-ai.notion.site/8b8e8749ed514b0cbf3f699013548683?v=bc67cff786b04b50b3ceb756fd05f68c
    - For other speakers visit the socaity references.

    Bark is developed by Suno.ai. With this client you interact with the Bark adaptation of socAIty.
    For the repos visit: https://github.com/SocAIty/BarkVoiceCloneREST
    """
    def __init__(self, endpoint_type: Union[EndPointType, str] = EndPointType.REMOTE, *args, **kwargs):
        super().__init__(
            model_type=ModelType.TEXT2VOICE,
            model_name="bark",
            endpoint_type=endpoint_type,
            *args, **kwargs
        )

    def validate_params(
            self,
            text: str | list,
            voice_name_or_embedding_path: str = "en_speaker_3",
            *args, **kwargs) -> (bool, str):
        """
        Method is executed before a job is created.
        Returns True if the parameters are valid, otherwise False.
        """
        return True, None

    def _pre_process(self, text: str | list, *args, **kwargs) -> dict:
        # add text again to args
        _kwargs = get_function_parameters_as_dict(self.run, locals(), kwargs)

        # attempt to make it batched.
        if isinstance(text, str):
            _kwargs["text"] = [text]

        return _kwargs

    def _post_process(self, result, *args, **kwargs):
        return audio_from_bytes(result, save_file_path=None)

    def __call__(
        self,
        text: str | list,
        voice_name_or_embedding_path: str = "en_speaker_3",
        semantic_temp=0.7,
        semantic_top_k=50,
        semantic_top_p=0.95,
        coarse_temp=0.7,
        coarse_top_k=50,
        coarse_top_p=0.95,
        fine_temp=0.5,
        **kwargs
    ):
        # just reuse args to easy pass them to super
        _kwargs = get_function_parameters_as_dict(self.run, locals(), kwargs)

        return super().__call__(**_kwargs)

    def run(
        self,
        text: str | list,
        voice_name_or_embedding_path: str = "en_speaker_3",
        semantic_temp=0.7,
        semantic_top_k=50,
        semantic_top_p=0.95,
        coarse_temp=0.7,
        coarse_top_k=50,
        coarse_top_p=0.95,
        fine_temp=0.5,
        **kwargs
    ) -> Union[Job, AsyncServerJob]:
        # just reuse args to easy pass them to super
        _kwargs = get_function_parameters_as_dict(self.run, locals(), kwargs)
        return self.__call__(**_kwargs)

    def run_sync(
        self,
        text: str | list,
        voice_name_or_embedding_path: str = "en_speaker_3",
        semantic_temp=0.7,
        semantic_top_k=50,
        semantic_top_p=0.95,
        coarse_temp=0.7,
        coarse_top_k=50,
        coarse_top_p=0.95,
        fine_temp=0.5,
        **kwargs):
        # just reuse args to easy pass them to super
        _kwargs = get_function_parameters_as_dict(self.run, locals(), kwargs)
        return super().run_sync(**_kwargs)