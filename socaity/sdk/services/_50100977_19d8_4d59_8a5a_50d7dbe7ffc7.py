from fastsdk import FastClient, APISeex

class deepseek_v3(FastClient):
    """
    Generated client based on deepseek-ai/deepseek-v3 format
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="50100977-19d8-4d59-8a5a-50d7dbe7ffc7", api_key=api_key)
    
    def predictions(self, top_p: float = 1.0, prompt: str = '', max_tokens: int = 2048, temperature: float = 0.1, presence_penalty: float = 0.0, frequency_penalty: float = 0.0, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            top_p: Top-p (nucleus) sampling Defaults to 1.0.
            
            prompt: Prompt Defaults to ''.
            
            max_tokens: The maximum number of tokens the model should generate as output. Defaults to 2048.
            
            temperature: The value used to modulate the next token probabilities. Defaults to 0.1.
            
            presence_penalty: Presence penalty Defaults to 0.0.
            
            frequency_penalty: Frequency penalty Defaults to 0.0.
            
        """
        return self.submit_job("/predictions", top_p=top_p, prompt=prompt, max_tokens=max_tokens, temperature=temperature, presence_penalty=presence_penalty, frequency_penalty=frequency_penalty, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions
