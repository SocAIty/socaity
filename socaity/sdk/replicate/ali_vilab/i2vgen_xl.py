from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class i2vgen_xl(FastSDK):
    """
    Generated client for ali-vilab/i2vgen-xl
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="d199690f-be1a-4727-9e5e-f027245f461a", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], prompt: str, max_frames: int = 16, guidance_scale: float = 9.0, num_inference_steps: int = 50, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Input image.
            
            prompt: Describe the input image.
            
            max_frames: Number of frames in the output Defaults to 16.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 9.0.
            
            num_inference_steps: Number of denoising steps Defaults to 50.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predictions", image=image, prompt=prompt, max_frames=max_frames, guidance_scale=guidance_scale, num_inference_steps=num_inference_steps, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions