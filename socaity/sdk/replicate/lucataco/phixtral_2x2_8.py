from fastsdk import FastSDK, APISeex
from typing import Dict, Optional, Any


class phixtral_2x2_8(FastSDK):
    """
    Generated client for lucataco/phixtral-2x2-8
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="e0465400-c5e2-4bec-bb79-ffd83cf47fe7", api_key=api_key)
    
    def no_name(self, **kwargs) -> APISeex:
        """
        None
        
        """
        return self.submit_job("/", **kwargs)
    
    def shutdown(self, **kwargs) -> APISeex:
        """
        None
        
        """
        return self.submit_job("/shutdown", **kwargs)
    
    def predictions(self, prompt: str, top_k: int = 50, top_p: float = 0.95, temperature: float = 0.7, max_new_tokens: int = 1024, seed: Optional[int] = None, **kwargs) -> APISeex:
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
        return self.submit_job("/predictions", prompt=prompt, top_k=top_k, top_p=top_p, temperature=temperature, max_new_tokens=max_new_tokens, seed=seed, **kwargs)
    
    def health_check(self, **kwargs) -> APISeex:
        """
        None
        
        """
        return self.submit_job("/health-check", **kwargs)
    
    def predictions_prediction_id(self, rediction_equest: Dict[str, Any], **kwargs) -> APISeex:
        """
        Run a single prediction on the model (idempotent creation).
        
        
        Args:
            rediction_equest: No description available.
            
        """
        return self.submit_job("/predictions/{prediction_id}", rediction_equest=rediction_equest, **kwargs)
    
    def predictions_prediction_id_cancel(self, **kwargs) -> APISeex:
        """
        Cancel a running prediction
        
        """
        return self.submit_job("/predictions/{prediction_id}/cancel", **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = no_name
    __call__ = no_name