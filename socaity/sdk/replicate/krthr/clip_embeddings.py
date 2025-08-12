from fastsdk import FastClient, APISeex
from typing import Union, Optional

from media_toolkit import MediaFile


class clip_embeddings(FastClient):
    """
    Generated client for krthr/clip-embeddings
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="32a10c5e-4802-46b1-8928-c4c78a1b294e", api_key=api_key)
    
    def predictions(self, text: Optional[str] = None, image: Optional[Union[MediaFile, str, bytes]] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            text: Input text Optional.
            
            image: Input image Optional.
            
        """
        return self.submit_job("/predictions", text=text, image=image, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions