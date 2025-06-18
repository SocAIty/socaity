from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class grounded_sam(FastSDK):
    """
    Generated client for schananas/grounded-sam
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="2312e3fb-6a3e-4d7c-b0b6-6f145b0c721f", api_key=api_key)
    
    def predictions(self, image: Union[MediaFile, str, bytes] = 'https://st.mngbcn.com/rcs/pics/static/T5/fotos/outfit/S20/57034757_56-99999999_01.jpg', mask_prompt: str = 'clothes,shoes', adjustment_factor: int = 0, negative_mask_prompt: str = 'pants', **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            image: Image Defaults to 'https://st.mngbcn.com/rcs/pics/static/T5/fotos/outfit/S20/57034757_56-99999999_01.jpg'.
            
            mask_prompt: Positive mask prompt Defaults to 'clothes,shoes'.
            
            adjustment_factor: Mask Adjustment Factor (-ve for erosion, +ve for dilation) Defaults to 0.
            
            negative_mask_prompt: Negative mask prompt Defaults to 'pants'.
            
        """
        return self.submit_job("/predictions", image=image, mask_prompt=mask_prompt, adjustment_factor=adjustment_factor, negative_mask_prompt=negative_mask_prompt, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions