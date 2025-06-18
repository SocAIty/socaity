from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class deoldify_video(FastSDK):
    """
    Generated client for arielreplicate/deoldify-video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="c65f8678-d8be-4042-b11e-e04d97122e91", api_key=api_key)
    
    def predictions(self, input_video: Union[MediaFile, str, bytes], render_factor: int = 21, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            input_video: Path to a video
            
            render_factor: The default value of 35 has been carefully chosen and should work -ok- for most scenarios (but probably won't be the -best-). This determines resolution at which the color portion of the image is rendered. Lower resolution will render faster, and colors also tend to look more vibrant. Older and lower quality images in particular will generally benefit by lowering the render factor. Higher render factors are often better for higher quality images, but the colors may get slightly washed out. Defaults to 21.
            
        """
        return self.submit_job("/predictions", input_video=input_video, render_factor=render_factor, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions