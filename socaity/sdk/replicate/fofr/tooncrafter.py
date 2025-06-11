from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class tooncrafter(FastSDK):
    """
    Generated client for tooncrafter
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="991c9bb6-6c87-4dc8-8b32-ddd644693c98", api_key=api_key)
    
    def predict(self, image_1: Union[MediaFile, str, bytes], image_2: Union[MediaFile, str, bytes], loop: bool = False, prompt: str = '', max_width: int = 512, max_height: int = 512, interpolate: bool = False, negative_prompt: str = '', color_correction: bool = True, seed: Optional[int] = None, image_3: Optional[Union[MediaFile, str, bytes]] = None, image_4: Optional[Union[MediaFile, str, bytes]] = None, image_5: Optional[Union[MediaFile, str, bytes]] = None, image_6: Optional[Union[MediaFile, str, bytes]] = None, image_7: Optional[Union[MediaFile, str, bytes]] = None, image_8: Optional[Union[MediaFile, str, bytes]] = None, image_9: Optional[Union[MediaFile, str, bytes]] = None, image_10: Optional[Union[MediaFile, str, bytes]] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image_1: First input image
            
            image_2: Second input image
            
            loop: Loop the video Defaults to False.
            
            prompt: prompt Defaults to ''.
            
            max_width: Maximum width of the video Defaults to 512.
            
            max_height: Maximum height of the video Defaults to 512.
            
            interpolate: Enable 2x interpolation using FILM Defaults to False.
            
            negative_prompt: Things you do not want to see in your video Defaults to ''.
            
            color_correction: If the colors are coming out strange, or if the colors between your input images are very different, disable this Defaults to True.
            
            seed: Set a seed for reproducibility. Random by default. Optional.
            
            image_3: Third input image (optional) Optional.
            
            image_4: Fourth input image (optional) Optional.
            
            image_5: Fifth input image (optional) Optional.
            
            image_6: Sixth input image (optional) Optional.
            
            image_7: Seventh input image (optional) Optional.
            
            image_8: Eighth input image (optional) Optional.
            
            image_9: Ninth input image (optional) Optional.
            
            image_10: Tenth input image (optional) Optional.
            
        """
        return self.submit_job("/predict", image_1=image_1, image_2=image_2, loop=loop, prompt=prompt, max_width=max_width, max_height=max_height, interpolate=interpolate, negative_prompt=negative_prompt, color_correction=color_correction, seed=seed, image_3=image_3, image_4=image_4, image_5=image_5, image_6=image_6, image_7=image_7, image_8=image_8, image_9=image_9, image_10=image_10, **kwargs)
     