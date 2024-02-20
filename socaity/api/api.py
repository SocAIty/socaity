"""
This file contains a library of ClientAPIs.
It comes with predefined classes (ClientAPIs) for the most used models.
Instead of using clients and jobs directly, you can use the predefined "model" ClientAPI classes to do the work.

A ClientAPI is a class that contains the logic to pre and post_process a request to an endpoint.
It is a wrapper around the client and job classes.

"""
from typing import Union
from socaity.core.ClientAPI import ClientAPI
from globals import ModelType, EndPointType
from socaity.utils.audio import audio_from_bytes


class Bark(ClientAPI):
    def __init__(self, endpoint_type: Union[EndPointType, str] = EndPointType.REMOTE):
        super().__init__(
            model_type=ModelType.TEXT2VOICE,
            model_name="bark",
            endpoint_type=endpoint_type
        )

    def validate_params(
            self,
            text: str | list,
            voice_name_or_embedding_path: str = "en_speaker_3",
            *args, **kwargs):

        # add named parameters to args
        args = (text, voice_name_or_embedding_path,) + args

        return args, kwargs

    def _pre_process(self, text: str | list, *args, **kwargs):
        # attempt to make it batched.
        if isinstance(text, str):
            text = [text]

        # add text again to args
        args = (text,) + args

        return args, kwargs

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
        *args,
        **kwargs
    ):
        # just reuse args to easy pass them to super
        _args = locals()
        _args = _args + (args,)

        return super.__call__(text, *args, **kwargs)

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
        *args, **kwargs
    ):
        # just reuse args to easy pass them to super
        _args = locals()
        _args = _args.values() + args

        return self.__call__(*args, **kwargs)



