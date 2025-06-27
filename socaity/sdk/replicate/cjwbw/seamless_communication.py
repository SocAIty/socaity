from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class seamless_communication(FastSDK):
    """
    Generated client for cjwbw/seamless-communication
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="c3a40fb8-137c-4114-bd7a-017ebfab9502", api_key=api_key)
    
    def predictions(self, task_name: str = 'S2ST (Speech to Speech translation)', input_text_language: str = 'None', max_input_audio_length: float = 60.0, target_language_text_only: str = 'Norwegian Nynorsk', target_language_with_speech: str = 'French', input_text: Optional[str] = None, input_audio: Optional[Union[str, MediaFile, bytes]] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            task_name: Choose a task Defaults to 'S2ST (Speech to Speech translation)'.
            
            input_text_language: Specify language of the input_text for T2ST and T2TT Defaults to 'None'.
            
            max_input_audio_length: Set maximum input audio length. Defaults to 60.0.
            
            target_language_text_only: Set target language for tasks with text output only: S2TT, T2TT and ASR. Defaults to 'Norwegian Nynorsk'.
            
            target_language_with_speech: Set target language for tasks with speech output: S2ST or T2ST. Less languages are available for speech compared to text output. Defaults to 'French'.
            
            input_text: Provide input for tasks with text: T2ST and T2TT. Optional.
            
            input_audio: Provide input file for tasks with speech input: S2ST, S2TT and ASR. Optional.
            
        """
        return self.submit_job("/predictions", task_name=task_name, input_text_language=input_text_language, max_input_audio_length=max_input_audio_length, target_language_text_only=target_language_text_only, target_language_with_speech=target_language_with_speech, input_text=input_text, input_audio=input_audio, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions