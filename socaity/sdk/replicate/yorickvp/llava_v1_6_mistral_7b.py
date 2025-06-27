from fastsdk import FastSDK, APISeex
from typing import Optional, List, Any, Union

from media_toolkit import MediaFile


class llava_v1_6_mistral_7b(FastSDK):
    """
    Generated client for yorickvp/llava-v1-6-mistral-7b
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="18776382-1adc-4140-bd5f-c2e1c58af2c5", api_key=api_key)
    
    def predictions(self, prompt: str, top_p: float = 1.0, max_tokens: int = 1024, temperature: float = 0.2, image: Optional[Union[str, MediaFile, bytes]] = None, history: Optional[Union[str, List[Any]]] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            prompt: Prompt to use for text generation
            
            top_p: When decoding text, samples from the top p percentage of most likely tokens; lower to ignore less likely tokens Defaults to 1.0.
            
            max_tokens: Maximum number of tokens to generate. A word is generally 2-3 tokens Defaults to 1024.
            
            temperature: Adjusts randomness of outputs, greater than 1 is random and 0 is deterministic Defaults to 0.2.
            
            image: Input image Optional.
            
            history: List of earlier chat messages, alternating roles, starting with user input. Include <image> to specify which message to attach the image to. Optional.
            
        """
        return self.submit_job("/predictions", prompt=prompt, top_p=top_p, max_tokens=max_tokens, temperature=temperature, image=image, history=history, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions