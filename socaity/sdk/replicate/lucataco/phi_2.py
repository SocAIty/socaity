from fastsdk import FastSDK, APISeex
from typing import Dict, Any


class phi_2(FastSDK):
    """
    Generated client for lucataco/phi-2
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="ce54bb7f-20cf-46b6-94bd-b83766b62268", api_key=api_key)
    
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
    
    def predictions(self, prompt: str, max_length: int = 200, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Input prompt
            
            max_length: Max length Defaults to 200.
            
        """
        return self.submit_job("/predictions", prompt=prompt, max_length=max_length, **kwargs)
    
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