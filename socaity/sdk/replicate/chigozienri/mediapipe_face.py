from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class mediapipe_face(FastSDK):
    """
    Generated client for mediapipe_face
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="828e0ad5-e15e-4bf2-998a-e68063727300", api_key=api_key)
    
    def predict(self, images: Union[MediaFile, str, bytes], bias: float = 0.0, blur_amount: float = 0.0, output_transparent_image: bool = False, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            images: Input image as png or jpeg, or zip/tar of input images
            
            bias: Bias to apply to mask (lightens background) Defaults to 0.0.
            
            blur_amount: Blur to apply to mask Defaults to 0.0.
            
            output_transparent_image: if true, outputs face image with transparent background Defaults to False.
            
        """
        return self.submit_job("/predict", images=images, bias=bias, blur_amount=blur_amount, output_transparent_image=output_transparent_image, **kwargs)
     