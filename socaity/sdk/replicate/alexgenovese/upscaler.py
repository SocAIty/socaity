from fastsdk import FastClient, APISeex
from media_toolkit import MediaFile


class upscaler(FastClient):
    """
    Generated client based on alexgenovese/upscaler format
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="e820dd9c-b415-438a-9757-fa53b88b3c2a", api_key=api_key)
    
    def predictions(self, image: MediaFile, scale: float = 4.0, face_enhance: bool = True, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Input image
            
            scale: Factor to scale image by Defaults to 4.0.
            
            face_enhance: Face enhance Defaults to True.
            
        """
        return self.submit_job("/predictions", image=image, scale=scale, face_enhance=face_enhance, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions
