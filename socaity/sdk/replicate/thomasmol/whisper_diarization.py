from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class whisper_diarization(FastSDK):
    """
    Generated client for thomasmol/whisper-diarization
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="85d70882-606b-4083-b164-1fa4acd98a0c", api_key=api_key)
    
    def predictions(self, translate: bool = False, group_segments: bool = True, file: Optional[Union[MediaFile, str, bytes]] = None, prompt: Optional[str] = None, file_url: Optional[str] = None, language: Optional[str] = None, file_string: Optional[str] = None, num_speakers: Optional[int] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            translate: Translate the speech into English. Defaults to False.
            
            group_segments: Group segments of same speaker shorter apart than 2 seconds Defaults to True.
            
            file: Or an audio file Optional.
            
            prompt: Vocabulary: provide names, acronyms and loanwords in a list. Use punctuation for best accuracy. Optional.
            
            file_url: Or provide: A direct audio file URL Optional.
            
            language: Language of the spoken words as a language code like 'en'. Leave empty to auto detect language. Optional.
            
            file_string: Either provide: Base64 encoded audio file, Optional.
            
            num_speakers: Number of speakers, leave empty to autodetect. Optional.
            
        """
        return self.submit_job("/predictions", translate=translate, group_segments=group_segments, file=file, prompt=prompt, file_url=file_url, language=language, file_string=file_string, num_speakers=num_speakers, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions