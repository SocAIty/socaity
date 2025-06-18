from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class ram_grounded_sam(FastSDK):
    """
    Generated client for idea-research/ram-grounded-sam
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="cdc115d5-e386-47a4-9b7f-8f447313f19c", api_key=api_key)
    
    def predictions(self, input_image: Union[MediaFile, str, bytes], use_sam_hq: bool = False, show_visualisation: bool = False, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            input_image: Input image
            
            use_sam_hq: Use sam_hq instead of SAM for prediction Defaults to False.
            
            show_visualisation: Output rounding box and masks on the image Defaults to False.
            
        """
        return self.submit_job("/predictions", input_image=input_image, use_sam_hq=use_sam_hq, show_visualisation=show_visualisation, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions