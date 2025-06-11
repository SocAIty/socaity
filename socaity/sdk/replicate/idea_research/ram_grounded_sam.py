from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class ram_grounded_sam(FastSDK):
    """
    Generated client for ram_grounded_sam
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="3206a605-e244-4e37-966b-1c46c1ef5473", api_key=api_key)
    
    def predict(self, input_image: Union[MediaFile, str, bytes], use_sam_hq: bool = False, show_visualisation: bool = False, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            input_image: Input image
            
            use_sam_hq: Use sam_hq instead of SAM for prediction Defaults to False.
            
            show_visualisation: Output rounding box and masks on the image Defaults to False.
            
        """
        return self.submit_job("/predict", input_image=input_image, use_sam_hq=use_sam_hq, show_visualisation=show_visualisation, **kwargs)
     