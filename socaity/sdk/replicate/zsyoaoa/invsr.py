from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class invsr(FastSDK):
    """
    Generated client for invsr
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="e008c209-df8b-4229-8818-cb7768b75a12", api_key=api_key)
    
    def predict(self, in_path: Union[MediaFile, str, bytes], seed: int = 12345, num_steps: int = 1, chopping_size: int = 128, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            in_path: Input low-quality image
            
            seed: Random seed. Leave blank to randomize the seed. Defaults to 12345.
            
            num_steps: Number of sampling steps. Defaults to 1.
            
            chopping_size: Chopping resolution Defaults to 128.
            
        """
        return self.submit_job("/predict", in_path=in_path, seed=seed, num_steps=num_steps, chopping_size=chopping_size, **kwargs)
     