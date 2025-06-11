from fastsdk.fastSDK import FastSDK
from typing import Optional


class sticker_maker(FastSDK):
    """
    Generated client for sticker_maker
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="b2086e03-aa11-46eb-a32e-f63ac866c27f", api_key=api_key)
    
    def predict(self, steps: int = 17, width: int = 1152, height: int = 1152, prompt: str = 'a cute cat', output_format: str = 'webp', output_quality: int = 90, negative_prompt: str = '', number_of_images: int = 1, seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            steps: steps Defaults to 17.
            
            width: width Defaults to 1152.
            
            height: height Defaults to 1152.
            
            prompt: prompt Defaults to 'a cute cat'.
            
            output_format: Format of the output images Defaults to 'webp'.
            
            output_quality: Quality of the output images, from 0 to 100. 100 is best quality, 0 is lowest quality. Defaults to 90.
            
            negative_prompt: Things you do not want in the image Defaults to ''.
            
            number_of_images: Number of images to generate Defaults to 1.
            
            seed: Fix the random seed for reproducibility Optional.
            
        """
        return self.submit_job("/predict", steps=steps, width=width, height=height, prompt=prompt, output_format=output_format, output_quality=output_quality, negative_prompt=negative_prompt, number_of_images=number_of_images, seed=seed, **kwargs)
     