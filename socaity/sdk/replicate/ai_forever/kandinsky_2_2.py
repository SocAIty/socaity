from fastsdk.fastSDK import FastSDK
from typing import Optional


class kandinsky_2_2(FastSDK):
    """
    Generated client for kandinsky_2_2
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="72368faa-6ba8-45fe-a06a-fbbd51b8efb2", api_key=api_key)
    
    def predict(self, width: int = 512, height: int = 512, prompt: str = 'A moss covered astronaut with a black background', num_outputs: int = 1, output_format: str = 'webp', num_inference_steps: int = 75, num_inference_steps_prior: int = 25, seed: Optional[int] = None, negative_prompt: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            width: Width of output image. Lower the setting if hits memory limits. Defaults to 512.
            
            height: Height of output image. Lower the setting if hits memory limits. Defaults to 512.
            
            prompt: Input prompt Defaults to 'A moss covered astronaut with a black background'.
            
            num_outputs: Number of images to output. Defaults to 1.
            
            output_format: Output image format Defaults to 'webp'.
            
            num_inference_steps: Number of denoising steps Defaults to 75.
            
            num_inference_steps_prior: Number of denoising steps for priors Defaults to 25.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
            negative_prompt: Specify things to not see in the output Optional.
            
        """
        return self.submit_job("/predict", width=width, height=height, prompt=prompt, num_outputs=num_outputs, output_format=output_format, num_inference_steps=num_inference_steps, num_inference_steps_prior=num_inference_steps_prior, seed=seed, negative_prompt=negative_prompt, **kwargs)
     