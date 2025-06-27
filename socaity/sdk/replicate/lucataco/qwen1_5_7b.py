from fastsdk import FastSDK, APISeex
from typing import Dict, Optional, Any


class qwen1_5_7b(FastSDK):
    """
    Generated client for lucataco/qwen1-5-7b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="5b024df1-64b6-4647-8a2a-7c64082f0339", api_key=api_key)
    
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
    
    def predictions(self, top_k: int = 1, top_p: float = 1.0, prompt: str = 'Give me a short introduction to large language model.', temperature: float = 1.0, system_prompt: str = 'You are a helpful assistant.', max_new_tokens: int = 512, repetition_penalty: float = 1.0, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            top_k: When decoding text, samples from the top k most likely tokens; lower to ignore less likely tokens. Defaults to 1.
            
            top_p: When decoding text, samples from the top p percentage of most likely tokens; lower to ignore less likely tokens. Defaults to 1.0.
            
            prompt: Input prompt Defaults to 'Give me a short introduction to large language model.'.
            
            temperature: Adjusts randomness of outputs, greater than 1 is random and 0 is deterministic, 0.75 is a good starting value. Defaults to 1.0.
            
            system_prompt: System prompt Defaults to 'You are a helpful assistant.'.
            
            max_new_tokens: The maximum number of tokens to generate Defaults to 512.
            
            repetition_penalty: Penalty for repeated words in generated text; 1 is no penalty, values greater than 1 discourage repetition, less than 1 encourage it. Defaults to 1.0.
            
            seed: The seed for the random number generator Optional.
            
        """
        return self.submit_job("/predictions", top_k=top_k, top_p=top_p, prompt=prompt, temperature=temperature, system_prompt=system_prompt, max_new_tokens=max_new_tokens, repetition_penalty=repetition_penalty, seed=seed, **kwargs)
    
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