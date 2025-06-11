from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class background_remover(FastSDK):
    """
    Generated client for background_remover
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="eaba2700-2b22-4086-92af-ed4170313bb1", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], format: str = 'png', reverse: bool = False, threshold: float = 0.0, background_type: str = 'rgba', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
            format: Output format (e.g., png, jpg). Defaults to png. Defaults to 'png'.
            
            reverse: If True, remove the foreground instead of the background. Defaults to False.
            
            threshold: Threshold for hard segmentation (0.0-1.0). If 0.0, uses soft alpha. Defaults to 0.0.
            
            background_type: Background type: 'rgba', 'map', 'green', 'white', [R,G,B] array, 'blur', 'overlay', or path to an image. Defaults to 'rgba'.
            
        """
        return self.submit_job("/predict", image=image, format=format, reverse=reverse, threshold=threshold, background_type=background_type, **kwargs)
     