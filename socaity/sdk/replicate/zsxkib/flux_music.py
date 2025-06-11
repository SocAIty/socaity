from fastsdk.fastSDK import FastSDK
from typing import Optional


class flux_music(FastSDK):
    """
    Generated client for flux_music
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="2d02637e-e0a0-41a2-ae73-676a9fe115e6", api_key=api_key)
    
    def predict(self, steps: int = 50, prompt: str = 'The song is an epic blend of space-rock, rock, and post-rock genres.', model_version: str = 'base', guidance_scale: float = 7.0, negative_prompt: str = 'low quality, gentle', save_spectrogram: bool = False, seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            steps: Number of sampling steps Defaults to 50.
            
            prompt: Text prompt for music generation Defaults to 'The song is an epic blend of space-rock, rock, and post-rock genres.'.
            
            model_version: Select the model version to use Defaults to 'base'.
            
            guidance_scale: Classifier-free guidance scale Defaults to 7.0.
            
            negative_prompt: Text prompt for negative guidance (unconditioned prompt) Defaults to 'low quality, gentle'.
            
            save_spectrogram: Whether to save the spectrogram image Defaults to False.
            
            seed: Random seed. Leave blank to randomize the seed Optional.
            
        """
        return self.submit_job("/predict", steps=steps, prompt=prompt, model_version=model_version, guidance_scale=guidance_scale, negative_prompt=negative_prompt, save_spectrogram=save_spectrogram, seed=seed, **kwargs)
     