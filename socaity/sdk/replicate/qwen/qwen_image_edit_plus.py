from fastsdk import FastClient, APISeex
from typing import List, Literal

from media_toolkit import MediaFile


class qwen_image_edit_plus(FastClient):
    """
    Generated client based on qwen/qwen-image-edit-plus format
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="a32a78f9-c367-4ed3-97a5-b819d2255937", api_key=api_key)
    
    def predictions(self, image: List[MediaFile], prompt: str, seed: int = 42, go_fast: bool = True, aspect_ratio: Literal["1:1", "16:9", "9:16", "4:3", "3:4", "match_input_image"] = 'match_input_image', output_format: Literal["webp", "jpg", "png"] = 'webp', output_quality: int = 95, disable_safety_checker: bool = False, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Images to use as reference. Must be jpeg, png, gif, or webp.
            
            prompt: Text instruction on how to edit the given image.
            
            seed: Random seed. Set for reproducible generation Defaults to 42.
            
            go_fast: Run faster predictions with additional optimizations. Defaults to True.
            
            aspect_ratio: Aspect ratio for the generated image Defaults to 'match_input_image'.
            
            output_format: Format of the output images Defaults to 'webp'.
            
            output_quality: Quality when saving the output images, from 0 to 100. 100 is best quality, 0 is lowest quality. Not relevant for .png outputs Defaults to 95.
            
            disable_safety_checker: Disable safety checker for generated images. Defaults to False.
            
        """
        return self.submit_job("/predictions", image=image, prompt=prompt, seed=seed, go_fast=go_fast, aspect_ratio=aspect_ratio, output_format=output_format, output_quality=output_quality, disable_safety_checker=disable_safety_checker, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions
