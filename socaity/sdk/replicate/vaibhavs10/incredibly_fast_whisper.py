from fastsdk.fastSDK import FastSDK
from typing import Optional, Union

from media_toolkit import MediaFile


class incredibly_fast_whisper(FastSDK):
    """
    Generated client for incredibly_fast_whisper
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="e29f06c8-213b-4426-aa73-45810bd60852", api_key=api_key)
    
    def predict(self, audio: Union[MediaFile, str, bytes], task: str = 'transcribe', language: str = 'None', timestamp: str = 'chunk', batch_size: int = 24, diarise_audio: bool = False, hf_token: Optional[str] = None, **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            audio: Audio file
            
            task: Task to perform: transcribe or translate to another language. Defaults to 'transcribe'.
            
            language: Language spoken in the audio, specify 'None' to perform language detection. Defaults to 'None'.
            
            timestamp: Whisper supports both chunked as well as word level timestamps. Defaults to 'chunk'.
            
            batch_size: Number of parallel batches you want to compute. Reduce if you face OOMs. Defaults to 24.
            
            diarise_audio: Use Pyannote.audio to diarise the audio clips. You will need to provide hf_token below too. Defaults to False.
            
            hf_token: Provide a hf.co/settings/token for Pyannote.audio to diarise the audio clips. You need to agree to the terms in 'https://huggingface.co/pyannote/speaker-diarization-3.1' and 'https://huggingface.co/pyannote/segmentation-3.0' first. Optional.
            
        """
        return self.submit_job("/predict", audio=audio, task=task, language=language, timestamp=timestamp, batch_size=batch_size, diarise_audio=diarise_audio, hf_token=hf_token, **kwargs)
     