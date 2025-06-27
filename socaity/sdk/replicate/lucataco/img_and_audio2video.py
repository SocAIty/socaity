from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class img_and_audio2video(FastSDK):
    """
    Generated client for lucataco/img-and-audio2video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="957da6c3-7cbb-441f-acd1-e738c018e0e1", api_key=api_key)
    
    def predictions(self, audio: Union[str, MediaFile, bytes], image: Union[str, MediaFile, bytes], **kwargs) -> APISeex:
        """
        
        
        
        Args:
            audio: Audio file
            
            image: Grayscale input image
            
        """
        return self.submit_job("/predictions", audio=audio, image=image, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions