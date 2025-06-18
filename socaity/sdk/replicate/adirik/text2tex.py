from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class text2tex(FastSDK):
    """
    Generated client for adirik/text2tex
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="617a3bde-432c-4750-b2b5-df52f4eedd7a", api_key=api_key)
    
    def predictions(self, prompt: str, obj_file: Union[MediaFile, str, bytes], ddim_steps: int = 50, update_mode: str = 'heuristic', new_strength: float = 1.0, update_steps: int = 20, num_viewpoints: int = 36, viewpoint_mode: str = 'predefined', negative_prompt: str = '', update_strength: float = 0.3, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Prompt to generate a 3D object.
            
            obj_file: 3D object (shape) file to generate the texture onto
            
            ddim_steps: Number of steps for DDIM Defaults to 50.
            
            update_mode: Update mode Defaults to 'heuristic'.
            
            new_strength: Amount of DDIM steps for the new view Defaults to 1.0.
            
            update_steps: Number of update steps Defaults to 20.
            
            num_viewpoints: Number of viewpoints Defaults to 36.
            
            viewpoint_mode: Viewpoint mode Defaults to 'predefined'.
            
            negative_prompt: Negative prompt to generate a 3D object. Defaults to ''.
            
            update_strength: Amount of DDIM steps for updating the view Defaults to 0.3.
            
            seed: Seed Optional.
            
        """
        return self.submit_job("/predictions", prompt=prompt, obj_file=obj_file, ddim_steps=ddim_steps, update_mode=update_mode, new_strength=new_strength, update_steps=update_steps, num_viewpoints=num_viewpoints, viewpoint_mode=viewpoint_mode, negative_prompt=negative_prompt, update_strength=update_strength, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions