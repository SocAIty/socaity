from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class high_resolution_controlnet_tile(FastSDK):
    """
    Generated client for fermatresearch/high-resolution-controlnet-tile
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="a3986265-ccf1-47d4-ac2e-80edc0d0ebe4", api_key=api_key)
    
    def predictions(self, hdr: float = 0.0, steps: int = 8, format: str = 'jpg', scheduler: str = 'DDIM', creativity: float = 0.35, guess_mode: bool = False, resolution: int = 2560, resemblance: float = 0.85, guidance_scale: float = 0.0, negative_prompt: str = 'teeth, tooth, open mouth, longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, mutant', lora_details_strength: float = 1.0, lora_sharpness_strength: float = 1.25, seed: Optional[int] = None, image: Optional[Union[str, MediaFile, bytes]] = None, prompt: Optional[str] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            hdr: HDR improvement over the original image Defaults to 0.0.
            
            steps: Steps Defaults to 8.
            
            format: Format of the output. Defaults to 'jpg'.
            
            scheduler: Choose a scheduler. Defaults to 'DDIM'.
            
            creativity: Denoising strength. 1 means total destruction of the original image Defaults to 0.35.
            
            guess_mode: In this mode, the ControlNet encoder will try best to recognize the content of the input image even if you remove all prompts. Defaults to False.
            
            resolution: Image resolution Defaults to 2560.
            
            resemblance: Conditioning scale for controlnet Defaults to 0.85.
            
            guidance_scale: Scale for classifier-free guidance, should be 0. Defaults to 0.0.
            
            negative_prompt: Negative prompt Defaults to 'teeth, tooth, open mouth, longbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, mutant'.
            
            lora_details_strength: Strength of the image's details Defaults to 1.0.
            
            lora_sharpness_strength: Strength of the image's sharpness. We don't recommend values above 2. Defaults to 1.25.
            
            seed: Seed Optional.
            
            image: Control image for scribble controlnet Optional.
            
            prompt: Prompt for the model Optional.
            
        """
        return self.submit_job("/predictions", hdr=hdr, steps=steps, format=format, scheduler=scheduler, creativity=creativity, guess_mode=guess_mode, resolution=resolution, resemblance=resemblance, guidance_scale=guidance_scale, negative_prompt=negative_prompt, lora_details_strength=lora_details_strength, lora_sharpness_strength=lora_sharpness_strength, seed=seed, image=image, prompt=prompt, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions