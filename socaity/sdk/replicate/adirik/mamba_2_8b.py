from fastsdk import FastSDK, APISeex
from typing import Optional


class mamba_2_8b(FastSDK):
    """
    Generated client for adirik/mamba-2-8b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="06d2a61c-8197-415c-8cad-f0ee31914e71", api_key=api_key)
    
    def predictions(self, prompt: str, top_k: int = 1, top_p: float = 1.0, max_length: int = 100, temperature: float = 1.0, repetition_penalty: float = 1.2, seed: Optional[int] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Text prompt to send to the model.
            
            top_k: When decoding text, samples from the top k most likely tokens; lower to ignore less likely tokens. Defaults to 1.
            
            top_p: When decoding text, samples from the top p percentage of most likely tokens; lower to ignore less likely tokens. Defaults to 1.0.
            
            max_length: Maximum number of tokens to generate. A word is generally 2-3 tokens. Defaults to 100.
            
            temperature: Adjusts randomness of outputs, greater than 1 is random and 0 is deterministic, 0.75 is a good starting value. Defaults to 1.0.
            
            repetition_penalty: Penalty for repeated words in generated text; 1 is no penalty, values greater than 1 discourage repetition, less than 1 encourage it. Defaults to 1.2.
            
            seed: The seed for the random number generator Optional.
            
        """
        return self.submit_job("/predictions", prompt=prompt, top_k=top_k, top_p=top_p, max_length=max_length, temperature=temperature, repetition_penalty=repetition_penalty, seed=seed, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions