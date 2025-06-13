from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class imagedream(FastSDK):
    """
    Generated client for adirik/imagedream
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="ce95efe9-fad5-4a29-a402-8d0fe4ba9630", api_key=api_key)
    
    def predict(self, image: Union[MediaFile, str, bytes], prompt: str, shading: bool = False, num_steps: int = 12500, guidance_scale: float = 5.0, negative_prompt: str = 'ugly, bad anatomy, blurry, pixelated obscure, unnatural colors, poor lighting, dull, and unclear, cropped, lowres, low quality, artifacts, duplicate, morbid, mutilated, poorly drawn face, deformed, dehydrated, bad proportions', seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image: Image to generate a 3D object from.
            
            prompt: Prompt to generate a 3D object.
            
            shading: Whether to use shading in the generated 3D object. ~40% slower but higher quality with shading. Defaults to False.
            
            num_steps: Number of iterations to run the model for. Defaults to 12500.
            
            guidance_scale: The scale of the guidance loss. Higher values will result in more accurate meshes but may also result in artifacts. Defaults to 5.0.
            
            negative_prompt: Prompt for the negative class. If not specified, a random prompt will be used. Defaults to 'ugly, bad anatomy, blurry, pixelated obscure, unnatural colors, poor lighting, dull, and unclear, cropped, lowres, low quality, artifacts, duplicate, morbid, mutilated, poorly drawn face, deformed, dehydrated, bad proportions'.
            
            seed: The seed to use for the generation. If not specified, a random value will be used. Optional.
            
        """
        return self.submit_job("/predictions", image=image, prompt=prompt, shading=shading, num_steps=num_steps, guidance_scale=guidance_scale, negative_prompt=negative_prompt, seed=seed, **kwargs)
     