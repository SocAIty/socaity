from fastsdk.fastSDK import FastSDK
from typing import Optional


class audio_ldm(FastSDK):
    """
    Generated client for haoheliu/audio-ldm
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="721cb0b6-c7ce-4298-a719-66ee16a93ad8", api_key=api_key)
    
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
        return self.submit_job("/predictions", text=text, duration=duration, n_candidates=n_candidates, guidance_scale=guidance_scale, random_seed=random_seed, **kwargs)
     