from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class texture(FastSDK):
    """
    Generated client for texture
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="6dbfd54a-4dd5-4cc0-a7fb-49f746296a16", api_key=api_key)
    
    def predict(self, shape_path: Union[MediaFile, str, bytes], seed: int = 0, prompt: str = 'A next gen nascar', shape_scale: float = 0.6, guidance_scale: float = 10.0, texture_resolution: int = 1024, texture_interpolation_mode: str = 'bilinear', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            shape_path: 3D object (shape) file to generate the texture onto
            
            seed: Seed for the inference Defaults to 0.
            
            prompt: Prompt to generate the texture from Defaults to 'A next gen nascar'.
            
            shape_scale: Factor to scale image by Defaults to 0.6.
            
            guidance_scale: Factor to scale the guidance image by Defaults to 10.0.
            
            texture_resolution: Resolution of the texture to generate Defaults to 1024.
            
            texture_interpolation_mode: Texture mapping interpolation mode from texture image, options: 'nearest', 'bilinear', 'bicubic' Defaults to 'bilinear'.
            
        """
        return self.submit_job("/predict", shape_path=shape_path, seed=seed, prompt=prompt, shape_scale=shape_scale, guidance_scale=guidance_scale, texture_resolution=texture_resolution, texture_interpolation_mode=texture_interpolation_mode, **kwargs)
     