from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class audio_super_resolution(FastSDK):
    """
    Generated client for nateraw/audio-super-resolution
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="9e7eb7fe-4918-4151-805d-4948aa6cdc90", api_key=api_key)
    
    def predictions(self, input_file: Union[MediaFile, str, bytes], ddim_steps: int = 50, guidance_scale: float = 3.5, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            input_file: Audio to upsample
            
            ddim_steps: Number of inference steps Defaults to 50.
            
            guidance_scale: Scale for classifier free guidance Defaults to 3.5.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predictions", input_file=input_file, ddim_steps=ddim_steps, guidance_scale=guidance_scale, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions