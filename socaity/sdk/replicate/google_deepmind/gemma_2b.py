from fastsdk import FastSDK, APISeex
from typing import Dict, Any


class gemma_2b(FastSDK):
    """
    Generated client for google-deepmind/gemma-2b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="e8528d60-07a8-4182-b671-aa3cd6786445", api_key=api_key)
    
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
    
    def predictions(self, top_k: int = 50, top_p: float = 0.95, prompt: str = 'Write me a poem about Machine Learning.', temperature: float = 0.7, max_new_tokens: int = 200, min_new_tokens: int = -1, repetition_penalty: float = 1.0, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            top_k: When decoding text, samples from the top k most likely tokens; lower to ignore less likely tokens Defaults to 50.
            
            top_p: When decoding text, samples from the top p percentage of most likely tokens; lower to ignore less likely tokens Defaults to 0.95.
            
            prompt: Prompt to send to the model. Defaults to 'Write me a poem about Machine Learning.'.
            
            temperature: Adjusts randomness of outputs, greater than 1 is random and 0 is deterministic, 0.75 is a good starting value. Defaults to 0.7.
            
            max_new_tokens: Maximum number of tokens to generate. A word is generally 2-3 tokens Defaults to 200.
            
            min_new_tokens: Minimum number of tokens to generate. To disable, set to -1. A word is generally 2-3 tokens. Defaults to -1.
            
            repetition_penalty: A parameter that controls how repetitive text can be. Lower means more repetitive, while higher means less repetitive. Set to 1.0 to disable. Defaults to 1.0.
            
        """
        return self.submit_job("/predictions", top_k=top_k, top_p=top_p, prompt=prompt, temperature=temperature, max_new_tokens=max_new_tokens, min_new_tokens=min_new_tokens, repetition_penalty=repetition_penalty, **kwargs)
    
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