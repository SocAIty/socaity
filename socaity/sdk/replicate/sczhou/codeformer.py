from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class codeformer(FastSDK):
    """
    Generated client for sczhou/codeformer
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="3c7452a1-b283-46c8-ac17-64d7335e7782", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], upscale: int = 2, face_upsample: bool = True, background_enhance: bool = True, codeformer_fidelity: float = 0.5, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
            upscale: The final upsampling scale of the image Defaults to 2.
            
            face_upsample: Upsample restored faces for high-resolution AI-created images Defaults to True.
            
            background_enhance: Enhance background image with Real-ESRGAN Defaults to True.
            
            codeformer_fidelity: Balance the quality (lower number) and fidelity (higher number). Defaults to 0.5.
            
        """
        return self.submit_job("/predictions", image=image, upscale=upscale, face_upsample=face_upsample, background_enhance=background_enhance, codeformer_fidelity=codeformer_fidelity, **kwargs)
     