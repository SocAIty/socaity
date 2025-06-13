from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class whisper_subtitles(FastSDK):
    """
    Generated client for m1guelpf/whisper-subtitles
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="21324c71-1e66-46e0-84bd-659122a52fd2", api_key=api_key)
    
    def predict(self, audio_path: Union[MediaFile, str, bytes], format: str = 'vtt', model_name: str = 'base', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            audio_path: Audio file to transcribe
            
            format: Whether to generate subtitles on the SRT or VTT format. Defaults to 'vtt'.
            
            model_name: Name of the Whisper model to use. Defaults to 'base'.
            
        """
        return self.submit_job("/predictions", audio_path=audio_path, format=format, model_name=model_name, **kwargs)
     