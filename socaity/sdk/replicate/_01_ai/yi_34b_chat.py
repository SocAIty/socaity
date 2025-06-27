from fastsdk import FastSDK, APISeex
from typing import Dict, Any


class yi_34b_chat(FastSDK):
    """
    Generated client for -01-ai/yi-34b-chat
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="6a87dce9-1dbe-4486-a56e-21fe9928e6a7", api_key=api_key)
    
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
    
    def predictions(self, prompt: str, top_k: int = 50, top_p: float = 0.8, temperature: float = 0.3, max_new_tokens: int = 1024, prompt_template: str = '<|im_start|>system\nYou are a helpful assistant<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n', repetition_penalty: float = 1.2, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: prompt
            
            top_k: The number of highest probability tokens to consider for generating the output. If > 0, only keep the top k tokens with highest probability (top-k filtering). Defaults to 50.
            
            top_p: A probability threshold for generating the output. If < 1.0, only keep the top tokens with cumulative probability >= top_p (nucleus filtering). Nucleus filtering is described in Holtzman et al. (http://arxiv.org/abs/1904.09751). Defaults to 0.8.
            
            temperature: The value used to modulate the next token probabilities. Defaults to 0.3.
            
            max_new_tokens: The maximum number of tokens the model should generate as output. Defaults to 1024.
            
            prompt_template: The template used to format the prompt. The input prompt is inserted into the template using the `{prompt}` placeholder. Defaults to '<|im_start|>system\nYou are a helpful assistant<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n'.
            
            repetition_penalty: Repetition penalty Defaults to 1.2.
            
        """
        return self.submit_job("/predictions", prompt=prompt, top_k=top_k, top_p=top_p, temperature=temperature, max_new_tokens=max_new_tokens, prompt_template=prompt_template, repetition_penalty=repetition_penalty, **kwargs)
    
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