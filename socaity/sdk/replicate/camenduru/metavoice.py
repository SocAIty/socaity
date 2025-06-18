from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class metavoice(FastSDK):
    """
    Generated client for camenduru/metavoice
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0c2da908-6738-4a6f-a4a0-7e289389d18b", api_key=api_key)
    
    def predictions(self, input_audio: Union[MediaFile, str, bytes], text: str = 'This is a demo of text to speech by MetaVoice-1B, an open-source foundational audio model by MetaVoice.', **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            input_audio: Input Image
            
            text: text Defaults to 'This is a demo of text to speech by MetaVoice-1B, an open-source foundational audio model by MetaVoice.'.
            
        """
        return self.submit_job("/predictions", input_audio=input_audio, text=text, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions