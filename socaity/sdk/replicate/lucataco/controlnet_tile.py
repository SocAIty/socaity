from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class controlnet_tile(FastSDK):
    """
    Generated client for lucataco/controlnet-tile
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="5bf66383-8a5d-4cec-9d37-3f9fe24288a8", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], scale: int = 2, strength: float = 0.5, num_inference_steps: int = 32, seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Input image
            
            scale: Scale multiplier Defaults to 2.
            
            strength: Strength of the diffusion Defaults to 0.5.
            
            num_inference_steps: Number of inference steps Defaults to 32.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predictions", image=image, scale=scale, strength=strength, num_inference_steps=num_inference_steps, seed=seed, **kwargs)
     