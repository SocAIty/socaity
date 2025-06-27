from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class whisper_diarization(FastSDK):
    """
    Generated client for nicknaskida/whisper-diarization
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="f6afd38a-eb3a-40d8-988e-21754d3a0c9a", api_key=api_key)
    
    def predictions(self, translate: bool = False, batch_size: int = 64, num_speakers: int = 2, group_segments: bool = True, offset_seconds: int = 0, transcript_output_format: str = 'both', file: Optional[Union[str, MediaFile, bytes]] = None, prompt: Optional[str] = None, file_url: Optional[str] = None, hf_token: Optional[str] = None, language: Optional[str] = None, file_string: Optional[str] = None, **kwargs) -> APISeex:
        """
        
        
        
        Args:
            translate: Translate the speech into English. Defaults to False.
            
            batch_size: Batch size for inference. (Reduce if face OOM error) Defaults to 64.
            
            num_speakers: Number of speakers, leave empty to autodetect. Defaults to 2.
            
            group_segments: Group segments of same speaker shorter apart than 2 seconds Defaults to True.
            
            offset_seconds: Offset in seconds, used for chunked inputs Defaults to 0.
            
            transcript_output_format: Specify the format of the transcript output: individual words with timestamps, full text of segments, or a combination of both. Defaults to 'both'.
            
            file: Or an audio file Optional.
            
            prompt: Vocabulary: provide names, acronyms and loanwords in a list. Use punctuation for best accuracy. Optional.
            
            file_url: Or provide: A direct audio file URL Optional.
            
            hf_token: Provide a hf.co/settings/token for Pyannote.audio to diarise the audio clips. You need to agree to the terms in 'https://huggingface.co/pyannote/speaker-diarization-3.1' and 'https://huggingface.co/pyannote/segmentation-3.0' first. Optional.
            
            language: Language of the spoken words as a language code like 'en'. Leave empty to auto detect language. Optional.
            
            file_string: Either provide: Base64 encoded audio file, Optional.
            
        """
        return self.submit_job("/predictions", translate=translate, batch_size=batch_size, num_speakers=num_speakers, group_segments=group_segments, offset_seconds=offset_seconds, transcript_output_format=transcript_output_format, file=file, prompt=prompt, file_url=file_url, hf_token=hf_token, language=language, file_string=file_string, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions