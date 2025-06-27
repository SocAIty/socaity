from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class llava_13b(FastSDK):
    """
    Generated client for yorickvp/llava-13b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="936c7574-c12b-4955-9db8-e3f1ede0c7f3", api_key=api_key)
    
    def predictions(self, image: Union[str, MediaFile, bytes], prompt: str, top_p: float = 1.0, max_tokens: int = 1024, temperature: float = 0.2, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            image: Input image
            
            prompt: Prompt to use for text generation
            
            top_p: When decoding text, samples from the top p percentage of most likely tokens; lower to ignore less likely tokens Defaults to 1.0.
            
            max_tokens: Maximum number of tokens to generate. A word is generally 2-3 tokens Defaults to 1024.
            
            temperature: Adjusts randomness of outputs, greater than 1 is random and 0 is deterministic Defaults to 0.2.
            
        """
        return self.submit_job("/predictions", image=image, prompt=prompt, top_p=top_p, max_tokens=max_tokens, temperature=temperature, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions