from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class xtts_v2(FastSDK):
    """
    Generated client for lucataco/xtts-v2
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="f31156fb-c378-43f0-86a4-3bec755a5347", api_key=api_key)
    
    def predictions(self, speaker: Union[MediaFile, str, bytes], text: str = "Hi there, I'm your new voice clone. Try your best to upload quality audio", language: str = 'en', cleanup_voice: bool = False, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            speaker: Original speaker audio (wav, mp3, m4a, ogg, or flv)
            
            text: Text to synthesize Defaults to "Hi there, I'm your new voice clone. Try your best to upload quality audio".
            
            language: Output language for the synthesised speech Defaults to 'en'.
            
            cleanup_voice: Whether to apply denoising to the speaker audio (microphone recordings) Defaults to False.
            
        """
        return self.submit_job("/predictions", speaker=speaker, text=text, language=language, cleanup_voice=cleanup_voice, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions