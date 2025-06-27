from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class background_remover(FastSDK):
    """
    Generated client for -851-labs/background-remover
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="41bbfe93-f999-4de3-b380-fabe0b960cb0", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], format: str = 'png', reverse: bool = False, threshold: float = 0.0, background_type: str = 'rgba', **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Input image
            
            format: Output format (e.g., png, jpg). Defaults to png. Defaults to 'png'.
            
            reverse: If True, remove the foreground instead of the background. Defaults to False.
            
            threshold: Threshold for hard segmentation (0.0-1.0). If 0.0, uses soft alpha. Defaults to 0.0.
            
            background_type: Background type: 'rgba', 'map', 'green', 'white', [R,G,B] array, 'blur', 'overlay', or path to an image. Defaults to 'rgba'.
            
        """
        return self.submit_job("/predictions", image=image, format=format, reverse=reverse, threshold=threshold, background_type=background_type, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions