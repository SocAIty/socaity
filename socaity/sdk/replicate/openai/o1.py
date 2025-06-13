from fastsdk.fastSDK import FastSDK
from typing import Union, List, Optional, Any

from media_toolkit import MediaFile


class o1(FastSDK):
    """
    Generated client for openai/o1
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="740bcd11-f6f4-430e-b7a4-49bcba46da7e", api_key=api_key)
    
    def predict(self, image_input: Union[List[Any], MediaFile, str, bytes] = [], reasoning_effort: str = 'medium', max_completion_tokens: int = 4096, prompt: Optional[str] = None, system_prompt: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            image_input: List of images to send to the model Defaults to [].
            
            reasoning_effort: Constrains effort on reasoning for reasoning models. Currently supported values are low, medium, and high. Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response. Defaults to 'medium'.
            
            max_completion_tokens: Maximum number of completion tokens to generate Defaults to 4096.
            
            prompt: The prompt to send to the model. Do not use if using messages. Optional.
            
            system_prompt: System prompt to set the assistant's behavior Optional.
            
        """
        return self.submit_job("/predictions", image_input=image_input, reasoning_effort=reasoning_effort, max_completion_tokens=max_completion_tokens, prompt=prompt, system_prompt=system_prompt, **kwargs)
     