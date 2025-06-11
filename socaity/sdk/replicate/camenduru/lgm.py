from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class lgm(FastSDK):
    """
    Generated client for lgm
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="89734639-8a8a-48c9-8f39-4bfbf86d49e9", api_key=api_key)
    
    def predict(self, input_image: Union[MediaFile, str, bytes], seed: int = 42, prompt: str = 'a songbird', negative_prompt: str = 'ugly, blurry, pixelated obscure, unnatural colors, poor lighting, dull, unclear, cropped, lowres, low quality, artifacts, duplicate', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            input_image: Input Image
            
            seed: seed Defaults to 42.
            
            prompt: prompt Defaults to 'a songbird'.
            
            negative_prompt: negative_prompt Defaults to 'ugly, blurry, pixelated obscure, unnatural colors, poor lighting, dull, unclear, cropped, lowres, low quality, artifacts, duplicate'.
            
        """
        return self.submit_job("/predict", input_image=input_image, seed=seed, prompt=prompt, negative_prompt=negative_prompt, **kwargs)
     