from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class parakeet_rnnt_1_1b(FastSDK):
    """
    Generated client for parakeet_rnnt_1_1b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="24c3582c-c233-429f-94b2-f27fb9de9e53", api_key=api_key)
    
    def predict(self, audio_file: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            audio_file: Input audio file to be transcribed by the ASR model
            
        """
        return self.submit_job("/predict", audio_file=audio_file, **kwargs)
     