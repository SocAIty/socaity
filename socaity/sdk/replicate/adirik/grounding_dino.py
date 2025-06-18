from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class grounding_dino(FastSDK):
    """
    Generated client for adirik/grounding-dino
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0c0c9e6c-2cb4-4fa7-87ad-752da9917d37", api_key=api_key)
    
    def predictions(self, box_threshold: float = 0.25, text_threshold: float = 0.25, show_visualisation: bool = True, image: Optional[Union[MediaFile, str, bytes]] = None, query: Optional[str] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            box_threshold: Confidence level for object detection Defaults to 0.25.
            
            text_threshold: Confidence level for object detection Defaults to 0.25.
            
            show_visualisation: Draw and visualize bounding boxes on the image Defaults to True.
            
            image: Input image to query Optional.
            
            query: Comma seperated names of the objects to be detected in the image Optional.
            
        """
        return self.submit_job("/predictions", box_threshold=box_threshold, text_threshold=text_threshold, show_visualisation=show_visualisation, image=image, query=query, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions