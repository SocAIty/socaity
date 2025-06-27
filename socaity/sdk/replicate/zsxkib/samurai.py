from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class samurai(FastSDK):
    """
    Generated client for zsxkib/samurai
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0a6c1511-3558-4796-bc3c-94417a13b5a7", api_key=api_key)
    
    def predictions(self, video: Union[str, MediaFile, bytes], width: int = 400, height: int = 300, x_coordinate: int = 100, y_coordinate: int = 100, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            video: Input video to process
            
            width: Width of bounding box Defaults to 400.
            
            height: Height of bounding box Defaults to 300.
            
            x_coordinate: x-coordinate of top-left corner of bounding box Defaults to 100.
            
            y_coordinate: y-coordinate of top-left corner of bounding box Defaults to 100.
            
        """
        return self.submit_job("/predictions", video=video, width=width, height=height, x_coordinate=x_coordinate, y_coordinate=y_coordinate, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions