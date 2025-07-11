from fastsdk import FastSDK, APISeex
from typing import Dict, Optional, Union, List, Any

from media_toolkit import MediaFile


class gpt_4_1(FastSDK):
    """
    Generated client for openai/gpt-4-1
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="40bc98bb-e6de-4750-a1c2-c2c2955ba947", api_key=api_key)
    
    def predictions(self, top_p: float = 1.0, messages: Union[Dict[str, Any], List[Any]] = [], image_input: Union[str, MediaFile, List[Any], bytes] = '[]', temperature: float = 1.0, presence_penalty: float = 0.0, frequency_penalty: float = 0.0, max_completion_tokens: int = 4096, prompt: Optional[str] = None, system_prompt: Optional[str] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            top_p: Nucleus sampling parameter - the model considers the results of the tokens with top_p probability mass. (0.1 means only the tokens comprising the top 10% probability mass are considered.) Defaults to 1.0.
            
            messages: A JSON string representing a list of messages. For example: [{"role": "user", "content": "Hello, how are you?"}]. If provided, prompt and system_prompt are ignored. Defaults to [].
            
            image_input: List of images to send to the model Defaults to '[]'.
            
            temperature: Sampling temperature between 0 and 2 Defaults to 1.0.
            
            presence_penalty: Presence penalty parameter - positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics. Defaults to 0.0.
            
            frequency_penalty: Frequency penalty parameter - positive values penalize the repetition of tokens. Defaults to 0.0.
            
            max_completion_tokens: Maximum number of completion tokens to generate Defaults to 4096.
            
            prompt: The prompt to send to the model. Do not use if using messages. Optional.
            
            system_prompt: System prompt to set the assistant's behavior Optional.
            
        """
        return self.submit_job("/predictions", top_p=top_p, messages=messages, image_input=image_input, temperature=temperature, presence_penalty=presence_penalty, frequency_penalty=frequency_penalty, max_completion_tokens=max_completion_tokens, prompt=prompt, system_prompt=system_prompt, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions