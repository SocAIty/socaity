from fastsdk import FastSDK, APISeex
from typing import Optional


class riffusion(FastSDK):
    """
    Generated client for riffusion/riffusion
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="043a836f-f6d6-4f1a-b0c1-18d68428b666", api_key=api_key)
    
    def predictions(self, alpha: float = 0.5, prompt_a: str = 'funky synth solo', denoising: float = 0.75, seed_image_id: str = 'vibes', num_inference_steps: int = 50, prompt_b: Optional[str] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            alpha: Interpolation alpha if using two prompts. A value of 0 uses prompt_a fully, a value of 1 uses prompt_b fully Defaults to 0.5.
            
            prompt_a: The prompt for your audio Defaults to 'funky synth solo'.
            
            denoising: How much to transform input spectrogram Defaults to 0.75.
            
            seed_image_id: Seed spectrogram to use Defaults to 'vibes'.
            
            num_inference_steps: Number of steps to run the diffusion model Defaults to 50.
            
            prompt_b: The second prompt to interpolate with the first, leave blank if no interpolation Optional.
            
        """
        return self.submit_job("/predictions", alpha=alpha, prompt_a=prompt_a, denoising=denoising, seed_image_id=seed_image_id, num_inference_steps=num_inference_steps, prompt_b=prompt_b, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions