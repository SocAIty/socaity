from fastsdk.fastSDK import FastSDK
from typing import Optional


class audio_ldm(FastSDK):
    """
    Generated client for audio_ldm
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="b0289d09-7afb-471e-9c0d-967e2139ffd5", api_key=api_key)
    
    def predict(self, text: str, duration: str = '5.0', n_candidates: int = 3, guidance_scale: float = 2.5, random_seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            text: Text prompt from which to generate audio
            
            duration: Duration of the generated audio (in seconds). Higher duration may OOM. Defaults to '5.0'.
            
            n_candidates: Return the best of n different candidate audios Defaults to 3.
            
            guidance_scale: Guidance scale for the model. (Large scale -> better quality and relavancy to text; small scale -> better diversity) Defaults to 2.5.
            
            random_seed: Random seed for the model (optional) Optional.
            
        """
        return self.submit_job("/predict", text=text, duration=duration, n_candidates=n_candidates, guidance_scale=guidance_scale, random_seed=random_seed, **kwargs)
     