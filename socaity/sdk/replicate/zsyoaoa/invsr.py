from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class invsr(FastSDK):
    """
    Generated client for zsyoaoa/invsr
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="3f8ab2b7-4850-4932-b8cd-ae93251d4ed0", api_key=api_key)
    
    def predict(self, in_path: Union[MediaFile, str, bytes], seed: int = 12345, num_steps: int = 1, chopping_size: int = 128, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            in_path: Input low-quality image
            
            seed: Random seed. Leave blank to randomize the seed. Defaults to 12345.
            
            num_steps: Number of sampling steps. Defaults to 1.
            
            chopping_size: Chopping resolution Defaults to 128.
            
        """
        return self.submit_job("/predictions", in_path=in_path, seed=seed, num_steps=num_steps, chopping_size=chopping_size, **kwargs)
     