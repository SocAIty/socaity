from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class spanish_f5_tts(FastSDK):
    """
    Generated client for fermatresearch/spanish-f5-tts
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="49bd6dea-f24a-4f9f-b32d-61610d872d20", api_key=api_key)
    
    def predictions(self, gen_text: str, ref_text: str, ref_audio: Union[str, MediaFile, bytes], remove_silence: bool = True, custom_split_words: str = '', **kwargs) -> APISeex:
        """
        
        
        
        Args:
            gen_text: Text to Generate
            
            ref_text: Reference Text
            
            ref_audio: Reference audio for voice cloning
            
            remove_silence: Automatically remove silences? Defaults to True.
            
            custom_split_words: Custom split words, comma separated Defaults to ''.
            
        """
        return self.submit_job("/predictions", gen_text=gen_text, ref_text=ref_text, ref_audio=ref_audio, remove_silence=remove_silence, custom_split_words=custom_split_words, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions