from fastsdk.fastSDK import FastSDK
from typing import Optional


class mvdream(FastSDK):
    """
    Generated client for adirik/mvdream
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="fc5360af-e2bf-4353-a7b2-32b701bb0fda", api_key=api_key)
    
    def predict(self, prompt: str = 'an astronaut riding a camel', max_steps: int = 10000, guidance_scale: float = 50.0, negative_prompt: str = 'ugly, bad anatomy, blurry, pixelated obscure, unnatural colors, poor lighting, dull, and unclear, cropped, lowres, low quality, artifacts, duplicate, morbid, mutilated, poorly drawn face, deformed, dehydrated, bad proportions', seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Prompt to generate a 3D object. Defaults to 'an astronaut riding a camel'.
            
            max_steps: Number of iterations to run the model for. Defaults to 10000.
            
            guidance_scale: Scale factor for the guidance loss. Defaults to 50.0.
            
            negative_prompt: Prompt for the negative class. If not specified, a random prompt will be used. Defaults to 'ugly, bad anatomy, blurry, pixelated obscure, unnatural colors, poor lighting, dull, and unclear, cropped, lowres, low quality, artifacts, duplicate, morbid, mutilated, poorly drawn face, deformed, dehydrated, bad proportions'.
            
            seed: The seed to use for the generation. If not specified, a random seed will be used. Optional.
            
        """
        return self.submit_job("/predictions", prompt=prompt, max_steps=max_steps, guidance_scale=guidance_scale, negative_prompt=negative_prompt, seed=seed, **kwargs)
     