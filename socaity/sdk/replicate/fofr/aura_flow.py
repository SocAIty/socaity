from fastsdk import FastSDK, APISeex
from typing import Optional


class aura_flow(FastSDK):
    """
    Generated client for fofr/aura-flow
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="926108a6-1ec1-4733-958c-a9f3a9bd63a1", api_key=api_key)
    
    def predictions(self, cfg: float = 3.5, shift: float = 1.73, steps: int = 25, width: int = 1024, height: int = 1024, prompt: str = '', sampler: str = 'uni_pc', scheduler: str = 'normal', output_format: str = 'webp', output_quality: int = 80, negative_prompt: str = '', number_of_images: int = 1, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            cfg: The guidance scale tells the model how similar the output should be to the prompt. Defaults to 3.5.
            
            shift: The timestep scheduling shift; shift values higher than 1.0 are better at managing noise in higher resolutions. Defaults to 1.73.
            
            steps: The number of steps to run the model for (more steps = better image but slower generation. Best results for this model are around 25 steps.) Defaults to 25.
            
            width: The width of the image Defaults to 1024.
            
            height: The height of the image Defaults to 1024.
            
            prompt: prompt Defaults to ''.
            
            sampler: sampler Defaults to 'uni_pc'.
            
            scheduler: scheduler Defaults to 'normal'.
            
            output_format: Format of the output images Defaults to 'webp'.
            
            output_quality: Quality of the output images, from 0 to 100. 100 is best quality, 0 is lowest quality. Defaults to 80.
            
            negative_prompt: Things you do not want to see in your image Defaults to ''.
            
            number_of_images: The number of images to generate Defaults to 1.
            
            seed: Set a seed for reproducibility. Random by default. Optional.
            
        """
        return self.submit_job("/predictions", cfg=cfg, shift=shift, steps=steps, width=width, height=height, prompt=prompt, sampler=sampler, scheduler=scheduler, output_format=output_format, output_quality=output_quality, negative_prompt=negative_prompt, number_of_images=number_of_images, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions