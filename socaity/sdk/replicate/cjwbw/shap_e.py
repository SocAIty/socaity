from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class shap_e(FastSDK):
    """
    Generated client for cjwbw/shap-e
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="01265335-2249-43c0-b787-453da9a6fbb0", api_key=api_key)
    
    def predictions(self, save_mesh: bool = False, batch_size: int = 1, render_mode: str = 'nerf', render_size: int = 128, guidance_scale: float = 15.0, image: Optional[Union[MediaFile, str, bytes]] = None, prompt: Optional[str] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            save_mesh: Save the latents as meshes. Defaults to False.
            
            batch_size: Number of output Defaults to 1.
            
            render_mode: Choose a render mode Defaults to 'nerf'.
            
            render_size: Set the size of the a renderer, higher values take longer to render Defaults to 128.
            
            guidance_scale: Set the scale for guidanece Defaults to 15.0.
            
            image: A synthetic view image for generating the 3D modeld. To get the best result, remove background from the input image Optional.
            
            prompt: Text prompt for generating the 3D model, ignored if an image is provide below Optional.
            
        """
        return self.submit_job("/predictions", save_mesh=save_mesh, batch_size=batch_size, render_mode=render_mode, render_size=render_size, guidance_scale=guidance_scale, image=image, prompt=prompt, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions