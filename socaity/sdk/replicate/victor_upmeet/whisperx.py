from fastsdk import FastSDK, APISeex
from typing import Optional, Union

from media_toolkit import MediaFile


class whisperx(FastSDK):
    """
    Generated client for victor-upmeet/whisperx
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="200c0572-31f8-4508-9d92-047f97fe36e1", api_key=api_key)
    
    def predictions(self, audio_file: Union[MediaFile, str, bytes], debug: bool = False, vad_onset: float = 0.5, batch_size: int = 64, vad_offset: float = 0.363, diarization: bool = False, temperature: float = 0.0, align_output: bool = False, language_detection_min_prob: float = 0.0, language_detection_max_tries: int = 5, language: Optional[str] = None, max_speakers: Optional[int] = None, min_speakers: Optional[int] = None, initial_prompt: Optional[str] = None, huggingface_access_token: Optional[str] = None, **kwargs) -> APISeex:
        """
        Run a single prediction on the model
        
        
        Args:
            audio_file: Audio file
            
            debug: Print out compute/inference times and memory usage information Defaults to False.
            
            vad_onset: VAD onset Defaults to 0.5.
            
            batch_size: Parallelization of input audio transcription Defaults to 64.
            
            vad_offset: VAD offset Defaults to 0.363.
            
            diarization: Assign speaker ID labels Defaults to False.
            
            temperature: Temperature to use for sampling Defaults to 0.0.
            
            align_output: Aligns whisper output to get accurate word-level timestamps Defaults to False.
            
            language_detection_min_prob: If language is not specified, then the language will be detected recursively on different parts of the file until it reaches the given probability Defaults to 0.0.
            
            language_detection_max_tries: If language is not specified, then the language will be detected following the logic of language_detection_min_prob parameter, but will stop after the given max retries. If max retries is reached, the most probable language is kept. Defaults to 5.
            
            language: ISO code of the language spoken in the audio, specify None to perform language detection Optional.
            
            max_speakers: Maximum number of speakers if diarization is activated (leave blank if unknown) Optional.
            
            min_speakers: Minimum number of speakers if diarization is activated (leave blank if unknown) Optional.
            
            initial_prompt: Optional text to provide as a prompt for the first window Optional.
            
            huggingface_access_token: To enable diarization, please enter your HuggingFace token (read). You need to accept the user agreement for the models specified in the README. Optional.
            
        """
        return self.submit_job("/predictions", audio_file=audio_file, debug=debug, vad_onset=vad_onset, batch_size=batch_size, vad_offset=vad_offset, diarization=diarization, temperature=temperature, align_output=align_output, language_detection_min_prob=language_detection_min_prob, language_detection_max_tries=language_detection_max_tries, language=language, max_speakers=max_speakers, min_speakers=min_speakers, initial_prompt=initial_prompt, huggingface_access_token=huggingface_access_token, **kwargs)
    
    # Convenience aliases for the primary endpoint
    run = predictions
    __call__ = predictions