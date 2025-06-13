from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class cogvlm2_video(FastSDK):
    """
    Generated client for chenxwh/cogvlm2-video
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="0290b9cc-95b5-4a7d-85ac-fecc261777e6", api_key=api_key)
    
    def predict(self, input_video: Union[MediaFile, str, bytes], top_p: float = 0.1, prompt: str = 'Describe this video.', temperature: float = 0.1, max_new_tokens: int = 2048, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            input_video: Input video
            
            top_p: When decoding text, samples from the top p percentage of most likely tokens; lower to ignore less likely tokens Defaults to 0.1.
            
            prompt: Input prompt Defaults to 'Describe this video.'.
            
            temperature: Adjusts randomness of outputs, greater than 1 is random and 0 is deterministic Defaults to 0.1.
            
            max_new_tokens: Maximum number of tokens to generate. A word is generally 2-3 tokens Defaults to 2048.
            
        """
        return self.submit_job("/predictions", input_video=input_video, top_p=top_p, prompt=prompt, temperature=temperature, max_new_tokens=max_new_tokens, **kwargs)
     