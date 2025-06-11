from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class imagebind(FastSDK):
    """
    Generated client for imagebind
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="a13f5445-f9f5-4b20-add6-6e94ec467038", api_key=api_key)
    
    def predict(self, modality: str = 'vision', input: Optional[Union[MediaFile, str, bytes]] = None, text_input: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            modality: modality of the input you'd like to embed Defaults to 'vision'.
            
            input: file that you want to embed. Needs to be text, vision, or audio. Optional.
            
            text_input: text that you want to embed. Provide a string here instead of a text file to input if you'd like. Optional.
            
        """
        return self.submit_job("/predict", modality=modality, input=input, text_input=text_input, **kwargs)
     