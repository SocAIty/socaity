from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class background_remover(FastSDK):
    """
    Generated client for codeplugtech/background-remover
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="ac005f5c-17c4-4693-a642-24824565c896", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Input image
            
        """
        return self.submit_job("/predictions", image=image, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions