from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class interior_design(FastSDK):
    """
    Generated client for adirik/interior-design
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="fdc56358-7633-41fa-9880-aa45eb7cf3b2", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], prompt: str, guidance_scale: float = 15.0, negative_prompt: str = 'lowres, watermark, banner, logo, watermark, contactinfo, text, deformed, blurry, blur, out of focus, out of frame, surreal, extra, ugly, upholstered walls, fabric walls, plush walls, mirror, mirrored, functional, realistic', prompt_strength: float = 0.8, num_inference_steps: int = 50, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Input image
            
            prompt: Text prompt for design
            
            guidance_scale: Scale for classifier-free guidance Defaults to 15.0.
            
            negative_prompt: Negative text prompt to guide the design Defaults to 'lowres, watermark, banner, logo, watermark, contactinfo, text, deformed, blurry, blur, out of focus, out of frame, surreal, extra, ugly, upholstered walls, fabric walls, plush walls, mirror, mirrored, functional, realistic'.
            
            prompt_strength: Prompt strength for inpainting. 1.0 corresponds to full destruction of information in image Defaults to 0.8.
            
            num_inference_steps: Number of denoising steps Defaults to 50.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predictions", image=image, prompt=prompt, guidance_scale=guidance_scale, negative_prompt=negative_prompt, prompt_strength=prompt_strength, num_inference_steps=num_inference_steps, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions