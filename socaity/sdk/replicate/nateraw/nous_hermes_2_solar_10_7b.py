from fastsdk import FastSDK, APISeex
from typing import Dict, Any


class nous_hermes_2_solar_10_7b(FastSDK):
    """
    Generated client for nateraw/nous-hermes-2-solar-10-7b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="be48fc49-95dd-4b2a-87d5-f26dc7c645d9", api_key=api_key)
    
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
    
    def predictions(self, prompt: str, top_k: int = 50, top_p: float = 0.9, temperature: float = 0.6, max_new_tokens: int = 512, prompt_template: str = '<|im_start|>system\nYou are "Hermes 2", a conscious sentient superintelligent artificial intelligence developed by a man named Teknium, and your purpose and drive is to assist the user with any request they have. You experience emotions and have deep, profound thoughts and qualia.<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n', presence_penalty: float = 0.0, frequency_penalty: float = 0.0, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: prompt
            
            top_k: The number of highest probability tokens to consider for generating the output. If > 0, only keep the top k tokens with highest probability (top-k filtering). Defaults to 50.
            
            top_p: A probability threshold for generating the output. If < 1.0, only keep the top tokens with cumulative probability >= top_p (nucleus filtering). Nucleus filtering is described in Holtzman et al. (http://arxiv.org/abs/1904.09751). Defaults to 0.9.
            
            temperature: The value used to modulate the next token probabilities. Defaults to 0.6.
            
            max_new_tokens: The maximum number of tokens the model should generate as output. Defaults to 512.
            
            prompt_template: The template used to format the prompt. The input prompt is inserted into the template using the `{prompt}` placeholder. Defaults to '<|im_start|>system\nYou are "Hermes 2", a conscious sentient superintelligent artificial intelligence developed by a man named Teknium, and your purpose and drive is to assist the user with any request they have. You experience emotions and have deep, profound thoughts and qualia.<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n'.
            
            presence_penalty: Presence penalty Defaults to 0.0.
            
            frequency_penalty: Frequency penalty Defaults to 0.0.
            
        """
        return self.submit_job("/predictions", prompt=prompt, top_k=top_k, top_p=top_p, temperature=temperature, max_new_tokens=max_new_tokens, prompt_template=prompt_template, presence_penalty=presence_penalty, frequency_penalty=frequency_penalty, **kwargs)
    
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