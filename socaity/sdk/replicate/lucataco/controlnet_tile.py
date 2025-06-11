from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class controlnet_tile(FastSDK):
    """
    Generated client for controlnet_tile
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="5ba3fb8f-e2f4-4f2d-8608-2e57330a2164", api_key=api_key)
    
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
        return self.submit_job("/predict", image=image, scale=scale, strength=strength, num_inference_steps=num_inference_steps, seed=seed, **kwargs)
     