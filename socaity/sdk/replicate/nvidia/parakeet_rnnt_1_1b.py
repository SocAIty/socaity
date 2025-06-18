from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class parakeet_rnnt_1_1b(FastSDK):
    """
    Generated client for nvidia/parakeet-rnnt-1-1b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="5a2f2250-0001-4849-b676-828f107dfc70", api_key=api_key)
    
    def predictions(self, audio_file: Union[MediaFile, str, bytes], **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            audio_file: Input audio file to be transcribed by the ASR model
            
        """
        return self.submit_job("/predictions", audio_file=audio_file, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions