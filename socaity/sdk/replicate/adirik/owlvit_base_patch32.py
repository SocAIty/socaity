from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class owlvit_base_patch32(FastSDK):
    """
    Generated client for adirik/owlvit-base-patch32
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="06f63a82-ad3f-4325-91f0-a348cd38852e", api_key=api_key)
    
    def predict(self, threshold: float = 0.1, show_visualisation: bool = True, image: Optional[Union[MediaFile, str, bytes]] = None, query: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            threshold: Confidence level for object detection Defaults to 0.1.
            
            show_visualisation: Draw and visualize bounding boxes on the image Defaults to True.
            
            image: Input image to query Optional.
            
            query: Comma seperated names of the objects to be detected in the image Optional.
            
        """
        return self.submit_job("/predictions", threshold=threshold, show_visualisation=show_visualisation, image=image, query=query, **kwargs)
     