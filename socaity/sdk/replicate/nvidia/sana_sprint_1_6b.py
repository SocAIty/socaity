from fastsdk import FastSDK, APISeex

class sana_sprint_1_6b(FastSDK):
    """
    Generated client for nvidia/sana-sprint-1-6b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="c153dcec-e536-4913-8b42-d020ccfb3ee2", api_key=api_key)
    
    def predictions(self, seed: int = -1, width: int = 1024, height: int = 1024, prompt: str = 'a tiny astronaut hatching from an egg on the moon', output_format: str = 'jpg', guidance_scale: float = 4.5, output_quality: int = 80, inference_steps: int = 2, intermediate_timesteps: float = 1.3, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            seed: Seed value. Set to a value less than 0 to randomize the seed Defaults to -1.
            
            width: Width of output image Defaults to 1024.
            
            height: Height of output image Defaults to 1024.
            
            prompt: Input prompt Defaults to 'a tiny astronaut hatching from an egg on the moon'.
            
            output_format: Format of the output images Defaults to 'jpg'.
            
            guidance_scale: CFG guidance scale Defaults to 4.5.
            
            output_quality: Quality when saving the output images, from 0 to 100. 100 is best quality, 0 is lowest quality. Not relevant for .png outputs Defaults to 80.
            
            inference_steps: Number of sampling steps Defaults to 2.
            
            intermediate_timesteps: Intermediate timestep value (only used when inference_steps=2, recommended values: 1.0-1.4) Defaults to 1.3.
            
        """
        return self.submit_job("/predictions", seed=seed, width=width, height=height, prompt=prompt, output_format=output_format, guidance_scale=guidance_scale, output_quality=output_quality, inference_steps=inference_steps, intermediate_timesteps=intermediate_timesteps, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions