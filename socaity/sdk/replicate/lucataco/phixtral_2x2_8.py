from fastsdk.fastSDK import FastSDK
from typing import Optional


class phixtral_2x2_8(FastSDK):
    """
    Generated client for phixtral_2x2_8
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="59c9cb03-62b5-4463-b92f-ffe154e68f44", api_key=api_key)
    
    def predict(self, prompt: str, top_k: int = 50, top_p: float = 0.95, temperature: float = 0.7, max_new_tokens: int = 1024, seed: Optional[int] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Input prompt
            
            top_k: Top k Defaults to 50.
            
            top_p: Top p Defaults to 0.95.
            
            temperature: Temperature Defaults to 0.7.
            
            max_new_tokens: Max new tokens Defaults to 1024.
            
            seed: The seed for the random number generator Optional.
            
        """
        return self.submit_job("/predict", prompt=prompt, top_k=top_k, top_p=top_p, temperature=temperature, max_new_tokens=max_new_tokens, seed=seed, **kwargs)
     