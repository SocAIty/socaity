from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class video_morpher(FastSDK):
    """
    Generated client for fofr/video-morpher
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0ce78050-64c8-4968-aa57-74b52618ac0e", api_key=api_key)
    
    def predictions(self, subject_image_1: Union[str, MediaFile, bytes], subject_image_2: Union[str, MediaFile, bytes], subject_image_3: Union[str, MediaFile, bytes], subject_image_4: Union[str, MediaFile, bytes], mode: str = 'medium', prompt: str = '', checkpoint: str = 'realistic', aspect_ratio: str = '2:3', style_strength: float = 1.0, use_controlnet: bool = True, negative_prompt: str = '', seed: Optional[int] = None, style_image: Optional[Union[str, MediaFile, bytes]] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            subject_image_1: The first subject of the video
            
            subject_image_2: The second subject of the video
            
            subject_image_3: The third subject of the video
            
            subject_image_4: The fourth subject of the video
            
            mode: Determines if you produce a quick experimental video or an upscaled interpolated one. (small ~20s, medium ~60s, upscaled ~2min, upscaled-and-interpolated ~4min) Defaults to 'medium'.
            
            prompt: The prompt has a small effect, but most of the video is driven by the subject images Defaults to ''.
            
            checkpoint: The checkpoint to use for the model Defaults to 'realistic'.
            
            aspect_ratio: The aspect ratio of the video Defaults to '2:3'.
            
            style_strength: How strong the style is applied Defaults to 1.0.
            
            use_controlnet: Use geometric circles to guide the generation Defaults to True.
            
            negative_prompt: What you do not want to see in the video Defaults to ''.
            
            seed: Set a seed for reproducibility. Random by default. Optional.
            
            style_image: Apply the style from this image to the whole video Optional.
            
        """
        return self.submit_job("/predictions", subject_image_1=subject_image_1, subject_image_2=subject_image_2, subject_image_3=subject_image_3, subject_image_4=subject_image_4, mode=mode, prompt=prompt, checkpoint=checkpoint, aspect_ratio=aspect_ratio, style_strength=style_strength, use_controlnet=use_controlnet, negative_prompt=negative_prompt, seed=seed, style_image=style_image, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions