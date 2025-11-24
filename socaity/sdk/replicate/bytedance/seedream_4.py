from fastsdk import FastClient, APISeex
from typing import List, Literal

from media_toolkit import MediaFile


class seedream_4(FastClient):
    """
    Generated client based on bytedance/seedream-4 format
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="a0f12979-8fb9-42bc-bda2-24ade4d227e4", api_key=api_key)
    
    def predictions(self, prompt: str, size: Literal["1K", "2K", "4K", "custom"] = '2K', width: int = 2048, height: int = 2048, max_images: int = 1, image_input: List[MediaFile] = [], aspect_ratio: Literal["match_input_image", "1:1", "4:3", "3:4", "16:9", "9:16", "3:2", "2:3", "21:9"] = 'match_input_image', sequential_image_generation: Literal["disabled", "auto"] = 'disabled', **kwargs) -> APISeex:
        """
        
        
        
        Args:
            prompt: Text prompt for image generation
            
            size: Image resolution: 1K (1024px), 2K (2048px), 4K (4096px), or 'custom' for specific dimensions. Defaults to '2K'.
            
            width: Custom image width (only used when size='custom'). Range: 1024-4096 pixels. Defaults to 2048.
            
            height: Custom image height (only used when size='custom'). Range: 1024-4096 pixels. Defaults to 2048.
            
            max_images: Maximum number of images to generate when sequential_image_generation='auto'. Range: 1-15. Total images (input + generated) cannot exceed 15. Defaults to 1.
            
            image_input: Input image(s) for image-to-image generation. List of 1-10 images for single or multi-reference generation. Defaults to [].
            
            aspect_ratio: Image aspect ratio. Only used when size is not 'custom'. Use 'match_input_image' to automatically match the input image's aspect ratio. Defaults to 'match_input_image'.
            
            sequential_image_generation: Group image generation mode. 'disabled' generates a single image. 'auto' lets the model decide whether to generate multiple related images (e.g., story scenes, character variations). Defaults to 'disabled'.
            
        """
        return self.submit_job("/predictions", prompt=prompt, size=size, width=width, height=height, max_images=max_images, image_input=image_input, aspect_ratio=aspect_ratio, sequential_image_generation=sequential_image_generation, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions
