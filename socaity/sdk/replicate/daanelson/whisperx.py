from fastsdk import FastSDK, APISeex
from typing import Union

from media_toolkit import MediaFile


class whisperx(FastSDK):
    """
    Generated client for daanelson/whisperx
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="1b739546-44d6-470b-8bb0-47a941587637", api_key=api_key)
    
    def predictions(self, audio: Union[str, MediaFile, bytes], debug: bool = False, only_text: bool = False, batch_size: int = 32, align_output: bool = False, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            audio: Audio file
            
            debug: Print out memory usage information. Defaults to False.
            
            only_text: Set if you only want to return text; otherwise, segment metadata will be returned as well. Defaults to False.
            
            batch_size: Parallelization of input audio transcription Defaults to 32.
            
            align_output: Use if you need word-level timing and not just batched transcription. Only works for English atm Defaults to False.
            
        """
        return self.submit_job("/predictions", audio=audio, debug=debug, only_text=only_text, batch_size=batch_size, align_output=align_output, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions