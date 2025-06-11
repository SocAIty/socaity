from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class metavoice(FastSDK):
    """
    Generated client for metavoice
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="7a353ba8-24da-4bf3-adf1-e85ab6cd0a32", api_key=api_key)
    
    def predict(self, input_audio: Union[MediaFile, str, bytes], text: str = 'This is a demo of text to speech by MetaVoice-1B, an open-source foundational audio model by MetaVoice.', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            input_audio: Input Image
            
            text: text Defaults to 'This is a demo of text to speech by MetaVoice-1B, an open-source foundational audio model by MetaVoice.'.
            
        """
        return self.submit_job("/predict", input_audio=input_audio, text=text, **kwargs)
     