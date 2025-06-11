from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class whisper_subtitles(FastSDK):
    """
    Generated client for whisper_subtitles
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="1da2fc53-7cb4-4f25-a4d6-40bf72269dde", api_key=api_key)
    
    def predict(self, audio_path: Union[MediaFile, str, bytes], format: str = 'vtt', model_name: str = 'base', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            audio_path: Audio file to transcribe
            
            format: Whether to generate subtitles on the SRT or VTT format. Defaults to 'vtt'.
            
            model_name: Name of the Whisper model to use. Defaults to 'base'.
            
        """
        return self.submit_job("/predict", audio_path=audio_path, format=format, model_name=model_name, **kwargs)
     