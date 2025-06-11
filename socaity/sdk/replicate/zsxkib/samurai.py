from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class samurai(FastSDK):
    """
    Generated client for samurai
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="bd5923e2-7495-44a9-9255-cb29b03be8da", api_key=api_key)
    
    def predict(self, video: Union[MediaFile, str, bytes], width: int = 400, height: int = 300, x_coordinate: int = 100, y_coordinate: int = 100, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            video: Input video to process
            
            width: Width of bounding box Defaults to 400.
            
            height: Height of bounding box Defaults to 300.
            
            x_coordinate: x-coordinate of top-left corner of bounding box Defaults to 100.
            
            y_coordinate: y-coordinate of top-left corner of bounding box Defaults to 100.
            
        """
        return self.submit_job("/predict", video=video, width=width, height=height, x_coordinate=x_coordinate, y_coordinate=y_coordinate, **kwargs)
     