from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class img_and_audio2video(FastSDK):
    """
    Generated client for img_and_audio2video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="7af8d381-9673-4fb7-9521-3b312a2be384", api_key=api_key)
    
    def predict(self, audio: Union[MediaFile, str, bytes], image: Union[MediaFile, str, bytes], **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            audio: Audio file
            
            image: Grayscale input image
            
        """
        return self.submit_job("/predict", audio=audio, image=image, **kwargs)
     