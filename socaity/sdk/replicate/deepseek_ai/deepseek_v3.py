from fastsdk import FastSDK, APISeex

class deepseek_v3(FastSDK):
    """
    Generated client for deepseek-ai/deepseek-v3
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="4cac0e8e-6418-4f48-b2cb-e5a237037f6a", api_key=api_key)
    
    def predictions(self, top_p: float = 1.0, prompt: str = '', max_tokens: int = 1024, temperature: float = 0.6, presence_penalty: float = 0.0, frequency_penalty: float = 0.0, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            top_p: Top-p (nucleus) sampling Defaults to 1.0.
            
            prompt: Prompt Defaults to ''.
            
            max_tokens: The maximum number of tokens the model should generate as output. Defaults to 1024.
            
            temperature: The value used to modulate the next token probabilities. Defaults to 0.6.
            
            presence_penalty: Presence penalty Defaults to 0.0.
            
            frequency_penalty: Frequency penalty Defaults to 0.0.
            
        """
        return self.submit_job("/predictions", top_p=top_p, prompt=prompt, max_tokens=max_tokens, temperature=temperature, presence_penalty=presence_penalty, frequency_penalty=frequency_penalty, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions