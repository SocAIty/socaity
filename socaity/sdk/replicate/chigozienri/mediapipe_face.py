from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class mediapipe_face(FastSDK):
    """
    Generated client for chigozienri/mediapipe-face
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="f5adba97-df80-4165-94ec-0014501d1719", api_key=api_key)
    
    def predictions(self, images: Union[str, MediaFile, bytes], bias: float = 0.0, blur_amount: float = 0.0, output_transparent_image: bool = False, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            images: Input image as png or jpeg, or zip/tar of input images
            
            bias: Bias to apply to mask (lightens background) Defaults to 0.0.
            
            blur_amount: Blur to apply to mask Defaults to 0.0.
            
            output_transparent_image: if true, outputs face image with transparent background Defaults to False.
            
        """
        return self.submit_job("/predictions", images=images, bias=bias, blur_amount=blur_amount, output_transparent_image=output_transparent_image, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions