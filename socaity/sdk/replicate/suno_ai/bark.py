from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class bark(FastSDK):
    """
    Generated client for bark
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="fe56b2ac-5e4c-4519-8d59-403c7ff64b1a", api_key=api_key)
    
    def predict(self, prompt: str = 'Hello, my name is Suno. And, uh — and I like pizza. [laughs] But I also have other interests such as playing tic tac toe.', text_temp: float = 0.7, output_full: bool = False, waveform_temp: float = 0.7, history_prompt: Optional[str] = None, custom_history_prompt: Optional[Union[MediaFile, str, bytes]] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            prompt: Input prompt Defaults to 'Hello, my name is Suno. And, uh — and I like pizza. [laughs] But I also have other interests such as playing tic tac toe.'.
            
            text_temp: generation temperature (1.0 more diverse, 0.0 more conservative) Defaults to 0.7.
            
            output_full: return full generation as a .npz file to be used as a history prompt Defaults to False.
            
            waveform_temp: generation temperature (1.0 more diverse, 0.0 more conservative) Defaults to 0.7.
            
            history_prompt: history choice for audio cloning, choose from the list Optional.
            
            custom_history_prompt: Provide your own .npz file with history choice for audio cloning, this will override the previous history_prompt setting Optional.
            
        """
        return self.submit_job("/predict", prompt=prompt, text_temp=text_temp, output_full=output_full, waveform_temp=waveform_temp, history_prompt=history_prompt, custom_history_prompt=custom_history_prompt, **kwargs)
     