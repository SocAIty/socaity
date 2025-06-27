from fastsdk import FastSDK, APISeex
from typing import Optional


class flux_music(FastSDK):
    """
    Generated client for zsxkib/flux-music
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="dc789e86-6ab2-4f69-8406-b7754b3a6775", api_key=api_key)
    
    def predictions(self, steps: int = 50, prompt: str = 'The song is an epic blend of space-rock, rock, and post-rock genres.', model_version: str = 'base', guidance_scale: float = 7.0, negative_prompt: str = 'low quality, gentle', save_spectrogram: bool = False, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            steps: Number of sampling steps Defaults to 50.
            
            prompt: Text prompt for music generation Defaults to 'The song is an epic blend of space-rock, rock, and post-rock genres.'.
            
            model_version: Select the model version to use Defaults to 'base'.
            
            guidance_scale: Classifier-free guidance scale Defaults to 7.0.
            
            negative_prompt: Text prompt for negative guidance (unconditioned prompt) Defaults to 'low quality, gentle'.
            
            save_spectrogram: Whether to save the spectrogram image Defaults to False.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predictions", steps=steps, prompt=prompt, model_version=model_version, guidance_scale=guidance_scale, negative_prompt=negative_prompt, save_spectrogram=save_spectrogram, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions