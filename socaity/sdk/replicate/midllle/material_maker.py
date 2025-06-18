from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class material_maker(FastSDK):
    """
    Generated client for midllle/material-maker
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="2b381d5e-1ef0-4efb-9876-a68d692f2e0f", api_key=api_key)
    
    def predictions(self, input_image: Union[MediaFile, str, bytes], mirror: bool = False, seamless: bool = False, ishiiruka: bool = False, replicate: bool = False, tile_size: int = 512, ishiiruka_texture_encoder: bool = False, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            input_image: Input image
            
            mirror: Mirrored seamless upscaling Defaults to False.
            
            seamless: Seamless upscaling Defaults to False.
            
            ishiiruka: Save textures in Ishiiruka Dolphin material map texture pack format Defaults to False.
            
            replicate: Replicate edge pixels for padding Defaults to False.
            
            tile_size: Tile size for splitting Defaults to 512.
            
            ishiiruka_texture_encoder: Save textures in Ishiiruka Dolphin's Texture Encoder format Defaults to False.
            
        """
        return self.submit_job("/predictions", input_image=input_image, mirror=mirror, seamless=seamless, ishiiruka=ishiiruka, replicate=replicate, tile_size=tile_size, ishiiruka_texture_encoder=ishiiruka_texture_encoder, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions