from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class audio_super_resolution(FastSDK):
    """
    Generated client for audio_super_resolution
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="868cb625-ed86-49e6-95a0-9c4c20c1a446", api_key=api_key)
    
    def predict(self, input_file: Union[MediaFile, str, bytes], ddim_steps: int = 50, guidance_scale: float = 3.5, seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            input_file: Audio to upsample
            
            ddim_steps: Number of inference steps Defaults to 50.
            
            guidance_scale: Scale for classifier free guidance Defaults to 3.5.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predict", input_file=input_file, ddim_steps=ddim_steps, guidance_scale=guidance_scale, seed=seed, **kwargs)
     