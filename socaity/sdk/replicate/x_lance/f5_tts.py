from fastsdk.fastSDK import FastSDK
from typing import Union, Optional

from media_toolkit import MediaFile


class f5_tts(FastSDK):
    """
    Generated client for x-lance/f5-tts
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="f3527621-8d19-4a30-a15a-f231a3b394f4", api_key=api_key)
    
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
        return self.submit_job("/predictions", gen_text=gen_text, ref_audio=ref_audio, speed=speed, remove_silence=remove_silence, custom_split_words=custom_split_words, ref_text=ref_text, **kwargs)
     