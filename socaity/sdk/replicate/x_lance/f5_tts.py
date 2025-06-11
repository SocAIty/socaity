from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class f5_tts(FastSDK):
    """
    Generated client for f5_tts
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="838eeee6-93dc-48b5-8336-a6e0253696aa", api_key=api_key)
    
    def predict(self, gen_text: str, ref_audio: Union[MediaFile, str, bytes], speed: float = 1.0, remove_silence: bool = True, custom_split_words: str = '', ref_text: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            gen_text: Text to Generate
            
            ref_audio: Reference audio for voice cloning
            
            speed: Speed of the generated audio Defaults to 1.0.
            
            remove_silence: Automatically remove silences? Defaults to True.
            
            custom_split_words: Custom split words, comma separated Defaults to ''.
            
            ref_text: Reference Text Optional.
            
        """
        return self.submit_job("/predict", gen_text=gen_text, ref_audio=ref_audio, speed=speed, remove_silence=remove_silence, custom_split_words=custom_split_words, ref_text=ref_text, **kwargs)
     