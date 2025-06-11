from fastsdk.fastSDK import FastSDK
from typing import Optional


class pixart_xl_2(FastSDK):
    """
    Generated client for pixart_xl_2
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0c2a11e9-5138-4ce9-938e-e1905b836868", api_key=api_key)
    
    def predict(self, style: str = 'None', width: int = 1024, height: int = 1024, prompt: str = 'A small cactus with a happy face in the Sahara desert', scheduler: str = 'DPMSolverMultistep', num_outputs: int = 1, guidance_scale: float = 4.5, num_inference_steps: int = 14, seed: Optional[int] = None, negative_prompt: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            style: Image style Defaults to 'None'.
            
            width: Width of output image Defaults to 1024.
            
            height: Height of output image Defaults to 1024.
            
            prompt: Input prompt Defaults to 'A small cactus with a happy face in the Sahara desert'.
            
            scheduler: scheduler Defaults to 'DPMSolverMultistep'.
            
            num_outputs: Number of images to output. Defaults to 1.
            
            guidance_scale: Scale for classifier-free guidance Defaults to 4.5.
            
            num_inference_steps: Number of denoising steps Defaults to 14.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
            negative_prompt: Negative prompt Optional.
            
        """
        return self.submit_job("/predict", style=style, width=width, height=height, prompt=prompt, scheduler=scheduler, num_outputs=num_outputs, guidance_scale=guidance_scale, num_inference_steps=num_inference_steps, seed=seed, negative_prompt=negative_prompt, **kwargs)
     