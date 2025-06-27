from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class wonder3d(FastSDK):
    """
    Generated client for adirik/wonder3d
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="9120889d-ff19-44ed-bfa9-03414b7f71e2", api_key=api_key)
    
    def predictions(self, num_steps: int = 3000, remove_bg: bool = True, image: Optional[Union[str, MediaFile, bytes]] = None, random_seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            num_steps: Number of iterations Defaults to 3000.
            
            remove_bg: Whether to remove image background. Set to false only if uploading image with removed background. Defaults to True.
            
            image: Input image to convert to 3D Optional.
            
            random_seed: Random seed for reproducibility, leave blank to randomize output Optional.
            
        """
        return self.submit_job("/predictions", num_steps=num_steps, remove_bg=remove_bg, image=image, random_seed=random_seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions